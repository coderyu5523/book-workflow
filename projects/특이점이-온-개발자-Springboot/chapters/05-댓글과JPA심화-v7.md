# 챕터 5. 댓글과 JPA 심화

오픈이는 인증 게시판에 이어 댓글 기능을 추가하기로 했습니다. 게시글을 조회할 때 여러 개의 댓글을 함께 보여줘야 하고, 게시글과 댓글은 각각 작성자 정보를 가지고 있습니다.

댓글 테이블을 설계하던 오픈이는 머릿속이 복잡해졌습니다.

*게시글, 게시글 작성자, 여러 개의 댓글, 그리고 댓글 작성자들까지... 이 많은 데이터를 한 화면에 다 보여주려면 어떻게 가져와야 하지?*

오픈이는 선배를 찾아갔습니다.

**오픈이**: "선배님, 게시글 상세 화면에 댓글까지 추가되니까 데이터를 어떻게 가져와야 할지 막막하네요."

**선배**: "실무에서는 크게 두 가지 방법을 써요. **첫 번째는 쿼리를 두 번으로 나누는 겁니다**. 게시글과 게시글 작성자를 먼저 조회하고, 그다음 이 게시글에 있는 댓글과 댓글 작성자 번호를 추가로 가져오는 거죠. 그리고 두 데이터를 DTO에 담아 합치는 방식이에요. 구조가 단순해서 실무에서도 많이 씁니다."

**오픈이**: "그럼 두 번째 방법은요?"

**선배**: "**JPA의 양방향 매핑을 쓰는 거예요**. 데이터베이스 테이블은 외래 키 하나로 양방향 조인이 가능하지만, 자바 객체는 참조하는 쪽으로만 갈 수 있는 일방통행이거든요. 그래서 양방향 매핑으로 게시글 객체 쪽에서도 댓글을 참조할 수 있게 열어주는 거예요. 이렇게 해두면 JPA에서 조인을 통해 한 번에 데이터를 가져올 수 있어요."

:::goal
**이번 챕터가 끝나면**

- **양방향 매핑**으로 게시글과 댓글이 서로를 참조하게 만들 수 있습니다
- **즉시 로딩과 지연 로딩**의 차이를 이해할 수 있습니다
- **join fetch**로 연관된 데이터를 한 번에 조회할 수 있습니다
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
│   ├── Board.java                        # [작성] @OneToMany replies, 작성자 지연 로딩
│   ├── BoardRepository.java              # [작성] findByIdJoinUserAndReplies
│   ├── BoardResponse.java                # [작성] DetailDTO에 replies
│   └── BoardService.java                 # [작성] 상세 조회를 join fetch로 교체
└── reply/
    ├── Reply.java                        # [작성] 댓글 엔티티(@ManyToOne user/board)
    ├── ReplyController.java              # [작성] 작성·삭제 엔드포인트
    ├── ReplyRepository.java              # [작성] JpaRepository 상속으로 저장·조회·삭제
    ├── ReplyRequest.java                 # [작성] 댓글 요청 DTO
    ├── ReplyResponse.java                # [작성] 댓글 응답 DTO
    └── ReplyService.java                 # [작성] 댓글 저장·삭제(소유자 검증)

spring-start/ch05/src/main/resources/
└── db/data.sql                           # [참고] 댓글 더미 데이터
```

챕터를 따라 코드를 채우고, 막히면 `spring-end`의 완성 코드를 참고하세요.
::::

## 5.1 양방향 매핑

먼저 게시글과 댓글의 관계를 알아보겠습니다. 하나의 게시글에는 여러 개의 댓글이 달릴 수 있습니다. 그리고 하나의 댓글은 하나의 게시글에만 속하므로, **게시글과 댓글은 1:N 관계입니다**.

관계형 데이터베이스에서는 외래 키가 어느 쪽에 있든 두 테이블을 조인하여 연관된 데이터를 가져올 수 있습니다. 예를 들어 외래 키가 댓글 테이블에 있으면, 조인으로 게시글과 댓글 데이터를 한 번에 조회할 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 720 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="board_tb와 reply_tb가 나란히 놓이고 두 박스를 잇는 직선의 양끝에 화살촉이 달려 있다. reply_tb에만 board_id 외래 키가 있다.">
  <defs>
    <marker id="c5tbl-two" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto-start-reverse"><path d="M0,0 L0,6 L8,3 z" fill="#334155"/></marker>
  </defs>
  <rect x="60" y="50" width="200" height="96" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="60" y="50" width="200" height="30" rx="10" fill="#eef2ff"/>
  <rect x="60" y="72" width="200" height="8" fill="#eef2ff"/>
  <text x="160" y="71" text-anchor="middle" font-size="15" font-family="monospace" font-weight="800" fill="#3730a3">board_tb</text>
  <text x="80" y="106" font-size="13" font-family="monospace" fill="#475569">id</text>
  <text x="80" y="130" font-size="13" font-family="monospace" fill="#475569">title</text>
  <rect x="460" y="50" width="200" height="124" rx="10" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <rect x="460" y="50" width="200" height="30" rx="10" fill="#fff4ed"/>
  <rect x="460" y="72" width="200" height="8" fill="#fff4ed"/>
  <text x="560" y="71" text-anchor="middle" font-size="15" font-family="monospace" font-weight="800" fill="#7b341e">reply_tb</text>
  <text x="480" y="106" font-size="13" font-family="monospace" fill="#475569">id</text>
  <text x="480" y="130" font-size="13" font-family="monospace" fill="#475569">comment</text>
  <text x="480" y="154" font-size="13" font-family="monospace" font-weight="800" fill="#c2410c">board_id</text>
  <path d="M260,98 H460" fill="none" stroke="#334155" stroke-width="2" marker-start="url(#c5tbl-two)" marker-end="url(#c5tbl-two)"/>
  <text x="284" y="88" text-anchor="middle" font-size="13" font-weight="800" fill="#334155">1</text>
  <text x="436" y="88" text-anchor="middle" font-size="13" font-weight="800" fill="#334155">N</text>
  <text x="360" y="206" text-anchor="middle" font-size="13" fill="#475569">외래 키 하나로 양쪽 모두 조인합니다</text>
</svg>
</div>

*그림 5-1. 테이블의 1:N 관계*

반면 자바 객체의 참조는 한 방향으로만 이루어집니다. **Reply** 객체에 **Board** 타입 필드를 두면 댓글에서 게시글을 참조할 수는 있지만, 반대로 **Board** 객체에는 댓글을 가리키는 필드가 없어 게시글에서 댓글에 접근할 수는 없습니다.

<div class="svg-figure">
<svg viewBox="0 0 720 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Board와 Reply가 나란히 놓이고, Reply의 board 필드에서 Board로 향하는 화살표 하나만 그려져 있다. Board 쪽에는 댓글을 가리키는 필드가 없다.">
  <defs>
    <marker id="c5obj-one" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#334155"/></marker>
  </defs>
  <rect x="60" y="50" width="200" height="96" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="60" y="50" width="200" height="30" rx="10" fill="#eef2ff"/>
  <rect x="60" y="72" width="200" height="8" fill="#eef2ff"/>
  <text x="160" y="71" text-anchor="middle" font-size="15" font-family="monospace" font-weight="800" fill="#3730a3">Board</text>
  <text x="80" y="106" font-size="13" font-family="monospace" fill="#475569">id</text>
  <text x="80" y="130" font-size="13" font-family="monospace" fill="#475569">title</text>
  <rect x="460" y="50" width="200" height="124" rx="10" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <rect x="460" y="50" width="200" height="30" rx="10" fill="#fff4ed"/>
  <rect x="460" y="72" width="200" height="8" fill="#fff4ed"/>
  <text x="560" y="71" text-anchor="middle" font-size="15" font-family="monospace" font-weight="800" fill="#7b341e">Reply</text>
  <text x="480" y="106" font-size="13" font-family="monospace" fill="#475569">id</text>
  <text x="480" y="130" font-size="13" font-family="monospace" fill="#475569">comment</text>
  <text x="480" y="154" font-size="13" font-family="monospace" font-weight="800" fill="#c2410c">Board board</text>
  <path d="M460,98 H260" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#c5obj-one)"/>
  <text x="360" y="88" text-anchor="middle" font-size="13" font-family="monospace" font-weight="800" fill="#334155">board</text>
  <text x="360" y="206" text-anchor="middle" font-size="13" fill="#475569">참조는 댓글에서 게시글 한 방향뿐입니다</text>
</svg>
</div>

*그림 5-2. 자바 객체의 한 방향 참조*

따라서 객체에서도 반대 방향으로 접근하려면 반대쪽 객체에도 참조를 위한 필드를 추가해야 합니다. JPA에서는 이런 방식을 **양방향 매핑(Bidirectional Mapping)** 이라고 합니다. 외래 키 참조를 위해 사용된 **@ManyToOne**과 짝을 이루도록, 반대편 객체에 **@OneToMany**를 추가하여 서로를 참조하게 만드는 방식입니다.

<div class="svg-figure">
<svg viewBox="0 0 720 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Board 박스에는 replies 필드가, Reply 박스에는 board 필드가 있다. Board에서 Reply로 향하는 위쪽 화살표에는 OneToMany가, Reply에서 Board로 향하는 아래쪽 화살표에는 ManyToOne이 적혀 있다.">
  <defs>
    <marker id="c5bi-l" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="c5bi-r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
  </defs>
  <rect x="30" y="40" width="230" height="100" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="2"/>
  <rect x="30" y="40" width="230" height="32" rx="10" fill="#eef2ff"/>
  <rect x="30" y="64" width="230" height="8" fill="#eef2ff"/>
  <text x="145" y="63" text-anchor="middle" font-size="16" font-weight="800" fill="#3730a3">Board</text>
  <text x="145" y="112" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#475569">List&lt;Reply&gt; replies</text>
  <rect x="460" y="40" width="230" height="100" rx="10" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <rect x="460" y="40" width="230" height="32" rx="10" fill="#fff4ed"/>
  <rect x="460" y="64" width="230" height="8" fill="#fff4ed"/>
  <text x="575" y="63" text-anchor="middle" font-size="16" font-weight="800" fill="#7b341e">Reply</text>
  <text x="575" y="112" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#475569">Board board</text>
  <path d="M260,80 H456" fill="none" stroke="#4f46e5" stroke-width="2" marker-end="url(#c5bi-r)"/>
  <text x="358" y="70" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#4f46e5">@OneToMany</text>
  <path d="M460,120 H264" fill="none" stroke="#ff7849" stroke-width="2" marker-end="url(#c5bi-l)"/>
  <text x="360" y="142" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#c2410c">@ManyToOne</text>
</svg>
</div>

*그림 5-3. 양방향 매핑*

### 5.1.1 댓글 엔티티

먼저 댓글 엔티티부터 정의합니다. 댓글 작성자 정보와 댓글이 포함된 게시글 정보를 위해 **User** 엔티티와 **Board** 엔티티를 필드로 추가합니다.

`reply/Reply.java`를 열어 아래와 같이 작성합니다.

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
    private User user;

    // 외래 키 필드
    @ManyToOne(fetch = FetchType.LAZY)
    private Board board;

    @CreationTimestamp
    private LocalDateTime createdAt;

    @Builder
    public Reply(Integer id, String comment, User user, Board board,
            LocalDateTime createdAt) {
        this.id = id;
        this.comment = comment;
        this.user = user;
        this.board = board;
        this.createdAt = createdAt;
    }
}
```

### 5.1.2 게시글에 댓글 목록 추가

양방향 매핑을 위해 **Board** 엔티티에 댓글 목록을 필드로 추가합니다.

양방향 참조를 설정할 때는 `mappedBy` 속성을 사용합니다. 한쪽 어노테이션에 `mappedBy`를 설정하고 상대방의 필드 이름을 명시해 주기만 하면 두 객체의 매핑이 연결됩니다.

`board/Board.java`를 열어 아래와 같이 작성자 필드를 변경하고 댓글 목록 필드를 추가합니다.

```java [실습 2] board/Board.java. 댓글 목록 추가와 작성자 필드 수정
    @ManyToOne(fetch = FetchType.LAZY)
    private User user;

    @OneToMany(mappedBy = "board", fetch = FetchType.LAZY, cascade = CascadeType.REMOVE)
    private List<Reply> replies = new ArrayList<>();
```

`cascade = CascadeType.REMOVE`를 설정하면 게시글을 삭제할 때 연관된 댓글도 함께 삭제됩니다. 두 필드에 함께 적은 `fetch`는 연관된 데이터를 언제 가져올지 정하는 속성으로, 다음 절에서 이어서 설명합니다.

### 5.1.3 더미 데이터

더미 데이터에 댓글을 추가합니다.

```sql [참고] resources/db/data.sql. 댓글 더미 데이터
insert into reply_tb(comment,board_id,user_id,created_at) values('comment1',1,1,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment2',1,1,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment3',1,2,now());
insert into reply_tb(comment,board_id,user_id,created_at) values('comment4',2,2,now());
```
## 5.2 즉시 로딩과 지연 로딩

JPA로 개발할 때의 대표적인 성능 문제는 당장 필요 없는 연관 데이터까지 함께 조회할 때 발생합니다. 회원 정보가 필요하지 않은 게시글 목록 화면을 예로 들어 보겠습니다. `findAll()`로 게시글 전체를 조회할 때 JPA가 연관된 회원 엔티티까지 가져온다면, 게시글 수만큼 회원 조회 쿼리가 추가로 실행됩니다. 결국 쓰지 않는 데이터 때문에 서버와 데이터베이스에 부하를 줍니다.

이러한 성능 저하를 막기 위해 JPA는 연관된 데이터를 **조회하는 시점에 한 번에 가져올지**, 아니면 **실제로 사용하는 시점에 조회할지**를 직접 지정할 수 있습니다.

### 5.2.1 즉시 로딩

**즉시 로딩(Eager Loading)** 은 특정 엔티티를 조회할 때 **연관된 엔티티의 데이터까지 한 번에 가져오는 방식**으로, **@ManyToOne** 어노테이션은 즉시 로딩이 기본 전략입니다. 그래서 속성을 별도로 지정하지 않으면, 게시글을 조회하는 순간 JPA가 회원 정보까지 조회해 **Board**의 `user` 필드에 채워 넣습니다.

이러한 설정 때문에 `findAll()`로 게시글 목록을 조회하면 문제가 발생합니다. JPA가 먼저 **board_tb**에서 게시글 목록을 읽어온 뒤, 각 게시글의 비어 있는 회원 정보를 채우기 위해 **user_tb**를 조회하는 쿼리를 따로 실행하기 때문입니다.

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
    <div><span class="tl-label">Hibernate:</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-hl">select u1_0.id, u1_0.created_at, u1_0.email, u1_0.password, u1_0.username</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;from user_tb u1_0</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;where u1_0.id=?<span class="tl-dim">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← 게시글마다 반복</span></div>
  </div>
</div>

*그림 5-4. 즉시 로딩으로 목록을 조회할 때의 쿼리*

### 5.2.2 지연 로딩

이러한 문제를 해결하기 위해 사용하는 방식이 **지연 로딩(Lazy Loading)** 입니다.

지연 로딩은 **기준이 되는 엔티티만 먼저 가져오고, 연관된 엔티티는 실제로 데이터에 접근하는 순간에 조회하는 방식**입니다. **@ManyToOne**의 `fetch` 속성을 LAZY로 설정하면 지연 로딩이 적용됩니다.

```java board/Board.java. 작성자 조회를 지연 로딩으로
    @ManyToOne(fetch = FetchType.LAZY)
    private User user;
```

LAZY로 설정하면 JPA는 게시글을 조회할 때 회원 엔티티 대신 외래 키(`user_id`)만 가져옵니다. 그리고 회원 정보가 필요한 시점에 외래 키를 사용해 쿼리를 실행합니다.

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">Hibernate:</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-hl">select b1_0.id, b1_0.content, b1_0.created_at, b1_0.title, b1_0.user_id</span></div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;from board_tb b1_0</div>
  </div>
</div>

*그림 5-5. 지연 로딩으로 목록을 조회할 때의 쿼리*

다만 지연 로딩은 연관된 엔티티에 접근할 때마다 조회 쿼리를 실행합니다. 연관된 엔티티를 함께 사용하는 조회에서는 접근하는 횟수만큼 쿼리가 추가로 실행되므로, 즉시 로딩과 마찬가지로 쿼리 수가 늘어납니다.

:::tip
**실무에서는 어떤 로딩 방식을 쓰는가**

연관된 데이터를 가져올 때 추가 쿼리가 계속해서 발생하는 문제를 방지하기 위해, 실무에서는 가급적 모든 연관관계를 지연 로딩으로 설정합니다. 두 엔티티를 항상 함께 사용하는 경우에 한해 즉시 로딩을 고려할 수 있지만, 기본적으로는 지연 로딩을 유지하면서 필요한 경우에만 쿼리(join fetch)를 통해 한 번에 가져오는 방식이 더 안전합니다. JPA에서 **@ManyToOne**의 기본 전략은 즉시 로딩(EAGER)이며, **@OneToMany**는 지연 로딩(LAZY)입니다.
:::

## 5.3 댓글 목록

이제 게시글 상세 화면에 댓글 목록을 추가해 보겠습니다.

게시글 상세 화면에서는 게시글과 게시글 작성자 정보, 그리고 댓글과 댓글 작성자 정보를 함께 가져와야 합니다. 이때 게시글의 작성자는 항상 존재하므로 INNER JOIN을 사용합니다. 반면 **댓글도 INNER JOIN을 사용하면 댓글이 없는 게시글은 조회되지 않으므로, LEFT OUTER JOIN을 사용해야 합니다**.

### 5.3.1 리포지토리

댓글 목록을 추가로 가져오기 위해 쿼리를 만들어 보겠습니다.

`board/BoardRepository.java`를 열어 아래와 같이 메서드를 작성합니다.

```java [실습 3] board/BoardRepository.java. 작성자와 댓글을 함께 가져오는 조회
    @Query("select b from Board b join fetch b.user left join fetch b.replies r "
            + "left join fetch r.user where b.id = :boardId")
    Optional<Board> findByIdJoinUserAndReplies(@Param("boardId") Integer boardId);
```

게시글 상세 화면의 응답 데이터에는 댓글 목록과 각 댓글 작성자 정보가 모두 포함되어야 합니다. 만약 fetch 없이 일반 조인만 사용하면 댓글과 작성자 정보는 지연 로딩으로 조회되어, **댓글과 작성자 정보를 실제로 사용하는 시점에 추가 쿼리가 실행**됩니다. 따라서 댓글과 댓글 작성자 정보도 join fetch를 사용하여 게시글과 함께 한 번에 가져옵니다.

### 5.3.2 응답 DTO

다음으로 데이터베이스에서 조회된 결과를 담을 수 있도록 DTO를 수정해 보겠습니다. 하나의 게시글에는 여러 개의 댓글이 있을 수 있으므로 DTO 내부에 **List** 타입의 DTO 필드를 추가하여 하나씩 담습니다.

`board/BoardResponse.java`의 **DetailDTO**를 아래와 같이 변경합니다.

```java [실습 4] board/BoardResponse.java. 상세에 댓글 목록 추가
    public record DetailDTO(
            Integer boardId,
            String title,
            String content,
            Integer userId,
            String username,
            Boolean isOwner,
            // List 타입의 댓글 DTO 필드
            List<ReplyDTO> replies) {

        public DetailDTO(Board board, User loginUser) {
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(),
                    board.getUser().getUsername(),
                    // 비로그인이면 false, 요청자와 작성자가 같으면 true
                    loginUser != null
                            && loginUser.getId().equals(board.getUser().getId()),
                    // 댓글 엔티티를 하나씩 ReplyDTO로 변환해 List에 담기
                    board.getReplies().stream()
                            .map(reply -> new ReplyDTO(reply, loginUser))
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
                        // 비로그인이면 false, 요청자와 작성자가 같으면 true
                        loginUser != null
                                && loginUser.getId().equals(reply.getUser().getId()));
            }
        }
    }
```

### 5.3.3 서비스

**BoardService**의 상세 메서드는 `findByIdJoinUser()` 대신 `findByIdJoinUserAndReplies()`를 호출합니다.

`board/BoardService.java`를 아래와 같이 변경합니다.

```java [실습 5] board/BoardService.java. 상세 조회를 join fetch로 교체
    public BoardResponse.DetailDTO 게시글상세(Integer boardId, User loginUser) {
        Board board = boardRepository.findByIdJoinUserAndReplies(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board, loginUser);
    }
```

ssar로 로그인해 게시글 상세 API를 호출하면 결과를 확인할 수 있습니다.

```json [Hoppscotch] 게시글 상세 조회
GET http://localhost:8080/api/boards/1
```

<!-- [CAPTURE NEEDED: 03_board-detail-with-replies
  path: assets/CH5/terminal/03_board-detail-with-replies.png
  desc: ssar로 로그인해 발급받은 토큰을 Authorization 헤더에 담고 보낸 GET /api/boards/1 요청에 대한 200 응답. body에 게시글(boardId 1, title1, content1, userId 1, username ssar)과 isOwner true가 담기고, replies 배열에 댓글 세 개(replyId 1·2는 ssar이 써서 isOwner true, replyId 3은 cos이 써서 isOwner false)가 이어지는 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH5/terminal/03_board-detail-with-replies.png)
*그림 5-6. 댓글이 담긴 상세 응답*

## 5.4 댓글 추가

### 5.4.1 리포지토리

댓글 추가 기능을 위해 Repository를 구현해야 합니다.

`reply/ReplyRepository.java`를 열어 아래와 같이 작성합니다.

```java [실습 6] reply/ReplyRepository.java. JpaRepository 상속
public interface ReplyRepository extends JpaRepository<Reply, Integer> {
}
```

### 5.4.2 요청 DTO

**SaveDTO**는 댓글 내용과 대상 게시글의 번호를 받고, 작성자 정보는 필터가 JWT를 확인해 요청 객체에 담아 둔 로그인 회원 정보를 사용합니다.

`reply/ReplyRequest.java`를 열어 아래와 같이 작성합니다.

```java [실습 7] reply/ReplyRequest.java. 댓글 요청 DTO
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

### 5.4.3 응답 DTO

댓글을 추가한 결과를 응답으로 반환할 **DTO**도 정의합니다.

`reply/ReplyResponse.java`를 열어 아래와 같이 작성합니다.

```java [실습 8] reply/ReplyResponse.java. 댓글 응답 DTO
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

### 5.4.4 서비스

서비스는 요청으로 받은 게시글 번호로 게시글을 조회합니다. 그리고 조회한 게시글과 로그인 회원 정보로 댓글 엔티티를 생성해 저장합니다.

`reply/ReplyService.java`를 열어 아래와 같이 작성합니다.

```java [실습 9] reply/ReplyService.java. 댓글 저장
@RequiredArgsConstructor
@Service
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;

    @Transactional
    public ReplyResponse.DTO 댓글추가(ReplyRequest.SaveDTO requestDTO, User loginUser) {
        // 1. 넘어온 유저가 없으면 로그인하지 않은 요청이다
        if (loginUser == null) {
            throw new Exception401("로그인이 필요합니다");
        }
        // 2. 댓글을 달 게시글을 찾아 연결한다
        Board board = boardRepository.findById(requestDTO.boardId())
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        Reply savedReply = replyRepository.save(requestDTO.toEntity(loginUser, board));
        return new ReplyResponse.DTO(savedReply);
    }
}
```

### 5.4.5 컨트롤러

마지막으로 댓글 작성 엔드포인트를 구현합니다.

`reply/ReplyController.java`를 열어 아래와 같이 작성합니다.

```java [실습 10] reply/ReplyController.java. 댓글 작성 엔드포인트
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/replies")
public class ReplyController {

    private final ReplyService replyService;

    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @RequestBody ReplyRequest.SaveDTO requestDTO) {
        User loginUser = (User) request.getAttribute("loginUser");
        ReplyResponse.DTO respDTO = replyService.댓글추가(requestDTO, loginUser);
        return Resp.ok(respDTO);
    }
}
```

ssar로 로그인해 1번 게시글에 댓글을 답니다.

```json [Hoppscotch] 댓글 작성
POST http://localhost:8080/api/replies

{
  "comment": "comment5",
  "boardId": 1
}
```

<!-- [CAPTURE NEEDED: 04_reply-save
  path: assets/CH5/terminal/04_reply-save.png
  desc: ssar 토큰을 Authorization 헤더에 담고 보낸 POST /api/replies 요청에 대한 200 응답. body에 replyId 5, comment "comment5", username ssar이 담긴 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH5/terminal/04_reply-save.png)
*그림 5-7. 댓글 추가 응답*

## 5.5 댓글 삭제

댓글 삭제는 로그인 여부를 확인하고, 댓글 작성자와 요청자가 같은지 검증한 뒤 삭제합니다. 반환할 데이터가 없으므로 성공만 응답합니다.

### 5.5.1 서비스

`reply/ReplyService.java`에 아래와 같이 메서드를 추가합니다.

```java [실습 11] reply/ReplyService.java. 댓글 삭제
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

### 5.5.2 컨트롤러

`reply/ReplyController.java`에 아래와 같이 메서드를 추가합니다.

```java [실습 12] reply/ReplyController.java. 댓글 삭제 엔드포인트
    @DeleteMapping("/{replyId}")
    public ResponseEntity<?> deleteById(
            HttpServletRequest request, @PathVariable("replyId") Integer replyId) {
        User loginUser = (User) request.getAttribute("loginUser");
        replyService.댓글삭제(replyId, loginUser);
        return Resp.ok(null);
    }
```

ssar로 로그인해 cos가 쓴 3번 댓글에 삭제를 요청합니다.

```json [Hoppscotch] 댓글 삭제
DELETE http://localhost:8080/api/replies/3
```

<!-- [CAPTURE NEEDED: 05_reply-delete-403
  path: assets/CH5/terminal/05_reply-delete-403.png
  desc: 두 장면을 위아래로 담은 캡처. (1) ssar 토큰으로 cos가 쓴 3번 댓글에 보낸 DELETE /api/replies/3 요청에 { "status": 403, "msg": "댓글을 삭제할 권한이 없습니다", "body": null }가 돌아오는 화면. (2) ssar이 쓴 1번 댓글에 보낸 DELETE /api/replies/1 요청이 200으로 성공하는 화면. Hoppscotch 또는 브라우저 응답.
] -->
![](../assets/CH5/terminal/05_reply-delete-403.png)
*그림 5-8. 댓글 삭제 응답*

오픈이는 1번 게시글의 상세 조회를 다시 호출했습니다. 게시글과 작성자, 그 아래 댓글 목록까지 응답 하나에 담겨 돌아옵니다.

**선배**: "한 번의 조회로 다 나오네요."

게시글만 있던 게시판에 댓글이 붙었습니다. 게시글과 댓글은 각각 작성자를 가지고, 로그인한 사람만 자기가 쓴 것을 고치고 지울 수 있습니다.

:::remember
**이것만은 기억하자**

- **객체는 참조 필드가 있어야 접근할 수 있으므로 양방향 매핑을 설정합니다.** 테이블은 외래 키 하나로 양쪽을 조인하지만, 객체는 게시글 쪽에 댓글 필드를 추가해야 게시글에서 댓글을 참조할 수 있습니다.
- **연관된 엔티티를 함께 조회할 때는 조인을 활용해 쿼리를 최적화합니다.** 불필요한 데이터 조회를 막기 위해 평소에는 지연 로딩을 기본으로 하고, 게시글과 댓글을 동시에 화면에 반환해야 할 때만 조인으로 묶어서 한 번에 가져옵니다.
- **자식 데이터가 존재하지 않을 수 있는 관계는 LEFT OUTER JOIN을 사용합니다.** INNER JOIN을 쓰면 댓글이 없는 게시글은 조회 결과에서 누락됩니다. 따라서 외부 조인으로 가져온 뒤, 게시글 응답 객체 내부에 댓글 목록을 중첩하여 반환합니다.
:::