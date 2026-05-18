# xfg-skills-template 🛠️

> Agent Skills 技能模板工程 — 安装后，AI Agent 帮你创建新技能

基于 [Agent Skills 开放标准](https://agentskills.io/)，安装此技能后，你的 AI Agent 就能帮你快速创建符合规范的新技能包。

## 它是什么

这是一个 **AI Agent 技能**（不是普通工具库）。安装到你的 Agent 后，当你需要创建新技能时，Agent 会自动加载它，按照规范帮你生成 SKILL.md 和目录结构。

**不安装** → 你需要自己翻规范、手写 SKILL.md、手动建目录  
**安装后** → 告诉 Agent "帮我创建一个 XX 技能"，它按流程帮你搞定

## 兼容的 AI Agent

| Agent | 安装路径 | 项目级路径 |
|-------|---------|-----------|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` |
| **GitHub Copilot** | `~/.agents/skills/` | `.agents/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` | `.codex/skills/` |
| **Cursor** | `~/.cursor/skills/` | `.cursor/skills/` |
| **OpenClaw** | `~/.qclaw/skills/` | - |
| **Roo Code** | `~/.roo/skills/` | `.roo/skills/` |
| **Gemini CLI** | `~/.gemini/skills/` | `.gemini/skills/` |

## 安装

```bash
# 克隆项目
git clone https://github.com/fuzhengwei/xfg-skills-template.git

# 安装到你使用的 Agent（选一个）
cp -r xfg-skills-template ~/.claude/skills/       # Claude Code
cp -r xfg-skills-template ~/.agents/skills/        # GitHub Copilot / 通用
cp -r xfg-skills-template ~/.qclaw/skills/         # OpenClaw
cp -r xfg-skills-template ~/.codex/skills/         # OpenAI Codex
```

安装后重启 Agent，即可使用。

## 使用方法

### 方式一：让 Agent 帮你创建（推荐）

直接告诉你的 AI Agent：

> "帮我创建一个技能，用于从 PDF 提取表格数据"

Agent 会自动加载 xfg-skills-template 技能，按以下流程帮你创建：

1. **选择模板** — 根据需求从 4 种模板中选一个
2. **生成 SKILL.md** — 填写 name、description、指令内容
3. **创建目录结构** — scripts/、references/、assets/ 按需生成
4. **验证** — 运行 validate.py 检查格式合规
5. **安装** — 复制到 Agent 的 skills 目录

### 方式二：手动创建

#### 1. 选模板

| 模板 | 适用场景 | 包含 |
|------|---------|------|
| `template/basic/` | 纯指令技能 | SKILL.md |
| `template/with-scripts/` | 需要运行脚本 | SKILL.md + scripts/ |
| `template/with-references/` | 有详细参考文档 | SKILL.md + references/ |
| `template/full-featured/` | 生产级完整技能 | 全部目录 |

```bash
cp -r template/with-scripts/ my-skill/
cd my-skill
```

#### 2. 编辑 SKILL.md

```markdown
---
name: my-skill              # 必需，小写+连字符，须匹配目录名
description: 当用户需要...时使用此技能  # 必需，≤1024字符
license: Apache-2.0         # 可选
metadata:                   # 可选
  author: your-name
  version: "1.0.0"
---

# 技能名称

## 功能概述
1-3句话说明

## 使用方法
具体操作步骤

## Gotchas
容易踩的坑
```

**关键规则**：
- `name`：仅小写字母+连字符，1-64字符，必须和目录名一致
- `description`：祈使语气，关注用户意图，这是 Agent 决定是否激活的**唯一依据**
- SKILL.md 保持 <500 行 / <5000 tokens，详细内容放 references/
- 文件引用用相对路径，保持一层深度

#### 3. 添加资源目录（可选）

```
my-skill/
├── SKILL.md              # 必需
├── scripts/              # 可执行脚本（避免交互式提示）
│   └── process.py
├── references/           # 参考文档（按需加载，节省 tokens）
│   └── api-reference.md
├── assets/               # 模板/静态资源
│   └── template.yaml
└── evals/                # 评估用例
    └── evals.json
```

**渐进式披露**：Agent 分三阶段加载
- 启动 → 仅加载 name+description（~100 tokens）
- 激活 → 加载完整 SKILL.md（<5000 tokens）
- 按需 → 读取 references/、运行 scripts/

#### 4. 验证

```bash
python3 tools/validate.py ./my-skill          # 基础验证
python3 tools/validate.py ./my-skill --strict  # 严格模式
python3 tools/validate.py ./my-skill --json    # JSON 输出
```

#### 5. 安装

```bash
cp -r my-skill ~/.claude/skills/    # Claude Code
cp -r my-skill .agents/skills/      # GitHub Copilot
cp -r my-skill ~/.qclaw/skills/     # OpenClaw
```

#### 6. 评估（可选）

```bash
bash tools/eval-runner.sh ./my-skill                      # 运行评估
python3 tools/description-optimizer.py ./my-skill          # 优化描述触发准确性
```

## 项目结构

```
xfg-skills-template/
├── SKILL.md                           # 技能入口（Agent 加载此文件）
├── README.md                          # 本文件
│
├── template/                          # 4 种技能模板
│   ├── basic/                         #   纯指令
│   ├── with-scripts/                  #   带脚本
│   ├── with-references/               #   带参考文档
│   └── full-featured/                 #   完整功能
│
├── examples/                          # 4 个完整示例技能
│   ├── code-review/                   #   代码审查
│   ├── data-analysis/                 #   数据分析
│   ├── api-integration/               #   API 集成
│   └── document-generator/            #   文档生成
│
├── references/                        # 参考文档（渐进式披露）
│   ├── specification.md               #   Agent Skills 完整规范
│   ├── best-practices.md              #   编写最佳实践
│   └── quickstart.md                  #   快速上手指南
│
└── tools/                             # 开发工具
    ├── validate.py                    #   技能验证器
    ├── eval-runner.sh                 #   评估运行器
    └── description-optimizer.py       #   描述优化器
```

## 编写最佳实践速查

### ✅ 应该

- description 用祈使语气："当用户需要处理 XX 时使用此技能"
- 只写 Agent 不知道的内容，省略常识
- SKILL.md < 500 行 / < 5000 tokens
- 提供默认值而非选项菜单
- 包含 Gotchas（最容易踩坑的点）
- 提供输出格式模板
- 脚本避免交互式提示，用 --help，写有用错误信息
- 结构化输出：JSON/CSV → stdout，诊断 → stderr

### ❌ 不应该

- description 过于模糊（"处理文件"）
- 解释 Agent 已知的概念（"PDF 是便携式文档格式"）
- 把所有内容塞进 SKILL.md
- 呈现多个平等选项不给默认值
- 脚本中使用交互式提示

## 已有的技能

基于此模板创建的技能：

| 技能 | 说明 | 仓库 |
|------|------|------|
| xfg-skills-docker-install | Docker 环境安装与软件部署 | [GitHub](https://github.com/fuzhengwei/xfg-skills-docker-install) |

## 参考资源

- [Agent Skills 官方规范](https://agentskills.io/specification) — 开放标准原文
- [Anthropic Skills 仓库](https://github.com/anthropics/skills) — 示例参考
- [SkillsMP 技能市场](https://skillsmp.com/zh) — 140万+ 技能
- [GitHub Copilot Skills 文档](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## 许可证

Apache License 2.0
