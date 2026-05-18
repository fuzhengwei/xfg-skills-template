# 快速上手指南（QUICKSTART.md）

> 5 分钟创建你的第一个 Agent Skill

---

# 快速上手

## 前提条件

- 一个支持 Agent Skills 的 AI Agent（Claude Code、GitHub Copilot、OpenAI Codex 等）
- 文本编辑器

## 第一步：创建技能目录

```bash
mkdir -p my-first-skill
cd my-first-skill
```

## 第二步：创建 SKILL.md

创建 `SKILL.md` 文件，这是技能的唯一必需文件：

```markdown
---
name: my-first-skill
description: 描述这个技能做什么以及在什么时候使用它。使用祈使语气，例如"当用户需要处理 XX 时使用此技能"。
---

# 我的第一个技能

## 功能概述
[详细说明该技能的功能]

## 使用方法
[使用步骤和最佳实践]

## 示例
[输入输出示例]
```

### Frontmatter 必填字段

| 字段 | 说明 |
|------|------|
| `name` | 技能名称（小写字母+数字+连字符，1-64字符，必须匹配目录名） |
| `description` | 功能描述+触发场景（1-1024字符） |

## 第三步：验证技能

```bash
python3 tools/validate.py ./my-first-skill
```

## 第四步：安装技能

将技能目录复制到你 Agent 的技能目录：

```bash
# 通用标准路径
cp -r my-first-skill ~/.agents/skills/

# 或项目级路径
cp -r my-first-skill .agents/skills/
```

## 第五步：测试技能

在 Agent 中提问，验证技能是否被正确触发。

---

## 进阶：添加脚本

创建 `scripts/` 目录，放入可执行脚本：

```
my-first-skill/
├── SKILL.md
└── scripts/
    └── process.py
```

在 SKILL.md 中引用：

```markdown
## 工作流

1. 运行处理脚本：
   ```bash
   python3 scripts/process.py --input data.csv
   ```
```

### 脚本最佳实践

- 使用 PEP 723 内联依赖声明（Python）
- 避免交互式提示，使用命令行参数
- 提供 `--help` 输出
- 使用结构化输出（JSON）
- 将数据发送到 stdout，诊断信息发送到 stderr

---

## 进阶：添加参考文档

将详细文档放在 `references/` 目录，SKILL.md 中按需引用：

```
my-first-skill/
├── SKILL.md
└── references/
    └── api-reference.md
```

```markdown
## 可用资源
- references/api-reference.md: API 参考文档

## 错误处理
如果 API 返回非 200 状态码，请读取 references/api-reference.md 获取错误码说明。
```

---

## 进阶：添加评估

创建 `evals/evals.json` 来测试技能质量：

```json
{
  "skill_name": "my-first-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "一个真实的用户提问",
      "expected_output": "期望输出的描述",
      "assertions": [
        "输出包含 X",
        "输出格式为 Y"
      ]
    }
  ]
}
```

---

## 从模板开始

本项目提供多种模板，选择最适合的：

| 模板 | 适用场景 | 位置 |
|------|---------|------|
| 基础模板 | 最简技能，只有 SKILL.md | `template/basic/` |
| 带脚本模板 | 需要执行脚本的技能 | `template/with-scripts/` |
| 带参考文档模板 | 需要详细文档的技能 | `template/with-references/` |
| 完整功能模板 | 生产级技能，全功能 | `template/full-featured/` |

```bash
# 从完整功能模板创建
cp -r template/full-featured my-production-skill
cd my-production-skill
# 编辑 SKILL.md，修改 name 和 description
```

---

## 技能编写速查表

### ✅ 应该做的

- ✅ description 使用祈使语气："当用户需要...时使用此技能"
- ✅ 专注 Agent 不知道的内容，省略常识
- ✅ 保持 SKILL.md < 500 行 / < 5000 tokens
- ✅ 提供具体的默认值而非选项菜单
- ✅ 包含 gotchas（容易踩坑的地方）
- ✅ 提供输出格式模板
- ✅ 使用渐进式披露，详细内容放 references/

### ❌ 不应该做的

- ❌ 在 description 中过于模糊（"处理文件"）
- ❌ 解释 Agent 已经知道的概念
- ❌ 让 SKILL.md 过于冗长
- ❌ 呈现多个平等选项而不提供默认值
- ❌ 脚本中使用交互式提示
- ❌ 将所有内容都塞进 SKILL.md

---

*开始创建你的第一个技能吧！🚀*
