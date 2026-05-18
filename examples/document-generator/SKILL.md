---
name: document-generator
description: 生成 Markdown 文档、API 文档、README、CHANGELOG 等技术文档。当用户需要编写或更新技术文档、生成 README、编写 API 文档、创建 CHANGELOG，或提到文档、README、文档生成时使用此技能。
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "1.0.0"
  category: documentation
---

# 文档生成技能

生成符合社区标准的技术文档。

## 支持的文档类型

### README.md

使用以下模板：

```markdown
# 项目名称

> 一句话描述项目

## 功能特色

- 特色 1
- 特色 2

## 快速开始

### 安装
```bash
npm install package-name
```

### 使用
```javascript
import { feature } from 'package-name';
```

## 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|

## API 文档

详见 [API.md](./API.md)

## 许可证

Apache-2.0
```

### CHANGELOG.md

遵循 [Keep a Changelog](https://keepachangelog.com/) 格式：

```markdown
# Changelog

## [Unreleased]

## [1.0.0] - 2025-01-15

### Added
- 新功能描述

### Changed
- 变更描述

### Fixed
- 修复描述

### Removed
- 移除描述
```

### API 文档

```markdown
# API Reference

## Endpoint: GET /users

**描述**: 获取用户列表

**参数**:
| Name | Type | Required | Description |
|------|------|----------|-------------|

**响应**:
```json
{ "example": "response" }
```

**错误码**:
| Code | Message | Description |
|------|---------|-------------|
```

## 工作流

1. 分析项目结构和现有代码
2. 确定需要生成的文档类型
3. 使用对应模板生成文档
4. 检查文档完整性和准确性

## 文档质量标准

- 所有代码示例必须是可运行的
- 所有链接必须有效
- 中英文之间有空格
- 表格对齐整齐
- 代码块指定语言类型

## Gotchas

- README 不要过度美化，内容 > 格式
- CHANGELOG 面向人类读者，不要自动生成无意义的条目
- API 文档中的示例应该是真实可用的，不是伪代码
- 项目有 `.github/` 目录时，也要检查 ISSUE_TEMPLATE 和 PR_TEMPLATE
