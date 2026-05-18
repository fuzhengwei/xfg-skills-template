---
name: xfg-skills-template
description: Agent Skills 技能模板与脚手架。当用户需要创建新的 AI Agent 技能（Skill）、编写 SKILL.md、搭建技能工程结构，或提到技能开发、技能模板、skill creator 时使用此技能。
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "1.0.0"
  category: tooling
  homepage: https://github.com/fuzhengwei/xfg-skills-template
---

# Agent Skills 技能模板

帮助快速创建符合 [Agent Skills 开放标准](https://agentskills.io/) 的技能包，兼容 Claude Code、GitHub Copilot、OpenAI Codex、Cursor 等 12+ AI Agent 客户端。

## 技能创建流程

### 第一步：选择模板

根据需求选择合适的模板，复制到目标目录：

| 模板 | 适用场景 | 包含内容 |
|------|---------|---------|
| `template/basic/` | 简单技能，纯指令 | 仅 SKILL.md |
| `template/with-scripts/` | 需要执行脚本 | SKILL.md + scripts/ |
| `template/with-references/` | 需要参考文档（渐进式披露） | SKILL.md + references/ |
| `template/full-featured/` | 生产级技能 | SKILL.md + scripts/ + references/ + assets/ + evals/ |

```bash
# 示例：创建一个带脚本的技能
cp -r template/with-scripts/ my-new-skill/
```

### 第二步：编写 SKILL.md

SKILL.md 是技能的**唯一必需文件**，格式如下：

```markdown
---
name: my-skill          # 必需，1-64字符，小写字母+连字符，须匹配目录名
description: 触发描述    # 必需，1-1024字符，说明何时使用此技能
license: Apache-2.0     # 可选
compatibility: 环境要求  # 可选，≤500字符
metadata:               # 可选，任意键值
  author: your-name
  version: "1.0.0"
  category: your-category
allowed-tools: Bash(python3:*) Read Write  # 可选，实验性
---

# 技能名称

## 功能概述
简洁描述（1-3句话）

## 使用方法
具体操作步骤

## Gotchas
容易踩的坑（最高价值内容）
```

**Frontmatter 规则**：
- `name`：1-64字符，仅小写字母和连字符，不能有连续连字符，**必须与目录名一致**
- `description`：1-1024字符，用祈使语气，关注用户意图，这是 Agent 决定是否激活技能的**唯一依据**
- 文件引用使用相对路径，保持一层深度

### 第三步：添加资源（可选）

```
my-skill/
├── SKILL.md              # 必需入口
├── scripts/              # 可执行脚本
│   └── process.py
├── references/           # 参考文档（按需加载，渐进式披露）
│   └── api-reference.md
├── assets/               # 静态资源/模板
│   └── template.yaml
└── evals/                # 评估用例
    └── evals.json
```

**渐进式披露原则**：
- 启动时仅加载元数据（~100 tokens/skill）
- 激活时加载完整指令（<5000 tokens）
- 按需加载 references/ 中的详细文档

### 第四步：验证

```bash
python3 tools/validate.py ./my-skill
python3 tools/validate.py ./my-skill --strict   # 严格模式
python3 tools/validate.py ./my-skill --json      # JSON 输出
```

### 第五步：评估（可选）

```bash
# 运行评估对比
bash tools/eval-runner.sh ./my-skill

# 优化描述的触发准确性
python3 tools/description-optimizer.py ./my-skill
```

### 第六步：安装

```bash
# Claude Code
cp -r my-skill ~/.claude/skills/

# GitHub Copilot
cp -r my-skill .agents/skills/

# OpenClaw
cp -r my-skill ~/.qclaw/skills/

# OpenAI Codex
cp -r my-skill ~/.codex/skills/
```

## SKILL.md 编写最佳实践

1. **从真实专长出发**，不要凭空编写泛泛的内容
2. **只写 Agent 不知道的**，省略它已知的常识
3. **Gotchas 节最有价值**：环境特有事实、常见陷阱
4. **提供默认值**而非菜单选项
5. **偏向过程性指令**而非声明性描述
6. **SKILL.md 保持 <500 行**，详细内容移到 references/
7. **脚本避免交互式提示**，提供 --help，写有用错误信息
8. **结构化输出**：JSON/CSV 到 stdout，诊断信息到 stderr

## 参考文档

- `references/specification.md` — Agent Skills 完整规范
- `references/best-practices.md` — 编写最佳实践详解
- `references/quickstart.md` — 5 分钟快速上手

## 示例技能

查看 `examples/` 目录中的完整示例：

| 示例 | 说明 |
|------|------|
| `examples/code-review/` | 代码审查技能 |
| `examples/data-analysis/` | 数据分析技能 |
| `examples/api-integration/` | API 集成技能 |
| `examples/document-generator/` | 文档生成技能 |
