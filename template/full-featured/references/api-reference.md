# API 参考文档

> 当需要查询 API 端点详情或错误码时读取此文档。

## 错误码表

| 退出码 | 含义 | 处理建议 |
|--------|------|---------|
| 0 | 成功 | - |
| 1 | 文件不存在 | 检查文件路径 |
| 2 | 格式错误 | 检查文件格式和编码 |
| 3 | 权限不足 | 检查文件权限 |

## 命令行接口

### validate.sh

```bash
bash scripts/validate.sh --input <file> [--verbose]
```

### process.py

```bash
python3 scripts/process.py --input <file> [--format json|csv|table] [--output <file>] [--limit N] [--verbose]
python3 scripts/process.py --validate <output_file>
```
