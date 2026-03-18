// ── 인용 블록: Design 2 (점선 박스) ──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: 10pt,
    below: 10pt,
    inset: (x: 14pt, y: 10pt),
    stroke: (
      dash: "dashed",
      paint: rgb("#aaaaaa"),
      thickness: 1pt,
    ),
    radius: 0pt,
    {
      set par(justify: true, leading: 0.9em)
      text(fill: rgb("#333333"))[#it.body]
    }
  )
}

// ── callout-box (회색 박스 + 프라이머리 라벨) ──
#let callout-box(label, body) = {
  block(
    width: 100%,
    above: 10pt,
    below: 10pt,
    inset: (x: 14pt, y: 10pt),
    fill: rgb("#f5f5f5"),
    radius: 4pt,
    stroke: none,
    {
      set par(justify: true, leading: 0.9em)
      if label == [] or label == none {
        text(fill: rgb("#333333"))[#body]
      } else {
        text[#text(weight: "bold", fill: rgb("#2563eb"))[#label] #text(fill: rgb("#333333"))[#body]]
      }
    }
  )
}
