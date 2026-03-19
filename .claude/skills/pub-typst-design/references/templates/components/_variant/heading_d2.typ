// ── 제목 스타일: Design 2 (컴팩트 모노) ──
// h1(챕터 오프닝)은 chapter_opening_d2.typ에서 정의

#show heading.where(level: 2): it => {
  v(18pt)
  block(
    width: 100%,
    below: heading-gap,
    sticky: true,
    text(10pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
  )
  v(heading-gap)
}

#show heading.where(level: 3): it => {
  v(14pt)
  block(
    below: heading-gap,
    sticky: true,
    text(10pt, weight: "semibold", fill: rgb("#374151"))[#it.body]
  )
  v(heading-gap)
}

#show heading.where(level: 4): it => {
  v(10pt)
  block(
    below: heading-gap,
    sticky: true,
    text(10pt, weight: "medium", fill: rgb("#555555"))[#it.body]
  )
  v(heading-gap)
}
