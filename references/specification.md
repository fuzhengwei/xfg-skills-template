# SPECIFICATION.md — Agent Skills 规范中文版

> 本文档是 [Agent Skills 官方规范](https://agentskills.io/specification) 的中文翻译版本。
> 原文遵循开放标准，被 Claude Code、GitHub Copilot、OpenAI Codex 等主流产品采用。

---

# Agent Skills 规范

## 目录结构

一个技能（Skill）是一个包含至少一个 `SKILL.md` 文件的目录：

```
skill-name/
├── SKILL.md          # 必需：元数据 + 指令
├── scripts/          # 可选：可执行代码
├── references/       # 可选：参考文档
├── assets/           # 可选：模板、静态资源
└── ...               # 任意其他文件或目录
```

## `SKILL.md` 格式

`SKILL.md` 文件必须包含 YAML frontmatter，后跟 Markdown 正文内容。

### Frontmatter 字段

| 字段 | 必需 | 约束 |
|------|------|------|
| `name` | 是 | 最多 64 字符。仅允许小写字母、数字和连字符。不能以连字符开头或结尾。 |
| `description` | 是 | 最多 1024 字符。非空。描述技能的功能和触发场景。 |
| `license` | 否 | 许可证名称或许可协议文件路径。 |
| `compatibility` | 否 | 最多 500 字符。说明环境要求（目标产品、系统依赖、网络访问等）。 |
| `metadata` | 否 | 任意键值对，用于额外元数据。 |
| `allowed-tools` | 否 | 空格分隔的预批准工具列表（实验性）。 |

---

#### `name` 字段

必需的 `name` 字段：
- 必须为 1-64 个字符
- 仅允许 Unicode 小写字母数字字符（`a-z`）和连字符（`-`）
- 不能以连字符开头或结尾
- 不能包含连续连字符（`--`）
- 必须与父目录名称一致

✅ 有效示例：
```yaml
name: pdf-processing
name: data-analysis
name: code-review
```

❌ 无效示例：
```yaml
name: PDF-Processing   # 不允许大写
name: -pdf            # 不能以连字符开头
name: pdf--processing # 不能有连续连字符
```

---

#### `description` 字段

必需的 `description` 字段：
- 必须为 1-1024 个字符
- 应同时描述技能的功能和触发场景
- 应包含帮助 Agent 识别相关任务的关键词

✅ 好的示例：
```yaml
description: 从 PDF 文件中提取文本和表格，填写 PDF 表单，合并多个 PDF。当处理 PDF 文档或用户提到 PDF、表单或文档提取时使用。
```

❌ 差的示例：
```yaml
description: 处理 PDF 文件。
```

---

#### `license` 字段

可选的 `license` 字段：
- 指定技能所适用的许可证
- 建议保持简短（许可证名称或许可文件路径）

```yaml
license: Apache-2.0
license: Proprietary. LICENSE.txt 包含完整条款
```

---

#### `compatibility` 字段

可选的 `compatibility` 字段：
- 如提供，必须为 1-500 字符
- 仅在技能有特定环境要求时才应包含
- 可说明目标产品、所需系统包、网络访问需求等

```yaml
compatibility: 为 Claude Code（或类似产品）设计
compatibility: 需要 git、docker、jq 和互联网访问
compatibility: 需要 Python 3.14+ 和 uv
```

> 大多数技能不需要 `compatibility` 字段。

---

#### `metadata` 字段

可选的 `metadata` 字段：
- 从字符串键到字符串值的映射
- 客户端可用此存储 Agent Skills 规范中未定义的额外属性
- 建议使键名具有足够唯一性，避免意外冲突

```yaml
metadata:
  author: example-org
  version: "1.0"
```

---

#### `allowed-tools` 字段（实验性）

可选的 `allowed-tools` 字段：
- 空格分隔的预批准工具名称字符串
- 支持程度因 Agent 实现而异

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

---

### 正文内容

frontmatter 之后的 Markdown 正文包含技能指令。格式无限制。编写任何有助于 Agent 有效执行任务的内容。

建议包含以下部分：
- 逐步指令
- 输入和输出示例
- 常见边缘情况

注意：一旦 Agent 决定激活技能，将加载整个 `SKILL.md` 文件。考虑将较长的正文内容拆分到引用文件中。

---

## 可选目录

### `scripts/`

包含 Agent 可以运行的可执行代码。脚本应：
- 自包含或清晰说明依赖
- 包含有用的错误消息
- 优雅地处理边缘情况

支持的语言取决于 Agent 实现。常见选项包括 Python、Bash 和 JavaScript。

### `references/`

包含 Agent 需要时可读的额外文档：
- `REFERENCE.md` — 详细技术参考
- `FORMS.md` — 表单模板或结构化数据格式
- 领域特定文件（`finance.md`、`legal.md` 等）

保持各[引用文件](#文件引用)聚焦。Agent 按需加载这些文件，较小的文件意味着较少的上下文占用。

### `assets/`

包含静态资源：
- 模板（文档模板、配置模板）
- 图片（图表、示例）
- 数据文件（查询表、模式）

---

## 渐进式披露（Progressive Disclosure）

Agent **渐进式**加载技能，仅在任务需要时才拉取更多细节。技能应结构化以利用这一点：

1. **元数据**（约 100 tokens）：启动时为所有技能加载 `name` 和 `description` 字段
2. **指令**（推荐 < 5000 tokens）：技能激活时加载完整 `SKILL.md` 正文
3. **资源**（按需）：文件（如 `scripts/`、`references/` 或 `assets/` 中的文件）仅在需要时才加载

将主 `SKILL.md` 保持在 500 行以内。将详细的参考材料移到单独的文件。

---

## 文件引用

在技能中引用其他文件时，使用相对于**技能根目录**的路径：

```markdown
参见 [参考指南](references/REFERENCE.md) 获取详情。

运行提取脚本：
scripts/extract.py
```

将文件引用保持在距 `SKILL.md` 一级深度。避免深度嵌套的引用链。

---

## 验证

使用 [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) 参考库验证你的技能：

```bash
skills-ref validate ./my-skill
```

这会检查你的 `SKILL.md` frontmatter 是否有效并遵循所有命名约定。

---

## 技能安装路径规范

Agent Skills 标准推荐使用以下目录结构进行技能发现：

| 作用域 | 路径 | 用途 |
|--------|------|------|
| 项目级 | `<项目>/.agents/skills/` | 跨客户端互操作性（推荐） |
| 项目级 | `<项目>/.<客户端>/skills/` | 客户端原生位置 |
| 用户级 | `~/.agents/skills/` | 跨客户端互操作性（推荐） |
| 用户级 | `~/.<客户端>/skills/` | 客户端原生位置 |

优先级：**项目级技能覆盖用户级技能**。

---

*本规范由 Agent Skills 社区维护，遵循开放标准。*
*中文翻译：xfg-skills-template 项目*
