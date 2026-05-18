#!/usr/bin/env python3
"""
技能描述优化工具

帮助测试和优化技能的 description 字段，提高触发准确率。

用法:
    python3 tools/description-optimizer.py ./my-skill
    python3 tools/description-optimizer.py ./my-skill --generate-queries
    python3 tools/description-optimizer.py ./my-skill --eval-queries queries.json

详见: https://agentskills.io/skill-creation/optimizing-descriptions
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(content: str):
    """解析 SKILL.md 的 YAML frontmatter。"""
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    metadata = {}
    for line in frontmatter_text.split("\n"):
        match = re.match(r'^(\w[\w-]*):\s*(.*)', line.strip())
        if match:
            key = match.group(1)
            value = match.group(2).strip().strip('"').strip("'")
            metadata[key] = value

    return metadata, body


def analyze_description(name: str, description: str) -> dict:
    """分析 description 的质量。"""
    issues = []
    suggestions = []

    # 长度检查
    if len(description) < 20:
        issues.append("description 过短，可能无法准确传达触发场景")
        suggestions.append("建议添加具体的触发场景，如'当用户需要处理 XX 或提到 YY 时使用'")
    elif len(description) > 1024:
        issues.append(f"description 超过 1024 字符限制（当前: {len(description)}）")

    # 祈使语气检查
    imperative_patterns = ["使用", "use", "when", "当", "用于", "适用于"]
    has_imperative = any(p in description.lower() for p in imperative_patterns)
    if not has_imperative:
        suggestions.append("建议使用祈使语气，如'当用户需要...时使用此技能'")

    # 关键词覆盖
    if name.replace("-", " ") not in description.lower():
        suggestions.append(f"建议在 description 中包含技能名称的关键词: {name}")

    # 触发场景明确性
    trigger_patterns = ["当", "when", "如果", "if", "适用于", "for"]
    has_trigger = any(p in description.lower() for p in trigger_patterns)
    if not has_trigger:
        suggestions.append("建议明确说明触发场景，告诉 Agent 何时应该激活此技能")

    return {
        "length": len(description),
        "max_length": 1024,
        "has_imperative": has_imperative,
        "has_trigger_context": has_trigger,
        "issues": issues,
        "suggestions": suggestions
    }


def generate_eval_queries(name: str, description: str) -> list:
    """生成评估查询用例（辅助手动创建 eval_queries.json）。"""
    queries = []

    # 基于技能名称生成 should-trigger 查询
    words = name.replace("-", " ").split()
    queries.append({
        "query": f"帮我{description[:20]}...",
        "should_trigger": True
    })
    queries.append({
        "query": f"我需要处理{name.replace('-', ' ')}相关的任务",
        "should_trigger": True
    })

    # 近似但不该触发的查询
    queries.append({
        "query": "帮我写一个斐波那契函数",
        "should_trigger": False
    })
    queries.append({
        "query": "今天天气怎么样？",
        "should_trigger": False
    })

    return queries


def main():
    parser = argparse.ArgumentParser(
        description="技能描述优化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 tools/description-optimizer.py ./my-skill
  python3 tools/description-optimizer.py ./my-skill --generate-queries
  python3 tools/description-optimizer.py ./my-skill --eval-queries queries.json"""
    )
    parser.add_argument("skill_dir", help="技能目录路径")
    parser.add_argument("--generate-queries", action="store_true",
                        help="生成评估查询用例模板")
    parser.add_argument("--eval-queries", help="评估查询文件路径（JSON）")

    args = parser.parse_args()

    skill_path = Path(args.skill_dir)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.is_file():
        print(f"❌ 未找到 SKILL.md: {skill_md}")
        sys.exit(1)

    content = skill_md.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    if metadata is None:
        print("❌ SKILL.md 格式错误：缺少 frontmatter")
        sys.exit(1)

    name = metadata.get("name", "")
    description = metadata.get("description", "")

    print(f"📋 技能名称: {name}")
    print(f"📝 当前描述: {description}")
    print(f"📏 描述长度: {len(description)} / 1024 字符")
    print()

    # 分析描述质量
    analysis = analyze_description(name, description)

    if analysis["issues"]:
        print("⚠️  问题:")
        for issue in analysis["issues"]:
            print(f"  • {issue}")
        print()

    if analysis["suggestions"]:
        print("💡 优化建议:")
        for suggestion in analysis["suggestions"]:
            print(f"  • {suggestion}")
        print()

    if not analysis["issues"] and not analysis["suggestions"]:
        print("✅ 描述质量良好！")

    # 生成查询用例
    if args.generate_queries:
        queries = generate_eval_queries(name, description)
        output_file = skill_path / "eval_queries.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(queries, f, ensure_ascii=False, indent=2)
        print(f"\n📝 已生成评估查询模板: {output_file}")
        print("   请根据实际场景补充更多查询用例")


if __name__ == "__main__":
    main()
