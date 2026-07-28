# 챕터 5. 댓글과 JPA 심화 - 연결하고, 빨라진다

게시판은 이제 글을 쓰고 읽고 고치고 지우는 데까지 왔고, 로그인한 본인만 자기 글을 건드립니다. 그런데 정작 게시판다운 것 하나가 비어 있습니다. 글 아래 댓글 입력칸에는 아무것도 달리지 않습니다.

글은 그 자체로 하나의 자원입니다. 하지만 댓글은 다릅니다. "누구의 어느 글에 달린 댓글인가"가 빠지면 댓글은 공중에 뜬 문장일 뿐입니다. 그래서 댓글을 만들려면, 먼저 댓글이 어느 글에 매달리는지부터 정해야 합니다. 이 이음새를 어떻게 잡아야 할지 감이 서지 않을 때, 선배가 방향을 하나 던져 줍니다.

**선배**: "댓글은 글에 붙이는 포스트잇 같은 거예요. 포스트잇마다 '몇 번 글에 붙는다'가 적혀 있고, 글이 사라지면 거기 붙은 포스트잇도 같이 사라져야 하잖아요. 그렇게 글과 댓글이 서로를 아는 관계를 만들어 두면 돼요."

포스트잇으로 관계를 잡아 두면, 게시글 상세를 부를 때 그 글에 붙은 댓글이 함께 나와야 합니다. 그런데 이 "함께 나오는 조회"가 뒤에서 문제를 일으킵니다.

<div class="svg-figure">
<svg viewBox="0 0 1000 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 5 한눈에 보기. 게시글 상세를 요청하면 글에 작성자와 댓글이 딸려 온다. 이 조회를 지연 로딩에 맡기면 작성자와 댓글을 꺼낼 때마다 쿼리가 붙어 1 더하기 N개가 되고, fetch join으로 묶으면 한 번의 조회로 작성자와 댓글까지 가져와 쿼리 하나로 끝난다.">
  <defs>
    <marker id="c5ov-i" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c5ov-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="500" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">챕터 5 한눈에 보기 - 연관관계부터 조회 성능까지</text>
  <text x="40" y="70" font-size="12" font-weight="700" fill="#475569">1단계 · 글에 작성자와 댓글이 딸린다</text>
  <rect x="40" y="82" width="150" height="64" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="115" y="110" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">클라이언트</text>
  <text x="115" y="130" text-anchor="middle" font-size="11" fill="#6b7280">상세 요청</text>
  <rect x="360" y="72" width="300" height="86" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="510" y="98" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">게시글(Board)</text>
  <rect x="378" y="112" width="128" height="32" rx="5" fill="#fff" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="442" y="132" text-anchor="middle" font-size="11" fill="#334155">작성자(User)</text>
  <rect x="516" y="112" width="128" height="32" rx="5" fill="#fff" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="580" y="132" text-anchor="middle" font-size="11" fill="#334155">댓글(Reply) 목록</text>
  <line x1="190" y1="114" x2="358" y2="114" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#c5ov-i)"/>
  <text x="274" y="106" text-anchor="middle" font-size="11" font-weight="600" fill="#4f46e5">GET /api/boards/1</text>
  <text x="40" y="206" font-size="12" font-weight="700" fill="#475569">2단계 · 이 조회를 어떻게 가져오나</text>
  <line x1="450" y1="158" x2="300" y2="234" stroke="#ff7849" stroke-width="1.7" stroke-dasharray="4,4" marker-end="url(#c5ov-s)"/>
  <line x1="570" y1="158" x2="700" y2="234" stroke="#4f46e5" stroke-width="1.7" marker-end="url(#c5ov-i)"/>
  <rect x="110" y="238" width="370" height="150" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.9"/>
  <text x="295" y="268" text-anchor="middle" font-size="14" font-weight="800" fill="#c2410c">지연 로딩</text>
  <text x="295" y="298" text-anchor="middle" font-size="12" fill="#334155">작성자와 댓글을 꺼낼 때마다</text>
  <text x="295" y="318" text-anchor="middle" font-size="12" fill="#334155">select가 하나씩 더 나간다</text>
  <rect x="185" y="336" width="220" height="38" rx="8" fill="#fff7ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="295" y="360" text-anchor="middle" font-size="13" font-weight="800" fill="#c2410c">합계 쿼리 1 + N개</text>
  <rect x="520" y="238" width="370" height="150" rx="10" fill="#fff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="705" y="268" text-anchor="middle" font-size="14" font-weight="800" fill="#3730a3">fetch join</text>
  <text x="705" y="298" text-anchor="middle" font-size="12" fill="#334155">글·작성자·댓글을 묶어</text>
  <text x="705" y="318" text-anchor="middle" font-size="12" fill="#334155">한 번의 조회로 가져온다</text>
  <rect x="595" y="336" width="220" height="38" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="705" y="360" text-anchor="middle" font-size="13" font-weight="800" fill="#3730a3">합계 쿼리 1개</text>
</svg>
</div>

*그림 5-1. 게시글 상세를 부르면 글에 작성자와 댓글이 딸려 오고, 그 조회를 지연 로딩에 맡기면 쿼리가 1+N개로 불어나지만 fetch join으로 묶으면 하나로 끝납니다*

:::goal
**이번 챕터가 끝나면**

- 양방향 연관관계와 연관관계 주인이 무엇인지 설명할 수 있습니다
- `@OneToMany`와 cascade로 게시글에 댓글을 연결하고, 게시글을 지우면 댓글도 함께 지웁니다
- 지연 로딩이 왜 쿼리를 늘리는지 이해하고, fetch join으로 조회를 한 번에 끝냅니다
:::

## 5.1 댓글은 글에 딸린다

### 5.1.1 양방향 연관관계와 주인

포스트잇에는 저마다 "어느 글의 것"이라는 표시가 적혀 있습니다. 글은 자기에게 붙은 포스트잇이 몇 장인지 일일이 들고 있지 않아도 됩니다. 각 포스트잇이 자기가 어느 글 소속인지 알고 있으니, 그 표시만 따라가면 글에 붙은 포스트잇을 전부 모을 수 있습니다.

이 관계를 자바 객체로 옮기면 양쪽이 서로를 가리킵니다. 게시글은 자기에게 달린 댓글 목록을 가지고, 댓글은 자기가 붙은 게시글을 가집니다. 이렇게 두 엔티티가 서로를 참조하는 관계를 양방향 연관관계(Bidirectional Relationship)라고 합니다.

그런데 데이터베이스는 이 관계를 한 곳에만 저장합니다. 포스트잇에 "몇 번 글"이라고 적는 것처럼, `reply_tb`에 `board_id` 칸을 두고 거기에 소속 글의 기본 키를 담습니다. 이 외래 키를 실제로 들고 있는 쪽, 즉 댓글이 이 관계의 연관관계 주인(Owner)입니다. 게시글 쪽은 외래 키를 갖지 않고, "이 관계는 댓글의 `board` 필드가 관리한다"고 표시만 해 둡니다. 이 표시가 `mappedBy`입니다.

포스트잇 비유에는 하나가 더 있습니다. 글이 사라지면 거기 붙은 포스트잇도 같이 사라져야 한다는 것입니다. 게시글을 지울 때 그 글에 달린 댓글이 데이터베이스에 그대로 남으면 주인 없는 댓글이 됩니다. 그래서 게시글을 지우면 딸린 댓글까지 함께 지워지도록 삭제를 댓글에 전이시킵니다. 이렇게 부모 엔티티의 작업을 자식 엔티티에 함께 적용하는 것을 영속성 전이(cascade)라고 합니다.

<div class="svg-figure">
<svg viewBox="0 0 820 390" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="게시글과 댓글의 연관관계. 가운데 위 게시글(Board) 공지 한 장 아래로 댓글(Reply) 포스트잇 세 장이 매달려 있고, 각 포스트잇은 자기가 어느 글에 붙는지 화살표로 게시글을 가리킨다. 이 참조를 가진 댓글이 연관관계 주인이다. 게시글에서 포스트잇으로 가는 화살표는 얇고 흐리며, 글을 떼면 포스트잇도 함께 떨어진다.">
  <defs>
    <marker id="c5rel-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
    <marker id="c5rel-b" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#cbd5e1"/></marker>
  </defs>
  <circle cx="410" cy="50" r="6" fill="#94a3b8"/>
  <rect x="300" y="56" width="220" height="112" rx="6" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="410" y="90" text-anchor="middle" font-size="14" font-weight="800" fill="#0f172a">게시글 (Board)</text>
  <text x="410" y="118" text-anchor="middle" font-size="12" fill="#334155">제목 · 내용</text>
  <text x="410" y="146" text-anchor="middle" font-size="11" fill="#6b7280">댓글을 모아 보여 준다</text>
  <g transform="rotate(-4 251 300)">
    <rect x="196" y="252" width="110" height="96" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
    <text x="251" y="290" text-anchor="middle" font-size="12" font-weight="800" fill="#7b341e">댓글 1</text>
    <text x="251" y="318" text-anchor="middle" font-size="11" fill="#7b341e">→ 1번 글</text>
  </g>
  <g transform="rotate(3 410 300)">
    <rect x="355" y="252" width="110" height="96" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
    <text x="410" y="290" text-anchor="middle" font-size="12" font-weight="800" fill="#7b341e">댓글 2</text>
    <text x="410" y="318" text-anchor="middle" font-size="11" fill="#7b341e">→ 1번 글</text>
  </g>
  <g transform="rotate(-2 569 300)">
    <rect x="514" y="252" width="110" height="96" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
    <text x="569" y="290" text-anchor="middle" font-size="12" font-weight="800" fill="#7b341e">댓글 3</text>
    <text x="569" y="318" text-anchor="middle" font-size="11" fill="#7b341e">→ 1번 글</text>
  </g>
  <line x1="255" y1="250" x2="360" y2="172" stroke="#4f46e5" stroke-width="1.7" marker-end="url(#c5rel-a)"/>
  <line x1="410" y1="248" x2="410" y2="172" stroke="#4f46e5" stroke-width="1.7" marker-end="url(#c5rel-a)"/>
  <line x1="565" y1="250" x2="462" y2="172" stroke="#4f46e5" stroke-width="1.7" marker-end="url(#c5rel-a)"/>
  <line x1="330" y1="168" x2="285" y2="246" stroke="#cbd5e1" stroke-width="1.3" stroke-dasharray="4,3" marker-end="url(#c5rel-b)"/>
  <text x="700" y="214" text-anchor="middle" font-size="11" font-weight="700" fill="#3730a3">연관관계 주인</text>
  <text x="700" y="232" text-anchor="middle" font-size="10" fill="#6b7280">댓글이 글을 가리킨다</text>
  <text x="628" y="96" text-anchor="middle" font-size="10" fill="#6b7280">글을 떼면</text>
  <text x="628" y="110" text-anchor="middle" font-size="10" fill="#6b7280">댓글도 함께 (cascade)</text>
  <text x="410" y="378" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">댓글 (Reply)</text>
</svg>
</div>
*그림 5-2. 댓글은 자기가 어느 글에 붙는지 표시를 들고 있고(연관관계 주인), 게시글은 그 표시를 따라 댓글을 모읍니다*

### 5.1.2 이번 챕터에서 만드는 것

| 클래스 | 역할 |
|--------|------|
| Reply (신규) | 댓글 한 건을 표현하는 엔티티. `reply_tb`와 매핑되고, 작성자와 게시글을 각각 `@ManyToOne`으로 가집니다. |
| ReplyRepository (신규) | `EntityManager`로 댓글을 저장하고 조회하고 삭제합니다. |
| ReplyRequest · ReplyResponse (신규) | 댓글 작성 요청과 응답을 담는 DTO입니다. |
| ReplyService (신규) | 댓글 저장(대상 글 조회)과 삭제(소유자 검증)를 처리합니다. |
| ReplyController (신규) | `/api/replies` 작성·삭제 엔드포인트를 제공합니다. |
| Board (변경) | 댓글 목록 `replies`가 추가되고, 작성자 조회가 지연 로딩으로 바뀝니다. |
| BoardRepository (변경) | 작성자와 댓글을 함께 가져오는 `findByIdJoinUserAndReply`가 추가됩니다. |
| BoardResponse (변경) | 상세 응답에 댓글 목록과 `isOwner`가 추가됩니다. |
| BoardService · BoardController (변경) | 상세가 `sessionUserId`를 받아 `isOwner`를 계산하고, 비로그인도 처리합니다. |
| WebMvcConfig (변경) | 인터셉터 보호 경로에 `/api/replies`가 더해집니다. |

::::prep
**소스코드 준비**

앞 챕터에서 클론한 예제 저장소에서 이번 챕터 폴더로 이동합니다. 패키지 루트는 앞 챕터와 같은 `com.metacoding.spring`입니다.

```bash [터미널] 챕터 5 폴더로 이동
cd spring-start/ch05
```

이번 챕터에서 새로 만들거나 고치는 파일은 다음과 같습니다.

```
spring-start/ch05  (신규·변경)
├── reply/Reply.java                      [설명] 댓글 엔티티(@ManyToOne user/board)
├── reply/ReplyRepository.java            [설명] EntityManager로 저장·조회·삭제
├── reply/ReplyRequest.java, ReplyResponse.java [참고] 댓글 DTO
├── reply/ReplyService.java               [실습] 댓글 저장·삭제(소유자 검증)
├── reply/ReplyController.java            [실습] 작성·삭제 엔드포인트
├── core/config/WebMvcConfig.java         [변경] 인터셉터에 /api/replies 추가
├── board/Board.java                      [실습] @OneToMany replies, user EAGER→LAZY
├── board/BoardRepository.java            [실습] findByIdJoinUserAndReply(fetch join)
├── board/BoardResponse.java              [설명] DetailDTO에 replies·isOwner
├── board/BoardService.java, BoardController.java [설명] 상세에 sessionUserId
└── test/board/BoardRepositoryTest.java   [실습] fetch 5단계(EAGER 토글 포함)
```

챕터를 따라 코드를 채우고, 막히면 `spring-end`의 완성 코드를 참고하세요.
::::

### 5.1.3 댓글 엔티티와 목록 매핑

먼저 댓글 엔티티부터 만듭니다. 댓글은 작성자와 게시글을 각각 참조하므로 두 개의 `@ManyToOne`을 가집니다. `reply/Reply.java`를 열고 아래 코드를 작성합니다.

```java [설명] reply/Reply.java. 댓글 엔티티
@NoArgsConstructor
@Data
@Entity
@Table(name = "reply_tb")
public class Reply {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String comment;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "board_id")
    private Board board;

    @CreationTimestamp
    private Timestamp createdAt;

    @Builder
    public Reply(Integer id, String comment, User user, Board board, Timestamp createdAt) {
        this.id = id;
        this.comment = comment;
        this.user = user;
        this.board = board;
        this.createdAt = createdAt;
    }
}
```

댓글 하나는 누가 썼는지(`user`)와 어느 글에 달렸는지(`board`)를 함께 담습니다. 댓글 여러 개가 한 명의 회원에 속하고 한 게시글에 속하므로 두 필드 모두 `@ManyToOne`입니다. 여기서 `@JoinColumn(name = "board_id")`이 앞서 말한 그 표시입니다. `reply_tb`에 `board_id` 칸을 두고 소속 글의 기본 키를 담으니, 외래 키를 든 이 댓글이 연관관계 주인입니다. 두 필드에 붙은 `fetch = FetchType.LAZY`는 지연 로딩 설정인데, 이것이 이번 챕터 후반의 핵심이 되므로 지금은 붙여만 두고 5.3에서 제대로 다룹니다.

이제 게시글 쪽에 반대 방향을 답니다. `board/Board.java`를 열고 TODO의 `pass`를 지우고 아래 필드를 추가합니다.

```java [실습 1] board/Board.java. 댓글 목록 연관관계 추가
    // 이 관계의 주인은 Reply의 board 필드다. Board는 목록만 비춰 본다
    @OneToMany(mappedBy = "board", fetch = FetchType.LAZY, cascade = CascadeType.REMOVE)
    private List<Reply> replies = new ArrayList<>();
```

게시글 하나에 댓글 여러 개가 달리므로 `@OneToMany`이고, `mappedBy = "board"`로 "이 관계의 주인은 `Reply`의 `board` 필드"라고 밝힙니다. 게시글은 외래 키를 갖지 않고 댓글의 `board_id`를 거꾸로 따라가 `replies`에 채우므로, 이 `replies`는 테이블 컬럼으로 생기지 않습니다. 뒤에 붙인 `cascade = CascadeType.REMOVE`가 영속성 전이여서, 게시글을 지우면 딸린 댓글까지 함께 지워집니다. `replies`를 `new ArrayList<>()`로 초기화하면 댓글이 없는 글도 빈 목록을 가집니다.

## 5.2 댓글을 쓰고 지운다

### 5.2.1 리포지토리와 DTO

두 엔티티를 연관관계로 연결했으니, 이제 댓글을 실제로 쓰고 지우는 부분을 만듭니다. 구조는 게시글을 만들 때와 같아서, 리포지토리로 저장하고 서비스가 흐름을 맡고 컨트롤러가 요청을 받습니다.

먼저 댓글을 저장하고 꺼내는 리포지토리입니다. `reply/ReplyRepository.java`를 열고 아래 코드를 작성합니다.

```java [설명] reply/ReplyRepository.java. EntityManager로 저장·조회·삭제
@RequiredArgsConstructor
@Repository
public class ReplyRepository {
    private final EntityManager em;

    public void save(Reply reply) {
        em.persist(reply);
    }

    public Optional<Reply> findById(Integer replyId) {
        return Optional.ofNullable(em.find(Reply.class, replyId));
    }

    public void delete(Reply reply) {
        em.remove(reply);
    }
}
```

2장에서 만든 `BoardRepository`와 같은 모양입니다. 댓글은 목록을 따로 조회하지 않는데, 게시글 상세를 부를 때 글과 함께 나가기 때문입니다.

요청과 응답을 담을 그릇도 앞 챕터의 방식을 그대로 씁니다. `reply/ReplyRequest.java`와 `reply/ReplyResponse.java`는 각각 이렇게 되어 있습니다.

```java [참고] reply/ReplyRequest.java, ReplyResponse.java. 댓글 DTO
public class ReplyRequest {
    public record SaveDTO(
            @NotEmpty(message = "댓글 내용을 입력해주세요") String comment,
            @NotNull(message = "게시글 번호가 필요합니다") Integer boardId) {
        // 로그인 유저와 대상 글을 받아 엔티티로 만든다
        public Reply toEntity(User user, Board board) {
            return Reply.builder().comment(comment).user(user).board(board).build();
        }
    }
}

public class ReplyResponse {
    public record DTO(Integer replyId, String comment, String username) {
        public DTO(Reply reply) {
            this(reply.getId(), reply.getComment(), reply.getUser().getUsername());
        }
    }
}
```

`SaveDTO`는 댓글 내용과 어느 글에 달지(`boardId`)를 받고, `toEntity`는 4장에서 게시글을 만들 때처럼 로그인 유저와 대상 글을 넘겨받아 댓글 엔티티로 옮겨 담습니다. `DTO`는 응답으로 나갈 댓글 하나를 담는 그릇입니다.

### 5.2.2 서비스와 컨트롤러

부품이 준비됐으니 서비스에 조립합니다. `reply/ReplyService.java`를 열고 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```java [실습 2] reply/ReplyService.java. 댓글 저장과 삭제
@RequiredArgsConstructor
@Service
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;

    // 1. 댓글 작성. 대상 글을 찾아 댓글을 연결해 저장한다
    @Transactional
    public ReplyResponse.DTO 댓글쓰기(ReplyRequest.SaveDTO requestDTO, User sessionUser) {
        // TODO: 대상 글 조회 → 엔티티 생성 → 저장
        Board board = boardRepository.findById(requestDTO.boardId())
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        Reply reply = requestDTO.toEntity(sessionUser, board);
        replyRepository.save(reply);
        return new ReplyResponse.DTO(reply);
    }

    // 2. 댓글 삭제. 작성자 본인만 지울 수 있다
    @Transactional
    public void 댓글삭제(Integer replyId, Integer sessionUserId) {
        // TODO: 조회 → 소유자 검증 → 삭제
        Reply reply = replyRepository.findById(replyId)
                .orElseThrow(() -> new Exception404("댓글을 찾을 수 없습니다"));
        if (!reply.getUser().getId().equals(sessionUserId)) {
            throw new Exception403("댓글을 삭제할 권한이 없습니다");
        }
        replyRepository.delete(reply);
    }
}
```

`댓글쓰기`는 `boardId`로 댓글을 달 글을 찾아, 없으면 `Exception404`를 던지고 있으면 `toEntity`로 로그인 유저와 그 글을 붙인 댓글을 만들어 저장합니다. `댓글삭제`는 대상이 글에서 댓글로 바뀌었을 뿐, 작성자 아이디를 견주는 소유자 검증은 4장과 똑같습니다.

두 서비스를 바깥과 연결하는 컨트롤러를 만듭니다. `reply/ReplyController.java`를 열고 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```java [실습 3] reply/ReplyController.java. 댓글 작성·삭제 엔드포인트
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/replies")
public class ReplyController {

    private final ReplyService replyService;

    // 1. 댓글 작성 (POST /api/replies)
    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @Valid @RequestBody ReplyRequest.SaveDTO requestDTO) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        ReplyResponse.DTO respDTO = replyService.댓글쓰기(requestDTO, sessionUser);
        return Resp.ok(respDTO);
    }

    // 2. 댓글 삭제 (DELETE /api/replies/1)
    @DeleteMapping("/{replyId}")
    public ResponseEntity<?> deleteById(HttpServletRequest request, @PathVariable("replyId") Integer replyId) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        replyService.댓글삭제(replyId, sessionUser.getId());
        return Resp.ok(null);
    }
}
```

두 엔드포인트 모두 `request.getAttribute("sessionUser")`로 로그인 유저를 꺼냅니다. 4장에서 필터가 달아 둔 그 이름표입니다. 작성은 그 유저를 작성자로 붙여 저장하고, 삭제는 그 유저의 아이디를 소유자 검증에 넘깁니다.

댓글 쓰기와 삭제도 로그인한 사람만 하도록 막아야 합니다. 4장에서 만든 인터셉터가 게시글 주소만 지키고 있으므로, `core/config/WebMvcConfig.java`의 `addPathPatterns`에 `/api/replies`와 그 하위 경로를 더합니다.

```java [실습 4] core/config/WebMvcConfig.java. 보호 경로에 댓글 추가
    registry.addInterceptor(new AuthInterceptor())
            .addPathPatterns("/api/boards", "/api/boards/**",
                    "/api/replies", "/api/replies/**"); // 댓글 주소도 보호
```

그러면 게시글과 똑같이 댓글 쓰기와 삭제도 로그인하지 않으면 인터셉터에서 401로 막힙니다.

### 5.2.3 상세 응답에 댓글 담기

댓글은 저장했지만 아직 화면에서 보이지 않습니다. 댓글은 게시글 상세에 함께 나가야 하는데, 5.1에서 게시글에 `replies` 목록을 달아 두었으니 상세 응답 그릇에 그 목록을 담습니다. `board/BoardResponse.java`의 `DetailDTO`를 아래처럼 고칩니다.

```java [설명] board/BoardResponse.java. 상세에 댓글 목록과 작성자 여부 추가
    public record DetailDTO(Integer boardId, String title, String content, Integer userId,
            String username, Boolean isOwner, List<ReplyDTO> replies) {
        public DetailDTO(Board board, Integer sessionUserId) {
            this(board.getId(), board.getTitle(), board.getContent(), board.getUser().getId(),
                    board.getUser().getUsername(), checkOwner(sessionUserId, board.getUser().getId()),
                    board.getReplies().stream().map(r -> new ReplyDTO(r, sessionUserId)).toList());
        }

        public record ReplyDTO(Integer replyId, String username, String comment, Boolean isOwner) {
            public ReplyDTO(Reply reply, Integer sessionUserId) {
                this(reply.getId(), reply.getUser().getUsername(), reply.getComment(),
                        checkOwner(sessionUserId, reply.getUser().getId()));
            }
        }

        // 로그인한 사용자가 작성자인지 (비로그인 시 false)
        private static boolean checkOwner(Integer sessionUserId, Integer writerId) {
            return sessionUserId != null && sessionUserId.equals(writerId);
        }
    }
```

`DetailDTO`에 두 가지가 붙었습니다. 하나는 댓글 목록입니다. `board.getReplies()`로 글에 달린 댓글을 꺼내 각각을 안쪽의 `ReplyDTO`로 바꿔 담으므로, 상세를 부르면 글과 함께 그 글의 댓글이 한 덩어리로 나갑니다. 다른 하나는 `isOwner`인데, 로그인한 사람이 이 글(또는 이 댓글)의 작성자인지를 참·거짓으로 알려 주는 값입니다. `checkOwner`가 요청을 보낸 사람의 아이디(`sessionUserId`)와 작성자 아이디를 견줘 같으면 `true`를 돌려주고, 비로그인이라 `sessionUserId`가 `null`이면 `false`입니다. 이 값은 화면에서 수정·삭제 버튼을 본인에게만 보여 줄 때 쓰입니다. 서버가 "이건 당신 글입니다"를 미리 계산해 내려 줍니다.

`isOwner`를 채우려면 상세 조회가 로그인한 사람이 누구인지 알아야 하므로, 서비스가 `sessionUserId`를 받습니다. `board/BoardService.java`의 상세 메서드를 아래처럼 고칩니다.

```java [설명] board/BoardService.java. 상세가 sessionUserId를 받는다
    public BoardResponse.DetailDTO 게시글상세(Integer boardId, Integer sessionUserId) {
        Board board = boardRepository.findByIdJoinUserAndReply(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board, sessionUserId);
    }
```

조회는 `findByIdJoinUserAndReply`로 합니다. 작성자와 댓글을 함께 가져오는 조회인데, 왜 이렇게 묶어 가져와야 하는지는 뒤에서 밝힙니다. 앞 장에서 `findByIdJoinUser`를 이름만 쓰고 넘어갔던 것과 같아서, 여기서는 "작성자와 댓글을 한 번에 가져오는 조회"로만 씁니다. 가져온 글과 `sessionUserId`를 `DetailDTO`에 넘기면 앞의 `isOwner`와 댓글 목록이 채워집니다.

마지막으로 컨트롤러가 로그인 유저를 꺼내 서비스로 넘깁니다. 상세는 공개라 로그인하지 않아도 볼 수 있으므로, `board/BoardController.java`의 상세 메서드는 `request.getAttribute("sessionUser")`로 유저를 꺼내되 비로그인이면 `null`을 넘깁니다. `null`이 넘어가도 `checkOwner`가 `false`를 돌려주므로, 로그인하지 않은 사람에게는 모든 `isOwner`가 `false`로 나갑니다.

이제 `ssar`로 로그인해 1번 글을 조회하면, 글과 함께 거기 달린 댓글이 함께 나옵니다.

```json
{
  "status": 200,
  "msg": "성공",
  "body": {
    "boardId": 1,
    "title": "title1",
    "content": "content1",
    "userId": 1,
    "username": "ssar",
    "isOwner": true,
    "replies": [
      { "replyId": 1, "username": "ssar", "comment": "comment1", "isOwner": true },
      { "replyId": 2, "username": "ssar", "comment": "comment2", "isOwner": true },
      { "replyId": 3, "username": "cos", "comment": "comment3", "isOwner": false }
    ]
  }
}
```

글의 `isOwner`가 `true`이고, `ssar`가 쓴 1·2번 댓글도 `true`, `cos`가 쓴 3번 댓글은 `false`입니다. 화면은 이 값만 보고 본인 것에만 삭제 버튼을 붙이면 됩니다.

## 5.3 조회 한 번에 쿼리가 폭증한다

댓글까지 나가는 것을 확인하고 나면, 4장에서 켜 둔 `show-sql` 설정 덕에 콘솔에 찍히는 SQL이 눈에 들어옵니다. 글 하나를 조회했을 뿐인데 select 문이 여러 줄 지나갑니다. 왜 이렇게 여러 번 나가는지 확인하려면 조회를 하나씩 뜯어보는 테스트가 필요합니다. 마침 선배가 지나가다 화면을 봅니다.

**선배**: "글 목록 불러올 때 작성자 이름도 같이 보여 주죠? 그거 쿼리 몇 개 나가는지 세어 봤어요?"

세어 본 적이 없는 질문입니다. 그 전에 짚어야 할 것이 지연 로딩입니다. 5.1에서 댓글에 붙인 `FetchType.LAZY`가 그것입니다. 4장에서는 `Board.user`를 `EAGER`로 두었는데, 이번 챕터에서 이 값을 `LAZY`로 바꿉니다. `board/Board.java`의 작성자 필드를 아래처럼 고칩니다.

```java [실습 5] board/Board.java. 작성자 조회를 지연 로딩으로
    // 4장의 EAGER에서 LAZY로 바꾼다
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
```

즉시 로딩(EAGER)은 글을 조회할 때 작성자를 무조건 함께 가져오고, 지연 로딩(LAZY)은 글만 먼저 가져온 뒤 작성자는 실제로 꺼내 쓰는 순간까지 미룹니다. 미뤄 둔 그 자리에는 진짜 작성자 대신 가짜 대리인이 들어앉는데, 이것을 프록시(Proxy)라고 합니다. 프록시는 겉으로는 `User`처럼 보이지만 속은 비어 있어서, `getUsername()`처럼 실제 값이 필요한 순간에야 데이터베이스에 작성자를 조회하는 쿼리를 내보냅니다.

말로는 잘 와닿지 않으니 테스트로 확인합니다. 먼저 조심할 것이 하나 있습니다. 지금 볼 테스트는 콘솔에 `board.getId()`만 찍는데, 즉시 로딩이든 지연 로딩이든 이 출력은 똑같습니다. 둘의 차이는 콘솔이 아니라 `show-sql`이 찍어 주는 SQL 로그에서 드러납니다.

`test/board/BoardRepositoryTest.java`에 `findByIdEager_test`와 `findByIdLazy_test`를 준비합니다. 두 테스트의 코드는 글자 그대로 같아서, 글 하나를 `findById`로 조회해 `board.getId()`만 출력하고 작성자는 건드리지 않습니다.

```java [실습 6] test/board/BoardRepositoryTest.java. 즉시·지연 로딩 비교 (두 테스트 본문이 같다)
    @Test
    public void findByIdLazy_test() {
        Board board = boardRepository.findById(1).get();
        System.out.println("Board ID : " + board.getId()); // 작성자는 건드리지 않는다
    }
```

다른 것은 `Board.user`의 어노테이션 상태뿐입니다. `findByIdEager_test`를 실행할 때는 방금 `LAZY`로 바꾼 작성자 필드를 잠시 `EAGER`로 되돌립니다. 이때 SQL 로그를 보면 `findById` 한 줄에 board와 user를 함께 조회하는 select가 나갑니다. 확인했으면 어노테이션을 다시 `LAZY`로 되돌리고 `findByIdLazy_test`를 실행합니다. 이번에는 같은 `findById`인데 board만 조회하는 select 한 줄만 나가고, 작성자는 프록시로 남아 로그에 나타나지 않습니다.

여기까지는 쿼리가 오히려 줄어든 것처럼 보입니다. 문제는 미뤄 둔 작성자를 실제로 꺼낼 때 드러납니다. `LAZY` 상태에서 작성자 이름을 꺼내는 테스트를 하나 더 작성해 확인합니다. `test/board/BoardRepositoryTest.java`를 열고 TODO의 `pass`를 지우고 아래 코드를 작성합니다.

```java [실습 7] test/board/BoardRepositoryTest.java. 프록시가 추가 쿼리를 부른다
    @Test
    public void findByIdLazyLoading_test() {
        Board board = boardRepository.findById(1).get(); // 여기선 board만 조회
        System.out.println("Board ID : " + board.getId());
        System.out.println("username : " + board.getUser().getUsername()); // 이 순간 user 조회가 나간다
    }
```

`findById`로 글을 가져올 때는 board select 하나만 나갑니다. 그런데 마지막 줄에서 `board.getUser().getUsername()`으로 작성자 이름을 꺼내는 순간, 미뤄 두었던 프록시가 그제서야 진짜 작성자를 가져오면서 SQL 로그에 user를 조회하는 select가 한 줄 더 찍힙니다. 글 하나를 조회하는 데 select가 두 번 나간 것입니다.

글 하나면 두 번이라 별것 아닌 것 같지만, 글이 여러 개인 목록이면 상황이 달라집니다. 글 목록을 불러 글마다 작성자 이름을 화면에 보여 준다고 하겠습니다. 먼저 목록을 조회하는 select가 한 번 나가고, 그다음 목록의 각 글에서 작성자 이름을 꺼낼 때마다 방금 본 그 추가 select가 글 수만큼 반복됩니다. 글이 N개면 작성자 조회가 N번 더 붙어 전부 1 + N개가 됩니다. 목록 하나를 불렀을 뿐인데 쿼리가 글 수에 비례해 불어나는 이 현상을 N+1 문제라고 합니다.

<div class="svg-figure">
<svg viewBox="0 0 940 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="지연 로딩은 글 목록 조회 1개에 글마다 작성자 조회가 붙어 1 더하기 N개의 쿼리가 나가지만, fetch join은 글과 작성자를 한 번에 가져와 쿼리 1개로 끝난다.">
  <defs>
    <marker id="c5nq-ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
  </defs>
  <rect x="20" y="26" width="440" height="288" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="240" y="54" text-anchor="middle" font-size="15" font-weight="800" fill="#0f172a">지연 로딩 (N+1)</text>
  <rect x="150" y="72" width="180" height="42" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
  <text x="240" y="98" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">글 목록 조회 (쿼리 1)</text>
  <line x1="240" y1="114" x2="240" y2="140" stroke="#94a3b8" stroke-width="1.4" marker-end="url(#c5nq-ar)"/>
  <rect x="48" y="146" width="120" height="40" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="1.3"/>
  <text x="108" y="171" text-anchor="middle" font-size="11" fill="#334155">1번 글 작성자</text>
  <rect x="180" y="146" width="120" height="40" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="1.3"/>
  <text x="240" y="171" text-anchor="middle" font-size="11" fill="#334155">2번 글 작성자</text>
  <rect x="312" y="146" width="120" height="40" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="1.3"/>
  <text x="372" y="171" text-anchor="middle" font-size="11" fill="#334155">N번 글 작성자</text>
  <line x1="200" y1="114" x2="118" y2="144" stroke="#94a3b8" stroke-width="1.3" marker-end="url(#c5nq-ar)"/>
  <line x1="240" y1="114" x2="240" y2="144" stroke="#94a3b8" stroke-width="1.3" marker-end="url(#c5nq-ar)"/>
  <line x1="280" y1="114" x2="362" y2="144" stroke="#94a3b8" stroke-width="1.3" marker-end="url(#c5nq-ar)"/>
  <text x="240" y="212" text-anchor="middle" font-size="11" fill="#6b7280">작성자를 꺼낼 때마다 쿼리가 하나씩 더 (쿼리 N)</text>
  <rect x="120" y="240" width="240" height="46" rx="8" fill="#fff7ed" stroke="#ff7849" stroke-width="1.9"/>
  <text x="240" y="269" text-anchor="middle" font-size="14" font-weight="800" fill="#c2410c">합계 쿼리 1 + N개</text>
  <rect x="480" y="26" width="440" height="288" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="700" y="54" text-anchor="middle" font-size="15" font-weight="800" fill="#0f172a">fetch join</text>
  <rect x="560" y="120" width="280" height="60" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="700" y="148" text-anchor="middle" font-size="12" font-weight="700" fill="#3730a3">글 + 작성자를 한 번에 조회</text>
  <text x="700" y="168" text-anchor="middle" font-size="11" fill="#3730a3">join으로 묶어서 가져온다</text>
  <rect x="580" y="240" width="240" height="46" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.9"/>
  <text x="700" y="269" text-anchor="middle" font-size="14" font-weight="800" fill="#3730a3">합계 쿼리 1개</text>
  <text x="700" y="212" text-anchor="middle" font-size="11" fill="#6b7280">작성자를 나중에 따로 조회하지 않는다</text>
</svg>
</div>

*그림 5-3. 지연 로딩은 작성자를 꺼낼 때마다 쿼리가 붙어 1+N개가 되고, fetch join은 글과 작성자를 한 번에 가져와 쿼리 하나로 끝냅니다*

그림의 오른쪽 해법이 눈에 들어옵니다. 작성자를 나중에 따로 가져오지 말고 글을 조회할 때 아예 함께 묶어 가져오면 쿼리는 한 번으로 끝납니다. 이 방법이 다음 절의 fetch join입니다.

## 5.4 fetch join으로 해결

작성자를 글과 함께 묶어 가져오는 조회는 이미 있습니다. 앞 장에서 `findByIdJoinUser`를 만들어 게시글 상세와 수정, 삭제에 썼습니다. 그때는 "작성자를 함께 가져오는 조회"라는 이름으로만 쓰고 왜 그렇게 묶어야 하는지는 미뤄 두었는데, 그 메서드의 JPQL이 `select b from Board b join fetch b.user where b.id = :id`였습니다.

핵심은 `join fetch b.user`입니다. 지연 로딩에서는 글을 먼저 가져오고 작성자를 프록시로 미뤄 두지만, `join fetch`는 글을 조회하는 그 select에 작성자 조회를 끼워 넣어 한 번에 가져옵니다. 그래서 이 메서드로 가져온 글은 작성자가 이미 채워져 있어, `getUser().getUsername()`을 불러도 추가 쿼리가 나가지 않습니다. 앞에서 본 두 번째 select가 사라집니다. 앞 장에서는 작성자가 즉시 로딩이라 어차피 함께 나왔지만, 이번 챕터에서 작성자를 지연 로딩으로 바꾼 지금은 이 fetch join이 비로소 N+1을 막는 장치가 됩니다.

댓글까지 함께 가져오는 조회도 같은 방식으로 만듭니다. 5.2에서 게시글 상세가 이름만 쓰고 넘어갔던 `findByIdJoinUserAndReply`입니다. `board/BoardRepository.java`를 열고 TODO의 `pass`를 지우고 아래 메서드를 작성합니다.

```java [실습 8] board/BoardRepository.java. 작성자와 댓글을 함께 가져오는 조회
    public Optional<Board> findByIdJoinUserAndReply(int boardId) {
        // TODO: 작성자와 댓글을 join fetch로 함께 가져온다
        return em.createQuery(
                "select b from Board b join fetch b.user left join fetch b.replies where b.id = :id", Board.class)
                .setParameter("id", boardId)
                .getResultStream().findFirst();
    }
```

이번에는 `join fetch`가 두 개입니다. `join fetch b.user`로 작성자를, `left join fetch b.replies`로 댓글 목록을 함께 가져옵니다. 댓글 쪽에 `left`를 붙인 것은 댓글이 하나도 없는 글도 조회에서 빠지지 않게 하기 위해서입니다. 댓글을 묶으면 글 하나가 댓글 수만큼 중복된 행으로 나오기 때문에, `getResultList` 대신 `getResultStream().findFirst()`로 첫 글 하나만 취합니다. 이 조회 하나로 글과 작성자와 댓글 목록이 채워진 채 돌아오므로, 상세 응답에서 `board.getUser()`나 `board.getReplies()`를 꺼내도 추가 쿼리가 나가지 않습니다. 다만 댓글 작성자(`reply.user`)는 이 조회에 묶지 않아, 그 이름을 꺼낼 때는 지연 로딩이 그대로 동작합니다.

이 조회가 실제로 쿼리를 한 번에 끝내는지 테스트로 확인합니다. `test/board/BoardRepositoryTest.java`에 `findByIdJoinUserAndReply_test`를 작성합니다.

```java [실습 9] test/board/BoardRepositoryTest.java. fetch join 조회
    @Test
    public void findByIdJoinUserAndReply_test() {
        Board board = boardRepository.findByIdJoinUserAndReply(1).get();
        System.out.println("Board ID : " + board.getId());
        System.out.println("username : " + board.getUser().getUsername());        // 추가 쿼리 없음
        System.out.println("Reply : " + board.getReplies().get(1).getComment());  // 추가 쿼리 없음
        System.out.println("Reply author : " + board.getReplies().get(1).getUser().getUsername()); // 여기서 댓글 작성자 조회가 나간다
    }
```

글 작성자와 댓글 내용을 꺼낼 때는 추가 select가 없습니다. 조회 한 번에 글·작성자·댓글이 담겨 왔기 때문입니다. 5.3의 `findByIdLazyLoading_test`에서는 작성자를 꺼내는 순간 select가 한 번 더 나갔지만, 여기서는 그 두 번째 select가 사라졌습니다. 그런데 마지막 줄에서 댓글 작성자 이름을 꺼내면 이야기가 다릅니다. 댓글 작성자는 이 조회에 묶이지 않은 지연 로딩이라, 그제서야 그 댓글의 작성자를 가져오는 select가 한 줄 더 나갑니다. 실제 상세 응답의 `DetailDTO`는 댓글을 하나씩 돌며 저마다 작성자 이름을 꺼내므로, 댓글이 N개면 이 select가 N번 붙습니다. N+1이 한 겹 더 안쪽에 남아 있습니다. 댓글 작성자까지 한 번에 묶고 싶다면 이 조회에 `left join fetch`를 한 겹 더 더하면 되지만, 늘 필요한 게 아니라면 지연 로딩으로 두고 꼭 필요한 조회에서만 묶는 편이 낫습니다.

두 로그를 나란히 두면 차이가 분명합니다.

```text [로그] show-sql 콘솔 (요약)
# findByIdLazyLoading_test — 지연 로딩
select ... from board_tb where id=?        # 1) 글만 조회
select ... from user_tb  where id=?        # 2) getUsername() 순간, 작성자 조회

# findByIdJoinUserAndReply_test — fetch join
select ... from board_tb b
    join user_tb u ... left join reply_tb r ... where b.id=?   # 글+작성자+댓글을 한 번에
select ... from user_tb  where id=?        # 댓글 작성자(reply.user)는 lazy라 꺼낼 때 추가
```

<!-- [CAPTURE NEEDED: 01_show-sql-nplus1-vs-fetchjoin
  path: assets/CH5/terminal/01_show-sql-nplus1-vs-fetchjoin.png
  desc: show-sql 로그 두 장면을 위아래로 담은 캡처. (1) findByIdLazyLoading_test 실행 로그. board를 조회하는 select 한 줄이 먼저 나가고, "username :"을 출력하기 직전에 user를 조회하는 select가 한 줄 더 나가 select가 총 두 번 찍힌 화면(지연 로딩의 추가 쿼리). (2) findByIdJoinUserAndReply_test 실행 로그. board와 user, replies를 join으로 함께 가져오는 select 한 줄만 나가고, username과 댓글을 출력할 때 추가 select가 없는 화면(fetch join 한 방). 각 로그에 select 문이 몇 번 나갔는지가 눈에 보이면 좋음. IDE 콘솔 또는 gradle test 출력.
] -->
![](../assets/CH5/terminal/01_show-sql-nplus1-vs-fetchjoin.png)
*그림 5-4. 지연 로딩은 작성자를 꺼낼 때 select가 한 번 더 나가지만, fetch join은 조회 한 번으로 작성자와 댓글까지 담아 옵니다*

게시글 상세를 `findByIdJoinUserAndReply`로 조회하도록 5.2에서 고쳐 둔 것도 같은 이유입니다. 상세 한 번에 글과 작성자와 댓글이 함께 나가야 하는데, 지연 로딩에 맡기면 그 자리에서 쿼리가 여러 번 나가기 때문입니다.

:::tip
**fetch 전략에서 생각해 볼 것들**

- **기본값**: `@ManyToOne`은 즉시 로딩, `@OneToMany`는 지연 로딩이 기본입니다. 어느 쪽이든 연관관계가 많아지면 조회 한 번이 쿼리 여러 개로 번질 수 있어, 필요한 조회에는 fetch join으로 가져올 것을 함께 정합니다.
- **지연 로딩을 기본으로**: 연관관계를 모두 즉시 로딩으로 두면, 그 글이 필요 없는 조회에서도 작성자와 댓글이 매번 함께 조회됩니다. 평소에는 지연 로딩으로 두고, 함께 필요한 조회에서만 fetch join으로 묶는 편이 낫습니다.
- **left join의 이유**: 댓글이 없는 글도 조회에서 빠지지 않게 하려고 `left`를 붙입니다. `left` 없이 묶으면 댓글이 하나도 없는 글은 결과에서 사라집니다.
:::

## 5.5 이것만은 기억하자

댓글까지 붙자, 오픈이는 화면을 붙이던 동료를 불렀습니다. 목록에서 1번 글을 눌러 상세를 열자, 글 아래로 댓글 세 개가 나란히 나타났습니다. 본인이 쓴 댓글에만 삭제 버튼이 붙어 있었습니다.

**동료**: "댓글도 되고, 남의 댓글엔 삭제 버튼도 안 뜨네요. 이제 진짜 게시판 같은데요."

게시판이 완성됐습니다. 글을 쓰고 읽고 고치고 지우고, 로그인한 본인만 자기 글과 댓글을 건드리고, 무거운 상세 조회도 fetch join으로 묶어 쿼리를 줄였습니다.

*처음엔 하나도 설명할 수 없던 것들이었는데.*

오픈이는 1장을 떠올렸습니다. 그때는 자바만으로 서버 뼈대를 짜다 학기가 끝날 판이었고, 스프링에 올린 메서드가 요청 한 번에 저절로 실행되는 것이 마법처럼 보였습니다. 2장에서는 저장하는 코드를 한 줄도 쓰지 않았는데 수정이 반영됐고, 방금은 조회 한 번에 쿼리가 여러 개 나갔습니다. 이제는 각각을 이름으로 부를 수 있습니다. 메서드가 저절로 실행되는 것은 리플렉션이 표식을 읽어 찾아 부르는 것이고, 저장 없이 수정이 반영되는 것은 더티체킹이며, 조회 한 번에 쿼리가 불어나는 것은 지연 로딩의 프록시가 뒤늦게 데이터를 가져오기 때문입니다. 프레임워크는 더 이상 열어 볼 수 없는 블랙박스가 아니라, 안에서 무슨 규칙이 도는지 알고 쓰는 도구가 됐습니다.

:::remember
**이것만은 기억하자**

- 댓글은 외래 키를 든 연관관계 주인이고, 게시글은 `mappedBy`로 그 관계의 주인을 가리킵니다. `cascade = REMOVE`로 게시글을 지우면 딸린 댓글도 함께 지워집니다.
- 지연 로딩은 연관 엔티티를 프록시로 미뤄 두었다가 꺼내는 순간 조회 쿼리를 냅니다. 이것이 목록으로 번지면 1+N개의 쿼리가 나가는데, `join fetch`로 함께 가져오면 쿼리 하나로 끝납니다. 4장에서 이름만 쓰던 `findByIdJoinUser`가 바로 이 해법이었습니다.
- 리플렉션에서 시작해 게시판 하나를 인증과 성능까지 챙겨 완성했습니다. 스프링이 대신 해 주던 일들의 이름을 이제 하나씩 부를 수 있습니다. 마법처럼 보이던 것은 리플렉션 위에 세운 규칙이었습니다.
:::
