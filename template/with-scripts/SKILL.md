---
name: with-scripts
description: 带脚本的技能模板。当需要执行可复用的自动化脚本时使用此模板，例如数据处理、文件转换、批量操作等场景。
---

# 带脚本的技能模板

本模板展示了如何在技能中集成可执行脚本，遵循 Agent Skills 开放标准。

## 使用方法

1. 将你的脚本放入 `scripts/` 目录
2. 在 SKILL.md 中用相对路径引用脚本
3. Agent 按需执行脚本

## 可用脚本

- **`scripts/example.py`** — 示例数据处理脚本

## 工作流

1. 准备输入数据
2. 运行处理脚本：
   ```bash
   python3 scripts/example.py --input data.csv
   ```
3. 检查输出结果

## 脚本编写规范

- ✅ 使用 PEP 723 声明依赖（Python）
- ✅ 提供 `--help` 输出
- ✅ 避免交互式提示
- ✅ 使用结构化输出（JSON）
- ✅ 数据输出到 stdout，诊断信息到 stderr
