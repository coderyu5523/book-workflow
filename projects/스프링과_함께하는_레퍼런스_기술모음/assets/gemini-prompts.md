# Gemini 인포그래픽 프롬프트 모음

아래 프롬프트를 Gemini Image Generation에 넣어서 PNG를 생성한 뒤, 각 경로에 저장합니다.

---

## 1. CH05 — 업로드 흐름 (그림 5-1a)
**저장 경로**: `assets/CH05/gemini/05_upload-flow.png`

```
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.
Use inner boxes with dashed/solid borders to separate sections.
Header bars with dark gray background and white text for section titles.
Korean labels throughout.

Title (top center, bold): "Presigned URL 업로드 흐름"
Thin horizontal rule below title.

Three sections left to right, connected by numbered arrows:

[Section 1 — rounded rectangle, thin black border]
  Header bar (dark gray bg, white text): "Client"
  Inner icon: minimalist monitor icon
  Footer: "브라우저 / 앱"

[Section 2 — rounded rectangle, thin black border]
  Header bar (dark gray bg, white text): "Spring 서버"
  Inner icon: minimalist server rack icon
  Footer: "Presigned URL 발급"

[Section 3 — rounded rectangle, thin black border]
  Header bar (dark gray bg, white text): "AWS S3"
  Inner icon: minimalist cloud icon
  Footer: "파일 저장소"

Arrow 1: Client → Spring, labeled "① Presigned URL 발급 요청"
Arrow 2: Spring → Client, labeled "② Presigned URL 응답"
Arrow 3: Client → S3, labeled "③ URL로 이미지 직접 업로드"
```

---

## 2. CH05 — 후처리 흐름 (그림 5-1b)
**저장 경로**: `assets/CH05/gemini/05_resize-flow.png`

```
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.
Use inner boxes with dashed/solid borders to separate sections.
Header bars with dark gray background and white text for section titles.
Korean labels throughout.

Title (top center, bold): "Lambda 리사이즈 후처리 흐름"
Thin horizontal rule below title.

Upper row — three sections left to right:

[Section 1 — rounded rectangle, thin black border]
  Header bar: "AWS S3"
  Inner icon: minimalist cloud icon
  Footer: "원본 이미지 저장"

[Section 2 — rounded rectangle, thin black border]
  Header bar: "AWS Lambda"
  Inner icon: minimalist lightning bolt icon
  Footer: "리사이즈 처리"

[Section 3 — rounded rectangle, thin black border]
  Header bar: "AWS S3"
  Inner icon: minimalist cloud icon
  Footer: "리사이즈 이미지 저장"

Arrow 1: S3 → Lambda, labeled "① ObjectCreated 이벤트"
Arrow 2: Lambda → S3, labeled "② 리사이즈 저장"

Lower row — separate flow:

[Section 4 — rounded rectangle, thin black border]
  Header bar: "Client"
  Inner icon: minimalist monitor icon

[Section 5 — rounded rectangle, thin black border]
  Header bar: "Spring 서버"
  Inner icon: minimalist server rack icon

Arrow 3: Client → Spring, labeled "③ /complete 호출 → DB 메타 저장"
```

---

## 3. CH06 — Polling / SSE / WebSocket 비교 (그림 6-1)
**저장 경로**: `assets/CH06/gemini/06_communication-compare.png`

```
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.
Use inner boxes with dashed/solid borders to separate sections (입력/처리/결과).
Header bars with dark gray background and white text for section titles.
Thin dotted line dividers between comparison columns.
Korean labels throughout.

Title (top center, bold): "실시간 통신 방식 비교 — Polling vs SSE vs WebSocket"
Thin horizontal rule below title.

Three columns separated by thin dotted vertical lines:

[Left column — rounded rectangle, light gray fill (#F5F5F5)]
  Header bar (dark gray bg, white text): "Polling"
  [Inner box — dashed border] Client icon + Server icon
  Repeating arrows: Client → Server (요청), Server → Client (응답) × 2회
  Footer label: "주기적 요청 반복 — 서버 부하 높음"

[Center column — same structure]
  Header bar: "SSE (Server-Sent Events)"
  [Inner box] Client icon + Server icon
  Single long arrow: Server → Client only (단방향)
  Footer label: "서버만 전송 — 알림·피드에 적합"

[Right column — same structure]
  Header bar: "WebSocket"
  [Inner box] Client icon + Server icon
  Double-headed arrow: Client ↔ Server (양방향)
  Footer label: "양방향 자유 통신 — 채팅에 적합"

[Bottom — comparison table, hairline borders, alternating light gray rows]
| 항목 | Polling | SSE | WebSocket |
| 방향 | 단방향 (요청-응답) | 단방향 (서버→클라) | 양방향 |
| 연결 | 매번 새 연결 | 한 번 연결 유지 | 한 번 연결 유지 |
| 용도 | 단순 상태 확인 | 알림, 피드 | 채팅, 게임 |
```

---

## 4. CH07 — HLS 스트리밍 흐름 (그림 7-1)
**저장 경로**: `assets/CH07/gemini/07_hls-flow.png`

```
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.
Use inner boxes with dashed/solid borders to separate sections.
Header bars with dark gray background and white text for section titles.
Korean labels throughout.

Title (top center, bold): "HLS 스트리밍 전체 흐름"
Thin horizontal rule below title.

Two rows of flow:

[Upper row — "업로드 & 인코딩"]
  Three sections left to right:
  [Box 1] Header: "사용자" / Inner: person icon / Footer: "영상 업로드"
  [Box 2] Header: "Spring 서버" / Inner: server rack icon / Footer: "업로드 수신"
  [Box 3] Header: "FFmpeg" / Inner: gear icon / Footer: "m3u8 + ts 생성"
  Arrow 1: 사용자 → Spring, labeled "① 영상 업로드"
  Arrow 2: Spring → FFmpeg, labeled "② 인코딩 요청"
  Arrow 3: FFmpeg → Spring, labeled "③ 인코딩 완료"

[Lower row — "재생"]
  Two sections:
  [Box 4] Header: "브라우저" / Inner: monitor icon / Footer: "HLS.js 플레이어"
  [Box 5] Header: "Spring 서버" / Inner: server rack icon / Footer: "정적 리소스 제공"
  Arrow 4: 브라우저 → Spring, labeled "④ m3u8 요청"
  Arrow 5: Spring → 브라우저, labeled "⑤ ts 세그먼트 순차 전송"
```

---

## 5. CH08 — 역인덱스 구조도 (그림 8-1)
**저장 경로**: `assets/CH08/gemini/08_inverted-index.png`

```
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.
Use inner boxes with dashed/solid borders to separate sections (입력/처리/결과).
Header bars with dark gray background and white text for section titles.
Korean labels throughout.

Title (top center, bold): "역인덱스(Inverted Index) — 단어에서 문서 찾기"
Thin horizontal rule below title.

Two sections side by side, connected by a large center arrow labeled "단어 → 문서":

[Left section — rounded rectangle, light gray fill (#F5F5F5)]
  Header bar (dark gray bg, white text): "문서 (Document)"
  Three inner boxes stacked vertically, each with solid border:
    [Box 1] "Doc1 — 갤럭시 노트 출시"
    [Box 2] "Doc2 — 아이폰 노트 비교"
    [Box 3] "Doc3 — 갤럭시 S 리뷰"

[Right section — same structure]
  Header bar: "역인덱스 (Inverted Index)"
  Three inner boxes stacked vertically:
    [Box A] "갤럭시 → Doc1, Doc3"
    [Box B] "아이폰 → Doc2"
    [Box C] "노트 → Doc1, Doc2, Doc3"

Thin arrows connecting each document to its matching term boxes.

[Bottom — hairline border table]
| 검색어 | 매칭 문서 | 설명 |
| "갤럭시" | Doc1, Doc3 | 키워드 포함 문서 즉시 반환 |
| "노트" | Doc1, Doc2, Doc3 | 전체 문서 스캔 없이 조회 |
```

---

## 6. CH09 — RabbitMQ 전체 흐름도 (그림 9-1)
**저장 경로**: `assets/CH09/gemini/09_rabbitmq-flow.png`

```
Black and white minimalist infographic. White background, black/dark gray elements only.
Clean geometric shapes, thin lines, rounded corners on boxes. Modern sans-serif font. 16:9.
Use inner boxes with dashed/solid borders to separate sections.
Header bars with dark gray background and white text for section titles.
Korean labels throughout.

Title (top center, bold): "RabbitMQ 메시지 흐름 — GitHub 변경 감지부터 파일 반영까지"
Thin horizontal rule below title.

Five sections left to right:

[Section 1 — rounded rectangle, thin black border]
  Header bar: "GitHub"
  Inner icon: code branch icon
  Footer: "README 수정"

[Section 2 — rounded rectangle, thin black border]
  Header bar: "Producer"
  Inner icon: server rack icon
  Footer: "폴링 + 변경 감지"

[Section 3+4 — dashed rounded rectangle enclosing two inner boxes, labeled "RabbitMQ"]
  [Inner box 3] Header: "Exchange" / Footer: "github.events"
  [Inner box 4] Header: "Queue" / Footer: "repo-updates"
  Arrow inside: Exchange → Queue, labeled "Routing Key 매칭"

[Section 5 — rounded rectangle, thin black border]
  Header bar: "Consumer"
  Inner icon: server rack icon
  Footer: "파일 반영"

Arrow 1: GitHub → Producer, labeled "① 변경 감지"
Arrow 2: Producer → Exchange, labeled "② 메시지 발행"
Arrow 3: Queue → Consumer, labeled "③ 메시지 소비"
```
