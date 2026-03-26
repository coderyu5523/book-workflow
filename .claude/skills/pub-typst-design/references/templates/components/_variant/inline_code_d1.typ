// ── 인라인 코드: Design 1 (회색 배경 박스) ──
#show raw.where(block: false): it => {
  box(
    fill: rgb("#f3f4f6"),
    inset: (x: 4pt, y: 2pt),
    radius: 3pt,
    text(size: inline-code-size, fill: color-code-text, font: ("D2Coding", "RIDIBatang"))[#it]
  )
}
