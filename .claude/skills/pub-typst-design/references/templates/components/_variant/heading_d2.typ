// ── 제목 스타일: Design 2 (컴팩트 모노) ──
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  block(
    width: 100%,
    below: heading-gap,
    sticky: true,
    {
      text(h1-size, weight: "bold", fill: color-text)[#it.body]
      v(8pt)
      line(length: 100%, stroke: 3pt + color-primary)
    }
  )
  v(heading-gap)
}

#show heading.where(level: 2): it => {
  v(18pt)
  block(
    width: 100%,
    below: heading-gap,
    sticky: true,
    text(h2-size, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
  )
  v(heading-gap)
}

#show heading.where(level: 3): it => {
  v(14pt)
  block(
    below: heading-gap,
    sticky: true,
    text(h3-size, weight: "semibold", fill: rgb("#374151"))[#it.body]
  )
  v(heading-gap)
}

#show heading.where(level: 4): it => {
  v(10pt)
  block(
    below: heading-gap,
    sticky: true,
    text(h4-size, weight: "medium", fill: rgb("#555555"))[#it.body]
  )
  v(heading-gap)
}
