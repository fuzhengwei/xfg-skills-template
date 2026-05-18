---
name: with-references
description: 带参考文档的技能模板。当技能需要详细的参考文档但不希望将所有内容塞入 SKILL.md 时使用此模板，利用渐进式披露优化上下文使用。
---

# 带参考文档的技能模板

本模板展示了如何使用 `references/` 目录存放详细文档，通过渐进式披露优化 Token 消耗。

## 使用方法

1. 核心指令放在 SKILL.md（< 5000 tokens）
2. 详细文档放在 `references/` 目录
3. 在 SKILL.md 中告诉 Agent **何时**加载参考文档

## 可用资源

- **`references/api-reference.md`** — API 参考文档

## 按需加载策略

```markdown
### 何时加载参考文档
- 当需要查询 API 端点详情时，读取 references/api-reference.md
- 当遇到错误码时，读取 references/api-reference.md 中的错误码表
```

## 示例工作流

1. 根据用户需求确定操作
2. 如果需要 API 详情，读取 `references/api-reference.md`
3. 执行操作
4. 验证结果
