# 챕터 3. 예외 처리와 DTO

게시판의 기본 기능인 목록, 상세 조회, 작성, 수정, 삭제 기능이 모두 완성되었습니다. 하지만 오픈이의 머릿속에는 앞서 동료가 무심코 던졌던 질문이 계속 맴돌았습니다.

*그런데, 없는 글 번호를 조회하면 어떻게 되지?*

오픈이는 서버에 없는 999번 글을 직접 조회해 보았습니다. 결과는 당황스러웠습니다. HTTP 상태는 200(성공)인데 응답 본문은 텅 비어 있었습니다.

*데이터가 없는데 성공이라고 답하네.*

이어서 존재하는 1번 글을 호출하자, 이번엔 `createdAt`(생성 일시) 같은 내부 기록용 필드까지 고스란히 노출되었습니다. 당장은 문제가 없지만, 나중에 비밀번호라도 추가된다면 클라이언트에게 여과 없이 전달될 상황이었습니다.

*하나는 없는 글인데 성공이라 답하고, 하나는 안 내보내도 될 값까지 내보내고 있잖아.*

두 응답을 화면에 나란히 띄워둔 채, 오픈이는 선배를 찾아갔습니다.

**오픈이**: "선배님, 없는 글을 부르면 성공으로 나오고, 있는 글을 부르면 숨겨야 할 내부 필드까지 같이 나가요. 어디서부터 손대야 할까요?"

**선배**: "둘 다 서버가 응답을 만드는 방식에서 생기는 문제예요. 두 가지만 바꾸면 돼요.

첫째, 데이터 없음은 결과가 아니라 **예외(Exception)** 로 다루세요. 조회한 값이 비었으면 즉시 예외를 던지고, 그 예외를 한 곳에서만 받게 하면 돼요. 그래야 없는 글에 정확한 에러 응답이 나가요.

둘째, 저장할 때 쓰는 **객체(Entity)** 를 그대로 내보내지 마세요. 화면에 보여줄 값만 옮겨 담는 응답용 객체를 따로 만들어야, 나중에 필드가 늘어도 엉뚱한 값이 딸려 나가지 않아요."

<div class="svg-figure">
<svg viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 3 한눈에 보기. 문제 1은 없는 글을 조회하면 200 성공에 빈 값이 돌아오던 것을, Optional과 예외와 전역 처리로 404 응답으로 바꾼다. 문제 2는 엔티티를 통째로 내보내 createdAt까지 나가던 것을, 응답 DTO로 감싸 boardId·title·content 세 값만 내보낸다.">
  <defs>
    <marker id="c3ov-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 3 한눈에 보기 - 두 문제를 바로잡는다</text>
  <text x="30" y="112" font-size="13" font-weight="700" fill="#c2410c">문제 1</text>
  <text x="30" y="131" font-size="11" fill="#6b7280">없는 글 조회</text>
  <rect x="150" y="86" width="230" height="64" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="265" y="112" text-anchor="middle" font-size="13" font-weight="700" fill="#c2410c">200 성공인데</text>
  <text x="265" y="132" text-anchor="middle" font-size="11" fill="#6b7280">body가 빈 값</text>
  <line x1="385" y1="118" x2="595" y2="118" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <text x="490" y="108" text-anchor="middle" font-size="11" fill="#4f46e5">Optional · 예외 · 전역 처리</text>
  <rect x="600" y="86" width="370" height="64" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="785" y="112" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">404 · 게시글을 찾을 수 없습니다</text>
  <text x="785" y="132" text-anchor="middle" font-size="11" fill="#3730a3">status·msg·body 형식을 갖춘 응답</text>
  <text x="30" y="262" font-size="13" font-weight="700" fill="#c2410c">문제 2</text>
  <text x="30" y="281" font-size="11" fill="#6b7280">엔티티 노출</text>
  <rect x="150" y="236" width="230" height="64" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="265" y="262" text-anchor="middle" font-size="13" font-weight="700" fill="#c2410c">엔티티를 통째로</text>
  <text x="265" y="282" text-anchor="middle" font-size="11" fill="#6b7280">createdAt까지 나감</text>
  <line x1="385" y1="268" x2="595" y2="268" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <text x="490" y="258" text-anchor="middle" font-size="11" fill="#4f46e5">응답 DTO로 감쌈</text>
  <rect x="600" y="236" width="370" height="64" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="785" y="262" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">DTO만 내보냄</text>
  <text x="785" y="282" text-anchor="middle" font-size="11" fill="#3730a3">boardId · title · content</text>
</svg>
</div>

*그림 3-1. 없는 글은 404로 정리하고, 응답은 엔티티 대신 DTO로 내보내 두 문제를 바로잡습니다*

:::goal
**이번 챕터가 끝나면**

- `JpaRepository`가 기본 조회·저장 메서드를 어떻게 대신하는지 이해합니다
- 엔티티를 응답에 직접 쓰지 않고 DTO로 감싸는 이유를 설명할 수 있습니다
- `Optional`과 `orElseThrow`로 없는 데이터를 예외로 바꾸고, 커스텀 예외가 왜 `RuntimeException`인지 이해합니다
- `@RestControllerAdvice`로 예외를 한 곳에서 JSON으로 바꿔, 없는 글도 깔끔한 404로 응답합니다
:::

::::prep
**소스코드 준비**

소스코드 준비에서 클론한 예제 저장소에서 이번 챕터 폴더로 이동합니다. 패키지 루트는 챕터 2와 같은 `com.metacoding.spring`입니다.

```bash [터미널] 챕터 3 폴더로 이동
cd spring-start/ch03
```

이번 챕터에서 새로 만들거나 고치는 파일은 다음과 같습니다. 나머지는 챕터 2 그대로입니다.

```
spring-start/ch03  (변경·신규만)
├── board/BoardResponse.java                 [실습] 응답 DTO(DTO/DetailDTO)
├── core/handler/ex/Exception404.java        [실습] 커스텀 예외
├── core/handler/GlobalExceptionHandler.java [실습] 전역 예외 처리
├── board/BoardRepository.java               [실습] JpaRepository 인터페이스로 전환
├── board/BoardService.java                  [설명] orElseThrow + DTO 반환
├── board/BoardController.java               [설명] 응답 타입 DTO로 교체
├── board/Board.java                         [설명] @Builder + 생성자 추가
└── board/BoardRequest.java                  [참고] toEntity() 추가
```

챕터를 따라 코드를 채우고, 막히면 `spring-end`의 완성 코드를 참고하세요.
::::

## 3.1 두 개의 문제

먼저 없는 글을 조회하는 첫 번째 문제입니다. 999번 상세를 요청하면 이런 응답이 돌아옵니다.

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

`status`는 200, `msg`는 성공인데 `body`가 비어 있습니다. 원인은 조회 코드에 있습니다. 챕터 2의 `findById`는 없는 글을 찾으면 글 대신 `null`을 돌려줍니다. `null`이 그대로 응답 `body`에 담겨, 없는 글인데도 성공이라 답하고 빈 값이 나갑니다. 응답을 받은 화면에서는 글이 없어서 빈 것인지, 정말 성공인지 구분할 수 없습니다.

두 번째 문제는 오히려 정상으로 동작하는 요청에 있습니다. 정상으로 존재하는 1번 글을 부르면 응답은 이렇게 돌아옵니다.

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

`body`를 보면 `createdAt` 같은 내부 기록 필드가 그대로 담겨 나갑니다. 지금은 사소해 보입니다. 그런데 응답에 엔티티를 통째로 담아 보내는 한, 엔티티에 필드가 붙을 때마다 값이 자동으로 바깥에 노출됩니다.

이 둘을 이번 챕터에서 차례로 막습니다. 먼저 리포지토리를 `JpaRepository`로 바꾸고, 엔티티가 응답에 그대로 실리는 문제를 응답 DTO로 막은 뒤, 없는 글이 성공으로 처리되는 문제를 예외로 처리합니다. 이번 챕터에서 새로 만들거나 손보는 클래스는 다음과 같습니다.

| 클래스 | 역할 |
|--------|------|
| BoardResponse | (신규) 응답으로 내보낼 값만 담는 DTO. `DTO`와 `DetailDTO` 두 가지를 작성합니다. |
| Exception404 | (신규) 자원을 찾을 수 없을 때 던지는 커스텀 예외입니다. |
| GlobalExceptionHandler | (신규) 던져진 예외를 한 곳에서 JSON 응답으로 바꾸는 전역 처리기입니다. |
| BoardRepository | (변경) `JpaRepository`를 상속하는 인터페이스로 바뀝니다. |
| BoardService | (변경) `orElseThrow`로 없음을 예외로 바꾸고, 엔티티 대신 DTO를 반환합니다. |
| BoardController | (변경) 응답 반환 타입이 엔티티에서 DTO로 바뀝니다. |
| BoardRequest | (변경) 요청 DTO를 엔티티로 바꾸는 `toEntity`를 더합니다. |
| Board | (변경) 빌더로 만들 수 있도록 `@Builder`와 생성자를 더합니다. |

## 3.2 JpaRepository로 바꾸기

두 문제를 손보기 전에 리포지토리부터 바꿉니다. 챕터 2에서 만든 다섯 메서드는 게시글에만 쓸 수 있는 코드가 아닙니다. 회원이든 댓글이든 기본 키로 한 건을 찾고, 전체를 가져오고, 저장하고, 지우는 일은 똑같습니다. 엔티티만 바뀔 뿐 안의 내용은 같습니다.

스프링은 이 반복을 인터페이스 하나로 대신합니다. `JpaRepository`를 상속하면 기본 메서드가 딸려 오고, 구현 클래스는 스프링이 실행 시점에 만들어 줍니다.

`board/BoardRepository.java`를 열고 아래 코드로 바꿉니다.

```java [실습 1] board/BoardRepository.java. JpaRepository 상속
public interface BoardRepository extends JpaRepository<Board, Integer> {
}
```

클래스가 인터페이스가 되고, 안이 비었습니다. `JpaRepository<Board, Integer>`의 두 자리에는 다룰 엔티티와 그 기본 키의 타입을 적습니다. `@Repository`도, `EntityManager` 주입도 필요 없습니다.

챕터 2에서 손으로 만든 메서드가 어디로 갔는지 보면 이렇습니다.

| 챕터 2에서 만든 것 | 지금 | 비고 |
|---|---|---|
| `findById(int)` | 상속 | 반환 타입이 `Optional<Board>`입니다 |
| `findAll()` | 상속 | JPQL을 쓰지 않습니다 |
| `save(Board)` | 상속 | 저장된 엔티티를 돌려줍니다 |
| `delete(Board)` | 상속 | 그대로입니다 |
| (수정 메서드 없음) | 그대로 | 더티체킹으로 처리합니다 |

`EntityManager`가 사라진 것은 아닙니다. `JpaRepository`의 구현체가 안에서 `EntityManager`를 그대로 씁니다. 챕터 2에서 본 영속성 컨텍스트와 캐싱, 쓰기 지연, 더티체킹도 그대로 동작합니다. 개발자가 반복해서 쓰던 코드만 걷어낸 것입니다.

뒤 챕터에서 조건이 붙는 조회가 필요해지면, 인터페이스 안에 메서드를 선언하고 `@Query`에 JPQL을 적어 붙입니다. 챕터 2에서 배운 JPQL은 그때 다시 쓰입니다.

## 3.3 응답 DTO

### 3.3.1 DTO가 필요한 이유

엔티티가 그대로 나가는 문제부터 막습니다. 응답에 엔티티를 그대로 담아 보내는 것은, 주방에서 쓰던 냄비를 손님상에 그대로 올리는 것과 같습니다. 엔티티는 데이터베이스와 직접 연결되어 온갖 정보를 담고, 값을 넣고 빼며 다루는 주방 냄비입니다. 손님상에 나가는 것은 접시라야 하고, 접시에는 손님이 볼 값만 덜어 담습니다.

응답으로 내보낼 접시를 따로 만들어 거기에 보여줄 값만 담으면, 엔티티는 주방 안에 남고 접시만 바깥으로 나갑니다. 이렇게 계층 사이에서 필요한 값만 담아 나르는 객체를 DTO(Data Transfer Object)라고 합니다.

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

### 3.3.2 응답 DTO 만들기

`board/BoardResponse.java`를 열고 아래 코드를 작성합니다.

```java [실습 2] board/BoardResponse.java. 응답 DTO
public class BoardResponse {

    // 1. 목록용 DTO. 엔티티를 받아 보여줄 값만 담는다
    public record DTO(Integer boardId, String title, String content) {
        public DTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }

    // 2. 상세용 DTO. 지금은 목록용과 같지만 앞으로 달라진다
    public record DetailDTO(Integer boardId, String title, String content) {
        public DetailDTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }
}
```

`record`는 챕터 2의 `BoardRequest`에서 이미 쓴 문법입니다. 두 DTO 모두 `Board`를 받는 생성자를 하나씩 작성합니다. 엔티티를 넘기면 `board.getId()`, `getTitle()`, `getContent()`에서 값을 꺼내 옮겨 담습니다. 이 생성자 덕분에 서비스에서 `new BoardResponse.DTO(board)` 한 줄로 엔티티를 DTO로 바꿀 수 있습니다. 응답 필드 이름을 엔티티의 `id`가 아니라 `boardId`로 정한 것도, 바깥에 나가는 이름을 응답 DTO에서 따로 정할 수 있기 때문입니다.

지금은 목록용 `DTO`와 상세용 `DetailDTO`의 내용이 똑같습니다. 그런데 상세 화면은 앞으로 댓글 같은 정보가 더 붙어 목록과 달라집니다. 미리 나눠 두면 그때 상세 DTO만 손보면 되고, 목록은 건드릴 필요가 없습니다.

두 DTO를 각각 파일로 두지 않고 `BoardResponse` 안에 넣은 데에도 이유가 있습니다. 게시글 응답에 쓰는 DTO가 한 파일에 모이면 어느 자원의 응답인지 이름에서 드러나고, 뒤 챕터에서 회원과 댓글이 생겨 `UserResponse.DTO`나 `ReplyResponse.DTO`가 만들어져도 이름이 겹치지 않습니다. 클래스 안에 선언한 `record`는 바깥 클래스의 객체를 따로 만들지 않아도 쓸 수 있어, 서비스에서 `new BoardResponse.DTO(board)`로 바로 호출합니다.

`record`로 선언하면 필드는 바깥에서 직접 바꿀 수 없고 `boardId()`, `title()` 같은 접근자로만 읽힙니다. 응답으로 나가는 값은 한 번 만들어진 뒤 바뀔 일이 없으므로, 값만 담아 나르는 DTO에 맞는 형태입니다.

## 3.4 요청 DTO와 엔티티 변환

들어오는 요청도 마찬가지로 DTO에 담습니다. 챕터 2에서 만든 `SaveDTO`에 `toEntity()`를 더해, 요청 DTO를 엔티티로 바꾸는 메서드를 더합니다. `board/BoardRequest.java`의 `SaveDTO`에 아래 메서드를 추가합니다.

```java [참고] board/BoardRequest.java. 요청 DTO에 toEntity 추가
    public record SaveDTO(String title, String content) {
        // 빌더로 요청 값을 엔티티에 옮겨 담는다
        public Board toEntity() {
            return Board.builder().title(title()).content(content()).build();
        }
    }
```

`toEntity()`가 `Board.builder()`를 쓰므로, 챕터 2에서 `@Data`만 붙였던 `Board` 엔티티에 빌더를 더합니다. `@Builder`는 아래처럼 명시 생성자 위에 붙입니다.

```java [설명] board/Board.java. 빌더로 생성할 수 있게
@NoArgsConstructor
@Data
@Entity
@Table(name = "board_tb")
public class Board {
    // id, title, content, createdAt 필드 (챕터 2와 같음)

    @Builder // 객체 생성 용도
    public Board(Integer id, String title, String content, Timestamp createdAt) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.createdAt = createdAt;
    }
}
```

명시 생성자를 만들면 자바가 자동으로 주던 기본 생성자가 사라지는데, JPA 엔티티는 기본 생성자가 있어야 하므로 `@NoArgsConstructor`도 함께 붙입니다. 빌더를 쓰면 필요한 필드만 골라 채워 엔티티를 만들 수 있습니다.

## 3.5 Optional과 orElseThrow

남은 문제는 없는 글이 성공으로 처리되는 것입니다. 챕터 2의 `findById`는 없는 글을 찾으면 `null`을 돌려줬습니다. `null`은 아무 표시가 없는 값이라, 이 값을 받은 코드는 진짜 글인지 아닌지 열어 보기 전엔 모릅니다.

`JpaRepository`의 `findById`는 `null`을 돌려주지 않습니다. 반환 타입이 `Optional<Board>`입니다.

```java
Optional<Board> board = boardRepository.findById(1);
```

`Optional`은 값이 있을 수도, 없을 수도 있음을 상자에 담아 드러내는 자바 문법입니다. 이 값을 받은 코드는 타입만 보고도 "빈 상자일 수 있다"는 걸 압니다. 리포지토리를 인터페이스로 바꾸면서 없음을 표현하는 방식까지 함께 따라온 것입니다.

### 3.5.1 상자를 여는 세 가지 방법

담았으면 꺼내야 합니다. `Optional`에서 값을 꺼내는 방법은 세 가지인데, 상자가 비어 있을 때의 처리가 각각 다릅니다.

| 메서드 | 값이 있으면 | 비어 있으면 |
|--------|------------|------------|
| `get()` | 값을 돌려줍니다 | `NoSuchElementException`이 발생합니다 |
| `orElse(기본값)` | 값을 돌려줍니다 | 괄호에 적은 기본값을 돌려줍니다 |
| `orElseThrow(예외)` | 값을 돌려줍니다 | 괄호에 적은 예외를 던집니다 |

<div class="svg-figure">
<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="비어 있는 Optional에서 값을 꺼내는 세 방법의 결과. get을 쓰면 NoSuchElementException이 발생하고, orElse를 쓰면 괄호에 적은 기본값이 나오며, orElseThrow를 쓰면 괄호에 적은 예외가 던져진다.">
  <defs>
    <marker id="c3opt-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <rect x="30" y="110" width="180" height="80" rx="9" fill="#f8fafc" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="120" y="142" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">빈 Optional</text>
  <text x="120" y="166" text-anchor="middle" font-size="11" fill="#6b7280">글을 찾지 못했습니다</text>
  <line x1="214" y1="146" x2="516" y2="60" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3opt-a)"/>
  <text x="360" y="88" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">get()</text>
  <line x1="214" y1="150" x2="516" y2="150" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3opt-a)"/>
  <text x="360" y="142" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">orElse(기본값)</text>
  <line x1="214" y1="154" x2="516" y2="240" stroke="#4f46e5" stroke-width="1.6" marker-end="url(#c3opt-a)"/>
  <text x="360" y="228" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">orElseThrow(예외)</text>
  <rect x="520" y="28" width="350" height="64" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="695" y="54" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">NoSuchElementException</text>
  <text x="695" y="76" text-anchor="middle" font-size="11" fill="#6b7280">무엇을 못 찾았는지 알리지 못합니다</text>
  <rect x="520" y="118" width="350" height="64" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="695" y="144" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">괄호에 적은 기본값</text>
  <text x="695" y="166" text-anchor="middle" font-size="11" fill="#6b7280">없는 글을 대신할 값은 없습니다</text>
  <rect x="520" y="208" width="350" height="64" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="695" y="234" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">괄호에 적은 예외</text>
  <text x="695" y="256" text-anchor="middle" font-size="11" fill="#3730a3">상황에 맞는 예외를 고를 수 있습니다</text>
</svg>
</div>

*그림 3-3. 비어 있는 Optional에서 값을 꺼낼 때 세 방법의 결과가 다릅니다*

`get()`은 값이 있다고 보고 꺼내는 방법입니다. 비어 있으면 `NoSuchElementException`이 발생하는데, 이 예외는 "없는 글을 조회했다"는 상황을 담고 있지 않습니다. 응답으로 바꿀 때 404인지 500인지 가릴 근거가 없습니다.

`orElse`는 비었을 때 대신 쓸 값을 정합니다. 조회 결과가 없으면 빈 목록을 주는 자리에는 맞지만, 없는 글에 가짜 글을 대신 줄 수는 없습니다.

남는 것이 `orElseThrow`입니다. 상자가 비었을 때 어떤 예외를 던질지 직접 정하므로, 없는 글에 맞는 예외를 골라 던질 수 있습니다. 던진 예외를 404 응답으로 바꾸는 것이 이 챕터가 가려는 곳입니다.

### 3.5.2 없는 글을 예외로

이제 서비스가 `orElseThrow`로 상자를 엽니다. 대표로 상세 조회 메서드를 보겠습니다. `board/BoardService.java`의 `게시글상세`를 아래처럼 고칩니다.

```java [설명] board/BoardService.java. 없으면 예외, 반환은 DTO
    // 없으면 Exception404를 던지고, 있으면 DetailDTO에 담아 반환한다
    public BoardResponse.DetailDTO 게시글상세(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board);
    }
```

이제 999번을 부르면 빈 성공 대신 조회하는 순간 `Exception404`가 나고, 반환도 엔티티가 아니라 `DetailDTO`로 바뀝니다.

목록은 조금 다릅니다. 한 건이 아니라 여러 건을 각각 `DTO`로 바꿔 리스트로 돌려줘야 합니다.

```java [설명] board/BoardService.java. 목록은 DTO 리스트로 반환
    public List<BoardResponse.DTO> 게시글목록() {
        return boardRepository.findAll().stream()
                .map(BoardResponse.DTO::new)
                .toList();
    }
```

`findAll()`이 돌려준 `List<Board>`에 `stream()`을 걸어 원소를 하나씩 다루고, `map`이 각 엔티티를 `DTO`로 바꾸고, `toList()`가 결과를 다시 리스트로 모읍니다. `BoardResponse.DTO::new`는 `board -> new BoardResponse.DTO(board)`를 줄여 쓴 것으로, 엔티티 하나를 받아 DTO 하나를 만드는 생성자를 가리킵니다. 반복문으로 하나씩 담아도 결과는 같지만, 여러 건을 같은 방식으로 바꾸는 자리에서는 이 세 단계가 더 짧습니다.

수정과 삭제는 상세와 같은 식으로, 없는 글이면 `Exception404`를 던집니다.

여기서 던지는 `Exception404`는 우리가 만들 커스텀 예외로, 아직 없는 클래스라 잠시 뒤에 정의합니다.

서비스가 DTO를 돌려주니, 컨트롤러가 받는 타입도 엔티티에서 DTO로 바뀝니다. 바뀌는 것은 받는 타입뿐이라, 컨트롤러는 표로 정리합니다.

| 엔드포인트 | 받는 타입(전) | 받는 타입(후) |
|-----------|--------------|--------------|
| `GET /api/boards` | `List<Board>` | `List<BoardResponse.DTO>` |
| `GET /api/boards/{boardId}` | `Board` | `BoardResponse.DetailDTO` |

서비스가 넘겨준 DTO를 받아 `Resp.ok`로 감싸는 것은 챕터 2와 같습니다. 주소와 HTTP 메서드도 그대로입니다. 작성과 수정도 똑같이 서비스가 넘겨준 DTO를 받습니다. 이제 상세를 부르면 DTO에 담긴 세 값만 나갑니다.

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

`createdAt`은 DTO에서 빠졌습니다. 두 번째 문제가 해결됐습니다.

이 과정에서 데이터를 담는 것이 셋으로 늘었습니다. 요청 DTO와 엔티티, 응답 DTO입니다. 셋은 각각 다른 구간에서만 쓰입니다.

글을 저장할 때는 바깥에서 들어온 JSON이 요청 DTO에 담기고, `toEntity`가 담긴 값을 엔티티로 옮기고, 리포지토리가 엔티티를 데이터베이스에 저장합니다. 요청 DTO는 값을 넘기고 나면 더 쓰이지 않습니다.

<div class="svg-figure">
<svg viewBox="0 0 860 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="저장 흐름. JSON에서 요청 DTO로, 요청 DTO에서 엔티티로, 엔티티에서 데이터베이스로 차례로 이어진다.">
  <defs>
    <marker id="c3in-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <rect x="20" y="34" width="150" height="62" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="95" y="71" text-anchor="middle" font-size="14" font-weight="800" fill="#3730a3">JSON</text>
  <line x1="176" y1="65" x2="216" y2="65" stroke="#4f46e5" stroke-width="2" marker-end="url(#c3in-ar)"/>
  <rect x="222" y="34" width="170" height="62" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="307" y="71" text-anchor="middle" font-size="14" fill="#0f172a">요청 DTO</text>
  <line x1="398" y1="65" x2="438" y2="65" stroke="#4f46e5" stroke-width="2" marker-end="url(#c3in-ar)"/>
  <rect x="444" y="34" width="170" height="62" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="529" y="71" text-anchor="middle" font-size="14" fill="#0f172a">엔티티</text>
  <line x1="620" y1="65" x2="660" y2="65" stroke="#4f46e5" stroke-width="2" marker-end="url(#c3in-ar)"/>
  <rect x="666" y="34" width="170" height="62" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="751" y="71" text-anchor="middle" font-size="14" fill="#0f172a">데이터베이스</text>
</svg>
</div>

*그림 3-4. 저장 요청은 JSON에서 요청 DTO와 엔티티를 거쳐 데이터베이스에 담깁니다*

조회는 반대 방향입니다. 리포지토리가 데이터베이스에서 엔티티를 가져오고, 서비스가 보여줄 값만 응답 DTO에 옮겨 담고, 응답 DTO가 JSON으로 바뀌어 나갑니다. 엔티티는 이 구간을 벗어나지 않으므로 `createdAt` 같은 내부 필드가 바깥으로 나가지 않습니다.

<div class="svg-figure">
<svg viewBox="0 0 860 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="조회 흐름. 데이터베이스에서 엔티티로, 엔티티에서 응답 DTO로, 응답 DTO에서 JSON으로 차례로 이어진다.">
  <defs>
    <marker id="c3out-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <rect x="20" y="34" width="170" height="62" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="105" y="71" text-anchor="middle" font-size="14" fill="#0f172a">데이터베이스</text>
  <line x1="196" y1="65" x2="236" y2="65" stroke="#4f46e5" stroke-width="2" marker-end="url(#c3out-ar)"/>
  <rect x="242" y="34" width="170" height="62" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="327" y="71" text-anchor="middle" font-size="14" fill="#0f172a">엔티티</text>
  <line x1="418" y1="65" x2="458" y2="65" stroke="#4f46e5" stroke-width="2" marker-end="url(#c3out-ar)"/>
  <rect x="464" y="34" width="170" height="62" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="549" y="71" text-anchor="middle" font-size="14" fill="#0f172a">응답 DTO</text>
  <line x1="640" y1="65" x2="680" y2="65" stroke="#4f46e5" stroke-width="2" marker-end="url(#c3out-ar)"/>
  <rect x="686" y="34" width="150" height="62" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="761" y="71" text-anchor="middle" font-size="14" font-weight="800" fill="#3730a3">JSON</text>
</svg>
</div>

*그림 3-5. 조회 결과는 데이터베이스에서 엔티티와 응답 DTO를 거쳐 JSON으로 나갑니다*

남은 것은 `Exception404`를 만들고, 던져진 예외를 깔끔한 404 응답으로 바꾸는 일입니다.

## 3.6 예외의 종류와 상태 코드

`orElseThrow`가 던지는 `Exception404`를 만듭니다. `core/handler/ex/Exception404.java`를 열고 아래 코드를 작성합니다.

```java [실습 3] core/handler/ex/Exception404.java. 커스텀 예외
// 자원을 찾을 수 없을 때 (HTTP 404)
public class Exception404 extends RuntimeException {
    public Exception404(String message) {
        super(message);
    }
}
```

우리가 상황에 맞게 직접 정의한 이런 예외를 커스텀 예외라고 합니다. 코드는 짧지만, `RuntimeException`을 상속한다는 한 줄이 이 챕터의 핵심입니다.

상속한 `RuntimeException`은 컴파일러가 처리를 강제하지 않는 Unchecked 예외입니다. 강제하는 Checked와 달리 그냥 던지면 되므로, 커스텀 예외는 이를 상속해 서비스는 던지기만 하고 받는 일은 뒤에서 한 곳에 몰아 처리합니다.

던질 때 붙이는 404라는 숫자는 HTTP 상태 코드입니다. 응답이 어떤 상황인지를 세 자리 숫자로 알리는 약속으로, 자주 쓰는 것은 다음과 같습니다.

| 상태 코드 | 뜻 | 예 |
|-----------|-----|-----|
| 400 | 요청이 잘못됨 | 제목 없이 글 작성 |
| 401 | 인증되지 않음 | 로그인 없이 접근 |
| 403 | 권한이 없음 | 남의 글 수정 |
| 404 | 자원이 없음 | 없는 글 조회 |
| 500 | 서버 내부 오류 | 처리하지 못한 예외 |

없는 글을 부른 상황은 404에 해당합니다. 200 성공으로 답하면 없는 글을 있는 것처럼 다루는 것이고, 500은 서버가 넘어졌다는 뜻이라 역시 맞지 않습니다. 없는 글은 서버의 잘못이 아니라 찾는 자원이 없는 것이니, 404로 응답해야 정확합니다. 이 표의 상태 코드마다 `Exception400`, `Exception401`처럼 짝이 되는 커스텀 예외를 하나씩 두는 것이 흔한 방식입니다. 이번 챕터는 없는 글을 다루니 `Exception404`만 만들고, 401과 403은 다음 챕터에서 인증과 권한을 붙이며 다시 만듭니다.

## 3.7 전역 예외 처리

던져진 `Exception404`는 어딘가에서 받아 404 JSON으로 바꿔야 합니다. 컨트롤러마다 `try-catch`로 잡으면 예외 처리 코드가 모든 컨트롤러에 흩어집니다.

스프링에는 이 일을 한 곳에 몰아주는 장치가 있습니다. 컨트롤러 어디에서 예외가 던져지든, 던져진 예외를 한 곳에서 받아 응답으로 바꾸는 자리를 하나 두면 됩니다. 이 역할을 맡는 것이 `@RestControllerAdvice`입니다.

`core/handler/GlobalExceptionHandler.java`를 열고 아래 코드를 작성합니다.

```java [실습 4] core/handler/GlobalExceptionHandler.java. 전역 예외 처리
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

`@RestControllerAdvice`는 이 클래스를 전역 예외 처리기로 등록하고, `@ExceptionHandler`가 어떤 예외를 맡을지 지정합니다. `Exception404`는 404로, 미처 대비하지 못한 나머지 예외는 500으로 바꿔, 어떤 경우에도 낯선 기본 화면이 나가지 않게 막습니다.

응답을 만드는 `Resp.fail`은 챕터 2에서 `Resp.ok`와 함께 준비해 둔 실패용 메서드로, 오류 응답도 `status`·`msg`·`body` 형식을 그대로 지킵니다.

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

*그림 3-6. 서비스에서 던진 예외는 위로 전파되고, @RestControllerAdvice가 이를 가로채 JSON으로 바꿔 응답합니다*

예외가 위로 전파될 때 한 가지가 더 일어납니다. 예외가 난 요청이 데이터를 바꾸는 작업이었다면, 그때까지 바꾼 내용이 데이터베이스에 반영되지 않고 되돌아갑니다. 챕터 2에서 쓰기 메서드에 붙인 `@Transactional`이 정한 범위가 여기서 작동합니다.

메서드가 끝까지 가면 그동안의 변경이 한꺼번에 반영됩니다.

<div class="svg-figure">
<svg viewBox="0 0 420 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="트랜잭션이 시작되고 값이 바뀐 뒤, 기록된 줄이 그대로 남아 데이터베이스에 반영된다.">
  <defs>
    <marker id="c3tx1-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
  </defs>
  <rect x="110" y="16" width="200" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="210" y="48" text-anchor="middle" font-size="14" fill="#0f172a">트랜잭션 시작</text>
  <line x1="210" y1="70" x2="210" y2="90" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#c3tx1-ar)"/>
  <rect x="110" y="94" width="200" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="210" y="126" text-anchor="middle" font-size="14" fill="#0f172a">값 변경</text>
  <line x1="210" y1="148" x2="210" y2="168" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#c3tx1-ar)"/>
  <rect x="110" y="172" width="200" height="106" rx="3" fill="#fff" stroke="#4f46e5" stroke-width="1.9"/>
  <line x1="132" y1="204" x2="288" y2="204" stroke="#475569" stroke-width="2.6"/>
  <line x1="132" y1="228" x2="288" y2="228" stroke="#475569" stroke-width="2.6"/>
  <line x1="132" y1="252" x2="238" y2="252" stroke="#475569" stroke-width="2.6"/>
  <text x="210" y="304" text-anchor="middle" font-size="15" font-weight="800" fill="#3730a3">반영</text>
</svg>
</div>

*그림 3-7. 메서드가 끝까지 가면 그동안의 변경이 데이터베이스에 반영됩니다*

도중에 예외가 나면 반영하지 않고 전부 없던 일로 되돌립니다. 이것을 롤백(rollback)이라고 합니다. 그래서 절반만 바뀐 데이터가 남지 않습니다.

<div class="svg-figure">
<svg viewBox="0 0 420 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="트랜잭션이 시작되고 값이 바뀐 뒤 예외가 나면, 기록된 줄에 굵은 줄이 그어져 그때까지의 변경이 전부 되돌아간다.">
  <defs>
    <marker id="c3tx2-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
  </defs>
  <rect x="110" y="16" width="200" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="210" y="48" text-anchor="middle" font-size="14" fill="#0f172a">트랜잭션 시작</text>
  <line x1="210" y1="70" x2="210" y2="90" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#c3tx2-ar)"/>
  <rect x="110" y="94" width="200" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="210" y="126" text-anchor="middle" font-size="14" fill="#0f172a">값 변경</text>
  <line x1="210" y1="148" x2="210" y2="168" stroke="#94a3b8" stroke-width="1.8" marker-end="url(#c3tx2-ar)"/>
  <rect x="110" y="172" width="200" height="106" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1.9"/>
  <line x1="132" y1="204" x2="288" y2="204" stroke="#cbd5e1" stroke-width="2.6"/>
  <line x1="132" y1="228" x2="288" y2="228" stroke="#cbd5e1" stroke-width="2.6"/>
  <line x1="132" y1="252" x2="238" y2="252" stroke="#cbd5e1" stroke-width="2.6"/>
  <line x1="122" y1="228" x2="298" y2="228" stroke="#ff7849" stroke-width="4.5"/>
  <text x="210" y="304" text-anchor="middle" font-size="15" font-weight="800" fill="#c2410c">되돌림</text>
</svg>
</div>

*그림 3-8. 도중에 예외가 나면 그때까지의 변경이 전부 되돌아갑니다*

지금 다루는 상세 조회는 데이터를 바꾸지 않으므로 되돌릴 것이 없습니다. 예외는 그대로 전파되어 404 응답이 됩니다.

이제 999번 글을 다시 불러 보겠습니다.

```bash [터미널] 없는 글 다시 조회
GET http://localhost:8080/api/boards/999
```

빈 값이 담긴 성공 대신 앞뒤가 맞는 404가 돌아옵니다.

<!-- [CAPTURE NEEDED: 01_404-response
  path: assets/CH3/terminal/01_404-response.png
  desc: GET /api/boards/999 요청에 대한 404 JSON 응답. { "status": 404, "msg": "게시글을 찾을 수 없습니다", "body": null } 형태. Hoppscotch 또는 브라우저 응답 화면. HTTP 상태 코드가 404로 표시되면 좋음.
] -->
![](../assets/CH3/terminal/01_404-response.png)
*그림 3-9. 없는 글을 조회하면 빈 값이 아니라 상태 코드 404를 담은 JSON이 돌아옵니다*

없는 글을 부르면 빈 값이 성공으로 나가던 곳에, 이제 "찾을 수 없다"는 응답이 형식을 갖춰 돌아옵니다. 응답으로 나가는 것도 엔티티가 아니라 DTO에 담긴 값뿐입니다. 두 문제가 모두 해결됐습니다.

오픈이는 목록 API를 받아 간 동료를 다시 불렀습니다. 키보드에서 손을 뗀 사무실이 잠깐 조용해졌습니다.

**오픈이**: "지난번에 없는 번호 넣으면 어떻게 되냐고 물었잖아요. 이제 없으면 없다고 딱 나와요."<br>
**동료**: "아, 3번 불러 볼게요. 없다고 딱 나오네요. 저번엔 성공이라면서 아무것도 없더니."

*여기까진 됐다.*

두 문제는 해결했지만, 오픈이는 화면을 내려다보다 한 가지가 걸렸습니다. 지금은 로그인 화면도, 글 주인을 확인하는 절차도 없습니다. 999번 하나 못 찾는 것은 막아 놨는데, 정작 아무나 남의 글을 고치고 지울 수 있는 서버였습니다.

*없는 글은 걸렀는데, 문은 여전히 다 열려 있잖아.*

다음 챕터에서는 로그인을 붙이고, 본인만 자기 글을 건드리게 합니다.

:::remember
**이것만은 기억하자**

- **엔티티를 응답에 직접 쓰지 않고 DTO에 담아 내보냅니다.** 내부 필드가 바깥으로 나가지 않고, 보여줄 값과 이름을 응답 DTO에서 따로 정할 수 있습니다.
- **없는 값은 `Optional`로 드러내고 `orElseThrow`로 예외를 던집니다.** 커스텀 예외는 `RuntimeException`을 상속해, 던지는 일과 받는 일을 나눕니다. 던져진 예외는 `@RestControllerAdvice`가 한 곳에서 받아 상태 코드에 맞는 JSON으로 바꿉니다.
:::
