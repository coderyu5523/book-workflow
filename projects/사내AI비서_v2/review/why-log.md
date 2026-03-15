# Why Log

## 2026-03-15-1: CH08 캡처 이미지 — 색상/여백 문제

**증상**: 캡처 이미지에 ANSI 색상(cyan, green, yellow)이 그대로 남아있고, 양쪽 여백이 과도함

**5 Whys**:

1. 왜 실패? → ANSI 색상이 그대로 HTML 색상으로 변환됨
2. 왜? → terminal_screenshot.py가 터미널 색상 보존 설계이고, rich_capture.py가 그대로 재사용
3. 왜 오버라이드 안 했나? → 서적용 캡처의 "블랙 텍스트 + 볼드만" 규칙이 어디에도 없음
4. 왜 규칙이 없나? → screenshot 스킬이 "터미널 재현" 목적으로만 설계됨
5. **근본 원인** → 서적 캡처 시 스타일 규칙(블랙/볼드/여백)이 부재

**수정**:

- `.claude/rules/style.md` — "ANSI 색상 변환 금지" + "불필요한 공백 금지" 규칙 2줄 추가
- `rich_capture.py` — `ansi_to_html()` 결과에서 모든 `color:` 값을 `#222222`로 치환
- `terminal_screenshot.py` — CSS: `min-width: auto`, `padding: 12px 16px`

**참조**: CH08 5개 캡처 (08_chunk-size, 08_overlap, 08_strategy-comparison, 08_reranker, 08_hybrid-search)

## 2026-03-15-2: CH08 캡처 이미지 — 오른쪽 여백 과다

**증상**: 색상/padding 수정 후에도 오른쪽에 큰 빈 공간이 남아있음

**5 Whys**:

1. 왜 오른쪽 여백? → `.terminal` 컨테이너가 테이블보다 넓음
2. 왜 넓음? → `white-space: pre`가 trailing 공백을 그대로 보존
3. 왜 trailing 공백? → `COLUMNS=100` 환경변수 → Rich가 100칸에 맞춰 줄 끝을 공백으로 채움
4. 왜 `width: fit-content`로 안 줄었나? → `pre` 모드에서 trailing 공백도 "콘텐츠"
5. **근본 원인** → Rich 출력의 각 줄 trailing 공백을 제거하지 않음

**수정**:

- `rich_capture.py` — HTML 변환 전 `line.rstrip()` + `run_and_capture(columns=80)` 으로 Rich 테이블 폭 축소
- `terminal_screenshot.py` — `run_and_capture()`에 `columns` 파라미터 추가 (기본값 100 유지)
- `.claude/rules/style.md` — "trailing 공백 제거" 규칙 추가
