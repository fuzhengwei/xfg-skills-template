# xfg-skills-template 🛠️

> Agent Skills 技能包模板工程 — 一套完整的技能开发规范、模板与工具链

基于 [Agent Skills 开放标准](https://agentskills.io/) 的技能包模板工程，帮助你快速创建、测试和分发高质量的 AI Agent 技能。

## 🌟 项目特色

- **符合开放标准**：完全兼容 [Agent Skills Specification](https://agentskills.io/specification)，支持 Claude Code、GitHub Copilot、OpenAI Codex、Cursor 等主流 AI Agent
- **开箱即用的模板**：提供多种场景模板（文档处理、数据分析、代码审查、API 集成等），复制即用
- **完整的开发工具链**：验证器、评估框架、描述优化工具，覆盖技能全生命周期
- **渐进式披露设计**：遵循三阶段加载规范，优化 Token 消耗
- **中文友好**：文档和注释均提供中英双语

## 📁 项目结构

```
xfg-skills-template/
├── README.md                          # 项目说明
├── SPECIFICATION.md                   # Agent Skills 规范中文翻译
├── BEST-PRACTICES.md                  # 技能编写最佳实践
├── QUICKSTART.md                      # 快速上手指南
├── LICENSE                            # Apache-2.0 许可证
│
├── template/                          # 技能模板目录
│   ├── basic/                         # 基础模板（最简结构）
│   │   └── SKILL.md
│   ├── with-scripts/                  # 带脚本的模板
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── example.py
│   ├── with-references/               # 带参考文档的模板
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── api-reference.md
│   └── full-featured/                 # 完整功能模板
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── validate.sh
│       │   └── process.py
│       ├── references/
│       │   ├── architecture.md
│       │   └── api-reference.md
│       ├── assets/
│       │   └── template.yaml
│       └── evals/
│           └── evals.json
│
├── examples/                          # 完整示例技能
│   ├── code-review/                   # 代码审查技能
│   ├── data-analysis/                 # 数据分析技能
│   ├── api-integration/               # API 集成技能
│   └── document-generator/            # 文档生成技能
│
└── tools/                             # 开发工具
    ├── validate.py                    # 技能验证器
    ├── eval-runner.sh                 # 评估运行器
    └── description-optimizer.py       # 描述优化工具
```

## 🚀 快速开始

### 1. 创建你的第一个技能

```bash
# 复制基础模板
cp -r template/basic my-skill

# 编辑 SKILL.md
cd my-skill
vim SKILL.md
```

### 2. 验证技能

```bash
python3 tools/validate.py ./my-skill
```

### 3. 安装到你的 Agent

根据你使用的 AI Agent，将技能目录复制到对应位置：

| Agent | 项目级路径 | 用户级路径 |
|-------|-----------|-----------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.agents/skills/` |
| OpenAI Codex | `.codex/skills/` | `~/.codex/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| 通用标准 | `.agents/skills/` | `~/.agents/skills/` |

## 📖 文档导航

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](./QUICKSTART.md) | 5 分钟创建第一个技能 |
| [SPECIFICATION.md](./SPECIFICATION.md) | Agent Skills 完整规范 |
| [BEST-PRACTICES.md](./BEST-PRACTICES.md) | 技能编写最佳实践 |

## 🔑 核心概念

### 渐进式披露（Progressive Disclosure）

技能加载分三个阶段，逐步按需加载内容：

1. **元数据**（~100 tokens）：启动时加载 `name` + `description`
2. **指令**（< 5000 tokens）：技能激活时加载完整 SKILL.md
3. **资源**（按需）：仅当指令引用时才加载 scripts/、references/、assets/

### SKILL.md 格式

```markdown
---
name: my-skill-name
description: 清晰描述技能的功能和触发场景
license: Apache-2.0
compatibility: Requires Python 3.10+
metadata:
  author: your-name
  version: "1.0"
allowed-tools: Bash(git:*) Read
---

# 技能名称

## 功能概述
[详细说明]

## 使用方法
[步骤和最佳实践]
```

### 技能目录结构

```
skill-name/
├── SKILL.md          # 必需：元数据 + 指令
├── scripts/          # 可选：可执行脚本
├── references/       # 可选：参考文档
├── assets/           # 可选：模板和静态资源
└── evals/            # 可选：评估测试用例
```

## 🤝 兼容性

本模板工程产出的技能兼容以下 AI Agent 产品：

- ✅ Claude Code / Claude.ai
- ✅ GitHub Copilot
- ✅ OpenAI Codex CLI
- ✅ Cursor
- ✅ VS Code Copilot Agent
- ✅ Roo Code
- ✅ Gemini CLI
- ✅ JetBrains Junie
- ✅ OpenHands
- ✅ Go Goose
- ✅ Spring AI
- ✅ 更多兼容 Agent Skills 标准的产品

## 📜 许可证

Apache License 2.0

## 🔗 参考资源

- [Agent Skills 官方规范](https://agentskills.io/specification)
- [Anthropic Skills 仓库](https://github.com/anthropics/skills)
- [SkillsMP 技能市场](https://skillsmp.com/zh)
- [GitHub Copilot Skills 文档](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
