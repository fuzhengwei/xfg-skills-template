#!/usr/bin/env python3
"""
Agent Skills 验证器

验证 SKILL.md 文件是否符合 Agent Skills 规范。

用法:
    python3 tools/validate.py ./my-skill
    python3 tools/validate.py ./my-skill --strict
    python3 tools/validate.py ./my-skill --json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


class ValidationResult:
    def __init__(self):
        self._errors = []
        self._warnings = []
        self._info = []

    def error(self, msg):
        self._errors.append(msg)

    def warn(self, msg):
        self._warnings.append(msg)

    def info(self, msg):
        self._info.append(msg)

    @property
    def errors(self):
        return self._errors

    @property
    def warnings(self):
        return self._warnings

    @property
    def info_list(self):
        return self._info

    @property
    def is_valid(self):
        return len(self._errors) == 0

    def to_dict(self):
        return {
            "valid": self.is_valid,
            "errors": self._errors,
            "warnings": self._warnings,
            "info": self._info
        }


def parse_frontmatter(content: str):
    """解析 SKILL.md 的 YAML frontmatter。"""
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # 简易 YAML 解析（不引入依赖）
    metadata = {}
    current_key = None
    current_value = None
    in_metadata = False

    for line in frontmatter_text.split("\n"):
        stripped = line.strip()

        # 处理嵌套 metadata
        if in_metadata:
            if stripped.startswith("- ") or not stripped:
                continue
            if line.startswith("  ") or line.startswith("\t"):
                continue
            else:
                if current_key == "metadata" and isinstance(current_value, dict):
                    metadata["metadata"] = current_value
                in_metadata = False

        # 解析 key: value
        match = re.match(r'^(\w[\w-]*):\s*(.*)', stripped)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            # 处理缩进的 metadata 块
            if value == "" and key == "metadata":
                in_metadata = True
                current_key = "metadata"
                current_value = {}
                continue

            # 去除引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            metadata[key] = value

    if in_metadata and current_key == "metadata" and isinstance(current_value, dict):
        metadata["metadata"] = current_value

    return metadata, body


def validate_skill(skill_dir: str, strict: bool = False) -> ValidationResult:
    """验证一个技能目录。"""
    result = ValidationResult()
    skill_path = Path(skill_dir)

    # 检查目录存在
    if not skill_path.is_dir():
        result.error(f"目录不存在: {skill_dir}")
        return result

    result.info(f"验证技能目录: {skill_dir}")

    # 检查 SKILL.md 存在
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        result.error("缺少必需的 SKILL.md 文件")
        return result

    # 读取并解析 SKILL.md
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        result.error(f"无法读取 SKILL.md: {e}")
        return result

    metadata, body = parse_frontmatter(content)

    if metadata is None:
        result.error("SKILL.md 缺少 YAML frontmatter（必须以 --- 开头和结尾）")
        return result

    # === 验证 name 字段 ===
    name = metadata.get("name")
    if not name:
        result.error("缺少必需的 'name' 字段")
    else:
        # 长度检查
        if len(name) > 64:
            result.error(f"name 超过 64 字符限制（当前: {len(name)}）")

        # 字符检查
        if not re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$', name):
            if re.search(r'[A-Z]', name):
                result.error(f"name 包含大写字母，仅允许小写字母、数字和连字符: '{name}'")
            elif name.startswith('-') or name.endswith('-'):
                result.error(f"name 不能以连字符开头或结尾: '{name}'")
            elif '--' in name:
                result.error(f"name 包含连续连字符: '{name}'")
            else:
                result.error(f"name 包含无效字符: '{name}'")

        # 与目录名匹配
        dir_name = skill_path.name
        if name != dir_name:
            if strict:
                result.error(f"name '{name}' 与目录名 '{dir_name}' 不匹配")
            else:
                result.warn(f"name '{name}' 与目录名 '{dir_name}' 不匹配")

    # === 验证 description 字段 ===
    description = metadata.get("description")
    if not description:
        result.error("缺少必需的 'description' 字段")
    else:
        if len(description) > 1024:
            result.error(f"description 超过 1024 字符限制（当前: {len(description)}）")
        if len(description) < 10:
            result.warn("description 过短，建议至少说明功能和触发场景")
        if strict and not any(kw in description.lower() for kw in ["使用", "use", "when", "当"]):
            result.warn("description 建议使用祈使语气，说明何时使用此技能")

    # === 验证可选字段 ===
    if "compatibility" in metadata:
        compat = metadata["compatibility"]
        if compat and len(compat) > 500:
            result.error(f"compatibility 超过 500 字符限制（当前: {len(compat)}）")

    # === 验证正文内容 ===
    if not body.strip():
        result.warn("SKILL.md 正文为空，建议添加使用说明")
    else:
        line_count = len(body.strip().split("\n"))
        if line_count > 500:
            result.warn(f"SKILL.md 正文有 {line_count} 行，建议保持在 500 行以内，详细内容移到 references/")

        # 检查正文中的文件引用
        ref_pattern = re.findall(r'\b(?:references|scripts|assets)/[\w./-]+', body)
        for ref in ref_pattern:
            ref_path = skill_path / ref
            if not ref_path.exists():
                result.warn(f"引用的文件不存在: {ref}")

    # === 验证可选目录 ===
    optional_dirs = {
        "scripts": "可执行脚本",
        "references": "参考文档",
        "assets": "静态资源",
        "evals": "评估用例"
    }

    for dir_name, desc in optional_dirs.items():
        dir_path = skill_path / dir_name
        if dir_path.is_dir():
            files = list(dir_path.iterdir())
            result.info(f"发现 {dir_name}/ 目录（{desc}），包含 {len(files)} 个文件")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Agent Skills 验证器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 tools/validate.py ./my-skill
  python3 tools/validate.py ./my-skill --strict
  python3 tools/validate.py ./my-skill --json"""
    )
    parser.add_argument("skill_dir", help="技能目录路径")
    parser.add_argument("--strict", action="store_true",
                        help="严格模式（name 必须与目录名匹配等）")
    parser.add_argument("--json", action="store_true",
                        help="以 JSON 格式输出结果")

    args = parser.parse_args()

    result = validate_skill(args.skill_dir, strict=args.strict)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        # 友好的文本输出
        if result.info_list:
            for msg in result.info_list:
                print(f"  ℹ️  {msg}")

        if result.warnings:
            for msg in result.warnings:
                print(f"  ⚠️  {msg}")

        if result.errors:
            for msg in result.errors:
                print(f"  ❌ {msg}")

        print()
        if result.is_valid:
            print(f"✅ 验证通过！发现 {len(result.warnings)} 个警告")
        else:
            print(f"❌ 验证失败！发现 {len(result.errors)} 个错误，{len(result.warnings)} 个警告")

    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
