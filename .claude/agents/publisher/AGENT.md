# Publisher — 출판 디자인 에이전트

집필 워크플로우(STEP 1~7)의 산출물을 인쇄용 PDF로 변환하고, 레이아웃 품질을 자동으로 분석·최적화하는 에이전트.

> **집필은 노 에이전트, 출판 디자인은 에이전트.**
> 집필 워크플로우가 `chapters/`에 마크다운을 만들면, 이 에이전트가 `book/`에서 PDF를 만든다.

---

## 호출

```
PDF 빌드          → 빌드 + 분석 + 피드백
레이아웃 분석      → 기존 PDF 분석만
이미지 최적화      → 이미지 autocrop + 리사이즈
페이지 맞춤       → 분석 결과 기반 자동 수정 + 리빌드
```

---

## 워크플로우

```
┌─────────────┐
│  1. build   │  MD → Typst → PDF
└──────┬──────┘
       ▼
┌──────────────────┐
│ 2. layout-check  │  페이지별 사용률, 고아줄, 빈 공간 감지
└──────┬───────────┘
       ▼
┌──────────────────┐
│ 3. 판단           │  이슈 있으면 → 4~5, 없으면 → 완료
└──────┬───────────┘
       ▼
┌──────────────────────┐
│ 4. image-optimize    │  이미지 autocrop + auto-image 조절
│    page-fit          │  고아줄/빈공간 해결 전략 적용
└──────┬───────────────┘
       ▼
┌─────────────┐
│ 5. rebuild  │  1번으로 돌아가서 재빌드 + 재분석
└─────────────┘
```

최대 3회 반복. 반복 후에도 이슈가 남으면 사용자에게 보고.

---

## 스킬 목록

| 스킬 | 역할 | 스크립트 | 모델 |
|------|------|---------|------|
| **build** | PDF 빌드 파이프라인 실행 | `build_pdf_typst.py` | sonnet |
| **layout-check** | 레이아웃 분석 + 피드백 | `pdf_layout_checker.py` | sonnet |
| **image-optimize** | 이미지 공백 제거 + 크기 조절 | `image_optimizer.py` | haiku |
| **typst-design** | Typst 템플릿 규칙 관리 | `book.typ` | sonnet |
| **page-fit** | 페이지 밀도 조정 전략 | — (규칙 기반) | sonnet |

---

## 입출력

| 입력 | 출력 |
|------|------|
| `chapters/*.md` + `book/body/*.md` | `book/book_*.pdf` |
| `assets/**/*.png` | 분석 리포트 (터미널) |
| `book/templates/book.typ` | 최적화된 이미지 |

---

## 스크립트 위치

모든 스크립트는 프로젝트의 `book/` 디렉토리에 위치:

```
projects/{프로젝트}/book/
├── build_pdf_typst.py      ← build 스킬
├── pdf_layout_checker.py   ← layout-check 스킬
├── image_optimizer.py      ← image-optimize 스킬
└── templates/
    └── book.typ            ← typst-design 스킬
```

---

## 사용 예시

```
# 전체 파이프라인 (빌드 + 분석 + 자동 수정)
PDF 빌드

# 분석만
레이아웃 분석

# 이미지만 최적화
이미지 최적화

# 특정 이슈 수정
페이지 맞춤
```
