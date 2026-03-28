// ── 제목 스타일: Design 1 (클래식 블루) ──
// D1은 00-variables.typ 기본값 사용 (변수 재정의 없음)
// ──OVERRIDES──
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  counter(figure).update(0)
  pagebreak(weak: true)
  block(above: h1-top, below: 0pt, width: 100%, sticky: true)[
    #text(h1-size, weight: h1-weight, fill: h1-fill)[#it.body]
    #v(8pt)
    #line(length: 100%, stroke: 3pt + color-primary)
  ]
  v(h1-below)
}

#show heading.where(level: 2): it => {
  block(above: h2-top, below: 0pt, width: 100%, sticky: true,
    inset: (left: h2-inset-left),
    stroke: (left: 4pt + color-primary))[
    #text(h2-size, weight: h2-weight, fill: h2-fill)[#it.body]
  ]
  v(h2-below)
}

#show heading.where(level: 3): it => {
  block(above: h3-top, below: 0pt, sticky: true)[
    #text(h3-size, weight: h3-weight, fill: h3-fill)[#it.body]
  ]
  v(h3-below)
}

#show heading.where(level: 4): it => {
  block(above: h4-top, below: 0pt, sticky: true)[
    #text(h4-size, weight: h4-weight, fill: h4-fill)[#it.body]
  ]
  v(h4-below)
}
