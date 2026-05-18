---
name: full-featured
description: 完整功能技能模板，包含脚本、参考文档、静态资源和评估用例。当构建生产级技能时使用此模板，涵盖技能全生命周期的最佳实践。
license: Apache-2.0
compatibility: 需要 Python 3.10+ 和 bash
metadata:
  author: xfg-studio
  version: "1.0.0"
  category: template
allowed-tools: Bash(python3:*) Bash(bash:*) Read Write
---

# 完整功能技能模板

本模板展示了生产级技能的完整结构，包含所有可选目录和最佳实践。

## 功能概述

描述此技能的核心功能。保持简洁，1-3 句话。

## 使用方法

### 基本工作流

1. **验证输入**：运行验证脚本确认输入有效
   ```bash
   bash scripts/validate.sh --input <input_file>
   ```

2. **处理数据**：运行处理脚本
   ```bash
   python3 scripts/process.py --input <input_file> --output <output_file>
   ```

3. **验证输出**：检查输出是否符合预期
   ```bash
   python3 scripts/process.py --validate <output_file>
   ```

### 输出格式

使用以下模板生成报告：

```markdown
# [报告标题]

## 摘要
[一段概述]

## 详情
- 项目 1
- 项目 2

## 建议
1. 可执行的建议
```

## 可用脚本

- **`scripts/validate.sh`** — 验证输入文件格式
- **`scripts/process.py`** — 数据处理（支持 PEP 723 依赖声明）

## 可用资源

- **`references/architecture.md`** — 架构设计文档（当需要理解系统设计时读取）
- **`references/api-reference.md`** — API 参考文档（当需要查询 API 详情时读取）
- **`assets/template.yaml`** — 配置模板（当需要生成配置文件时使用）

## Gotchas

- 输入文件编码必须为 UTF-8，否则脚本会报错
- 处理脚本默认限制输出 1000 行，使用 `--limit` 参数调整
- 验证脚本需要 bash 4.0+，macOS 自带版本可能不兼容

## 错误处理

- 如果脚本返回非零退出码，阅读 stderr 输出的错误消息
- 常见错误：文件不存在（退出码 1）、格式错误（退出码 2）、权限不足（退出码 3）
- 遇到 API 错误时，读取 `references/api-reference.md` 中的错误码表
