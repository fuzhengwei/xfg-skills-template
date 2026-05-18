#!/usr/bin/env bash
# validate.sh — 验证输入文件格式
#
# 用法:
#   bash scripts/validate.sh --input <input_file>
#   bash scripts/validate.sh --input data.json --verbose
#
# 退出码:
#   0 - 验证通过
#   1 - 文件不存在
#   2 - 格式错误
#   3 - 权限不足

set -euo pipefail

INPUT_FILE=""
VERBOSE=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --input)  INPUT_FILE="$2"; shift 2 ;;
        --verbose) VERBOSE=1; shift ;;
        --help|-h)
            echo "用法: bash scripts/validate.sh --input <input_file> [--verbose]"
            echo ""
            echo "验证输入文件格式"
            echo ""
            echo "选项:"
            echo "  --input FILE    输入文件路径 (必填)"
            echo "  --verbose       输出详细信息"
            echo "  --help          显示帮助信息"
            echo ""
            echo "示例:"
            echo "  bash scripts/validate.sh --input data.json"
            exit 0
            ;;
        *)
            echo "Error: 未知参数: $1" >&2
            exit 2
            ;;
    esac
done

if [[ -z "$INPUT_FILE" ]]; then
    echo "Error: --input 是必填参数" >&2
    echo "用法: bash scripts/validate.sh --input <input_file>" >&2
    exit 2
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: 文件不存在: $INPUT_FILE" >&2
    exit 1
fi

if [[ ! -r "$INPUT_FILE" ]]; then
    echo "Error: 权限不足，无法读取: $INPUT_FILE" >&2
    exit 3
fi

if [[ $VERBOSE -eq 1 ]]; then
    echo "[INFO] 正在验证: $INPUT_FILE" >&2
fi

# === 在此处添加你的验证逻辑 ===
# 示例: 检查是否为有效的 JSON
if command -v python3 &>/dev/null; then
    if python3 -c "import json; json.load(open('$INPUT_FILE'))" 2>/dev/null; then
        if [[ $VERBOSE -eq 1 ]]; then
            echo "[INFO] JSON 格式验证通过" >&2
        fi
    else
        echo "Error: 文件不是有效的 JSON 格式: $INPUT_FILE" >&2
        exit 2
    fi
fi
# ==============================

echo '{"status": "valid", "file": "'"$INPUT_FILE"'"}'
