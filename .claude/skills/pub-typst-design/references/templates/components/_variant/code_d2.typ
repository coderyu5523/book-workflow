// ── 코드 블록: Design 2 (위아래 회색 실선) ──
#show raw.where(block: true): it => {
  set text(size: 6pt, weight: "bold", font: ("Menlo", "KoPubDotum_Pro"))
  v(6pt)
  line(length: 100%, stroke: code-rule-stroke + rgb("#999999"))
  block(
    width: 100%,
    fill: white,
    inset: (x: code-inset-x, y: code-inset-y),
    radius: 0pt,
    stroke: none,
    breakable: true,
    text(fill: rgb("#1a1a1a"))[#it]
  )
  line(length: 100%, stroke: code-rule-stroke + rgb("#999999"))
  v(6pt)
}
