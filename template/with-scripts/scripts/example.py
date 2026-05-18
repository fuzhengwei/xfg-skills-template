# /// script
# dependencies = [
#   "rich",
# ]
# ///
"""
示例数据处理脚本

用法:
    python3 scripts/example.py --input data.csv
    python3 scripts/example.py --input data.csv --format json
    python3 scripts/example.py --help
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="示例数据处理脚本",
        epilog="示例:\n"
               "  python3 scripts/example.py --input data.csv\n"
               "  python3 scripts/example.py --input data.csv --format json",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--format", choices=["json", "csv", "table"],
                        default="json", help="输出格式 (默认: json)")
    parser.add_argument("--output", help="输出文件路径 (默认: stdout)")
    parser.add_argument("--verbose", action="store_true",
                        help="输出进度信息到 stderr")

    args = parser.parse_args()

    try:
        if args.verbose:
            print(f"[INFO] 正在处理: {args.input}", file=sys.stderr)

        # === 在此处添加你的处理逻辑 ===
        result = {
            "status": "success",
            "input": args.input,
            "format": args.format,
            "message": "处理完成"
        }
        # ==============================

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            if args.verbose:
                print(f"[INFO] 结果已写入: {args.output}", file=sys.stderr)
        else:
            print(output)

    except FileNotFoundError:
        print(f"Error: 文件未找到: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: 处理失败: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
