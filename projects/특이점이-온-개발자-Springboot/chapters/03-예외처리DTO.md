# 챕터 3. 예외 처리와 DTO - 터지지 않고, 새어 나가지 않게

게시판은 목록과 상세, 작성과 수정, 삭제까지 동작합니다. 그런데 앞 챕터를 닫으며 물음이 하나 남았습니다. 없는 번호로 상세를 부르면 어떻게 되느냐는 것이었습니다. 목록에 글이 두 건뿐인 서버에 아직 없는 999번 상세를 요청하면, 응답은 멀쩡히 돌아옵니다. 그런데 이상합니다. 없는 글인데도 `status`는 200 성공인데, 정작 `body`는 비어 있습니다. 없는 글을 두고 성공이라 답하고 있습니다.

이것만 문제가 아닙니다. 정상으로 존재하는 1번 글을 부르면 응답은 잘 돌아옵니다. 그런데 그 응답 안에는 `createdAt` 같은 내부 기록 필드가 그대로 실려 나갑니다. 지금은 사소해 보이지만, 뒤 챕터에서 엔티티에 작성자나 비밀번호가 붙으면, 응답을 감싸지 않는 한 그 값까지 바깥으로 새어 나갑니다.

두 개의 구멍이 한꺼번에 드러났습니다. 없는 글인데 성공이라 답하며 빈 값이 나가는 것과, 내부 엔티티가 응답으로 새어 나가는 것입니다.

<div class="svg-figure">
<svg viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 3 한눈에 보기. 구멍 1은 없는 글을 조회하면 200 성공에 빈 값이 돌아오던 것을, Optional과 예외와 전역 처리로 404 응답으로 바꾼다. 구멍 2는 엔티티를 통째로 내보내 createdAt까지 새어 나가던 것을, 응답 DTO로 감싸 boardId·title·content 세 값만 내보낸다.">
  <defs>
    <marker id="c3ov-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 3 한눈에 보기 - 두 구멍을 막는다</text>
  <text x="30" y="112" font-size="13" font-weight="700" fill="#c2410c">구멍 1</text>
  <text x="30" y="131" font-size="11" fill="#6b7280">없는 글 조회</text>
  <rect x="150" y="86" width="230" height="64" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="265" y="112" text-anchor="middle" font-size="13" font-weight="700" fill="#c2410c">200 성공인데</text>
  <text x="265" y="132" text-anchor="middle" font-size="11" fill="#6b7280">body가 빈 값</text>
  <line x1="385" y1="118" x2="595" y2="118" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <text x="490" y="108" text-anchor="middle" font-size="11" fill="#4f46e5">Optional · 예외 · 전역 처리</text>
  <rect x="600" y="86" width="370" height="64" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="785" y="112" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">404 · 게시글을 찾을 수 없습니다</text>
  <text x="785" y="132" text-anchor="middle" font-size="11" fill="#3730a3">status·msg·body 형식을 갖춘 응답</text>
  <text x="30" y="262" font-size="13" font-weight="700" fill="#c2410c">구멍 2</text>
  <text x="30" y="281" font-size="11" fill="#6b7280">엔티티 노출</text>
  <rect x="150" y="236" width="230" height="64" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="265" y="262" text-anchor="middle" font-size="13" font-weight="700" fill="#c2410c">엔티티를 통째로</text>
  <text x="265" y="282" text-anchor="middle" font-size="11" fill="#6b7280">createdAt까지 새어 나감</text>
  <line x1="385" y1="268" x2="595" y2="268" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <text x="490" y="258" text-anchor="middle" font-size="11" fill="#4f46e5">응답 DTO로 감쌈</text>
  <rect x="600" y="236" width="370" height="64" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="785" y="262" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">DTO만 내보냄</text>
  <text x="785" y="282" text-anchor="middle" font-size="11" fill="#3730a3">boardId · title · content</text>
</svg>
</div>

*그림 3-1. 없는 글은 404로 정리하고, 응답은 엔티티 대신 DTO로 내보내 두 구멍을 막습니다*

:::goal
**이번 챕터가 끝나면**

- 엔티티를 응답에 직접 쓰지 않고 DTO로 감싸는 이유를 설명할 수 있습니다
- `Optional`과 `orElseThrow`로 없는 데이터를 예외로 바꾸고, 커스텀 예외가 왜 `RuntimeException`인지 이해합니다
- `@RestControllerAdvice`로 예외를 한 곳에서 JSON으로 바꿔, 없는 글도 깔끔한 404로 응답합니다
:::

## 3.1 두 개의 구멍

먼저 없는 글을 조회하는 첫 번째 구멍입니다. 999번 상세를 요청하면 이런 응답이 돌아옵니다.

```bash [터미널] 없는 글 조회
GET http://localhost:8080/api/boards/999
```

```json
{
  "status": 200,
  "msg": "성공",
  "body": null
}
```

`status`는 200, `msg`는 성공인데 `body`가 비어 있습니다. 원인은 조회 코드에 있습니다. 앞 챕터의 `findById`는 없는 글을 찾으면 글 대신 `null`을 돌려줍니다. 그 `null`이 그대로 응답 `body`에 담겨, 없는 글인데도 성공이라 답하고 빈 값이 나갑니다. 받는 쪽은 글이 없어서 빈 것인지, 정말 성공인지 구분할 수 없습니다.

두 번째 구멍은 오히려 정상으로 동작하는 요청에 있습니다. 정상으로 존재하는 1번 글을 부르면 응답은 이렇게 돌아옵니다.

```json
{
  "status": 200,
  "msg": "성공",
  "body": {
    "id": 1,
    "title": "title1",
    "content": "content1",
    "createdAt": "2026-07-21T09:10:02.123+00:00"
  }
}
```

`body`를 보면 `createdAt` 같은 내부 기록 필드가 그대로 실려 나갑니다. 지금은 사소해 보입니다. 그런데 응답에 엔티티를 통째로 실어 보내는 한, 엔티티에 필드가 붙을 때마다 그 값이 자동으로 바깥에 노출됩니다.

이 둘을 이번 챕터에서 차례로 막습니다. 먼저 엔티티가 새어 나가는 쪽을 응답 그릇으로 막고, 그다음 없는 글이 성공으로 빠져나가는 쪽을 예외로 처리합니다. 이번 챕터에서 새로 만들거나 손보는 클래스는 다음과 같습니다.

| 클래스 | 역할 |
|--------|------|
| BoardResponse | (신규) 응답으로 내보낼 값만 담는 DTO. `DTO`와 `DetailDTO` 두 그릇을 둡니다. |
| Exception404 | (신규) 자원을 찾을 수 없을 때 던지는 커스텀 예외입니다. |
| GlobalExceptionHandler | (신규) 던져진 예외를 한 곳에서 JSON 응답으로 바꾸는 전역 처리기입니다. |
| BoardRepository | (변경) `findById`가 `null` 대신 `Optional`을 반환합니다. |
| BoardService | (변경) `orElseThrow`로 없음을 예외로 바꾸고, 엔티티 대신 DTO를 반환합니다. |
| BoardController | (변경) 응답 반환 타입이 엔티티에서 DTO로 바뀝니다. |
| BoardRequest | (변경) 요청 DTO를 엔티티로 바꾸는 `toEntity`를 더합니다. |

::::prep
**소스코드 준비**

앞 챕터에서 클론한 예제 저장소에서 이번 챕터 폴더로 이동합니다. 패키지 루트는 앞 챕터와 같은 `com.metacoding.spring`입니다.

```bash [터미널] 챕터 3 폴더로 이동
cd spring-start/ch03
```

이번 챕터에서 새로 만들거나 고치는 파일은 다음과 같습니다. 나머지는 앞 챕터 그대로입니다.

```
spring-start/ch03  (변경·신규만)
├── board/BoardResponse.java                 [실습] 응답 DTO(DTO/DetailDTO)
├── core/handler/ex/Exception404.java        [실습] 커스텀 예외
├── core/handler/GlobalExceptionHandler.java [실습] 전역 예외 처리
├── board/BoardRepository.java               [설명] findById → Optional
├── board/BoardService.java                  [설명] orElseThrow + DTO 반환
├── board/BoardController.java               [설명] 응답 타입 DTO로 교체
└── board/BoardRequest.java                  [참고] toEntity() 추가
```

챕터를 따라 코드를 채우고, 막히면 `spring-end`의 완성 코드를 참고하세요.
::::

## 3.2 응답 그릇을 따로 만든다

새어 나가는 구멍부터 막습니다. 응답에 엔티티를 그대로 실어 보내는 것은, 주방에서 쓰던 냄비를 손님상에 그대로 올리는 것과 같습니다. 엔티티는 데이터베이스와 맞닿아 온갖 정보를 담고, 값을 넣고 빼며 다루는 주방 냄비입니다. 손님상에 나가는 것은 접시라야 하고, 접시에는 손님이 볼 값만 덜어 담습니다.

응답으로 내보낼 그릇을 따로 만들어 거기에 보여줄 값만 담으면, 엔티티는 주방 안에 남고 접시만 바깥으로 나갑니다. 이렇게 계층 사이에서 필요한 값만 담아 나르는 객체를 DTO(Data Transfer Object)라고 합니다.

<div class="svg-figure">
<svg viewBox="0 0 900 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="엔티티와 DTO 경계. 왼쪽 내부에는 title, content, createdAt에 작성자, 비밀번호까지 담은 Board 엔티티가 있고, 가운데 벽의 창구에는 'DTO만 통과' 표지가 붙어 있다. 창구를 지나 오른쪽 응답으로 나온 것은 boardId, title, content 세 줄만 담은 작은 DTO다.">
  <defs>
    <marker id="c3dto-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="175" y="30" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">내부</text>
  <text x="661" y="30" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">응답 (바깥)</text>
  <rect x="40" y="46" width="270" height="256" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="175" y="78" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">Board 엔티티</text>
  <text x="175" y="110" text-anchor="middle" font-size="12" fill="#334155">title : 제목</text>
  <text x="175" y="134" text-anchor="middle" font-size="12" fill="#334155">content : 내용</text>
  <text x="175" y="158" text-anchor="middle" font-size="12" fill="#334155">createdAt : 작성시각</text>
  <text x="175" y="186" text-anchor="middle" font-size="12" fill="#cbd5e1">userId : 작성자</text>
  <text x="175" y="208" text-anchor="middle" font-size="12" fill="#cbd5e1">password : ****</text>
  <text x="175" y="250" text-anchor="middle" font-size="11" fill="#6b7280">내부 정보가 다 들어 있다</text>
  <rect x="430" y="40" width="14" height="270" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>
  <rect x="418" y="150" width="38" height="52" rx="4" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <rect x="388" y="102" width="98" height="28" rx="6" fill="#4f46e5"/>
  <text x="437" y="121" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">DTO만 통과</text>
  <rect x="556" y="118" width="210" height="130" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="661" y="148" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">BoardResponse.DTO</text>
  <text x="661" y="178" text-anchor="middle" font-size="12" fill="#334155">boardId : 1</text>
  <text x="661" y="202" text-anchor="middle" font-size="12" fill="#334155">title : 제목</text>
  <text x="661" y="226" text-anchor="middle" font-size="12" fill="#334155">content : 내용</text>
  <line x1="310" y1="176" x2="416" y2="176" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3dto-a)"/>
  <line x1="458" y1="176" x2="554" y2="176" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3dto-a)"/>
</svg>
</div>

*그림 3-2. 엔티티는 내부에 두고, 응답으로 나갈 값만 DTO에 담아 내보냅니다*

`board/BoardResponse.java`를 열고 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```java [실습 1] board/BoardResponse.java. 응답 DTO
public class BoardResponse {

    // 1. 목록용 그릇. 엔티티를 받아 보여줄 값만 담는다
    public record DTO(Integer boardId, String title, String content) {
        public DTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }

    // 2. 상세용 그릇. 지금은 DTO와 같지만 앞으로 달라진다
    public record DetailDTO(Integer boardId, String title, String content) {
        public DetailDTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }
}
```

`record`는 값을 담기만 하는 간단한 클래스를 짧게 정의하는 자바 문법으로, 앞 챕터의 `BoardRequest`에서 이미 썼습니다. 두 그릇 모두 `Board`를 받는 생성자를 하나씩 두었습니다. 엔티티를 넘기면 `board.getId()`, `getTitle()`, `getContent()`에서 값을 꺼내 그릇에 옮겨 담습니다. 이 생성자 덕분에 서비스에서 `new BoardResponse.DTO(board)` 한 줄로 엔티티를 접시로 바꿀 수 있습니다. 응답 필드 이름을 엔티티의 `id`가 아니라 `boardId`로 둔 것도, 바깥에 나가는 이름을 응답 그릇에서 따로 정할 수 있기 때문입니다.

지금은 목록용 `DTO`와 상세용 `DetailDTO`의 내용이 똑같습니다. 그런데 상세 화면은 앞으로 댓글 같은 정보가 더 붙어 목록과 달라집니다. 미리 나눠 두면 그때 상세 그릇만 손보면 되고, 목록은 건드릴 필요가 없습니다.

들어오는 요청도 마찬가지로 그릇에 담습니다. 앞 챕터에서 만든 `SaveDTO`에 `toEntity()`를 더해, 요청 그릇을 엔티티로 바꾸는 통로를 냅니다. `board/BoardRequest.java`의 `SaveDTO`에 아래 메서드를 추가합니다.

```java [참고] board/BoardRequest.java. 요청 DTO에 toEntity 추가
    public record SaveDTO(String title, String content) {
        // 빌더로 요청 값을 엔티티에 옮겨 담는다
        public Board toEntity() {
            return Board.builder().title(title()).content(content()).build();
        }
    }
```

`toEntity()`가 `Board.builder()`를 쓰므로, 앞 챕터에서 `@Data`만 붙였던 `Board` 엔티티에 `@Builder`를 더합니다. 빌더를 쓰면 필요한 필드만 골라 채워 엔티티를 만들 수 있습니다.

## 3.3 없음을 예외로 바꾼다

그릇을 만들었으니 이제 서비스가 엔티티를 접시에 담아 넘기게 고칩니다. 그런데 그 전에 첫 번째 구멍, 없는 글이 성공으로 빠져나가는 문제를 같이 다뤄야 합니다. 두 문제가 모두 조회 메서드에서 만나기 때문입니다.

빈 값이 성공으로 나가는 원인은 `findById`가 없는 글에 `null`을 돌려주기 때문입니다. `null`은 아무 표시가 없는 빈손입니다. 받는 쪽은 그것이 진짜 글인지 빈손인지 열어 보기 전엔 모릅니다. 자바에는 이 애매함을 걷어내는 문법이 있습니다. 값이 있을 수도, 없을 수도 있음을 상자에 담아 드러내는 `Optional`입니다.

`findById`가 `null` 대신 `Optional`을 돌려주면, 받는 쪽은 타입만 보고도 "빈 상자일 수 있다"는 걸 압니다. `board/BoardRepository.java`의 `findById`를 아래처럼 고칩니다.

```java [설명] board/BoardRepository.java. findById가 Optional을 반환
    // 없으면 null 대신 빈 Optional을 돌려준다
    public Optional<Board> findById(int boardId) {
        return Optional.ofNullable(em.find(Board.class, boardId));
    }
```

`Optional.ofNullable`은 `em.find`의 결과가 글이면 그 글을 담은 상자를, `null`이면 빈 상자를 만들어 줍니다. `findAll`, `save`, `delete`는 앞 챕터 그대로 두고 `findById`만 바꿉니다.

이제 서비스가 이 상자를 열어 씁니다. 상자를 여는 방법은 `orElseThrow`입니다. 상자에 값이 있으면 꺼내 주고, 비었으면 괄호 안에 적은 예외를 던집니다. 대표로 상세 조회 메서드를 보겠습니다. `board/BoardService.java`의 `게시글상세`를 아래처럼 고칩니다.

```java [설명] board/BoardService.java. 없으면 예외, 반환은 DTO
    // 없으면 Exception404를 던지고, 있으면 DetailDTO에 담아 반환한다
    public BoardResponse.DetailDTO 게시글상세(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board);
    }
```

한 메서드 안에서 두 가지가 바뀌었습니다. 하나는 조회입니다. `findById`가 돌려준 상자에 `orElseThrow`를 걸어, 없는 글이면 `null`을 넘기는 대신 `Exception404`를 던집니다. 이제 999번을 부르면 `null`이 그대로 성공 응답에 실려 나가는 게 아니라, 조회하는 순간 바로 예외가 납니다. 다른 하나는 반환입니다. 조회한 엔티티를 `DetailDTO`에 담아 돌려줍니다. 냄비 대신 접시가 나가는 것입니다.

나머지 메서드도 같은 식으로 바뀝니다. `게시글목록`은 `findAll`로 가져온 엔티티 목록을 `stream`으로 훑어 하나씩 `BoardResponse.DTO`로 바꿔 `.map(BoardResponse.DTO::new).toList()`로 반환합니다. `게시글수정`과 `게시글삭제`도 조회할 때 상세와 똑같이 `orElseThrow`로 없는 글이면 `Exception404`를 던집니다.

여기서 던지는 `Exception404`는 우리가 만들 커스텀 예외입니다. 아직 없는 클래스라 잠시 뒤에 정의합니다. 값을 바꾸는 `게시글추가`, `게시글수정`, `게시글삭제`에만 `@Transactional`을 붙이고, 조회만 하는 목록과 상세에는 붙이지 않습니다. 앞서 정한 대로, 작업대를 여는 트랜잭션 경계는 쓰기가 일어나는 메서드에만 그어 둡니다.

서비스가 DTO를 돌려주니, 컨트롤러가 받는 타입도 엔티티에서 DTO로 바뀝니다. 바뀌는 것은 받는 타입뿐이라, 컨트롤러는 표로 정리합니다.

| 엔드포인트 | 받는 타입(전) | 받는 타입(후) |
|-----------|--------------|--------------|
| `GET /api/boards` | `List<Board>` | `List<BoardResponse.DTO>` |
| `GET /api/boards/{boardId}` | `Board` | `BoardResponse.DetailDTO` |

서비스가 넘겨준 DTO를 받아 `Resp.ok`로 감싸는 것은 앞 챕터와 같습니다. 주소와 HTTP 메서드도 그대로입니다. 작성, 수정, 삭제도 똑같이 서비스가 넘겨준 DTO를 받습니다. 이제 상세를 부르면 접시에 담긴 세 값만 나갑니다.

```json
{
  "status": 200,
  "msg": "성공",
  "body": {
    "boardId": 1,
    "title": "title1",
    "content": "content1"
  }
}
```

`createdAt`은 접시에서 빠졌습니다. 두 번째 구멍이 막혔습니다. 남은 것은 `Exception404`를 만들고, 그 예외를 깔끔한 404 응답으로 바꾸는 일입니다.

## 3.4 예외의 종류와 상태 코드

`orElseThrow`가 던질 `Exception404`를 만들 차례입니다. `core/handler/ex/Exception404.java`를 열고 아래 코드를 작성합니다.

```java [실습 2] core/handler/ex/Exception404.java. 커스텀 예외
// 자원을 찾을 수 없을 때 (HTTP 404)
public class Exception404 extends RuntimeException {
    public Exception404(String message) {
        super(message);
    }
}
```

우리가 상황에 맞게 직접 정의한 이런 예외를 커스텀 예외라고 합니다. 코드는 짧지만, `RuntimeException`을 상속한다는 한 줄이 이 챕터의 핵심입니다.

자바의 예외는 크게 두 가지입니다. 하나는 `IOException`처럼 컴파일러가 처리를 강제하는 예외로, 이를 Checked 예외라고 합니다. 이 예외를 쓰면 부르는 쪽마다 `try-catch`로 감싸거나 `throws`를 달아야 컴파일이 됩니다. 그러면 예외를 처리하는 코드가 서비스 곳곳에 끼어들어 흐름이 지저분해집니다.

다른 하나는 `RuntimeException`을 상속한 Unchecked 예외입니다. 컴파일러가 처리를 강제하지 않습니다. 그냥 던지면, 잡을 곳에서 잡습니다. 서비스는 `orElseThrow`로 던지기만 하고, 이 예외를 받아 응답으로 바꾸는 일은 뒤에서 한 곳에 몰아 처리합니다. 그래서 커스텀 예외는 `RuntimeException`을 상속합니다. 서비스 코드를 예외 처리로 어지럽히지 않고, 던지는 일과 받는 일을 갈라놓기 위해서입니다.

던질 때 붙이는 404라는 숫자는 HTTP 상태 코드입니다. 응답이 어떤 상황인지를 세 자리 숫자로 알리는 약속으로, 자주 쓰는 것은 다음과 같습니다.

| 상태 코드 | 뜻 | 예 |
|-----------|-----|-----|
| 400 | 요청이 잘못됨 | 제목 없이 글 작성 |
| 401 | 인증되지 않음 | 로그인 없이 접근 |
| 403 | 권한이 없음 | 남의 글 수정 |
| 404 | 자원이 없음 | 없는 글 조회 |
| 500 | 서버 내부 오류 | 처리하지 못한 예외 |

없는 글을 부른 상황은 404에 해당합니다. 200 성공으로 답하면 없는 글을 있는 것처럼 다루는 것이고, 500은 서버가 넘어졌다는 뜻이라 역시 맞지 않습니다. 없는 글은 서버의 잘못이 아니라 찾는 자원이 없는 것이니, 404로 응답해야 정확합니다. 이 표의 상태 코드마다 `Exception400`, `Exception401`처럼 짝이 되는 커스텀 예외를 하나씩 두는 것이 흔한 방식입니다. 이번 챕터는 없는 글을 다루니 `Exception404`만 만들고, 401과 403은 다음 챕터에서 인증과 권한을 붙이며 다시 만듭니다.

## 3.5 예외를 한 곳에서 받는다

이제 던져진 `Exception404`를 받아 404 JSON으로 바꿀 차례입니다. 서비스는 예외를 던지기만 할 뿐, 그것을 응답으로 만드는 코드는 어디에도 없습니다. 컨트롤러마다 `try-catch`를 넣어 잡을 수도 있지만, 그러면 예외 처리 코드가 모든 컨트롤러에 흩어집니다. 던지는 일과 받는 일을 갈라놓기로 한 보람이 없습니다.

스프링에는 이 일을 한 곳에 몰아주는 장치가 있습니다. 건물 어느 층에서 문제가 터지든 신고가 경비실 한 곳으로 모이는 것과 같습니다. 컨트롤러 어디에서 예외가 던져지든, 그 예외를 가로채 응답으로 바꾸는 창구를 하나 두는 것입니다. 이 창구가 `@RestControllerAdvice`입니다.

`core/handler/GlobalExceptionHandler.java`를 열고 아래 코드를 작성합니다.

```java [실습 3] core/handler/GlobalExceptionHandler.java. 전역 예외 처리
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 1. Exception404는 404 JSON으로 바꾼다
    @ExceptionHandler(Exception404.class)
    public ResponseEntity<?> ex404(Exception404 e) {
        return Resp.fail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    // 2. 나머지 모든 예외는 500으로 처리한다
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> exUnknown(Exception e) {
        return Resp.fail(HttpStatus.INTERNAL_SERVER_ERROR, "서버 오류가 발생했습니다");
    }
}
```

`@RestControllerAdvice`는 이 클래스를 모든 컨트롤러의 예외를 지켜보는 전역 창구로 등록합니다. 그 안의 `@ExceptionHandler`는 어떤 예외를 맡을지 지정합니다. `ex404`는 `Exception404`가 던져질 때만 불려, 그 예외의 메시지를 담아 404 응답을 만듭니다. `exUnknown`은 미처 대비하지 못한 나머지 예외를 모두 받아 500으로 처리합니다. 예상한 오류는 정확한 코드로, 예상 못 한 오류는 500으로 감싸 어떤 경우에도 낯선 기본 화면이 나가지 않게 막습니다.

응답을 만드는 `Resp.fail`은 새로 만든 것이 아닙니다. 앞 챕터에서 `Resp.ok`와 함께 미리 준비해 둔 실패용 정적 메서드입니다. 상태 코드와 메시지를 받아, 성공 응답과 똑같이 `status`, `msg`, `body` 세 칸을 가진 모양으로 돌려줍니다. 덕분에 오류 응답도 성공 응답과 같은 형식을 지킵니다.

<div class="svg-figure">
<svg viewBox="0 0 980 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="서비스에서 던진 Exception404가 위로 전파되어 RestControllerAdvice가 가로채고, 상태 코드 404를 담은 JSON으로 바뀌어 응답된다.">
  <defs>
    <marker id="c3ex-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c3ex-warn" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <rect x="30" y="150" width="140" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="100" y="176" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">컨트롤러</text>
  <text x="100" y="196" text-anchor="middle" font-size="11" fill="#6b7280">요청을 받는 입구</text>
  <rect x="230" y="150" width="160" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="310" y="174" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">서비스</text>
  <text x="310" y="194" text-anchor="middle" font-size="11" fill="#c2410c">Exception404 던짐</text>
  <line x1="170" y1="180" x2="228" y2="180" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ex-ar)"/>
  <rect x="360" y="40" width="250" height="72" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="485" y="68" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">@RestControllerAdvice</text>
  <text x="485" y="90" text-anchor="middle" font-size="11" fill="#3730a3">전파된 예외를 한 곳에서 가로챈다</text>
  <path d="M330,150 C330,112 372,98 400,90" fill="none" stroke="#ff7849" stroke-width="1.9" stroke-dasharray="4,4" marker-end="url(#c3ex-warn)"/>
  <text x="300" y="124" text-anchor="middle" font-size="11" fill="#c2410c">예외 전파</text>
  <rect x="700" y="140" width="250" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="825" y="166" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">404 JSON 응답</text>
  <text x="825" y="188" text-anchor="middle" font-size="11" fill="#6b7280">status 404, msg,</text>
  <text x="825" y="204" text-anchor="middle" font-size="11" fill="#6b7280">body null</text>
  <path d="M610,90 C670,102 700,120 738,138" fill="none" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ex-ar)"/>
  <text x="672" y="96" text-anchor="middle" font-size="11" fill="#4f46e5">Resp.fail</text>
</svg>
</div>

*그림 3-3. 서비스에서 던진 예외는 위로 전파되고, @RestControllerAdvice가 이를 가로채 JSON으로 바꿔 응답합니다*

이제 999번 글을 다시 불러 보겠습니다.

```bash [터미널] 없는 글 다시 조회
GET http://localhost:8080/api/boards/999
```

빈 값이 실린 성공 대신 앞뒤가 맞는 404가 돌아옵니다.

<!-- [CAPTURE NEEDED: 01_404-response
  path: assets/CH3/terminal/01_404-response.png
  desc: GET /api/boards/999 요청에 대한 404 JSON 응답. { "status": 404, "msg": "게시글을 찾을 수 없습니다", "body": null } 형태. Postman 또는 브라우저 응답 화면. HTTP 상태 코드가 404로 표시되면 좋음.
] -->
![](../assets/CH3/terminal/01_404-response.png)
*그림 3-4. 없는 글을 조회하면 빈 값이 아니라 상태 코드 404를 담은 JSON이 돌아옵니다*

없는 글을 부르면 빈 값이 성공인 척 나가던 곳에, 이제 "찾을 수 없다"는 응답이 형식을 갖춰 돌아옵니다. 응답으로 나가는 것도 엔티티가 아니라 접시에 담긴 값뿐입니다. 두 구멍이 모두 막혔습니다.

오픈이는 목록 API를 받아 간 동료를 다시 불렀습니다. 키보드에서 손을 뗀 사무실이 잠깐 조용해졌습니다.

**오픈이**: "지난번에 없는 번호 넣으면 어떻게 되냐고 물었잖아요. 이제 없으면 없다고 딱 나와요."<br>
**동료**: "아, 3번 불러 볼게요. 없다고 딱 나오네요. 저번엔 성공이라면서 아무것도 없더니."

*여기까진 됐다.*

두 구멍은 막았지만, 오픈이는 화면을 내려다보다 한 가지가 걸렸습니다. 지금은 로그인 화면도, 글 주인을 확인하는 절차도 없습니다. 999번 하나 못 찾는 것은 막아 놨는데, 정작 아무나 남의 글을 고치고 지울 수 있는 서버였습니다.

*없는 글은 걸렀는데, 문은 여전히 다 열려 있잖아.*

## 3.6 이것만은 기억하자

이번 챕터에서 비유로 먼저 풀어낸 개념들을 정식 용어로 정리합니다.

| 비유 | 용어 | 정식 정의 |
|------|------|-----------|
| 손님상에 내가는 접시 | DTO | 계층 사이에서 필요한 값만 담아 나르는 객체. 엔티티를 응답에 직접 노출하지 않기 위해 사용 |
| 값이 있을 수도 없을 수도 있는 상자 | Optional | 값의 있음·없음을 타입으로 드러내는 자바 문법. `orElseThrow`로 비었을 때 예외를 던짐 |
| 상황에 맞게 직접 만든 예외 | 커스텀 예외 | 도메인 상황을 표현하려 정의한 예외. `RuntimeException`을 상속해 Unchecked로 던짐 |
| 문제 신고가 모이는 경비실 | @RestControllerAdvice | 모든 컨트롤러의 예외를 한 곳에서 가로채 응답으로 바꾸는 전역 예외 처리 장치 |

:::remember
**이것만은 기억하자**

- 엔티티를 응답에 직접 쓰지 않고 DTO에 담아 내보냅니다. 내부 필드가 새어 나가지 않고, 바깥에 보여줄 값과 이름을 응답 그릇에서 따로 정할 수 있습니다.
- 없는 값은 `Optional`로 드러내고 `orElseThrow`로 예외를 던집니다. 커스텀 예외는 `RuntimeException`을 상속해, 던지는 일과 받는 일을 나눕니다. 던져진 예외는 `@RestControllerAdvice`가 한 곳에서 받아 상태 코드에 맞는 JSON으로 바꿉니다.
- 그런데 이 게시판은 아직 완전히 열려 있습니다. 로그인도, 주인 확인도 없어 아무나 남의 글을 수정하고 삭제할 수 있습니다. 다음 챕터에서는 로그인을 붙이고, 본인만 자기 글을 건드리게 합니다.
:::
