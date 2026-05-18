# /// script
# dependencies = [
#   "rich",
# ]
# ///
"""
数据处理脚本

用法:
    python3 scripts/process.py --input data.json
    python3 scripts/process.py --input data.json --format csv --output report.csv
    python3 scripts/process.py --validate output.json
    python3 scripts/process.py --help
"""

import argparse
import json
import sys
from pathlib import Path


def process_data(input_file: str, output_format: str = "json",
                 output_file: str = None, limit: int = 1000,
                 verbose: bool = False) -> dict:
    """处理数据的主函数。替换为你的实际逻辑。"""
    if verbose:
        print(f"[INFO] 正在处理: {input_file}", file=sys.stderr)

    # 读取输入
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # === 在此处添加你的处理逻辑 ===
    result = {
        "status": "success",
        "input_file": input_file,
        "format": output_format,
        "records_processed": len(data) if isinstance(data, list) else 1,
        "message": "处理完成"
    }
    # ==============================

    return result


def validate_output(output_file: str) -> bool:
    """验证输出文件。"""
    path = Path(output_file)
    if not path.exists():
        print(f"Error: 输出文件不存在: {output_file}", file=sys.stderr)
        return False
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        print(f"Error: 输出文件不是有效的 JSON: {output_file}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="数据处理脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 scripts/process.py --input data.json
  python3 scripts/process.py --input data.json --format csv --output report.csv
  python3 scripts/process.py --validate output.json"""
    )
    parser.add_argument("--input", help="输入文件路径")
    parser.add_argument("--format", choices=["json", "csv", "table"],
                        default="json", help="输出格式 (默认: json)")
    parser.add_argument("--output", help="输出文件路径 (默认: stdout)")
    parser.add_argument("--validate", help="验证输出文件而非处理")
    parser.add_argument("--limit", type=int, default=1000,
                        help="输出行数限制 (默认: 1000)")
    parser.add_argument("--verbose", action="store_true",
                        help="输出进度信息到 stderr")

    args = parser.parse_args()

    # 验证模式
    if args.validate:
        if validate_output(args.validate):
            print(json.dumps({"status": "valid", "file": args.validate}))
            sys.exit(0)
        else:
            sys.exit(2)

    # 处理模式
    if not args.input:
        print("Error: 处理模式需要 --input 参数", file=sys.stderr)
        print("用法: python3 scripts/process.py --input <input_file>", file=sys.stderr)
        sys.exit(2)

    try:
        result = process_data(
            args.input,
            output_format=args.format,
            output_file=args.output,
            limit=args.limit,
            verbose=args.verbose
        )

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
    except json.JSONDecodeError:
        print(f"Error: 文件不是有效的 JSON: {args.input}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: 处理失败: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
