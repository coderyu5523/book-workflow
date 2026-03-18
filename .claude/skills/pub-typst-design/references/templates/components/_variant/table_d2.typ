// ── 표 스타일: Design 2 (회색 헤더, 검정 글씨, 좌측 정렬) ──
#set table(
  stroke: 0.5pt + rgb("#d1d5db"),
  inset: (x: 10pt, y: 8pt),
  align: left,
  fill: (_, y) => if y == 0 { rgb("#e5e5e5") } else if calc.odd(y) { rgb("#fafafa") } else { white },
)

#show table.cell.where(y: 0): set text(fill: rgb("#1a1a1a"), weight: "bold")

#show table: it => {
  set text(size: 1em)
  set par(justify: false)
  align(left, block(breakable: true)[#it])
}
