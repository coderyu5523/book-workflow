# 챕터 3. 예외 처리와 DTO

게시판의 다섯 기능이 모두 돌아갑니다. 그런데 동료가 화면을 붙이다 던진 질문에는 아직 답하지 못했습니다. 없는 3번 글을 조회하면 빈 값이 성공으로 돌아온다는 것까지는 확인했습니다.

*조회가 이런데, 수정하고 삭제하면?*

없는 999번으로 수정을 걸자 500이 돌아왔고, 삭제도 마찬가지였습니다. 존재하는 1번 글을 부르자 엔티티에 적힌 필드가 그대로 JSON이 되어 나왔습니다. 응답에 담을 값도, 이름도 고를 수 없었습니다.

*없는 글 하나에 답이 두 개네. 응답 모양도 내가 정한 게 아니고.*

오픈이는 선배를 찾아가 화면을 보여줬습니다.

**오픈이**: "선배님, 없는 글 번호로 요청을 보냈는데 에러가 안 나고 성공으로 떨어집니다. 정상 글을 조회하면 엔티티에 있는 필드가 JSON에 그대로 나옵니다."

**선배**: "지금 코드가 글을 찾았을 때와 못 찾았을 때를 구분하지 않아서 그래요. 못 찾으면 빈 값이 그대로 나가니까 조회는 성공이 되고, 수정과 삭제는 빈 값을 건드리다 터집니다. 없다는 걸 코드가 그냥 넘기지 못하게 막고, 내보낼 값도 따로 골라 담아야 합니다."

<div class="svg-figure">
<svg viewBox="0 0 1000 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 2가 남긴 다섯 곳과 챕터 3에서 바꾸는 모습. 엔티티를 그대로 응답에 싣던 것은 응답 DTO에 담아 내보내고, 서비스가 엔티티를 조립하던 것은 요청 DTO가 변환을 맡고, 리포지토리 네 메서드를 직접 적고 없으면 null을 돌려주던 것은 JpaRepository를 상속해 빈 Optional을 돌려주고, 없는 글 조회가 200이고 수정과 삭제가 500이던 것은 Exception404를 던져 404가 되고, 예외를 받을 곳이 없던 것은 한 곳에서 JSON으로 바뀐다.">
  <defs>
    <marker id="c3ov-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="28" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 3 한눈에 보기 - 챕터 2 코드에서 고칠 다섯 곳</text>
  <text x="285" y="58" text-anchor="middle" font-size="12" font-weight="700" fill="#c2410c">챕터 2가 남긴 것</text>
  <text x="750" y="58" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">챕터 3에서 바꾸는 것</text>

  <rect x="120" y="70" width="330" height="54" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="285" y="94" text-anchor="middle" font-size="12" fill="#0f172a">엔티티를 그대로 응답에 싣는다</text>
  <text x="285" y="113" text-anchor="middle" font-size="11" fill="#6b7280">응답 모양을 엔티티가 정한다</text>
  <line x1="456" y1="97" x2="536" y2="97" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <rect x="542" y="70" width="330" height="54" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="707" y="102" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">응답 DTO에 담아 내보낸다</text>

  <rect x="120" y="138" width="330" height="54" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="285" y="170" text-anchor="middle" font-size="12" fill="#0f172a">서비스가 엔티티를 조립한다</text>
  <line x1="456" y1="165" x2="536" y2="165" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <rect x="542" y="138" width="330" height="54" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="707" y="170" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">요청 DTO가 변환을 맡는다</text>

  <rect x="120" y="206" width="330" height="54" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="285" y="230" text-anchor="middle" font-size="12" fill="#0f172a">리포지토리 네 메서드를 직접 적는다</text>
  <text x="285" y="249" text-anchor="middle" font-size="11" fill="#6b7280">못 찾으면 null이 돌아온다</text>
  <line x1="456" y1="233" x2="536" y2="233" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <rect x="542" y="206" width="330" height="54" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="707" y="230" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">JpaRepository를 상속한다</text>
  <text x="707" y="249" text-anchor="middle" font-size="11" fill="#3730a3">못 찾으면 빈 Optional이 돌아온다</text>

  <rect x="120" y="274" width="330" height="54" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="285" y="298" text-anchor="middle" font-size="12" fill="#0f172a">없는 글 조회는 200으로 나간다</text>
  <text x="285" y="317" text-anchor="middle" font-size="11" fill="#6b7280">수정과 삭제는 500이 난다</text>
  <line x1="456" y1="301" x2="536" y2="301" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <rect x="542" y="274" width="330" height="54" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="707" y="306" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">Exception404를 던진다</text>

  <rect x="120" y="342" width="330" height="54" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="285" y="374" text-anchor="middle" font-size="12" fill="#0f172a">던진 예외를 받을 곳이 없다</text>
  <line x1="456" y1="369" x2="536" y2="369" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ov-i)"/>
  <rect x="542" y="342" width="330" height="54" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="707" y="366" text-anchor="middle" font-size="12" font-weight="800" fill="#3730a3">한 곳에서 404 JSON으로 바꾼다</text>
  <text x="707" y="385" text-anchor="middle" font-size="11" fill="#3730a3">status · msg · body 형식을 지킨다</text>
</svg>
</div>

*그림 3-1. 챕터 2가 남긴 다섯 곳을 이번 챕터에서 차례로 고칩니다*

:::goal
**이번 챕터가 끝나면**

- 엔티티를 응답에 직접 쓰지 않고 DTO로 감싸는 이유를 설명할 수 있습니다
- `JpaRepository`로 바꾸면 없는 데이터가 왜 `Optional`로 돌아오는지 이해합니다
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

## 3.1 응답 DTO

### 3.1.1 DTO가 필요한 이유

챕터 2의 컨트롤러는 `Board` 엔티티를 그대로 돌려주고, `@RestController`가 이를 JSON으로 바꿉니다. 그래서 엔티티에 선언한 필드가 곧 응답 JSON입니다.

응답으로 내보낼 값만 담는 클래스를 따로 만들면, 컨트롤러는 엔티티 대신 이 클래스를 돌려줍니다. 챕터 2에서 요청을 받을 때 쓴 DTO를, 이번에는 응답을 내보낼 때도 사용합니다.

<div class="svg-figure">
<svg viewBox="0 0 900 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="엔티티와 DTO 경계. 왼쪽 내부에는 id, title, content, createdAt을 테이블 그대로 담은 Board 엔티티가 있고, 가운데 벽의 창구에는 'DTO만 통과' 표지가 붙어 있다. 창구를 지나 오른쪽 응답으로 나온 것은 boardId, title, content 세 줄만 담은 작은 DTO로, createdAt은 빠지고 id는 boardId로 이름이 바뀌었다.">
  <defs>
    <marker id="c3dto-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="175" y="30" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">내부</text>
  <text x="661" y="30" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">응답 (바깥)</text>
  <rect x="40" y="46" width="270" height="256" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="175" y="78" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">Board 엔티티</text>
  <text x="175" y="118" text-anchor="middle" font-size="12" fill="#334155">id : 1</text>
  <text x="175" y="146" text-anchor="middle" font-size="12" fill="#334155">title : 제목</text>
  <text x="175" y="174" text-anchor="middle" font-size="12" fill="#334155">content : 내용</text>
  <text x="175" y="202" text-anchor="middle" font-size="12" fill="#334155">createdAt : 작성시각</text>
  <text x="175" y="250" text-anchor="middle" font-size="11" fill="#6b7280">테이블에 있는 그대로입니다</text>
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

### 3.1.2 응답 DTO 만들기

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

엔티티를 받는 생성자를 두었으므로 서비스에서 `new BoardResponse.DTO(board)` 한 줄로 변환합니다. 응답 필드 이름이 `id`가 아니라 `boardId`인 것처럼, 바깥에 나가는 이름은 응답 DTO에서 따로 정합니다.

## 3.2 요청 DTO와 엔티티 변환

데이터베이스에 저장되려면 영속성 컨텍스트가 관리하는 객체, 곧 엔티티여야 합니다. `SaveDTO`는 값을 담아 나르는 일반 객체라 영속 상태가 되지 못하므로, DTO 안에 엔티티로 바꾸는 `toEntity()`를 둡니다.

변환은 `Board`를 새로 만드는 일이라, 엔티티에 값을 받는 생성자가 먼저 필요합니다. `board/Board.java`에 생성자를 추가하고 `@Builder`를 붙입니다.

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

명시 생성자를 만들면 자바가 자동으로 주던 기본 생성자가 사라지는데, JPA 엔티티는 기본 생성자가 있어야 하므로 `@NoArgsConstructor`도 함께 붙입니다.

:::tip
**빌더 패턴은 값을 채운 뒤 마지막에 객체를 받습니다**

빌더 패턴(Builder Pattern)은 생성자로 객체를 한 번에 만들지 않고, 값을 모아 두는 빌더를 거쳐 만드는 방식입니다. 빌더에 필요한 값을 하나씩 채운 다음 `build()`를 호출하면 완성된 객체가 돌아옵니다.

`Board.builder().title("제목").content("내용").build()`처럼 필드 이름을 적어 값을 넘기므로, 생성자처럼 인자를 선언 순서대로 맞출 필요가 없고 넣지 않을 값은 생략합니다. 롬복의 `@Builder`는 생성자를 보고 이 빌더를 컴파일 시점에 만들어 줍니다.
:::

`board/BoardRequest.java`의 `SaveDTO`에 엔티티로 바꾸는 메서드를 추가합니다.

```java [참고] board/BoardRequest.java. 요청 DTO에 toEntity 추가
    public record SaveDTO(String title, String content) {
        // 빌더로 요청 값을 엔티티에 옮겨 담는다
        public Board toEntity() {
            return Board.builder().title(title()).content(content()).build();
        }
    }
```

## 3.3 JpaRepository로 바꾸기

없는 글을 조회했는데 성공이 돌아온 것은 챕터 2의 조회 코드 때문입니다. `findById`가 `null`을 돌려주면 서비스와 컨트롤러는 그대로 넘겨 200으로 내보냅니다.

이 문제를 해결하기 위해 `JpaRepository`를 사용합니다. `JpaRepository`는 조회 결과를 `Optional`에 담아 돌려주므로, 값이 없을 때 예외를 던져 처리할 수 있습니다.

`board/BoardRepository.java`를 열고 아래 코드로 바꿉니다.

```java [실습 1] board/BoardRepository.java. JpaRepository 상속
public interface BoardRepository extends JpaRepository<Board, Integer> {
}
```

리포지토리는 클래스가 아니라 인터페이스로 선언합니다. `JpaRepository<Board, Integer>`의 두 자리에는 다룰 엔티티와 기본 키의 타입을 적고, `@Repository`도 `EntityManager` 주입도 하지 않습니다.

챕터 2에서 손으로 만든 메서드가 어디로 갔는지 보면 이렇습니다.

| 챕터 2에서 만든 것 | 지금 | 비고 |
|---|---|---|
| `findById(int)` | 상속 | 반환 타입이 `Optional<Board>`입니다 |
| `findAll()` | 상속 | JPQL을 쓰지 않습니다 |
| `save(Board)` | 상속 | 저장된 엔티티를 돌려줍니다 |
| `delete(Board)` | 상속 | 그대로입니다 |
| (수정 메서드 없음) | 그대로 | 더티체킹으로 처리합니다 |

회원이든 댓글이든 기본 키로 찾고, 전체를 가져오고, 저장하고, 지우는 일은 똑같아서, 스프링이 구현을 대신 만듭니다.

`EntityManager`가 사라진 것은 아닙니다. `JpaRepository` 구현체가 안에서 그대로 쓰므로, 챕터 2에서 본 영속성 컨텍스트와 캐싱, 쓰기 지연, 더티체킹도 그대로 동작합니다.

## 3.4 없음을 예외로

앞에서 바꾼 리포지토리는 조회 결과를 `Optional<Board>`에 담아 돌려줍니다.

```java
Optional<Board> board = boardRepository.findById(1);
```

`Optional`은 값이 있을 수도, 없을 수도 있음을 상자에 담아 드러내는 자바 문법입니다. 이 값을 받은 코드는 타입만 보고도 "빈 상자일 수 있다"는 걸 압니다.

### 3.4.1 상자를 여는 세 가지 방법

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

`get()`이 던지는 `NoSuchElementException`에는 없는 글을 조회했다는 상황이 담기지 않아, 404인지 500인지 가릴 근거가 없습니다. `orElse`는 빈 목록을 주는 자리에는 맞지만 없는 글에 가짜 글을 대신 줄 수는 없습니다. 남는 것이 `orElseThrow`입니다. 상황에 맞는 예외를 직접 골라 던질 수 있습니다.

### 3.4.2 커스텀 예외와 상태 코드

`orElseThrow`가 던지는 `Exception404`를 만듭니다. `core/handler/ex/Exception404.java`를 열고 아래 코드를 작성합니다.

```java [실습 3] core/handler/ex/Exception404.java. 커스텀 예외
// 자원을 찾을 수 없을 때 (HTTP 404)
public class Exception404 extends RuntimeException {
    public Exception404(String message) {
        super(message);
    }
}
```

상황에 맞게 직접 정의한 예외를 커스텀 예외라고 합니다. `RuntimeException`은 컴파일러가 처리를 강제하지 않는 Unchecked 예외라, 서비스는 던지기만 하고 받는 일은 뒤에서 한 곳에 몰아 처리할 수 있습니다.

404는 HTTP 상태 코드입니다. 응답이 어떤 상황인지 세 자리 숫자로 알리는 약속으로, 자주 쓰는 것은 다음과 같습니다.

| 상태 코드 | 뜻 | 예 |
|-----------|-----|-----|
| 400 | 요청이 잘못됨 | 제목 없이 글 작성 |
| 401 | 인증되지 않음 | 로그인 없이 접근 |
| 403 | 권한이 없음 | 남의 글 수정 |
| 404 | 자원이 없음 | 없는 글 조회 |
| 500 | 서버 내부 오류 | 처리하지 못한 예외 |

없는 글을 부른 상황은 404에 해당합니다. 200으로 답하면 없는 글을 있는 것처럼 다루게 되고, 500은 서버가 넘어졌다는 뜻이라 맞지 않습니다. 상태 코드마다 `Exception400`, `Exception401`처럼 짝이 되는 커스텀 예외를 두는 것이 흔한 방식이지만, 이번 챕터는 없는 글만 다루므로 `Exception404` 하나만 만듭니다.

### 3.4.3 없는 글을 예외로

`board/BoardService.java`의 `게시글상세`를 `orElseThrow`로 고칩니다.

```java [설명] board/BoardService.java. 없으면 예외, 반환은 DTO
    // 없으면 Exception404를 던지고, 있으면 DetailDTO에 담아 반환한다
    public BoardResponse.DetailDTO 게시글상세(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board);
    }
```

목록은 여러 건을 각각 `DTO`로 바꿔 리스트로 돌려줍니다.

```java [설명] board/BoardService.java. 목록은 DTO 리스트로 반환
    // 엔티티 리스트를 DTO 리스트로 바꾼다
    public List<BoardResponse.DTO> 게시글목록() {
        return boardRepository.findAll().stream()
                .map(BoardResponse.DTO::new)
                .toList();
    }
```

`BoardResponse.DTO::new`는 `board -> new BoardResponse.DTO(board)`를 줄여 쓴 것입니다.

수정과 삭제는 상세와 같은 식으로, 없는 글이면 `Exception404`를 던집니다.

컨트롤러는 받는 타입만 바뀝니다.

| 엔드포인트 | 받는 타입(전) | 받는 타입(후) |
|-----------|--------------|--------------|
| `GET /api/boards` | `List<Board>` | `List<BoardResponse.DTO>` |
| `GET /api/boards/{boardId}` | `Board` | `BoardResponse.DetailDTO` |

주소와 HTTP 메서드는 챕터 2와 같습니다. 상세를 부르면 DTO에 담긴 세 값만 나갑니다.

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

값을 옮겨 담는 자리는 이제 셋입니다. 들어오는 값은 요청 DTO에 담겨 엔티티로 옮겨지고, 나가는 값은 엔티티에서 응답 DTO로 옮겨집니다. 엔티티는 서비스와 리포지토리 사이를 벗어나지 않습니다.

남은 것은 던져진 예외를 404 응답으로 바꾸는 일입니다.

## 3.5 전역 예외 처리

던져진 `Exception404`는 어딘가에서 받아 404 JSON으로 바꿔야 합니다. 컨트롤러마다 `try-catch`로 잡으면 같은 코드가 모든 컨트롤러에 흩어집니다.

스프링은 컨트롤러 어디에서 예외가 던져지든 한 자리에서 받아 응답으로 바꾸는 장치를 줍니다. `@RestControllerAdvice`입니다.

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

*그림 3-4. 서비스에서 던진 예외는 위로 전파되고, @RestControllerAdvice가 이를 가로채 JSON으로 바꿔 응답합니다*

이제 없는 999번을 조회해 보겠습니다.

```bash [터미널] 없는 글 다시 조회
GET http://localhost:8080/api/boards/999
```

빈 값이 담긴 성공 대신 앞뒤가 맞는 404가 돌아옵니다.

<!-- [CAPTURE NEEDED: 01_404-response
  path: assets/CH3/terminal/01_404-response.png
  desc: GET /api/boards/999 요청에 대한 404 JSON 응답. { "status": 404, "msg": "게시글을 찾을 수 없습니다", "body": null } 형태. Hoppscotch 또는 브라우저 응답 화면. HTTP 상태 코드가 404로 표시되면 좋음.
] -->
![](../assets/CH3/terminal/01_404-response.png)
*그림 3-5. 없는 글을 조회하면 빈 값이 아니라 상태 코드 404를 담은 JSON이 돌아옵니다*

응답으로 나가는 것도 엔티티가 아니라 DTO에 담긴 값뿐입니다. 챕터 2가 남긴 다섯 곳이 모두 정리됐습니다.

오픈이는 목록 API를 받아 간 동료를 다시 불렀습니다. 키보드에서 손을 뗀 사무실이 잠깐 조용해졌습니다.

**오픈이**: "지난번에 없는 번호 넣으면 어떻게 되냐고 물었잖아요. 이제 없으면 없다고 딱 나와요."<br>
**동료**: "아, 3번 불러 볼게요. 없다고 딱 나오네요. 저번엔 성공이라면서 아무것도 없더니."

*여기까진 됐다.*

다섯 곳을 정리했지만, 오픈이는 화면을 내려다보다 한 가지가 걸렸습니다. 지금은 로그인 화면도, 글 주인을 확인하는 절차도 없습니다. 999번 하나 못 찾는 것은 막아 놨는데, 정작 아무나 남의 글을 고치고 지울 수 있는 서버였습니다.

*없는 글은 걸렀는데, 문은 여전히 다 열려 있잖아.*

다음 챕터에서는 로그인을 붙이고, 본인만 자기 글을 건드리게 합니다.

:::remember
**이것만은 기억하자**

- **엔티티를 응답에 직접 쓰지 않고 DTO에 담아 내보냅니다.** 응답에 나갈 값과 이름을 엔티티가 아니라 응답 DTO에서 정합니다.
- **없는 값은 `Optional`로 드러내고 `orElseThrow`로 예외를 던집니다.** 커스텀 예외는 `RuntimeException`을 상속해, 던지는 일과 받는 일을 나눕니다. 던져진 예외는 `@RestControllerAdvice`가 한 곳에서 받아 상태 코드에 맞는 JSON으로 바꿉니다.
:::
