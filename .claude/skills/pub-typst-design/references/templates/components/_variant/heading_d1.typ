// ── 제목 스타일: Design 1 (클래식 블루) ──
// h1(챕터 오프닝)은 chapter_opening_d1.typ에서 정의

#show heading.where(level: 2): it => {
  v(24pt)
  block(
    width: 100%,
    below: 8pt,
    sticky: true,
    inset: (left: 12pt),
    stroke: (left: 4pt + rgb("#2563eb")),
    text(16pt, weight: "bold", fill: rgb("#1e40af"))[#it.body]
  )
  v(6pt)
}

#show heading.where(level: 3): it => {
  v(16pt)
  block(
    below: 6pt,
    sticky: true,
    text(13pt, weight: "semibold", fill: rgb("#1e3a5f"))[#it.body]
  )
  v(4pt)
}

#show heading.where(level: 4): it => {
  v(12pt)
  block(
    below: 4pt,
    sticky: true,
    text(11pt, weight: "semibold", fill: rgb("#374151"))[#it.body]
  )
  v(2pt)
}
