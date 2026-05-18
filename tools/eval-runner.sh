#!/usr/bin/env bash
# eval-runner.sh — Agent Skills 评估运行器
#
# 用法:
#   bash tools/eval-runner.sh <skill_dir> [workspace_dir]
#   bash tools/eval-runner.sh ./my-skill
#   bash tools/eval-runner.sh ./my-skill ./my-skill-workspace
#
# 评估流程:
#   1. 读取 evals/evals.json 中的测试用例
#   2. 对每个用例运行技能（with_skill）和不运行技能（without_skill）
#   3. 记录结果和计时
#   4. 生成 benchmark.json 汇总

set -euo pipefail

SKILL_DIR="${1:?用法: $0 <skill_dir> [workspace_dir]}"
WORKSPACE_DIR="${2:-${SKILL_DIR}-workspace}"
ITERATION="${EVAL_ITERATION:-1}"
RUNS="${EVAL_RUNS:-1}"

ITER_DIR="${WORKSPACE_DIR}/iteration-${ITERATION}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 evals.json
EVALS_FILE="${SKILL_DIR}/evals/evals.json"
if [[ ! -f "$EVALS_FILE" ]]; then
    log_error "未找到评估文件: ${EVALS_FILE}"
    echo "请在技能目录下创建 evals/evals.json"
    exit 1
fi

# 检查依赖
if ! command -v jq &>/dev/null; then
    log_error "需要 jq 工具，请先安装: brew install jq"
    exit 1
fi

# 创建工作目录
mkdir -p "$ITER_DIR"
log_info "评估工作目录: ${ITER_DIR}"

# 读取技能名称
SKILL_NAME=$(jq -r '.skill_name // "unknown"' "$EVALS_FILE")
log_info "评估技能: ${SKILL_NAME}"

# 读取评估用例数量
EVAL_COUNT=$(jq '.evals | length' "$EVALS_FILE")
log_info "评估用例数: ${EVAL_COUNT}"

# 遍历每个评估用例
for i in $(seq 0 $((EVAL_COUNT - 1))); do
    EVAL_ID=$(jq -r ".evals[$i].id" "$EVALS_FILE")
    EVAL_PROMPT=$(jq -r ".evals[$i].prompt" "$EVALS_FILE")
    EVAL_DIR="${ITER_DIR}/eval-${EVAL_ID}"

    log_info "━━━ 运行评估 #${EVAL_ID} ━━━"
    log_info "提示: ${EVAL_PROMPT:0:80}..."

    # 创建评估目录
    mkdir -p "${EVAL_DIR}/with_skill/outputs"
    mkdir -p "${EVAL_DIR}/without_skill/outputs"

    # 运行 with_skill 和 without_skill
    for MODE in "with_skill" "without_skill"; do
        MODE_DIR="${EVAL_DIR}/${MODE}"

        log_info "运行 ${MODE}..."

        # 记录开始时间
        START_MS=$(python3 -c "import time; print(int(time.time() * 1000))")

        # === 在此处添加你的 Agent 调用逻辑 ===
        # 示例（Claude Code）:
        # if [[ "$MODE" == "with_skill" ]]; then
        #     claude -p "$EVAL_PROMPT" --skill-path "$SKILL_DIR" \
        #         --output-format json > "${MODE_DIR}/outputs/result.json" 2>/dev/null
        # else
        #     claude -p "$EVAL_PROMPT" \
        #         --output-format json > "${MODE_DIR}/outputs/result.json" 2>/dev/null
        # fi

        # 占位：模拟运行
        echo '{"status": "placeholder", "mode": "'"$MODE"'"}' > "${MODE_DIR}/outputs/result.json"
        # =====================================

        # 记录结束时间
        END_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
        DURATION_MS=$((END_MS - START_MS))

        # 保存计时数据
        cat > "${MODE_DIR}/timing.json" <<EOF
{
    "duration_ms": ${DURATION_MS},
    "mode": "${MODE}",
    "eval_id": ${EVAL_ID}
}
EOF

        log_ok "${MODE} 完成（${DURATION_MS}ms）"
    done

    log_ok "评估 #${EVAL_ID} 完成"
done

log_ok "━━━ 所有评估完成 ━━━"
log_info "结果保存在: ${ITER_DIR}"
log_info ""
log_info "下一步:"
log_info "  1. 检查各评估目录的输出结果"
log_info "  2. 编写 assertions 并进行 grading"
log_info "  3. 运行 benchmark 汇总"
