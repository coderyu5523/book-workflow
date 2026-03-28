// ── 코드 블록: Design 1 (둥근 테두리 박스) ──
// ──OVERRIDES──
#show raw.where(block: true): it => {
  set text(size: code-size, weight: "bold", font: ("D2Coding", "RIDIBatang"))
  block(
    width: 100%,
    fill: code-fill,
    inset: (x: code-inset-x, y: code-inset-y),
    radius: code-radius,
    stroke: code-stroke-width + code-stroke-color,
    breakable: true,
    text(fill: color-text)[#it]
  )
}
