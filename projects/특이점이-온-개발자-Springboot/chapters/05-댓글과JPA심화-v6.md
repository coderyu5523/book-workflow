# 챕터 5. 댓글과 JPA 심화

인증 기능이 적용되며 게시판의 기본 뼈대가 완성되었습니다. 이제 로그인한 사용자만 글을 작성할 수 있고, 본인이 쓴 글만 수정하거나 삭제할 수 있습니다. 다음 순서는 '댓글' 기능입니다.

오픈이는 댓글 테이블에 필요한 컬럼을 정리하다가 멈칫했습니다.

*게시글 하나에 댓글이 여러 개 달리니까 게시글과 댓글은 1대N 관계인데, 그럼 회원과 댓글은 어떻게 연결해야 하지?*

오픈이는 선배를 찾아갔습니다.

**오픈이**: "선배님, 댓글 테이블에 게시글 번호를 넣는 것까지는 알겠는데 회원과는 어떻게 이어야 할지 헷갈립니다. 게시글처럼 1대N 관계로 보면 될까요?"

**선배**: "맞아요. 회원 한 명이 여러 개의 댓글을 작성하니까 회원과 댓글 역시 1대N 관계죠. 두 관계 모두 'N'쪽이 댓글이라서, 댓글 테이블에 게시글 번호와 회원 번호가 나란히 들어가게 됩니다."

선배는 자바 객체에서의 설계 방향도 덧붙여 주었습니다.

**선배**: "다만 DB 테이블과 달리, 자바 객체로 설계할 때는 게시글 객체만 댓글 목록을 리스트로 가집니다. 게시글 화면을 띄울 때는 달린 댓글도 같이 필요하지만, 회원 정보를 조회할 때 그 사람이 쓴 전체 댓글까지 한 번에 불러올 필요는 없으니까요."

<div class="svg-figure">
<svg viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="왼쪽 테이블 구조에서는 board_tb와 user_tb가 각각 reply_tb와 1대N으로 이어지고 외래 키는 reply_tb에만 있다. 오른쪽 자바 객체 구조에서는 Board에 replies 목록 필드가 더 생겨 Board와 Reply가 양쪽 필드로 이어지고, User 쪽에는 목록 필드가 없다.">
  <text x="245" y="32" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">테이블</text>
  <text x="755" y="32" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">자바 객체</text>
  <line x1="500" y1="50" x2="500" y2="380" stroke="#e2e8f0" stroke-width="2"/>

  <rect x="40" y="60" width="150" height="76" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="40" y="60" width="150" height="28" rx="8" fill="#eef2ff"/>
  <rect x="40" y="80" width="150" height="8" fill="#eef2ff"/>
  <text x="115" y="79" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#3730a3">board_tb</text>
  <text x="56" y="108" font-size="12" font-family="monospace" fill="#475569">id</text>
  <text x="56" y="128" font-size="12" font-family="monospace" fill="#475569">title</text>

  <rect x="40" y="290" width="150" height="76" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="40" y="290" width="150" height="28" rx="8" fill="#eef2ff"/>
  <rect x="40" y="310" width="150" height="8" fill="#eef2ff"/>
  <text x="115" y="309" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#3730a3">user_tb</text>
  <text x="56" y="338" font-size="12" font-family="monospace" fill="#475569">id</text>
  <text x="56" y="358" font-size="12" font-family="monospace" fill="#475569">username</text>

  <rect x="290" y="150" width="160" height="124" rx="8" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <rect x="290" y="150" width="160" height="28" rx="8" fill="#fff4ed"/>
  <rect x="290" y="170" width="160" height="8" fill="#fff4ed"/>
  <text x="370" y="169" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#7b341e">reply_tb</text>
  <text x="306" y="200" font-size="12" font-family="monospace" fill="#475569">id</text>
  <text x="306" y="222" font-size="12" font-family="monospace" fill="#475569">comment</text>
  <text x="306" y="244" font-size="12" font-family="monospace" font-weight="800" fill="#c2410c">board_id</text>
  <text x="306" y="266" font-size="12" font-family="monospace" font-weight="800" fill="#c2410c">user_id</text>

  <path d="M190,110 H240 V210 H290" fill="none" stroke="#334155" stroke-width="1.8"/>
  <line x1="215" y1="100" x2="215" y2="120" stroke="#334155" stroke-width="1.8"/>
  <text x="215" y="94" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">1</text>
  <path d="M278,200 L290,210 L278,220 M278,210 L290,210" fill="none" stroke="#334155" stroke-width="1.8"/>
  <text x="272" y="196" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">N</text>

  <path d="M190,326 H240 V236 H290" fill="none" stroke="#334155" stroke-width="1.8"/>
  <line x1="215" y1="316" x2="215" y2="336" stroke="#334155" stroke-width="1.8"/>
  <text x="215" y="352" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">1</text>
  <path d="M278,226 L290,236 L278,246 M278,236 L290,236" fill="none" stroke="#334155" stroke-width="1.8"/>
  <text x="272" y="262" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">N</text>

  <rect x="550" y="60" width="180" height="104" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="550" y="60" width="180" height="28" rx="8" fill="#eef2ff"/>
  <rect x="550" y="80" width="180" height="8" fill="#eef2ff"/>
  <text x="640" y="79" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#3730a3">Board</text>
  <text x="566" y="108" font-size="12" font-family="monospace" fill="#475569">id</text>
  <text x="566" y="130" font-size="12" font-family="monospace" fill="#475569">title</text>
  <rect x="556" y="138" width="168" height="20" rx="4" fill="#eef2ff"/>
  <text x="566" y="153" font-size="12" font-family="monospace" font-weight="800" fill="#3730a3">List&lt;Reply&gt; replies</text>

  <rect x="550" y="290" width="180" height="76" rx="8" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="550" y="290" width="180" height="28" rx="8" fill="#eef2ff"/>
  <rect x="550" y="310" width="180" height="8" fill="#eef2ff"/>
  <text x="640" y="309" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#3730a3">User</text>
  <text x="566" y="338" font-size="12" font-family="monospace" fill="#475569">id</text>
  <text x="566" y="358" font-size="12" font-family="monospace" fill="#475569">username</text>

  <rect x="800" y="150" width="180" height="124" rx="8" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <rect x="800" y="150" width="180" height="28" rx="8" fill="#fff4ed"/>
  <rect x="800" y="170" width="180" height="8" fill="#fff4ed"/>
  <text x="890" y="169" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#7b341e">Reply</text>
  <text x="816" y="200" font-size="12" font-family="monospace" fill="#475569">id</text>
  <text x="816" y="222" font-size="12" font-family="monospace" fill="#475569">comment</text>
  <text x="816" y="244" font-size="12" font-family="monospace" font-weight="800" fill="#c2410c">Board board</text>
  <text x="816" y="266" font-size="12" font-family="monospace" font-weight="800" fill="#c2410c">User user</text>

  <path d="M730,148 H762 V244 H800" fill="none" stroke="#334155" stroke-width="1.8"/>
  <circle cx="730" cy="148" r="4" fill="#3730a3"/>
  <line x1="746" y1="138" x2="746" y2="158" stroke="#334155" stroke-width="1.8"/>
  <text x="746" y="132" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">1</text>
  <circle cx="800" cy="244" r="4" fill="#c2410c"/>
  <path d="M788,234 L800,244 L788,254 M788,244 L800,244" fill="none" stroke="#334155" stroke-width="1.8"/>
  <text x="782" y="230" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">N</text>

  <path d="M800,266 H772 V326 H730" fill="none" stroke="#334155" stroke-width="1.8"/>
  <circle cx="800" cy="266" r="4" fill="#c2410c"/>
  <path d="M812,256 L800,266 L812,276 M800,266 L812,266" fill="none" stroke="#334155" stroke-width="1.8"/>
  <text x="818" y="288" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">N</text>
  <line x1="750" y1="316" x2="750" y2="336" stroke="#334155" stroke-width="1.8"/>
  <text x="750" y="352" text-anchor="middle" font-size="12" font-weight="800" fill="#334155">1</text>
</svg>
</div>

*그림 5-1. 테이블에서는 댓글에만 번호가 들어가지만, 자바에서는 게시글에 댓글 목록이 하나 더 생깁니다*

:::goal
**이번 챕터가 끝나면**

- 양방향 매핑과 연관관계 주인이 무엇인지 설명하고, **@OneToMany**와 cascade로 게시글에 댓글을 연결합니다
- 즉시 로딩과 지연 로딩의 차이를 로그로 확인하고, `join fetch`로 연관 엔티티를 함께 조회합니다
- 게시글 상세 응답에 댓글 목록을 담고, 댓글 쓰기와 삭제를 구현합니다
:::

::::prep
**소스코드 준비**

소스코드 준비에서 클론한 예제 저장소에서 이번 챕터 폴더로 이동합니다. 패키지 루트는 챕터 4와 같은 `com.metacoding.spring`입니다.

```bash [터미널] 챕터 5 폴더로 이동
cd spring-start/ch05
```

이번 챕터에서 새로 만들거나 고치는 파일은 다음과 같습니다.

```text ch05 파일 구조
spring-start/ch05/src/main/java/com/metacoding/spring/
├── board/
│   ├── Board.java                        # [작성] @OneToMany replies, user EAGER→LAZY
│   ├── BoardRepository.java              # [작성] findByIdJoinUserAndReply
│   ├── BoardResponse.java                # [작성] DetailDTO에 replies
│   └── BoardService.java                 # [작성] 상세 조회를 fetch join으로 교체
└── reply/
    ├── Reply.java                        # [작성] 댓글 엔티티(@ManyToOne user/board)
    ├── ReplyController.java              # [작성] 작성·삭제 엔드포인트
    ├── ReplyRepository.java              # [작성] JpaRepository 상속으로 저장·조회·삭제
    ├── ReplyRequest.java                 # [작성] 댓글 요청 DTO
    ├── ReplyResponse.java                # [작성] 댓글 응답 DTO
    └── ReplyService.java                 # [작성] 댓글 저장·삭제(소유자 검증)

spring-start/ch05/src/main/resources/
└── db/data.sql                           # [작성] 댓글 더미 데이터

spring-start/ch05/src/test/java/com/metacoding/spring/
└── board/BoardRepositoryTest.java        # [작성] 즉시 로딩과 지연 로딩 확인
```

챕터를 따라 코드를 채우고, 막히면 `spring-end`의 완성 코드를 참고하세요.
::::

## 5.1 양방향 매핑

게시글 하나에 댓글이 여러 개 달리는 1대N 관계입니다. 데이터베이스는 댓글 쪽에 외래 키 하나만 두면 양쪽 조회가 다 가능하고, 자바에서도 매번 쿼리를 날려 댓글을 가져오면 됩니다. 하지만 JPA는 매번 쿼리를 짜는 대신, `board.getReplies()`처럼 자바 코드에서 연관 데이터를 바로 꺼내보는 편의성을 제공합니다.

이렇게 객체를 통해 데이터를 탐색하려면 게시글 객체 내부에도 댓글 목록(**List**)을 둬야 합니다. 그리고 이 리스트가 DB의 1대N 관계라는 것을 JPA에 알려주는 설정이 바로 **@OneToMany**입니다. 댓글의 **@ManyToOne**과 짝을 이뤄 서로를 연결해 주는 이 방식을 **양방향 매핑(Bidirectional Mapping)** 이라고 합니다.

<div class="svg-figure">
<svg viewBox="0 0 720 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Board 엔티티와 Reply 엔티티가 서로를 참조하는 그림. Board에는 @OneToMany가, Reply에는 @ManyToOne이 붙어 있다. Reply에서 Board로 향하는 화살표에 getBoard()가, Board에서 Reply로 향하는 화살표에 getReplies()가 적혀 있다.">
  <defs>
    <marker id="c5bi-l" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="c5bi-r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>

  <rect x="60" y="60" width="220" height="110" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <text x="170" y="98" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#3730a3">@OneToMany</text>
  <text x="170" y="134" text-anchor="middle" font-size="19" font-weight="800" fill="#0f172a">Board</text>

  <rect x="440" y="60" width="220" height="110" rx="10" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="550" y="98" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#c2410c">@ManyToOne</text>
  <text x="550" y="134" text-anchor="middle" font-size="19" font-weight="800" fill="#0f172a">Reply</text>

  <line x1="436" y1="95" x2="288" y2="95" stroke="#ff7849" stroke-width="2" marker-end="url(#c5bi-l)"/>
  <text x="362" y="82" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#c2410c">getBoard()</text>

  <line x1="284" y1="140" x2="432" y2="140" stroke="#4f46e5" stroke-width="2" marker-end="url(#c5bi-r)"/>
  <text x="358" y="166" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#3730a3">getReplies()</text>
</svg>
</div>

*그림 5-2. 게시글은 @OneToMany로 댓글 목록을, 댓글은 @ManyToOne으로 게시글을 참조합니다*

먼저 댓글 엔티티부터 정의합니다. **User** 엔티티와 **Board** 엔티티를 참조하는 필드를 포함하면, 각 댓글이 어떤 회원이 어떤 게시글에 작성했는지를 알 수 있습니다. 이를 위해 `reply/Reply.java`를 열어 아래와 같이 작성합니다.

```java [실습 1] reply/Reply.java. 댓글 엔티티
@NoArgsConstructor
@Data
@Entity
@Table(name = "reply_tb")
public class Reply {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String comment;

    // 외래 키 필드
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    // 외래 키 필드
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "board_id")
    private Board board;

    @CreationTimestamp
    private Timestamp createdAt;

    @Builder
    public Reply(Integer id, String comment, User user, Board board,
            Timestamp createdAt) {
        this.id = id;
        this.comment = comment;
        this.user = user;
        this.board = board;
        this.createdAt = createdAt;
    }
}
```

양방향 매핑을 위해 **Board** 엔티티에 **Reply** 컬렉션을 필드로 추가합니다. 게시글에 달린 댓글을 한 번에 조회할 수 있도록 **List** 타입으로 선언하고, `mappedBy`에는 **Reply**에서 **Board**를 참조하는 필드 이름을 지정합니다. 이를 위해 `board/Board.java`를 열어 아래와 같이 필드를 작성합니다.

```java [실습 2] board/Board.java. 댓글 목록 연관관계 추가
    // 이 관계의 주인은 Reply의 board 필드다
    @OneToMany(mappedBy = "board", fetch = FetchType.LAZY, cascade = CascadeType.REMOVE)
    private List<Reply> replies = new ArrayList<>();
```

`cascade = CascadeType.REMOVE`를 설정하면 게시글을 삭제할 때 연관된 댓글도 함께 삭제됩니다. 또한 필드를 `new ArrayList<>()`로 초기화하면 댓글이 없는 경우에도 null 대신 빈 목록을 가지므로, 에러 없이 댓글 개수(0)를 확인할 수 있습니다.

:::note
**@OneToMany 필드는 테이블 컬럼이 아닙니다**

**@OneToMany**에 선언한 필드는 엔티티 사이의 참조만 나타내며, 실제 데이터베이스 테이블에는 컬럼으로 추가되지 않습니다. 게시글 쪽에는 외래 키가 없고, JPA가 댓글의 `board_id`를 따라가 `replies`를 채웁니다.
:::

댓글 테이블이 추가되었으므로 시작할 때 넣어 둘 데이터에도 댓글을 더합니다. 이를 위해 `resources/db/data.sql`을 열어 회원·게시글 아래에 아래와 같이 작성합니다.

```sql [실습 3] resources/db/data.sql. 댓글 더미 데이터
insert into reply_tb(comment,board_id,user_id,created_at) values('comment1',1,1,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment2',1,1,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment3',1,2,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment4',2,2,now());
```
## 5.2 즉시 로딩과 지연 로딩

**Board** 엔티티에는 작성자와 댓글이 연관관계 필드로 매핑되어 있습니다. JPA에서는 게시글을 조회할 때 연관된 데이터까지 한 번에 가져올지, 아니면 해당 데이터를 실제 사용하는 시점에 가져올지 결정해야 합니다. 이 동작 방식은 연관관계 어노테이션의 `fetch` 속성으로 설정합니다. 앞서 **Reply** 엔티티와 `replies` 필드에 지정한 `FetchType.LAZY`가 이 설정입니다.

**즉시 로딩(Eager Loading)** 은 게시글을 조회할 때 연관된 **User** 엔티티까지 함께 조회하는 전략입니다. **@ManyToOne**의 기본 전략은 즉시 로딩이며, 현재는 EAGER로 설정이 명시되어 있습니다.

`test/board/BoardRepositoryTest.java`를 열어 게시글 번호만 출력하는 테스트를 추가합니다.

```java [실습 4] test/board/BoardRepositoryTest.java. 즉시 로딩 확인
    @Test
    public void findByIdEager_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findById(id).get();
        // eye
        System.out.println("Board ID : " + board.getId());
    }
```

`findById()`로 게시글 하나를 조회했을 뿐인데 **board_tb**와 **user_tb**를 조인하는 SELECT 쿼리가 실행됩니다. select 목록에도 `u1_0.username`을 비롯한 회원 컬럼이 그대로 들어갑니다. 조회 시점에 **User** 엔티티를 완성해 두어야 하므로 `user_id`만 읽고 끝내지 않습니다.

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">Hibernate:</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;select b1_0.id, b1_0.content, b1_0.created_at, b1_0.title,</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;u1_0.id, u1_0.created_at, u1_0.email, u1_0.password, u1_0.username</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;from board_tb b1_0</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-hl">left join user_tb u1_0 on u1_0.id=b1_0.user_id</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;where b1_0.id=?</div>
    <div><span class="tl-val">Board ID : 1</span></div>
  </div>
</div>

*그림 5-3. 즉시 로딩은 게시글을 조회하는 시점에 회원 테이블까지 조인해 함께 읽습니다*

출력한 값은 게시글 번호뿐인데도 회원 데이터를 읽었습니다. 게시글 목록처럼 제목과 내용만 사용하는 화면에서는 이 조회가 그대로 낭비됩니다. 이럴 때는 반대 전략인 지연 로딩을 선택합니다.

**지연 로딩(Lazy Loading)** 은 게시글 데이터만 먼저 조회하고, 회원 데이터는 실제로 접근하는 순간에 쿼리를 실행해 가져오는 방식입니다. `board/Board.java`의 작성자 필드 `fetch` 속성을 아래와 같이 변경해 봅니다.

```java [실습 5] board/Board.java. 작성자 조회를 지연 로딩으로
    // 챕터 4의 EAGER에서 LAZY로 바꾼다
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
```

테스트 코드는 수정하지 않고, 앞서 작성한 `findByIdEager_test()`를 다시 실행합니다. 조인이 사라지고 **board_tb**만 조회하는 SELECT 쿼리가 실행됩니다. select 목록에 남은 `b1_0.user_id`는 외래 키 컬럼이며, **User** 엔티티는 이 값만 가진 상태로 자리만 잡아 둡니다.

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">Hibernate:</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;select b1_0.id, b1_0.content, b1_0.created_at, b1_0.title, <span class="tl-hl">b1_0.user_id</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;from board_tb b1_0</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;where b1_0.id=?</div>
    <div><span class="tl-val">Board ID : 1</span></div>
  </div>
</div>

*그림 5-4. 지연 로딩은 회원 데이터를 사용하지 않으면 회원 테이블을 읽지 않습니다*

이번에는 회원 데이터를 사용하는 경우를 확인합니다. `test/board/BoardRepositoryTest.java`에 게시글 번호와 작성자 이름을 함께 출력하는 테스트를 추가합니다.

```java [실습 6] test/board/BoardRepositoryTest.java. 지연 로딩 시점 확인
    @Test
    public void findByIdLazyLoading_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findById(id).get();
        // eye
        System.out.println("Board ID : " + board.getId());
        System.out.println("username : " + board.getUser().getUsername());
    }
```

SELECT 쿼리가 두 번 실행됩니다. 먼저 **board_tb**를 조회하는 쿼리가 실행되어 `Board ID : 1`이 출력됩니다. 이후 `username : ssar`을 출력하기 위해 **User** 엔티티에 접근하는 순간, **user_tb**를 조회하는 두 번째 쿼리가 실행됩니다.

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">Hibernate:</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;select b1_0.id, b1_0.content, b1_0.created_at, b1_0.title, b1_0.user_id</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;from board_tb b1_0</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;where b1_0.id=?</div>
    <div><span class="tl-val">Board ID : 1</span></div>
    <div><span class="tl-label">Hibernate:</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-hl">select u1_0.id, u1_0.created_at, u1_0.email, u1_0.password, u1_0.username</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;from user_tb u1_0</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;where u1_0.id=?</div>
    <div><span class="tl-val">username : ssar</span></div>
  </div>
</div>

*그림 5-5. 지연 로딩은 작성자 이름을 사용하는 순간 회원 테이블을 한 번 더 읽습니다*

## 5.3 댓글 목록

게시글 상세를 조회할 때는 작성자와 댓글이 모두 필요합니다. 지연 로딩에 맡기면 꺼낼 때마다 조회가 따로 실행되므로, JOIN으로 함께 가져오는 조회를 구현합니다. JPQL의 JOIN은 연관관계 필드를 통해서만 사용합니다.

```sql [JPQL] 기본 JOIN
select b from Board b join b.user u where u.username = :username
```

일치하는 값이 없어도 기준 테이블을 조회하고 싶다면 LEFT OUTER JOIN을 사용합니다.

```sql [JPQL] LEFT OUTER JOIN
select b from Board b left join b.replies r where b.id = :boardId
```

일반 JOIN은 지연 로딩을 그대로 사용합니다. 조회할 때 연관 엔티티를 한 번에 가져오고 싶다면 FETCH JOIN을 사용해야 합니다.

```sql [JPQL] FETCH JOIN
select b from Board b join fetch b.user where b.id = :boardId
```

챕터 4에서 만든 `findByIdJoinUser()`가 이 형태입니다. 여기에 댓글을 더한 조회를 구현합니다. INNER JOIN은 매칭되는 행만 반환하므로 댓글이 없는 게시글은 결과에서 제외됩니다. 그런 게시글까지 조회하려면 댓글 쪽에 LEFT OUTER JOIN을 써야 합니다. 이를 위해 `board/BoardRepository.java`를 열어 아래와 같이 메서드를 작성합니다.

```java [실습 7] board/BoardRepository.java. 작성자와 댓글을 함께 가져오는 조회
    @Query("select b from Board b join fetch b.user "
            + "left join fetch b.replies where b.id = :boardId")
    Optional<Board> findByIdJoinUserAndReply(@Param("boardId") Integer boardId);
```

`join fetch b.user`로 작성자를, `left join fetch b.replies`로 댓글 목록을 함께 가져옵니다. 데이터베이스에서는 게시글 하나가 댓글 수만큼 중복된 행으로 반환되지만, JPA가 같은 **Board** 하나로 합쳐 주므로 결과는 게시글 한 건입니다.

:::tip
**언제 FETCH JOIN을 쓰는가**

연관 데이터는 기본 속성을 `LAZY`로 두어 실제 접근할 때만 로딩합니다. 다만 화면별 시나리오에 따라 지연 로딩이 불필요한 추가 조회를 유발할 수 있으므로, 필요한 조회에서만 FETCH JOIN으로 묶어 쿼리 수와 전송량을 줄입니다.
:::

조회한 댓글을 응답에 담습니다. **List** 타입 필드는 **DTO** 안에서 또 다른 **DTO** 객체를 생성해, 엔티티를 하나씩 변환하여 담습니다. 이를 반영하여 `board/BoardResponse.java`의 **DetailDTO**를 아래와 같이 변경합니다.

```java [실습 8] board/BoardResponse.java. 상세에 댓글 목록 추가
    public record DetailDTO(
            Integer boardId,
            String title,
            String content,
            Integer userId,
            String username,
            Boolean isOwner,
            List<ReplyDTO> replies) {

        public DetailDTO(Board board, User loginUser) {
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(),
                    board.getUser().getUsername(),
                    loginUser != null && loginUser.getId()
                            .equals(board.getUser().getId()),
                    board.getReplies().stream()
                            .map(r -> new ReplyDTO(r, loginUser))
                            .toList());
        }

        // List 타입의 댓글을 담는 DTO
        public record ReplyDTO(
                Integer replyId,
                String username,
                String comment,
                Boolean isOwner) {

            public ReplyDTO(Reply reply, User loginUser) {
                this(
                        reply.getId(),
                        reply.getUser().getUsername(),
                        reply.getComment(),
                        loginUser != null && loginUser.getId()
                                .equals(reply.getUser().getId()));
            }
        }
    }
```

`board.getReplies()`로 게시글에 달린 댓글을 꺼내 각각을 안쪽의 **ReplyDTO**로 바꿔 담습니다. 댓글에도 작성자 본인인지 알려 주는 값이 필요하므로 **ReplyDTO**도 챕터 4와 같은 방식으로 두 아이디를 비교해 `isOwner`를 채웁니다. 화면은 이 값으로 본인이 쓴 댓글에만 삭제 버튼을 보여 줍니다.

**BoardService**의 상세 메서드에서 기존 `findByIdJoinUser()` 호출을 `findByIdJoinUserAndReply()`로 대체합니다. 이를 반영하여 `board/BoardService.java`를 아래와 같이 변경합니다.

```java [실습 9] board/BoardService.java. 상세 조회를 fetch join으로 교체
    public BoardResponse.DetailDTO 게시글상세(Integer boardId, User loginUser) {
        Board board = boardRepository.findByIdJoinUserAndReply(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board, loginUser);
    }
```

게시글이 없다면 **Exception404**로 처리합니다. 컨트롤러는 챕터 4에서 이미 로그인 유저를 꺼내 넘기도록 고쳤으므로 그대로 둡니다.

ssar로 로그인해 게시글 상세 API를 호출하면 결과를 확인할 수 있습니다.

```json [Hoppscotch] 게시글 상세 조회
GET http://localhost:8080/api/boards/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9...
```

<!-- [CAPTURE NEEDED: 03_board-detail-with-replies
  path: assets/CH5/terminal/03_board-detail-with-replies.png
  desc: ssar로 로그인해 발급받은 토큰을 Authorization 헤더에 담고 보낸 GET /api/boards/1 요청에 대한 200 응답. body에 게시글(boardId 1, title1, content1, userId 1, username ssar)과 isOwner true가 담기고, replies 배열에 댓글 세 개(replyId 1·2는 ssar이 써서 isOwner true, replyId 3은 cos이 써서 isOwner false)가 이어지는 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH5/terminal/03_board-detail-with-replies.png)
*그림 5-6. 상세 응답에 게시글과 댓글이 함께 담기고, 본인이 쓴 것에만 isOwner가 true입니다*

게시글의 `isOwner`가 true이고, ssar가 쓴 1·2번 댓글도 true, cos가 쓴 3번 댓글은 false입니다.

## 5.4 댓글 쓰기

읽는 쪽이 끝났으니 쓰는 쪽을 구현합니다. **SaveDTO**는 댓글 내용과 대상 게시글의 번호(`boardId`)를 받고, 작성자 정보는 필터가 담아 둔 **User** 엔티티를 활용합니다. 이를 위해 `reply/ReplyRequest.java`를 열어 아래와 같이 작성합니다.

```java [실습 10] reply/ReplyRequest.java. 댓글 요청 DTO
public class ReplyRequest {

    public record SaveDTO(String comment, Integer boardId) {

        public Reply toEntity(User user, Board board) {
            return Reply.builder()
                    .comment(comment)
                    .user(user)
                    .board(board)
                    .build();
        }
    }
}
```

`toEntity()`는 챕터 4에서 게시글을 만들 때처럼 로그인 유저와 대상 게시글을 넘겨받아 댓글 엔티티로 옮겨 담습니다.

응답으로 반환할 댓글 하나를 담을 **DTO**도 정의합니다. 이를 위해 `reply/ReplyResponse.java`를 열어 아래와 같이 작성합니다.

```java [실습 11] reply/ReplyResponse.java. 댓글 응답 DTO
public class ReplyResponse {

    public record DTO(Integer replyId, String comment, String username) {

        public DTO(Reply reply) {
            this(
                    reply.getId(),
                    reply.getComment(),
                    reply.getUser().getUsername());
        }
    }
}
```

댓글을 저장하고 조회하는 리포지토리를 구현합니다. 이를 위해 `reply/ReplyRepository.java`를 열어 아래와 같이 작성합니다.

```java [실습 12] reply/ReplyRepository.java. JpaRepository 상속
public interface ReplyRepository extends JpaRepository<Reply, Integer> {
}
```

챕터 3에서 바꾼 **BoardRepository**와 같은 모양입니다. 저장할 `save()`, 권한 확인에 쓸 `findById()`, 삭제할 `delete()`가 모두 상속으로 들어오므로 안이 비어 있습니다.

서비스는 전달받은 게시글 아이디와 로그인 유저로 **Reply** 엔티티를 생성하고 `save()`를 호출합니다. 이를 위해 `reply/ReplyService.java`를 열어 아래와 같이 작성합니다.

```java [실습 13] reply/ReplyService.java. 댓글 저장
@RequiredArgsConstructor
@Service
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;

    @Transactional
    public ReplyResponse.DTO 댓글쓰기(ReplyRequest.SaveDTO requestDTO, User loginUser) {
        // 1. 넘어온 유저가 없으면 로그인하지 않은 요청이다
        if (loginUser == null) {
            throw new Exception401("로그인이 필요합니다");
        }
        // 2. 댓글을 달 게시글을 찾아 연결한다
        Board board = boardRepository.findById(requestDTO.boardId())
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        Reply reply = requestDTO.toEntity(loginUser, board);
        replyRepository.save(reply);
        return new ReplyResponse.DTO(reply);
    }
}
```

챕터 4의 게시글 쓰기와 순서가 같습니다. 로그인하지 않은 요청이면 **Exception401**을 발생시키고, `boardId`로 댓글을 달 게시글을 찾아 없으면 **Exception404**를 발생시킵니다.

댓글을 저장하려면 그 댓글이 어느 게시글에 속하는지 알아야 하므로, 클라이언트는 요청 본문에 `boardId`를 함께 담아 전달합니다. 이를 위해 `reply/ReplyController.java`를 열어 아래와 같이 작성합니다.

```java [실습 14] reply/ReplyController.java. 댓글 작성 엔드포인트
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/replies")
public class ReplyController {

    private final ReplyService replyService;

    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @RequestBody ReplyRequest.SaveDTO requestDTO) {
        User loginUser = (User) request.getAttribute("loginUser");
        ReplyResponse.DTO respDTO = replyService.댓글쓰기(requestDTO, loginUser);
        return Resp.ok(respDTO);
    }
}
```

`request.getAttribute("loginUser")`로 로그인 유저를 꺼내 서비스로 전달합니다. 챕터 4에서 필터가 담아 둔 유저입니다. 꺼낸 유저가 null이어도 그대로 전달하고, 막을지 말지는 서비스가 정합니다.

ssar로 로그인해 1번 게시글에 댓글을 답니다.

```json [Hoppscotch] 댓글 작성
POST http://localhost:8080/api/replies
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9...

{ "comment": "comment5", "boardId": 1 }
```

<!-- [CAPTURE NEEDED: 04_reply-save
  path: assets/CH5/terminal/04_reply-save.png
  desc: ssar 토큰을 Authorization 헤더에 담고 보낸 POST /api/replies 요청에 대한 200 응답. body에 replyId 5, comment "comment5", username ssar이 담긴 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH5/terminal/04_reply-save.png)
*그림 5-7. 댓글을 저장하면 저장된 댓글이 응답에 담겨 돌아옵니다*

## 5.5 댓글 삭제

삭제도 저장과 같은 순서로 구현합니다.

서비스는 댓글 작성자의 아이디와 로그인 유저의 아이디를 비교해 권한을 검증한 후, 조건을 만족하면 댓글을 삭제합니다. 이를 위해 `reply/ReplyService.java`에 아래와 같이 메서드를 추가합니다.

```java [실습 15] reply/ReplyService.java. 댓글 삭제
    @Transactional
    public void 댓글삭제(Integer replyId, User loginUser) {
        // 1. 넘어온 유저가 없으면 로그인하지 않은 요청이다
        if (loginUser == null) {
            throw new Exception401("로그인이 필요합니다");
        }
        Reply reply = replyRepository.findById(replyId)
                .orElseThrow(() -> new Exception404("댓글을 찾을 수 없습니다"));
        // 2. 작성자 본인이 아니면 막는다
        if (!reply.getUser().getId().equals(loginUser.getId())) {
            throw new Exception403("댓글을 삭제할 권한이 없습니다");
        }
        replyRepository.delete(reply);
    }
```

대상이 게시글에서 댓글로 바뀌었을 뿐, 로그인 확인과 작성자 아이디를 비교하는 소유자 검증은 챕터 4와 똑같습니다. 댓글 작성자가 아니라면 **Exception403**이 발생합니다.

`reply/ReplyController.java`에 아래와 같이 메서드를 추가합니다.

```java [실습 16] reply/ReplyController.java. 댓글 삭제 엔드포인트
    @DeleteMapping("/{replyId}")
    public ResponseEntity<?> deleteById(
            HttpServletRequest request, @PathVariable("replyId") Integer replyId) {
        User loginUser = (User) request.getAttribute("loginUser");
        replyService.댓글삭제(replyId, loginUser);
        return Resp.ok(null);
    }
```

삭제는 반환할 데이터가 없으므로 `Resp.ok(null)`로 성공만 응답합니다. 게시글과 똑같이 댓글도 로그인하지 않으면 401에서, 작성자가 아니면 403에서 막힙니다.

ssar로 로그인해 cos가 쓴 3번 댓글에 삭제를 요청합니다.

```json [Hoppscotch] 댓글 삭제
DELETE http://localhost:8080/api/replies/3
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9...
```

<!-- [CAPTURE NEEDED: 05_reply-delete-403
  path: assets/CH5/terminal/05_reply-delete-403.png
  desc: 두 장면을 위아래로 담은 캡처. (1) ssar 토큰으로 cos가 쓴 3번 댓글에 보낸 DELETE /api/replies/3 요청에 { "status": 403, "msg": "댓글을 삭제할 권한이 없습니다", "body": null }가 돌아오는 화면. (2) ssar이 쓴 1번 댓글에 보낸 DELETE /api/replies/1 요청이 200으로 성공하는 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH5/terminal/05_reply-delete-403.png)
*그림 5-8. 다른 사람이 쓴 댓글은 403으로 막히고, 본인이 쓴 댓글만 지워집니다*

댓글까지 되자 게시판이 완성됐습니다. 게시글을 쓰고 읽고 고치고 지우고, 게시글과 댓글은 작성자만 관리합니다.

*처음엔 하나도 설명할 수 없던 것들이었는데.*

오픈이는 챕터 1을 떠올렸습니다. 그때는 자바만으로 서버 뼈대를 만들다 학기가 끝날 상황이었고, 스프링에 올린 메서드가 요청 한 번에 저절로 실행되는 것이 마법처럼 보였습니다. 챕터 2에서는 저장하는 코드를 한 줄도 쓰지 않았는데 수정이 반영됐고, 방금은 조회 뒤에 select가 한 번 더 실행됐습니다. 이제는 각각을 이름으로 부를 수 있습니다. 메서드가 저절로 실행되는 것은 리플렉션이 어노테이션을 읽어 찾아 호출하는 것이고, 저장 없이 수정이 반영되는 것은 더티체킹이며, 조회 뒤에 select가 하나 더 붙는 것은 지연 로딩이 뒤늦게 데이터를 가져오기 때문입니다. 프레임워크는 더 이상 열어 볼 수 없는 블랙박스가 아니라, 안에서 어떤 규칙이 동작하는지 알고 사용하는 도구가 됐습니다.

:::remember
**이것만은 기억하자**

- **양방향 매핑에서 외래 키를 가진 쪽이 연관관계 주인입니다.** 댓글에 `board_id`가 있으므로 주인이고, 게시글은 `mappedBy`로 주인을 가리킵니다. **@OneToMany** 필드는 테이블 컬럼이 아니며, `cascade = REMOVE`를 붙이면 게시글을 지울 때 연관된 댓글도 함께 지워집니다.
- **즉시 로딩은 연관 엔티티를 함께 가져오고, 지연 로딩은 접근하는 순간 조회합니다.** 기본은 지연 로딩으로 두고, 한 번에 가져와야 하는 조회에서만 `join fetch`로 묶습니다. 댓글이 없는 게시글까지 조회하려면 `left join fetch`를 씁니다.
- **리플렉션에서 시작해 게시판 하나를 인증과 댓글까지 챙겨 완성했습니다.** 스프링이 대신 해 주던 일들의 이름을 이제 하나씩 부를 수 있습니다. 마법처럼 보이던 것은 리플렉션 위에 세운 규칙이었습니다.
:::
