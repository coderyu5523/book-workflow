---
name: screenshot
description: 터미널 실행 결과와 브라우저 웹 UI를 PNG 스크린샷으로 생성하는 스킬. terminal_screenshot.py(터미널 컬러), book_capture.py(서적용 흰배경), Playwright MCP(브라우저)를 지원한다. 챕터 집필 완료 후 [CAPTURE NEEDED] 플레이스홀더를 실제 이미지로 교체할 때 사용.
---

# 스크린샷 스킬

## 로드 시점

| 상황 | 설명 |
|------|------|
| 챕터 집필 완료 후 | `[CAPTURE NEEDED]` 플레이스홀더를 실제 캡처로 교체 |
| 실습 결과 확인 시 | 예제 코드 실행 결과를 PNG로 저장 |

## 핵심 규칙

- 스크린샷 명령어에 절대경로/venv 경로를 노출하지 않는다 (`--display` 사용)
- 출력 PNG는 `{project}/assets/CH{N}/`에 저장한다
- 파일명: `{NN}_{설명}.png` (예: `06_main-pipeline.png`)
- 캡처 후 반드시 PNG 파일 존재와 크기(>5KB)를 검증한다

## 3가지 캡처 방식

| 방식 | 스크립트 | 용도 |
|------|---------|------|
| 터미널 (컬러) | `scripts/terminal_screenshot.py` | 일반 터미널 출력 (macOS 스타일 프레임) |
| 서적용 (흰배경) | `scripts/book_capture.py` | Rich 테이블/실험 결과 (흰 배경 + 검정 텍스트) |
| 브라우저 | Playwright MCP | 웹 UI 캡처 |

---

## 스크립트 작성 규칙

캡처 대상이 되는 실험/실습 스크립트는 다음을 지켜야 한다.

- `print()` 대신 `console.print()` 사용 (Rich Console)
- 장식선 금지 (`console.rule()`, `───` 등)
- 제목은 `console.print("[bold]제목[/bold]")`로 간결하게
- Rich Table 사용 시 `title` 파라미터로 섹션 구분

## 참조 파일

| 파일 | 로드 시점 |
|------|---------|
| `references/terminal-capture.md` | 터미널 스크린샷 생성 시 (book_capture + terminal_screenshot + 배치 캡처 상세) |
| `references/browser-capture.md` | 브라우저 웹 UI 캡처 시 |

## 스크립트 목록

| 스크립트 | 상태 | 용도 |
|----------|------|------|
| `scripts/book_capture.py` | **추천** | 서적용 흰배경 캡처 (Rich SVG → PNG) |
| `scripts/terminal_screenshot.py` | 유지 | 터미널 컬러 캡처 (ANSI → HTML → PNG) |
| `scripts/capture.py` | 유지 | 배치 래퍼 (여러 스크린샷 한 번에) |
