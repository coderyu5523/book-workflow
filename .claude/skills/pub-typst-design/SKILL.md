---
name: pub-typst-design
description: "Typst 템플릿의 타이포그래피, 페이지 설정, 스타일 규칙 관리"
disable-model-invocation: true
---

# typst-design — Typst 템플릿 디자인

## 구조

| 파일 | 위치 | 역할 |
|------|------|------|
| `book_base.typ` | **스킬 소유** (`references/templates/`) | 범용 스타일 (폰트, 여백, heading, 코드, 표, 표지, 목차, auto-image, dual-image) |
| `book.typ` | **프로젝트** (`book/templates/`) | 프로젝트별 설정 (제목, 부제, 설명, 헤더 제목) |

프로젝트의 `book.typ`에서 변수를 정의하고, 스킬의 `book_base.typ`이 그 변수를 사용한다.
빌드 엔진이 Python 레벨에서 `book.typ` → `book_base.typ` → 본문 순서로 concat한다.

## 역할

`book_base.typ`의 스타일 규칙을 관리한다.
새 프로젝트에서 `book.typ`만 작성하면 동일한 스타일을 재사용할 수 있다.

## 프로젝트 설정 변수 (book.typ)

```typst
#let book-title = "책 제목"
#let book-subtitle = "부제"
#let book-description = [설명 텍스트]
#let book-header-title = "헤더에 표시할 제목"
```

## 새 프로젝트에서 사용하기

1. `book/templates/book.typ` 작성 (위 4개 변수만)
2. `book/templates/book_base.typ` → 스킬 심볼릭 링크 생성
3. `python3 book/build_pdf_typst.py` 실행

## 조판 변수

| 변수 | 기본값 | 역할 |
|------|--------|------|
| `body-leading` | 8pt | 본문 행간 |
| `body-tracking` | 0pt | 본문 자간 |
| `heading-gap` | body-leading | 제목↔문단 간격 (전 레벨 통일) |
| `code-inset-x` | 16pt | 코드 블록 좌우 여백 |
| `code-inset-y` | 6pt | 코드 블록 상하 여백 |
| `code-rule-stroke` | 2pt | 코드 블록 구분선 두께 |

## 이미지 함수

| 함수 | 용도 |
|------|------|
| `auto-image(path, alt, max-width)` | 1열 중앙 정렬, 페이지 공간에 맞게 자동 축소 |
| `dual-image(path1, path2, caption1, caption2, gap)` | 2열 이미지 나란히 배치 |

## 디자인 샘플

| 파일 | 용도 |
|------|------|
| [sample_test.md](references/samples/sample_test.md) | 샘플 마크다운 (heading, 코드, 표, 인용, 이미지 테스트) |
| [sample_test.pdf](references/samples/sample_test.pdf) | 빌드 결과 PDF (디자인 기준) |
| [build_sample.py](references/samples/build_sample.py) | 샘플 빌드 스크립트 |
| [sample_diagram.d2](references/samples/sample_diagram.d2) | D2 다이어그램 예시 |
| [sample_diagram.png](references/samples/sample_diagram.png) | D2 렌더링 결과 |

디자인 수정 시 `sample_test.md`로 빌드하여 결과를 `sample_test.pdf`와 비교한다.

## 주의사항

- 마크다운 heading 레벨(h1/h2/h3)을 변경하면 반드시 `book_base.typ`의 `outline(depth:)` 값을 함께 점검하라 → why-log.md#2026-03-15-3
- 프로젝트의 `book_base.typ`은 반드시 스킬 원본의 **심볼릭 링크**로 유지하라. 복사본은 수정이 전파되지 않는다 → why-log.md#2026-03-15-4

## 참조

- [typography.md](references/typography.md) — 타이포그래피 규칙 상세
