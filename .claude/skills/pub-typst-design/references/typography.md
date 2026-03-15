# 타이포그래피 규칙

> 기준: 국내 IT 출판사 관행 + 해외 기술 서적 표준 (docs/book-design-guide.md 참조)

## 페이지 설정

| 항목 | 값 | 근거 |
|------|-----|------|
| 판형 | **46배판 (188x257mm)** | 국내 IT 서적 사실상 표준 |
| 상단 여백 | 20mm | 출판 표준 15~20mm |
| 하단 여백 | 28mm | 아래 > 위 (시각적 안정감) |
| 안쪽 여백 (Gutter) | 25mm | 제본 여백 포함 (22~28mm) |
| 바깥쪽 여백 | 16mm | 안쪽 > 바깥쪽 (비대칭) |
| 줄간격 | 1.0em (≈본문 크기의 200%) | 권장 140~200%, 가독성 확보 |
| 양쪽 정렬 | true | 출판 표준 |
| 첫 줄 들여쓰기 | 0pt | 기술서적 관행 |

## 폰트 체계

| 용도 | 폰트 | 크기 | 비고 |
|------|------|------|------|
| 본문 | KoPubDotum_Pro, Apple SD Gothic Neo | 10pt | IT 서적 표준 9.5~10.5pt |
| h1 (챕터) | Bold | 16pt | 챕터 오프닝 전용 |
| h2 (섹션) | Bold | 10pt | 본문과 동일 크기, 굵기로 구분. 숫자 접두사("1.") |
| h3 (소제목) | SemiBold | 10pt | 진회색(#374151). 숫자 접두사("1.1") |
| h4 (하위제목) | Medium | 10pt | 회색(#555555). 숫자 접두사("1.1.1") |
| 코드 블록 | Menlo, KoPubDotum_Pro | 8pt | 본문보다 2pt 작게 (권장 8~9pt) |
| 인라인 코드 | 본문 폰트 (볼드) | 10pt | 배경 없이 볼드 처리 |
| 캡션 | KoPubDotum_Pro | 8pt | 회색(#6b7280) |
| 헤더 | KoPubDotum_Pro | 8pt | 회색(#999999) |
| 푸터 | KoPubDotum_Pro | 9pt | 회색(#888888) |

## 헤더 (머릿말)

- **좌측**: 책 제목 (book-header-title 변수)
- **우측**: 현재 챕터명 (h1 state 추적)
- **구분선**: 0.3pt 연회색
- **표지/목차**: 숨김 (page-num > 2일 때만 표시)

## 푸터

- 하단 중앙, 페이지 번호
- 표지/목차: 숨김

## heading 규칙

### h1 (챕터 오프닝)

| 요소 | 값 | 근거 |
|------|-----|------|
| 상단 여백 | 60pt | 페이지 상단 1/3 비움 (출판 표준) |
| 제목 크기 | 26pt Bold | |
| 밑줄 | 3pt 파란선 | |
| 하단 간격 | 14pt | |
| pagebreak | weak: true | 항상 새 페이지에서 시작 |
| sticky | true | 고아 방지 |

### h2~h4

- 모두 10pt 통일. weight(Bold/SemiBold/Medium)와 색상으로 레벨 구분
- 마크다운 원문에서 숫자 접두사(1. / 1.1 / 1.1.1) 직접 작성
- 모두 `sticky: true`로 heading이 페이지 하단에 혼자 남지 않도록 방지
- **제목 아래 여백**: `heading-gap` 변수로 전 레벨 통일 (기본값 = `body-leading`)
- **제목 위 여백 > 아래 여백** (소속 관계 표현)
  - h2: 위 18pt, 아래 heading-gap
  - h3: 위 14pt, 아래 heading-gap
  - h4: 위 10pt, 아래 heading-gap

## 코드 블록

> 회의 피드백 #6: 코드블록은 위아래 두꺼운 회색 테두리만. 박스/radius 제거.

```typst
fill: white                              // 흰 배경
stroke: none                             // 좌우 테두리 없음
inset: (x: 16pt, y: 14pt)               // 패딩
breakable: true                          // 긴 코드도 페이지 넘김 가능
weight: "bold"                           // 볼드 텍스트
text(fill: rgb("#1a1a1a"))               // 어두운 텍스트
// 위아래 두꺼운 회색 테두리
above: line(length: 100%, stroke: 2pt + rgb("#d1d5db"))
below: line(length: 100%, stroke: 2pt + rgb("#d1d5db"))
```

**핵심**: radius 제거, 좌우 테두리 없음. 위아래 두꺼운 회색 라인만.

## 인용 블록 (blockquote) — 2가지 디자인

### 디자인 A: 점선 박스 (기본)

일반 blockquote에 적용. 라벨 키워드 없는 `>` 인용문.

```typst
stroke: (dash: "dashed", paint: rgb("#aaaaaa"), thickness: 1pt)
radius: 0pt
text(size: 9pt, fill: rgb("#333333"))
leading: 0.9em
```

### 디자인 B: 회색 박스 + 프라이머리 라벨 (callout)

`> **참고**: 설명...` 패턴 감지 시 자동 적용. 지원 라벨: 참고, 팁, Note, 주의.

```typst
fill: rgb("#f5f5f5")                     // 연회색 배경
radius: 4pt
stroke: none
라벨: text(9pt, bold, fill: rgb("#2563eb"))  // 프라이머리 색
본문: text(9pt, fill: rgb("#333333"))
```

후처리(typst_builder.py)에서 `#quote(block: true)[#strong[참고]: ...]` → `#callout-box([참고], [...])` 변환.

## 표 스타일

- 헤더 행: 연회색 배경(#e5e5e5) + 검정 볼드 텍스트
- 홀수 행: 연회색(#fafafa)
- 짝수 행: 흰색
- 테두리: 하단만 연회색 0.5pt

## 볼드/이탤릭

- **볼드**: 네이비(#1e3a5f)
- *이탤릭*: 회색(#6b7280)

## 표지

```typst
#page(numbering: none, header: none, footer: none)[
  book-title (42pt, 파란 볼드)     // 프로젝트 변수
  book-subtitle (15pt)              // 프로젝트 변수
  book-description (10.5pt, 회색)   // 프로젝트 변수
]
```

## 목차

**주의**: 목차에서 `#heading`을 사용하면 h1 show rule의 `pagebreak(weak: true)`가 트리거되어 빈 페이지 발생. 반드시 직접 텍스트 스타일링 사용:

```typst
// 올바른 방법
text(24pt, weight: "bold")[목차]

// 잘못된 방법 (빈 페이지 생성)
#heading(outlined: false, level: 1)[목차]
```

## 이미지 배치 기준

| 항목 | 값 |
|------|-----|
| 이미지-텍스트 간격 | 상하 8pt |
| 캡션 스타일 | 8pt, 회색(#6b7280), 중앙 정렬 |
| 캡션-이미지 간격 | 2pt |
| 캡션 형식 | "그림 N-M: 설명" |
| auto-image 기본 max-width | 0.7 (70%) |
| dual-image 간격 | 16pt (column-gutter) |
