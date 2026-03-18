// ── 본문 스타일: Design 2 (컴팩트 모노) ──

// 변수 재정의 (Design 2 값)
#let body-leading = 8pt
#let body-tracking = 0pt
#let heading-gap = 8pt
#let code-inset-x = 16pt
#let code-inset-y = 6pt
#let code-rule-stroke = 2pt

#set text(
  font: ("KoPubDotum_Pro", "Apple SD Gothic Neo"),
  size: 8pt,
  lang: "ko",
  fill: rgb("#1a1a1a"),
  tracking: body-tracking,
)

#set par(
  leading: body-leading,
  first-line-indent: 0pt,
  justify: true,
)
