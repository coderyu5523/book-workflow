// ── 코드 블록: Design 1 (둥근 테두리 박스) ──
#show raw.where(block: true): it => {
  set text(size: code-size, weight: "bold", font: ("D2Coding", "RIDIBatang"))
  block(
    width: 100%,
    fill: white,
    inset: (x: 16pt, y: 14pt),
    radius: 8pt,
    stroke: 1pt + rgb("#d1d5db"),
    breakable: true,
    text(fill: color-text)[#it]
  )
}
