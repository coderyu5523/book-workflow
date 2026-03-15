# 터미널 스크린샷 캡처 워크플로우

## 스크립트 위치

```
.claude/skills/screenshot/scripts/terminal_screenshot.py  ← 터미널 컬러 캡처
.claude/skills/screenshot/scripts/book_capture.py          ← 서적용 캡처 (추천)
.claude/skills/screenshot/scripts/capture.py               ← 배치 래퍼
```

---

## 방식 1: 서적용 캡처 (book_capture.py) — 추천

Rich SVG export → Playwright PNG 파이프라인.
흰 배경 + 검정 텍스트 + 볼드만 유지. 표 정렬 완벽, 오른쪽 여백 없음.

### 원리

1. 명령 실행 → ANSI 출력 획득 (`FORCE_COLOR=1`, `COLUMNS=200`)
2. Rich `Text.from_ansi()` → `Console.export_svg()` (흰배경/검정 테마)
3. SVG에 고정폭 한글 웹폰트(Nanum Gothic Coding) 주입
4. `rich.cells.cell_len`으로 콘텐츠 너비를 정확히 계산 → 타이트한 SVG
5. Playwright로 SVG element를 PNG로 캡처 (element screenshot → 여백 없음)

### CLI 사용법

```bash
SCRIPT=".claude/skills/screenshot/scripts/book_capture.py"

python3 "$SCRIPT" \
    --cmd ".venv/bin/python -m tuning.step1_chunk_experiment --step 1-1" \
    --cwd "projects/사내AI비서_v2/code/ex08" \
    --output "projects/사내AI비서_v2/assets/CH08/08_chunk-size.png" \
    --title "step 1-1: 청크 크기 실험"
```

### 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `--cmd` | Y | 실행할 셸 명령 (venv 경로 포함 가능) |
| `--output` | Y | 출력 PNG 경로 |
| `--cwd` | - | 명령 실행 디렉토리 (기본: 현재) |
| `--title` | - | 타이틀바 제목 (기본: 빈 타이틀바) |
| `--columns` | - | COLUMNS 환경변수 (기본: 200) |
| `--max-lines` | - | 최대 줄 수 (기본: 무제한) |
| `--title-filter` | - | 본문 내 제목 행 식별 키워드 (쉼표 구분) |
| `--title-replace` | - | 본문 내 제목 행 교체 텍스트 |
| `--title-pad` | - | 본문 내 제목 앞 공백 수 (기본: 28) |
| `--font-wait` | - | 폰트 로딩 대기 ms (기본: 1000) |

### 제목 장식선 정리

Rich 실험 출력에 `═══ step 1-1: 청크 크기 실험 ═══` 같은 장식선이 있으면
`--title-filter`와 `--title-replace`로 깔끔하게 교체한다.

```bash
python3 "$SCRIPT" \
    --cmd ".venv/bin/python -m tuning.step1_chunk_experiment --step 1-1" \
    --cwd "projects/사내AI비서_v2/code/ex08" \
    --output "assets/CH08/08_chunk-size.png" \
    --title-filter "step 1-1:,청크 크기 실험" \
    --title-replace "step 1-1: 청크 크기 실험"
```

### Python 호출

```python
from book_capture import book_capture_png

book_capture_png(
    cmd=".venv/bin/python -m tuning.step1_chunk_experiment --step 1-1",
    output="assets/CH08/08_chunk-size.png",
    cwd="projects/사내AI비서_v2/code/ex08",
    title="step 1-1: 청크 크기 실험",
)
```

---

## 방식 2: 터미널 컬러 캡처 (terminal_screenshot.py)

macOS 스타일 프레임(점 3개) + ANSI 컬러 → HTML → Playwright PNG.
컬러 출력이 필요한 일반 터미널 캡처용.

```bash
SCRIPT=".claude/skills/screenshot/scripts/terminal_screenshot.py"

python3 "$SCRIPT" "{ACTUAL_COMMAND}" \
    --png {OUTPUT_PNG} \
    --display "{DISPLAY_COMMAND}" \
    --cwd {WORKING_DIR} \
    --title "{TITLE}" \
    --timeout 120
```

### 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `command` | Y | 실제 실행할 명령어 (venv 경로 포함 가능) |
| `--png` | Y | 출력 PNG 파일 경로 |
| `--display` | Y | 스크린샷에 표시할 깨끗한 명령어 |
| `--cwd` | Y | 명령어 실행 디렉토리 |
| `--title` | Y | 터미널 창 타이틀바에 표시할 제목 |
| `--timeout` | - | 타임아웃 초 (기본 60, 임베딩 등은 120 권장) |
| `--output` | - | HTML도 보존하려면 경로 지정 |

### Display Command 규칙

`--display`에는 독자가 따라할 수 있는 깨끗한 명령어를 지정한다.

| Bad (절대경로) | Good (--display) |
|---|---|
| `/Users/me/.venv/bin/python src/main.py` | `python src/main.py` |
| `/opt/homebrew/bin/python3 src/cli_search.py --query '연차'` | `python src/cli_search.py --query '연차'` |

---

## 배치 캡처 (capture.py)

여러 스크린샷을 한 번에 생성:

```bash
python3 .claude/skills/screenshot/scripts/capture.py batch --config screenshots.json
```

`screenshots.json` 예시:
```json
{
  "cwd": "projects/사내AI비서_v2/code/ex08",
  "assets_dir": "projects/사내AI비서_v2/assets/CH08",
  "venv": ".venv",
  "timeout": 120,
  "screenshots": [
    {
      "cmd": "python -m tuning.step1_chunk_experiment --step 1-1",
      "filename": "08_chunk-size.png",
      "title": "실험 1-1: 청크 크기 비교"
    }
  ]
}
```

---

## 검증 체크리스트

캡처 후 반드시 확인:

1. **파일 존재**: PNG 파일이 생성되었는가
2. **파일 크기**: 5KB 이상인가 (빈 이미지 방지)
3. **내용 확인**: Read 도구로 이미지를 열어 확인
   - 하단이 잘리지 않았는가
   - prompt에 절대경로가 노출되지 않았는가
   - 이모지/특수문자가 정상 렌더링되었는가

## Troubleshooting

### Playwright 미설치
```bash
pip install playwright && playwright install chromium
```

### 한글 깨짐
- book_capture.py: Google Fonts Nanum Gothic Coding 로드 (인터넷 필요)
- terminal_screenshot.py: Google Fonts Noto Sans KR 로드 (인터넷 필요)
- 오프라인: macOS `Apple SD Gothic Neo` 폴백

### 이미지 잘림
- terminal_screenshot: `--output`으로 HTML을 보존하고 브라우저에서 직접 확인
- book_capture: SVG가 element screenshot으로 잘리므로 잘림 문제 없음

### 타임아웃
임베딩 모델 로드가 포함된 명령어는 `--timeout 120` 이상을 사용한다.

### 오른쪽 여백 (trailing 공백)
book_capture.py는 자동으로 trailing 공백을 제거하고 `cell_len`으로 타이트하게 맞춘다.
terminal_screenshot.py 사용 시 여백이 발생하면 book_capture.py로 전환한다.
