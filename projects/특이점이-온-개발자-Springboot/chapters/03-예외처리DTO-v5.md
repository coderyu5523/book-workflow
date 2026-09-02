# 챕터 3. 예외 처리와 DTO

게시판의 기본 기능이 완료되었습니다. 오픈이는 뿌듯한 마음으로 선배에게 화면을 보여줬습니다.

선배는 목록과 상세 조회를 한 번씩 눌러보더니, 주소창 끝에 있는 게시글 번호를 슬쩍 '999'로 바꿨습니다.

**선배**: "없는 번호예요. 이런 예외 상황도 테스트해 봤어요?"

엔터를 치자 응답 창에는 여전히 '200 성공'이 떴습니다. 하지만 응답 바디는 비어 있었습니다.

*게시글이 없는 번호인데 왜 응답이 성공으로 나오지?*

**선배**: "데이터베이스에서 게시글을 못 찾으면 빈 값으로 응답이 오는데, 이 빈 값을 그대로 응답에 담아버리니 성공으로 응답이 뜨는 거에요. 만약 없는 게시글을 수정이나 삭제하려고 한다면 오류가 발생하겠죠. 서버에서는 이런 예외(Exception)가 발생했을 경우를 위해 미리 예외 처리를 해야 해요. 그래야 어떤 사유로 요청이 실패했는지 클라이언트에게 명확히 알려줄 수 있어요."

<div class="svg-figure">
<svg viewBox="0 0 1000 296" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="예외가 발생하면 어디서 받는가. 요청은 클라이언트에서 디스패처 서블릿, 컨트롤러, 서비스를 거쳐 리포지토리로 간다. 서비스에서 예외가 발생하면 컨트롤러도 잡지 않아 디스패처 서블릿까지 전달된다. 디스패처 서블릿은 예외 처리를 전역 예외 처리기에 맡기고, RestControllerAdvice가 붙은 전역 예외 처리기가 예외를 JSON 응답으로 바꿔 클라이언트에게 돌려준다.">
  <defs>
    <marker id="c3f-g" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="c3f-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="c3f-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <text x="500" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 3 한눈에 보기 - 예외가 발생하면 어디서 받는가</text>
  <rect x="20" y="62" width="115" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="77" y="98" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">클라이언트</text>
  <line x1="135" y1="92" x2="198" y2="92" stroke="#475569" stroke-width="1.7" marker-end="url(#c3f-g)"/>
  <text x="166" y="82" text-anchor="middle" font-size="11" font-weight="600" fill="#475569">요청</text>
  <rect x="200" y="62" width="165" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="282" y="98" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">디스패처 서블릿</text>
  <line x1="365" y1="92" x2="428" y2="92" stroke="#475569" stroke-width="1.7" marker-end="url(#c3f-g)"/>
  <rect x="430" y="62" width="145" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="502" y="98" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">컨트롤러</text>
  <line x1="575" y1="92" x2="638" y2="92" stroke="#475569" stroke-width="1.7" marker-end="url(#c3f-g)"/>
  <rect x="640" y="62" width="145" height="60" rx="8" fill="#fff7ed" stroke="#ff7849" stroke-width="1.9"/>
  <text x="712" y="98" text-anchor="middle" font-size="13" font-weight="800" fill="#c2410c">서비스</text>
  <line x1="785" y1="92" x2="848" y2="92" stroke="#475569" stroke-width="1.7" marker-end="url(#c3f-g)"/>
  <rect x="850" y="62" width="135" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="917" y="98" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">리포지토리</text>
  <path d="M712,122 V168 H300 V126" fill="none" stroke="#ff7849" stroke-width="1.9" marker-end="url(#c3f-s)"/>
  <text x="724" y="146" font-size="12" font-weight="700" fill="#c2410c">예외 발생</text>
  <line x1="240" y1="122" x2="240" y2="202" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3f-i)"/>
  <text x="232" y="168" text-anchor="end" font-size="11.5" font-weight="600" fill="#4f46e5">예외 처리를 맡긴다</text>
  <path d="M110,238 H77 V126" fill="none" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3f-i)"/>
  <text x="88" y="186" font-size="11.5" font-weight="600" fill="#4f46e5">응답</text>
  <rect x="110" y="204" width="330" height="68" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="275" y="230" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">전역 예외 처리기</text>
  <text x="275" y="251" text-anchor="middle" font-family="Consolas, 'D2Coding', monospace" font-size="11.5" fill="#3730a3">@RestControllerAdvice</text>
</svg>
</div>

*그림 3-1. 챕터 3의 실습 흐름*

:::goal
**이번 챕터가 끝나면**

- **DTO**로 엔티티를 그대로 내보내지 않고 요청과 응답 전용 클래스를 만들 수 있습니다
- **JpaRepository**로 기본 조회, 저장, 삭제 메서드를 물려받고 결과를 **Optional**로 받을 수 있습니다
- **커스텀 예외**와 **전역 예외 처리**로 실패 상황을 상태 코드에 맞는 JSON 응답으로 바꿀 수 있습니다
:::

::::prep
**소스코드 준비**

소스코드 준비에서 클론한 예제 저장소에서 이번 챕터 폴더로 이동합니다. 패키지 루트는 챕터 2와 같은 `com.metacoding.spring`입니다.

```bash [터미널] 챕터 3 폴더로 이동
cd spring-start/ch03
```

이번 챕터에서 새로 만들거나 고치는 파일은 다음과 같습니다. 나머지는 챕터 2 그대로입니다.

```text ch03 파일 구조
spring-start/ch03/src/main/java/com/metacoding/spring/
├── board/
│   ├── Board.java                    # [작성] @Builder + 생성자 추가
│   ├── BoardController.java          # [작성] 요청·응답 타입 DTO로 교체
│   ├── BoardRequest.java             # [작성] 요청 DTO(SaveDTO/UpdateDTO) + toEntity()
│   ├── BoardRepository.java          # [작성] JpaRepository 인터페이스로 전환
│   ├── BoardResponse.java            # [작성] 응답 DTO(DTO/DetailDTO)
│   └── BoardService.java             # [작성] orElseThrow + DTO 반환
└── core/handler/
    ├── ex/Exception400,401,403,404,500.java   # [작성] 커스텀 예외
    └── GlobalExceptionHandler.java        # [작성] 전역 예외 처리
```

챕터를 따라 코드를 채우고, 막히면 `spring-end`의 완성 코드를 참고하세요.
::::

## 3.1 요청 DTO

챕터 2의 컨트롤러는 요청을 **Board** 엔티티로 직접 받고, 응답할 때도 엔티티를 그대로 반환합니다. 하지만 실무에서는 엔티티를 요청이나 응답에 직접 사용하지 않습니다. 엔티티는 데이터베이스의 테이블 구조와 동일해서, 그대로 사용할 경우 응답에 불필요한 데이터가 노출되거나 테이블 구조가 변경될 때 예상치 못한 오류가 발생할 수 있기 때문입니다. 따라서 클라이언트와 주고받을 때는 필요한 데이터만 담아서 전달할 전용 객체를 사용해야 합니다.

### 3.1.1 DTO

계층 사이에서 데이터 전달만을 목적으로 하는 객체를 **DTO(Data Transfer Object)** 라고 합니다. 컨트롤러와 서비스처럼 서로 다른 계층 사이에서 필요한 값만 담아 전달합니다. DTO를 사용하면 요청 받을 값과 응답을 보낼 값을 필요한 형태로 정할 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="왼쪽 Board 엔티티는 id, title, content, createdAt 네 값을 담고 있고, 오른쪽 DTO는 boardId, title, content 세 값만 담고 있다. 화살표가 왼쪽에서 오른쪽으로 이어지며 필요한 값만 담는다고 적혀 있다.">
  <defs>
    <marker id="c3dto-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <rect x="40" y="36" width="260" height="148" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="170" y="64" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">Board 엔티티</text>
  <text x="170" y="96" text-anchor="middle" font-size="12" fill="#334155">id : 1</text>
  <text x="170" y="120" text-anchor="middle" font-size="12" fill="#334155">title : 제목</text>
  <text x="170" y="144" text-anchor="middle" font-size="12" fill="#334155">content : 내용</text>
  <text x="170" y="168" text-anchor="middle" font-size="12" fill="#334155">createdAt : 작성시각</text>
  <line x1="304" y1="110" x2="452" y2="110" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3dto-a)"/>
  <text x="378" y="100" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">필요한 값만 담는다</text>
  <rect x="460" y="49" width="260" height="122" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.6"/>
  <text x="590" y="77" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">DTO</text>
  <text x="590" y="109" text-anchor="middle" font-size="12" fill="#334155">boardId : 1</text>
  <text x="590" y="133" text-anchor="middle" font-size="12" fill="#334155">title : 제목</text>
  <text x="590" y="157" text-anchor="middle" font-size="12" fill="#334155">content : 내용</text>
</svg>
</div>

*그림 3-2. 엔티티와 DTO가 담는 값*

### 3.1.2 엔티티 생성자

JPA는 엔티티만 데이터베이스에 저장할 수 있습니다. 따라서 요청으로 받은 DTO를 데이터베이스에 저장하려면 먼저 엔티티로 변환하는 과정이 필요합니다. 이를 처리할 수 있도록 **Board** 클래스에 생성자를 추가합니다.

```java [실습 1] board/Board.java. 빌더로 생성할 수 있게
@NoArgsConstructor // 기본 생성자 추가
@Data
@Entity
@Table(name = "board_tb")
public class Board {
    // id, title, content, createdAt 필드 (챕터 2와 같음)

    @Builder // 객체 생성 용도
    public Board(Integer id, String title, String content, LocalDateTime createdAt) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.createdAt = createdAt;
    }
}
```

새로운 생성자를 직접 추가하면 자바가 기본으로 제공하던 기본 생성자가 사라집니다. 하지만 JPA 엔티티는 기본 생성자가 반드시 있어야 하므로, **@NoArgsConstructor** 어노테이션을 함께 붙여줍니다.

:::tip
**빌더 패턴(Builder Pattern)이란?**

객체를 생성할 때 순서에 의존하지 않고, 어떤 필드에 어떤 값이 들어가는지 명시적으로 지정하는 패턴입니다. **@Builder**를 사용하면 복잡한 매개변수 순서를 외울 필요 없이, 내가 원하는 필드의 값을 채워 넣을 수 있습니다.
:::

### 3.1.3 요청 DTO 만들기

요청 DTO는 클라이언트가 전송한 데이터를 담는 클래스입니다. 클라이언트가 데이터를 보내면, 스프링이 요청 바디에 담긴 값들을 이름이 일치하는 DTO 필드에 자동으로 채워줍니다. 덕분에 컨트롤러는 복잡한 변환 과정 없이 이 DTO를 매개변수로 받아 바로 사용할 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 800 172" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="요청 데이터와 DTO. 클라이언트가 제목과 내용을 application/json 타입으로 보내면, 그 값이 DTO의 title과 content로 자동 매핑되고, 컨트롤러가 이 DTO를 받는다.">
  <defs>
    <marker id="c3dto-a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#475569"/></marker>
  </defs>
  <text x="107" y="26" text-anchor="middle" font-size="15.3" font-weight="800" fill="#0f172a">클라이언트</text>
  <text x="432" y="26" text-anchor="middle" font-size="15.3" font-weight="800" fill="#3730a3">DTO</text>
  <text x="703" y="26" text-anchor="middle" font-size="15.3" font-weight="800" fill="#0f172a">컨트롤러</text>
  <rect x="14" y="40" width="185" height="96" rx="9" fill="#fff" stroke="#475569" stroke-width="1.5"/>
  <rect x="339" y="40" width="185" height="96" rx="9" fill="#f8fafc" stroke="#4f46e5" stroke-width="1.6"/>
  <rect x="619" y="40" width="167" height="96" rx="9" fill="#fff" stroke="#475569" stroke-width="1.5"/>
  <text x="107" y="80" text-anchor="middle" font-size="13.3" fill="#334155">title : 제목3</text>
  <text x="107" y="104" text-anchor="middle" font-size="13.3" fill="#334155">content : 내용3</text>
  <rect x="355" y="62" width="153" height="54" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.5"/>
  <text x="432" y="83" text-anchor="middle" font-size="13.3" fill="#3730a3">title : 제목3</text>
  <text x="432" y="105" text-anchor="middle" font-size="13.3" fill="#3730a3">content : 내용3</text>
  <text x="703" y="94" text-anchor="middle" font-size="13.3" fill="#334155">POST /api/boards</text>
  <line x1="199" y1="88" x2="337" y2="88" stroke="#475569" stroke-width="1.5" marker-end="url(#c3dto-a)"/>
  <text x="268" y="78" text-anchor="middle" font-size="12.7" fill="#475569">1. 요청</text>
  <text x="268" y="108" text-anchor="middle" font-size="12.1" fill="#475569">application/json 타입</text>
  <text x="432" y="158" text-anchor="middle" font-size="12.7" fill="#64748b">2. 자동 매핑</text>
  <line x1="524" y1="88" x2="617" y2="88" stroke="#475569" stroke-width="1.5" marker-end="url(#c3dto-a)"/>
  <text x="570" y="78" text-anchor="middle" font-size="12.7" fill="#475569">3. 전달</text>
</svg>
</div>

*그림 3-3. 요청 데이터와 DTO*

데이터베이스에 저장되려면 영속성 컨텍스트가 관리하는 엔티티여야 합니다. **SaveDTO**는 값만 담은 일반 객체라 영속 상태가 되지 못하므로, DTO 안에 엔티티로 바꾸는 `toEntity()`를 둡니다.

`board/BoardRequest.java`를 열어 아래와 같이 작성합니다.

```java [실습 2] board/BoardRequest.java. 요청 DTO와 엔티티 변환
public class BoardRequest {
    public record SaveDTO(String title, String content) {

        // DTO를 엔티티로 변환한다
        public Board toEntity() {
            return Board.builder()
                    .title(title)
                    .content(content)
                    .build();
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
```

`record`는 데이터 전달을 목적으로 하는 특수 클래스입니다. 필드만 선언하면 생성자와 getter 같은 메서드를 자동으로 만들어 줍니다.

## 3.2 응답 DTO

응답으로 내보낼 값만 담는 클래스를 만듭니다.

`board/BoardResponse.java`를 열어 아래와 같이 작성합니다.

```java [실습 3] board/BoardResponse.java. 응답 DTO
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

엔티티를 받는 생성자를 두었으므로 서비스에서 `new BoardResponse.DTO(board)` 한 줄로 변환합니다. 응답 필드 이름이 `id`가 아니라 `boardId`인 것처럼, 응답에 담길 이름은 응답 DTO에서 따로 지정합니다.

## 3.3 JpaRepository 적용

없는 게시글을 조회해도 예외가 발생하지 않아 서버는 정상 응답을 내보냅니다.

이 결과를 예외로 바꾸려면 조회가 무엇을 반환하는지부터 달라져야 합니다. 그래서 **JpaRepository**로 바꿉니다. **JpaRepository**는 Spring Data JPA가 제공하는 리포지토리 인터페이스입니다. 이 인터페이스를 상속하면 기본 조회·저장·삭제 메서드를 그대로 사용할 수 있고, **Optional** 타입을 통해 예외 처리를 할 수 있습니다.

`board/BoardRepository.java`를 열어 아래와 같이 변경합니다.

```java [실습 4] board/BoardRepository.java. JpaRepository 상속
public interface BoardRepository extends JpaRepository<Board, Integer> {
}
```

리포지토리는 클래스가 아니라 인터페이스로 선언합니다. `JpaRepository<Board, Integer>`의 꺾쇠 안에는 다룰 엔티티와 기본 키의 타입을 차례로 적습니다.

챕터 2에서 **EntityManager**를 주입받아 직접 작성한 네 메서드와 클래스 본문은 모두 지웁니다. 조회·저장·삭제는 **JpaRepository**가 이미 갖고 있어 다시 만들 필요가 없습니다. 챕터 2에서 익힌 JPQL도 사라지는 것은 아닙니다. 기본 메서드로 표현할 수 없는 조회가 필요해지면 그때 다시 작성하며, 다음 챕터에서 작성자를 함께 가져오는 조회에 사용합니다.

상속만 해 두면 아래 메서드를 호출할 수 있습니다.

| 메서드 | 하는 일 |
|---|---|
| `save(엔티티)` | 저장하고 저장된 엔티티를 반환합니다 |
| `findById(기본 키)` | 기본 키로 한 건을 조회해 **Optional**에 담아 반환합니다 |
| `findAll()` | 전체를 **List**로 반환합니다 |
| `delete(엔티티)` | 삭제합니다 |
| `findBy필드명(값)` | 직접 선언합니다. `findBy` 뒤 필드 이름을 보고 select 문이 생성됩니다 |

## 3.4 예외 처리 추가

**Optional**은 값이 존재할 수도, 존재하지 않을 수도 있는 상태를 감싸는 **래퍼(Wrapper)** 클래스로, 주로 null로 인한 에러를 방지하기 위해 사용됩니다. 내부에 담긴 값을 꺼낼 때는 `orElseThrow()` 메서드를 사용합니다. 이 메서드는 값이 존재하면 해당 값을 그대로 반환하고, 비어있을 경우 인자로 전달한 지정된 예외를 발생시킵니다.

### 3.4.1 커스텀 예외 만들기

예외 처리에 사용할 **Exception404**를 정의합니다.

`core/handler/ex/Exception404.java`를 열어 아래와 같이 작성합니다.

```java [실습 5] core/handler/ex/Exception404.java. 커스텀 예외
public class Exception404 extends RuntimeException {
    public Exception404(String message) {
        super(message);
    }
}
```

상황에 맞게 직접 정의한 예외를 커스텀 예외라고 합니다. **RuntimeException**을 상속하면 이 예외를 사용하는 곳마다 `try-catch`를 적지 않아도 됩니다.

같은 폴더의 **Exception400**, **Exception401**, **Exception403**, **Exception500**도 상태 코드만 다를 뿐 형태가 동일합니다. 회원가입과 로그인, 권한을 다루는 다음 챕터에서 사용하므로 미리 준비해 둡니다.

404는 HTTP 상태 코드입니다. 응답이 어떤 상황인지 세 자리 숫자로 알리는 약속입니다. 이 책에서 사용하는 것은 다음과 같습니다.

| 상태 코드 | 뜻 | 예 |
|---|---|---|
| 400 | 요청이 잘못됨 | 이미 쓰는 유저네임으로 가입 |
| 401 | 인증되지 않음 | 로그인 없이 접근 |
| 403 | 권한이 없음 | 작성자가 아닌 사람의 게시글 수정 |
| 404 | 자원이 없음 | 없는 게시글 조회 |
| 500 | 서버 내부 오류 | 처리하지 못한 예외 |

### 3.4.2 전역 예외 처리

다음으로 예외가 발생했을 때 처리할 핸들러를 구현해 보겠습니다. **@RestControllerAdvice** 어노테이션이 지정된 클래스는 각 컨트롤러에서 요청을 처리하는 도중 발생하는 예외를 전역적(Global)으로 가로채어 한 곳에서 일괄 처리하는 역할을 합니다. 컨트롤러와 서비스는 예외를 발생시키기만 하고, 응답으로 바꾸는 일은 이 클래스가 담당합니다.

`core/handler/GlobalExceptionHandler.java`를 열어 아래와 같이 작성합니다.

```java [실습 6] core/handler/GlobalExceptionHandler.java. 전역 예외 처리
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 1. 커스텀 예외는 저마다의 상태 코드로 바꾼다
    @ExceptionHandler(Exception400.class)
    public ResponseEntity<?> exApi400(Exception400 e) {
        return Resp.fail(HttpStatus.BAD_REQUEST, e.getMessage());
    }

    @ExceptionHandler(Exception401.class)
    public ResponseEntity<?> exApi401(Exception401 e) {
        return Resp.fail(HttpStatus.UNAUTHORIZED, e.getMessage());
    }

    @ExceptionHandler(Exception403.class)
    public ResponseEntity<?> exApi403(Exception403 e) {
        return Resp.fail(HttpStatus.FORBIDDEN, e.getMessage());
    }

    @ExceptionHandler(Exception404.class)
    public ResponseEntity<?> exApi404(Exception404 e) {
        return Resp.fail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Exception500.class)
    public ResponseEntity<?> exApi500(Exception500 e) {
        return Resp.fail(HttpStatus.INTERNAL_SERVER_ERROR, e.getMessage());
    }

    // 2. 나머지 모든 예외는 500으로 처리한다
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> exUnKnown(Exception e) {
        return Resp.fail(HttpStatus.INTERNAL_SERVER_ERROR, "서버 오류가 발생했습니다");
    }
}
```

**@ExceptionHandler**는 메서드마다 어떤 예외를 맡을지 지정합니다. 커스텀 예외 넷은 저마다 400·401·403·404 응답이 되고, 그 밖의 예외는 모두 500 응답이 됩니다.

<div class="svg-figure">
<svg viewBox="0 0 980 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="서비스에서 발생한 Exception404가 위로 전파되어 RestControllerAdvice가 가로채고, 상태 코드 404를 담은 JSON으로 바뀌어 응답된다.">
  <defs>
    <marker id="c3ex-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c3ex-warn" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <rect x="30" y="150" width="140" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="100" y="176" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">컨트롤러</text>
  <text x="100" y="196" text-anchor="middle" font-size="14" fill="#6b7280">요청을 받는 입구</text>
  <rect x="230" y="150" width="160" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="310" y="174" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">서비스</text>
  <text x="310" y="194" text-anchor="middle" font-size="14" fill="#c2410c">Exception404 던짐</text>
  <line x1="170" y1="180" x2="228" y2="180" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ex-ar)"/>
  <rect x="360" y="40" width="250" height="72" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="485" y="68" text-anchor="middle" font-size="16" font-weight="800" fill="#3730a3">@RestControllerAdvice</text>
  <text x="485" y="90" text-anchor="middle" font-size="14" fill="#3730a3">전파된 예외를 한 곳에서 가로챈다</text>
  <path d="M330,150 C330,112 372,98 400,90" fill="none" stroke="#ff7849" stroke-width="1.9" stroke-dasharray="4,4" marker-end="url(#c3ex-warn)"/>
  <text x="300" y="124" text-anchor="middle" font-size="14" fill="#c2410c">예외 전파</text>
  <rect x="700" y="140" width="250" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="825" y="166" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">404 JSON 응답</text>
  <text x="825" y="188" text-anchor="middle" font-size="14" fill="#6b7280">status 404, msg,</text>
  <text x="825" y="204" text-anchor="middle" font-size="14" fill="#6b7280">body null</text>
  <path d="M610,90 C670,102 700,120 738,138" fill="none" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c3ex-ar)"/>
  <text x="672" y="96" text-anchor="middle" font-size="14" fill="#4f46e5">Resp.fail</text>
</svg>
</div>

*그림 3-4. 전역 예외 처리 흐름*

## 3.5 서비스와 컨트롤러에 적용

### 3.5.1 서비스

**BoardService**가 DTO로 값을 주고받고 예외 처리까지 수행하도록 변경합니다.

`board/BoardService.java`를 열어 아래와 같이 작성합니다.

```java [실습 7] board/BoardService.java. 주고받는 타입을 DTO로, 없으면 예외
    public List<BoardResponse.DTO> 게시글목록() {
        return boardRepository.findAll().stream()
                .map(BoardResponse.DTO::new)
                .toList();
    }

    public BoardResponse.DetailDTO 게시글상세(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board);
    }

    @Transactional
    public BoardResponse.DTO 게시글쓰기(BoardRequest.SaveDTO requestDTO) {
        Board savedBoard = boardRepository.save(requestDTO.toEntity()); // DTO -> 엔티티
        return new BoardResponse.DTO(savedBoard); // 저장된 게시글 반환
    }

    @Transactional
    public BoardResponse.DTO 게시글수정(Integer boardId, BoardRequest.UpdateDTO requestDTO) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        // 더티 체킹
        board.setTitle(requestDTO.title());
        board.setContent(requestDTO.content());
        return new BoardResponse.DTO(board); // 수정된 게시글 반환
    }

    @Transactional
    public void 게시글삭제(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        boardRepository.delete(board);
    }
```

### 3.5.2 컨트롤러

컨트롤러는 요청으로 받는 값과 서비스에서 전달받는 값이 모두 DTO 타입으로 바뀝니다.

`board/BoardController.java`를 열어 아래와 같이 작성합니다.

```java [실습 8] board/BoardController.java. 요청·응답 타입을 DTO로
    @GetMapping
    public ResponseEntity<?> findAll() {
        List<BoardResponse.DTO> respDTOList = boardService.게시글목록();
        return Resp.ok(respDTOList);
    }

    @GetMapping("/{boardId}")
    public ResponseEntity<?> findById(@PathVariable("boardId") Integer boardId) {
        BoardResponse.DetailDTO respDTO = boardService.게시글상세(boardId);
        return Resp.ok(respDTO);
    }

    @PostMapping
    public ResponseEntity<?> save(@RequestBody BoardRequest.SaveDTO requestDTO) {
        BoardResponse.DTO respDTO = boardService.게시글쓰기(requestDTO);
        return Resp.ok(respDTO);
    }

    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(@PathVariable("boardId") Integer boardId,
            @RequestBody BoardRequest.UpdateDTO requestDTO) {
        BoardResponse.DTO respDTO = boardService.게시글수정(boardId, requestDTO);
        return Resp.ok(respDTO);
    }

    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(@PathVariable("boardId") Integer boardId) {
        boardService.게시글삭제(boardId);
        return Resp.ok(null);
    }
```

주소와 HTTP 메서드는 챕터 2와 같습니다. 게시글 상세 API를 호출하면 응답에는 DTO에 담긴 세 값만 담깁니다.

```json [Hoppscotch] 게시글 상세 조회
GET http://localhost:8080/api/boards/1
```

<!-- [CAPTURE NEEDED: 01_board-detail-dto
  path: assets/CH3/terminal/01_board-detail-dto.png
  desc: GET /api/boards/1 요청에 대한 200 응답. { "status": 200, "msg": "성공", "body": { "boardId": 1, "title": "title1", "content": "content1" } } 형태로, 엔티티가 가진 나머지 필드 없이 DTO에 담긴 세 값만 나온 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH3/terminal/01_board-detail-dto.png)
*그림 3-5. 상세 조회 응답*

앞에서 만든 전역 예외 처리기가 실제로 404를 돌려주는지, 없는 999번을 조회해 확인합니다.

```json [Hoppscotch] 없는 게시글 다시 조회
GET http://localhost:8080/api/boards/999
```

빈 값이 담긴 성공 대신 404 응답을 받습니다.

<!-- [CAPTURE NEEDED: 02_404-response
  path: assets/CH3/terminal/02_404-response.png
  desc: GET /api/boards/999 요청에 대한 404 JSON 응답. { "status": 404, "msg": "게시글을 찾을 수 없습니다", "body": null } 형태. Hoppscotch 또는 브라우저 응답 화면. HTTP 상태 코드가 404로 표시되면 좋음.
] -->
![](../assets/CH3/terminal/02_404-response.png)
*그림 3-6. 404 응답*

오픈이는 목록 API를 받아 간 동료를 다시 불렀습니다. 키보드에서 손을 뗀 사무실이 잠깐 조용해졌습니다.

**오픈이**: "지난번에 없는 번호 넣으면 어떻게 되냐고 물었잖아요. 이제 없으면 없다고 딱 나와요."<br>
**동료**: "아, 999번 호출해 볼게요. 없다고 딱 나오네요. 저번엔 성공이라면서 아무것도 없더니."

*여기까진 됐다.*

다섯 곳을 정리했지만, 오픈이는 화면을 내려다보다 한 가지가 걸렸습니다. 지금은 로그인 화면도, 게시글 주인을 확인하는 절차도 없습니다. 999번 하나 못 찾는 것은 막아 놨는데, 정작 누구나 게시글을 고치고 지울 수 있는 서버였습니다.

*없는 게시글은 걸렀는데, 문은 여전히 다 열려 있잖아.*

다음 챕터에서는 인증 기능을 추가해, 작성자 본인만 자기 게시글을 관리할 수 있게 합니다.

:::remember
**이것만은 기억하자**

- **엔티티를 요청과 응답에 직접 사용하지 않고 DTO로 주고받습니다.** 받을 값과 내보낼 값, 그 이름을 엔티티가 아니라 DTO에서 정합니다.
- **없는 값은 `Optional`에 담고 `orElseThrow`로 예외를 발생시킵니다.** 커스텀 예외는 **RuntimeException**을 상속해, 발생시키는 일과 받는 일을 나눕니다. 발생한 예외는 **@RestControllerAdvice**가 한 곳에서 받아 상태 코드에 맞는 JSON으로 바꿉니다.
:::
