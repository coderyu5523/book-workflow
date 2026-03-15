
#let book-title = "사내 AI 비서"
#let book-subtitle = "RAG 기반 업무 자동화"
#let book-description = [사내 문서를 활용한 AI 비서 구축 가이드]
#let book-header-title = "사내 AI 비서"

// ── 범용 북 템플릿 (Typst) ──
// 이 파일은 스킬(pub-typst-design) 소유. 프로젝트에서 심볼릭 링크로 참조.
// 프로젝트의 book.typ에서 정의한 변수(book-title 등)를 사용합니다.
//
// 필수 변수 (book.typ에서 정의):
//   #let book-title = "책 제목"
//   #let book-subtitle = "부제"
//   #let book-description = [설명]
//   #let book-header-title = "헤더 표시 제목"

// ── 조판 설정 변수 ──
// 행간: 줄과 줄 사이 간격 (pt 단위)
#let body-leading = 8pt
// 자간: 글자와 글자 사이 간격 (pt 단위, 0pt = 기본)
#let body-tracking = 0pt
// 제목-문단 간격: 제목 아래 본문까지의 여백 (행간과 동일)
#let heading-gap = body-leading
// 코드 블록: 구분선과 코드 사이 여백
#let code-inset-x = 16pt
#let code-inset-y = 6pt
// 코드 블록: 구분선 두께
#let code-rule-stroke = 2pt

// ── 챕터 추적 (헤더용) ──
#let chapter-title = state("chapter-title", none)

// ── 페이지 설정 ──
// 46배판 (188x257mm) — 국내 IT 서적 표준 판형
#set page(
  width: 188mm,
  height: 257mm,
  margin: (top: 20mm, bottom: 28mm, left: 20mm, right: 20mm),
  numbering: "1",
  number-align: center,
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 {
      set text(8pt, fill: rgb("#999999"))
      grid(
        columns: (1fr, 1fr),
        align(left)[#book-header-title],
        align(right)[#chapter-title.get()],
      )
      v(2pt)
      line(length: 100%, stroke: 0.3pt + rgb("#dddddd"))
    }
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 2 {
      align(center, text(9pt, fill: rgb("#888888"))[#counter(page).display()])
    }
  },
)

// ── 폰트 설정 ──
#set text(
  font: ("KoPubDotum_Pro", "Apple SD Gothic Neo"),
  size: 10pt,
  lang: "ko",
  fill: rgb("#1a1a1a"),
  tracking: body-tracking,
)

#set par(
  leading: body-leading,
  first-line-indent: 0pt,
  justify: true,
)

// ── 제목 스타일 ──
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  block(
    width: 100%,
    below: heading-gap,
    sticky: true,
    {
      text(16pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
      v(8pt)
      line(length: 100%, stroke: 3pt + rgb("#2563eb"))
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
    text(10pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
  )
  v(heading-gap)
}

#show heading.where(level: 3): it => {
  v(14pt)
  block(
    below: heading-gap,
    sticky: true,
    text(10pt, weight: "semibold", fill: rgb("#374151"))[#it.body]
  )
  v(heading-gap)
}

#show heading.where(level: 4): it => {
  v(10pt)
  block(
    below: heading-gap,
    sticky: true,
    text(10pt, weight: "medium", fill: rgb("#555555"))[#it.body]
  )
  v(heading-gap)
}

// ── 코드 블록 (위아래 굵은 회색선만, 좌우 없음) ──
#show raw.where(block: true): it => {
  set text(size: 8pt, weight: "bold", font: ("Menlo", "KoPubDotum_Pro"))
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
}

// ── 인라인 코드 (볼드 통일) ──
#show raw.where(block: false): it => {
  text(weight: "bold", fill: rgb("#1e3a5f"))[#it.text]
}

// ── 인용 블록 — 디자인 A: 점선 박스 (기본 blockquote) ──
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
      text(size: 9pt, fill: rgb("#333333"))[#it.body]
    }
  )
}

// ── 인용 블록 — 디자인 B: 회색 박스 + 프라이머리 라벨 (callout) ──
// [라벨 - 본문] 형태로 한 줄에 이어서 표시
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
      text(size: 9pt)[#text(weight: "bold", fill: rgb("#2563eb"))[#label] #text(fill: rgb("#333333"))[\- #body]]
    }
  )
}

// ── 표 스타일 (B&W + 그레이, 가는 실선 테두리, 왼쪽 정렬) ──
#set table(
  stroke: 0.5pt + rgb("#d1d5db"),
  inset: (x: 10pt, y: 8pt),
  align: left,
  fill: (_, y) => if y == 0 { rgb("#e5e5e5") } else if calc.odd(y) { rgb("#fafafa") } else { white },
)

#show table.cell.where(y: 0): set text(fill: rgb("#1a1a1a"), weight: "bold")

#show table: it => {
  set text(size: 8.5pt)
  align(left, block(breakable: true)[#it])
}

// ── 볼드/이탤릭 ──
#show strong: set text(fill: rgb("#1e3a5f"))
#show emph: set text(fill: rgb("#6b7280"))

// ── 수평선은 후처리에서 #v + block으로 변환됨 ──

// ── figure 스타일 ──
#show figure: it => {
  v(8pt)
  align(center, it.body)
  if it.caption != none {
    v(2pt)
    align(center, text(8pt, fill: rgb("#6b7280"))[#it.caption.body])
  }
  v(4pt)
}

// ── 링크 스타일 ──
#show link: it => {
  text(fill: rgb("#2563eb"))[#it]
}

// ── 자동 크기 조절 이미지 ──
// 남은 페이지 공간을 감지하여 이미지 크기를 자동으로 조절합니다.
// max-width: 이미지 최대 너비 비율 (0.0~1.0)
// 이미지가 남은 공간보다 크면 자동 축소, 너무 작아지면 다음 페이지로 넘김
#let auto-image(path, alt: none, max-width: 0.7) = layout(size => context {
  let target-width = size.width * max-width
  let img = image(path, width: target-width)
  let img-size = measure(img)
  let caption-h = if alt != none { 28pt } else { 0pt }
  let needed = img-size.height + caption-h + 24pt

  let final-width = if needed > size.height and size.height > 120pt {
    // 남은 공간에 맞게 축소 시도
    let available = size.height - caption-h - 24pt
    let ratio = available / img-size.height
    if ratio >= 0.5 {
      target-width * ratio
    } else {
      target-width  // 너무 작아지면 원래 크기 (다음 페이지로)
    }
  } else {
    target-width
  }

  if alt != none {
    figure(image(path, width: final-width), caption: [#alt])
  } else {
    align(center, image(path, width: final-width))
  }
})

// ── 2열 이미지 (이미지 2개 나란히) ──
// 이미지 두 개를 좌우로 나란히 배치합니다.
// caption1, caption2: 각 이미지의 캡션 (없으면 캡션 없이 배치)
#let dual-image(path1, path2, caption1: none, caption2: none, gap: 16pt) = {
  v(8pt)
  grid(
    columns: (1fr, 1fr),
    column-gutter: gap,
    align: center,
    if caption1 != none { figure(image(path1, width: 100%), caption: [#caption1]) } else { image(path1, width: 100%) },
    if caption2 != none { figure(image(path2, width: 100%), caption: [#caption2]) } else { image(path2, width: 100%) },
  )
  v(8pt)
}

// ══════════════════════════════════════
// 표지
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #v(1fr)
  #align(center)[
    // 상단 장식선
    #line(length: 40%, stroke: 2pt + rgb("#2563eb"))
    #v(24pt)
    #text(42pt, weight: "bold", fill: rgb("#1e40af"), tracking: 2pt)[#book-title]
    #v(16pt)
    #line(length: 60%, stroke: 0.5pt + rgb("#93c5fd"))
    #v(16pt)
    #text(15pt, fill: rgb("#374151"), weight: "medium")[#book-subtitle]
    #v(48pt)
    #block(
      width: 70%,
      inset: (x: 20pt, y: 16pt),
      radius: 4pt,
      fill: rgb("#f8fafc"),
      stroke: 0.5pt + rgb("#e2e8f0"),
      text(10.5pt, fill: rgb("#64748b"))[#book-description]
    )
  ]
  #v(1fr)
  #align(center)[
    #text(9pt, fill: rgb("#94a3b8"))[RAG 실전 가이드]
  ]
  #v(20pt)
]

// ══════════════════════════════════════
// 목차 (자동 생성)
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #v(30pt)
  #block(width: 100%, below: 12pt, {
    text(24pt, weight: "bold", fill: rgb("#1a1a1a"))[목차]
    v(6pt)
    line(length: 100%, stroke: 3pt + rgb("#2563eb"))
  })
  #v(12pt)

  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt)
  #show outline.entry.where(level: 1): it => {
    v(6pt)
    it
  }
  #show outline.entry.where(level: 3): set text(size: 8.5pt, fill: rgb("#6b7280"))

  #outline(
    title: none,
    indent: 1.5em,
    depth: 2,
  )
]

// ══════════════════════════════════════
// 본문 시작 — 이 아래에 Pandoc 변환 내용이 들어갑니다
// ══════════════════════════════════════

= 1장. 샘플 챕터 제목

이것은 본문 텍스트입니다. `인라인 코드`가 볼드로 표시되는지 확인합니다. 또한 `LangChain`이나 `vectorstore` 같은 용어도 확인해 보겠습니다.

== 1. 첫 번째 섹션

RAG(Retrieval-Augmented Generation) 파이프라인의 핵심은 #strong[검색] 과 #strong[생성] 두 단계입니다. 사용자의 질문이 들어오면, 먼저 관련 문서를 벡터 데이터베이스에서 검색합니다.

=== 1.1 벡터 검색의 원리

벡터 검색은 `embedding` 모델을 사용하여 텍스트를 고차원 벡터로 변환합니다. 이 벡터들 사이의 유사도를 계산하여 가장 관련 있는 문서를 찾아냅니다.

==== 1.1.1 코사인 유사도

두 벡터 사이의 각도를 측정하여 유사도를 계산합니다. 값이 1에 가까울수록 두 문서가 유사합니다.

```python
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
query_vector = embeddings.embed_query("회의실 예약 방법")
```

목적 한 줄로 설명하면, 사용자 질문을 벡터로 변환하는 코드입니다.

== 2. 인용문 디자인 테스트

아래는 일반 인용문(디자인 A - 점선 박스)입니다.

#quote(block: true)[
벡터 데이터베이스는 전통적인 관계형 데이터베이스와 달리, 고차원 벡터 데이터를 효율적으로 저장하고 검색할 수 있도록 설계되었습니다.
]

아래는 라벨이 있는 인용문(디자인 B - 회색 박스)입니다.

#callout-box([참고], [ChromaDB는 로컬 환경에서 빠르게 프로토타이핑할 수 있는 벡터 데이터베이스입니다. 설치가 간단하고 Python API를 제공합니다.])

#callout-box([팁], [운영 환경에서는 Pinecone이나 Weaviate 같은 관리형 서비스를 고려하세요. 확장성과 안정성 면에서 유리합니다.])

#callout-box([주의], [API 키를 코드에 직접 하드코딩하지 마세요. 환경 변수나 시크릿 매니저를 사용하는 것이 보안상 안전합니다.])

== 3. 표 디자인 테스트

#table(
    columns: 3,
    table.header([벡터 DB], [특징], [적합한 용도],),
    [ChromaDB], [경량, 로컬 실행], [프로토타이핑],
    [Pinecone], [관리형, 서버리스], [운영 환경],
    [Weaviate], [하이브리드 검색], [복합 검색],
    [Milvus], [대규모 처리], [엔터프라이즈],
  )

=== 3.1 성능 비교

#table(
    columns: 3,
    table.header([항목], [ChromaDB], [Pinecone],),
    [설치 난이도], [쉬움], [보통],
    [확장성], [제한적], [높음],
    [비용], [무료], [유료],
    [검색 속도], [빠름], [매우 빠름],
  )

== 4. 제목-문단 간격 비교

이 섹션은 h2 제목 직후의 본문입니다. heading-gap 변수가 행간(body-leading)과 동일하게 적용되었는지 확인합니다. 제목과 이 문단 사이의 간격이 본문 줄 간격과 같아야 합니다.

=== 4.1 h3 제목 직후 본문

이 문단은 h3 제목 바로 아래에 위치합니다. h2와 동일한 간격이 적용되어야 합니다. 벡터 검색에서 코사인 유사도는 가장 널리 사용되는 유사도 측정 방식입니다.

==== 4.1.1 h4 제목 직후 본문

이 문단은 h4 제목 바로 아래에 위치합니다. 역시 동일한 heading-gap이 적용됩니다. 임베딩 모델의 선택은 검색 품질에 직접적인 영향을 미칩니다.

== 5. 이미지 레이아웃 테스트

=== 5.1 1열 이미지 (auto-image)

아래는 `auto-image` 함수로 배치한 1열 중앙 정렬 이미지입니다. 남은 페이지 공간에 맞게 자동 축소됩니다.

#auto-image("sample_diagram.png", alt: "1열 레이아웃: 자동 크기 조절 다이어그램")
이미지 아래 본문이 이어집니다. 캡션 스타일과 이미지-텍스트 간격(상하 8pt)을 확인합니다.

=== 5.2 2열 이미지

아래는 이미지 2개를 나란히 배치한 2열 레이아웃입니다.

#dual-image("sample_diagram.png", "sample_diagram.png", caption1: "왼쪽 다이어그램", caption2: "오른쪽 다이어그램")
2열 이미지 아래 본문이 이어집니다. 이미지 간 간격(16pt)과 캡션 스타일을 확인합니다.
