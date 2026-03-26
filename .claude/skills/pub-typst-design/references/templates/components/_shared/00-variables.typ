// 조판 설정 변수 — 기본값은 Design 1 (클래식 블루)
// Design 2에서 body_d2.typ 상단에서 재정의. D1 파일은 값을 직접 사용 (기본값과 동일하므로)
// 소비자: _variant/body_d2.typ(재정의), _variant/heading_d2.typ, _variant/code_d2.typ

// 행간: 줄과 줄 사이 간격
#let body-leading = 1.0em
// 자간: 글자와 글자 사이 간격 (0pt = 기본)
#let body-tracking = 0pt
// 제목-문단 간격: 제목 아래 본문까지의 여백
#let heading-gap = 16pt
// 코드 블록: 구분선과 코드 사이 여백
#let code-inset-x = 16pt
#let code-inset-y = 14pt
// 코드 블록: 구분선 두께
#let code-rule-stroke = 1pt

// 제목 크기 — 에디터 오버라이드 대상
#let h1-size = 26pt
#let h2-size = 16pt
#let h3-size = 13pt
#let h4-size = 11pt
// 코드 블록 크기 — 에디터 오버라이드 대상
#let code-size = 8pt
// 인용/표/인라인코드 크기 — 에디터 오버라이드 대상
#let quote-size = 9pt
#let table-size = 8.5pt
#let inline-code-size = 8.5pt
// 목차 깊이 — 에디터 오버라이드 대상
#let toc-depth = 2

// 색상 변수 — 에디터 오버라이드 대상
#let color-primary = rgb("#2563eb")
#let color-primary-dark = rgb("#1e40af")
#let color-primary-light = rgb("#93c5fd")
#let color-text = rgb("#1a1a1a")
#let color-code-text = rgb("#1e40af")
#let color-quote-bg = rgb("#f5f8ff")
#let color-quote-border = rgb("#93b4e8")

// 이미지 설정 변수 — 에디터 오버라이드 대상
#let img-gemini-width = 0.7
#let img-gemini-style = "bordered"
#let img-terminal-width = 0.7
#let img-terminal-style = "minimal"
#let img-diagram-width = 0.6
#let img-diagram-style = "minimal"
#let img-default-width = 0.6
#let img-default-style = "plain"
