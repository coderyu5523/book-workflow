// ── 인용 블록: Design 1 (파란 좌측선) ──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: 10pt,
    below: 10pt,
    inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
    stroke: (left: 3pt + color-quote-border),
    fill: color-quote-bg,
    radius: (right: 4pt),
    {
      set par(justify: true, leading: 0.9em)
      text(size: quote-size, fill: rgb("#4b5563"))[#it.body]
    }
  )
}

// ── callout-box 호환 정의 ──
// Design 2의 callout-box를 본문에서 호출할 때 컴파일 에러 방지
#let callout-box(label, body) = {
  block(
    width: 100%,
    above: 10pt,
    below: 10pt,
    inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
    stroke: (left: 3pt + color-quote-border),
    fill: color-quote-bg,
    radius: (right: 4pt),
    {
      set par(justify: true, leading: 0.9em)
      if label == [] or label == none {
        text(size: quote-size, fill: rgb("#4b5563"))[#body]
      } else {
        text(size: quote-size)[#text(weight: "bold", fill: color-primary)[#label] #text(fill: rgb("#4b5563"))[#body]]
      }
    }
  )
}
