#!/bin/bash
# CH04 터미널 캡처 스크립트 (가상환경 활성화 버전)
WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$WORKSPACE/.claude/skills/screenshot/scripts/terminal_screenshot.py"
EX04="$WORKSPACE/projects/사내AI비서_v2/code/ex04"
ASSETS="$WORKSPACE/projects/사내AI비서_v2/assets/CH04"

# 가상환경 활성화
source "$EX04/.venv/bin/activate"
echo "✅ 가상환경 활성화: $(which python)"

echo ""
echo "=== 캡처 1: 파이프라인 실행 결과 ==="
python3 "$SCRIPT" \
  "python src/main.py" \
  --png "$ASSETS/04_pipeline-result.png" \
  --display "python src/main.py" \
  --cwd "$EX04" \
  --title "전체 파이프라인 실행" \
  --timeout 120

echo ""
echo "=== 캡처 2: CLI 검색 결과 ==="
python3 "$SCRIPT" \
  "python src/cli_search.py --query '연차 사용 규정' --top-k 3" \
  --png "$ASSETS/04_cli-search.png" \
  --display "python src/cli_search.py --query '연차 사용 규정' --top-k 3" \
  --cwd "$EX04" \
  --title "벡터 검색 CLI" \
  --timeout 120

echo ""
echo "=== 캡처 완료. 파일 확인 ==="
ls -la "$ASSETS/04_pipeline-result.png" "$ASSETS/04_cli-search.png" 2>&1

# 가상환경 비활성화
deactivate
