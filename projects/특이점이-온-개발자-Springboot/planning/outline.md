# 목차 (뼈대)

> 재료: `seed.md`(의도) + `code-analysis.md`(코드) + `scenario.md`(스토리 아크) + 스프링-뼈대 v1·v2 병합 지도.
> 원칙: 이해 8 / 구축 2. 코드는 핵심만, 전체는 GitHub. 흐름은 v1, 코드는 완성코드, 개념은 v1·v2 병합.
> 인증은 JWT만(Security 없음). 테스트는 단위 테스트만. 관리자·바이브코딩·REST Docs 제외.

## 코드 실습 분류 기준

| 분류 | 표시 | 의미 | 독자 액션 |
|------|------|------|----------|
| 실습 | [실습] | 챕터 핵심 코드 | 독자가 직접 작성 |
| 설명 | [설명] | 중요하지만 핵심 아닌 코드 | 코드 읽고 이해 |
| 참고 | [참고] | 이 챕터 주제가 아닌 코드 | 파일명 + 한 줄만 |

레포: 완성본 `spring-end`, 예제 `spring-start`. 패키지 `com.metacoding.spring`(CH2~), `com.reflection`(CH1).

---

## Part 1: 마법의 정체

### Ch.1: 리플렉션 : 스프링은 어떻게 내 코드를 알아서 실행하는가 (앱 이전)

**핵심 개념**: 프레임워크(제어의 역전) / 리플렉션 / 커스텀 어노테이션 / 컴포넌트 스캔의 원리 / 빈·의존성 주입(DI, 개념) / DispatcherServlet·요청 처리 메커니즘(개념)
**기술**: 순수 자바, `java.lang.reflect`, `@interface`, `ClassLoader`
**버전 성과**: 콘솔에 `insert 호출됨` — 어노테이션 표식만으로 메서드가 자동 호출·스캔되는 것을 눈으로 확인. "스프링은 마법이 아니라 리플렉션 위의 규칙"임을 이해
**예상 분량**: ~20p

**절 구성**:
- 1.1 프레임워크란 무엇인가 — 라이브러리는 내가 부른다, 프레임워크는 내 코드를 대신 부른다(제어의 역전)
- 1.2 스프링은 어떻게 내 코드를 찾아 실행하나 — "등록한 적도 없는 내 메서드를 어떻게 부르지?"
- 1.3 [실습] if-else 라우팅과 그 한계 — 메서드가 늘 때마다 손으로 고쳐야 하는 문제 (ex01)
- 1.4 [실습] 리플렉션 + 표식으로 찾아 호출 — 커스텀 어노테이션과 `method.invoke()` (ex02)
- 1.5 [실습] 폴더를 뒤져 자동 등록·실행 — 클래스로더 스캔 (ex03)
- 1.6 스프링이 객체를 만들어 넣어준다 — ex03의 "객체 자동 생성"이 곧 빈·의존성 주입(DI). 개념만 가볍게 (다음 챕터 생성자 주입의 밑그림)
- 1.7 스프링의 요청 처리 메커니즘 — Tomcat·스레드풀·DispatcherServlet·계층까지 한 장으로 (개념, v1 챕터3-10)
- 1.8 이것만은 기억하자 — 마법의 정체는 리플렉션. "이제 진짜 만들자"

**코드 실습 분류**:
```
spring-ch01(com.reflection)/
├── ex01/App.java, BoardController.java              [실습] if-else 라우팅
├── ex02/App.java, BoardController.java              [실습] 리플렉션 호출
│   └── RequestMapping.java                          [실습] 커스텀 어노테이션
└── ex03/App.java, BoardController.java              [실습] 클래스로더 스캔
    ├── Controller.java                              [실습] 타입 어노테이션
    └── RequestMapping.java                          [설명] ex02 재사용
```
**실습 요약**: 작성 3세트(ex01→ex02→ex03) / 설명 1 / 참고 0. IDE에서 각 `App.main()` 실행
**주의**: 리플렉션 실습(ex01~03)은 "찾아서 호출·스캔"에 집중. 빈·DI는 ex03의 "객체 자동 생성"에 이어 **개념만 가볍게** 얹는다(빈 스코프·주입 방식 등 깊은 DI 메커니즘은 유보)

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 1-1 | GEMINI PROMPT | 라이브러리 vs 프레임워크(제어의 역전) 개념도 |
| 그림 1-2 | HTML 다이어그램 | if-else → 리플렉션 → 스캔 3단계 진화 흐름 |
| 그림 1-3 | HTML 다이어그램 | 요청 처리 메커니즘(Tomcat·스레드풀·DispatcherServlet·C/S/R/PC) |
| 그림 1-4 | CAPTURE NEEDED | ex03 실행 콘솔 출력(파일명 스캔 + delete 호출됨) |

---

## Part 2: 게시판을 만든다

### Ch.2: 게시판 CRUD : 글을 저장하고 불러온다 — v0.1

**핵심 개념**: REST/HTTP 메서드(짧게) / ORM·객체-테이블 불일치 / 영속성 컨텍스트(캐싱·쓰기지연·더티체킹) / 엔티티 생명주기 / 트랜잭션 경계 / Lombok / 3계층 아키텍처 / JPQL / 단위 테스트(given-when-then)
**기술**: Spring Boot, `@RestController`, JPA(`EntityManager`), H2, `@Transactional`, Lombok, `@DataJpaTest`
**버전 성과**: 게시글 목록·상세·작성·수정·삭제가 JSON으로 실제 동작
**예상 분량**: ~28p

**절 구성**:
- 2.1 우리가 만들 건 REST API다 — 화면이 아니라 JSON을 주고받는 서버. HTTP 메서드(GET·POST·PUT·DELETE)로 자원을 다룬다(짧게, URI 규범은 생략)
- 2.2 소스코드 준비 — git clone, 파일 트리([실습]·[설명]·[참고]), start·end 안내
- 2.3 JPA와 ORM — 객체 세계와 테이블 세계의 불일치, JPA가 그 사이를 번역 (개념, v1 챕터3-3)
- 2.4 영속성 컨텍스트 — 1차 캐시·쓰기지연·더티체킹 (개념, v1)
- 2.5 엔티티 생명주기와 트랜잭션 경계 — 비영속·영속·준영속·삭제, `@Transactional`이 긋는 경계(더티체킹이 왜 그 끝에서 일어나나)
- 2.6 엔티티와 DB — `Board` 엔티티, Lombok이 대신 써주는 코드(`@Data`·`@Builder`, "게터는 어디 있지?"), H2 설정, `data.sql` 더미
- 2.7 [실습] Repository — `EntityManager`로 find·persist·remove·JPQL
- 2.8 [실습] Service·Controller — 3계층으로 목록·상세·작성·삭제 API
- 2.9 더티체킹으로 수정하기 — `save()` 없이 값만 바꾸면 저장되는 이유
- 2.10 단위 테스트 — `@DataJpaTest`로 Repository 검증(given-when-then, 눈으로 확인)
- 2.11 이것만은 기억하자 + "없는 글을 조회하면 터진다"

**코드 실습 분류**:
```
v0.1 (spring-ch02)/
├── board/Board.java              [실습] 엔티티(@Entity, @Id, @CreationTimestamp)
├── board/BoardRepository.java    [실습] EntityManager 기반 CRUD
├── board/BoardService.java       [실습] 3계층 + 더티체킹 수정
├── board/BoardController.java    [실습] REST 엔드포인트 5개
├── board/BoardRequest.java       [설명] SaveDTO/UpdateDTO
├── core/util/Resp.java           [설명] 공통 응답 래퍼
├── Springv3Application.java      [참고] 진입점
├── resources/application.properties [설명] H2·JPA 설정
├── resources/db/data.sql         [참고] 더미 데이터
└── test/BoardRepositoryTest.java [실습] 단위 테스트
```
**실습 요약**: 작성 5 / 설명 3 / 참고 2
**집필 가드**: 2.3~2.5 개념 3절이 코드(2.6) 앞에 연속된다. 짧은 비유로 가볍게 통과시키고 개념의 무게는 2.6 이후 코드에서 회수한다(코드 없는 추상 3연속으로 초입 이탈 방지)

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 2-1 | GEMINI PROMPT | 객체 세계 ↔ 테이블 세계, JPA가 번역 |
| 그림 2-2 | GEMINI PROMPT | 영속성 컨텍스트(1차 캐시·쓰기지연·더티체킹) |
| 그림 2-3 | HTML 다이어그램 | 요청 → Controller → Service → Repository → H2 흐름 |
| 그림 2-4 | CAPTURE NEEDED | 목록/상세 API JSON 응답 |
| 그림 2-5 | CAPTURE NEEDED | 단위 테스트 통과 결과 |

---

### Ch.3: 예외 처리와 DTO : 터지지 않고, 새어나가지 않게 — v0.2

**핵심 개념**: 응답 DTO 분리(캡슐화) / Optional·orElseThrow / 예외 종류(Unchecked·RuntimeException) / HTTP 상태 코드 / 전역 예외 처리(@RestControllerAdvice) / 커스텀 예외 계층
**기술**: Java record, `Optional`, `@RestControllerAdvice`, `@ExceptionHandler`
**버전 성과**: 없는 글 조회 시 깔끔한 404 JSON, 응답이 DTO로 정리됨
**예상 분량**: ~16p

**절 구성**:
- 3.1 두 개의 구멍 — 없는 글 조회하면 그대로 터지고, 내부 엔티티가 응답에 샌다
- 3.2 [실습] 응답 DTO 분리 — 엔티티 대신 `BoardResponse.DTO`/`DetailDTO`
- 3.3 Optional로 없음을 표현하고 예외를 던진다 — `findById().orElseThrow(Exception404)`
- 3.4 예외의 종류와 HTTP 상태 코드 — 커스텀 예외가 왜 `RuntimeException`(Unchecked)인가, 404·400·401·403·500이 뜻하는 것
- 3.5 [실습] 전역 예외 처리 — `@RestControllerAdvice`가 예외를 JSON으로 일괄 변환
- 3.6 이것만은 기억하자 + "그런데 아무나 남의 글을 수정·삭제한다"

**코드 실습 분류**:
```
v0.2 (spring-ch03)/  (변경·신규만 표기)
├── board/BoardResponse.java              [실습] 응답 DTO(DTO/DetailDTO)
├── core/handler/GlobalExceptionHandler.java [실습] @RestControllerAdvice
├── core/handler/ex/Exception404.java     [실습] 커스텀 예외
├── board/BoardService.java               [설명] Optional+orElseThrow로 변경
├── board/BoardRepository.java            [설명] findById → Optional 반환
├── board/BoardRequest.java               [참고] toEntity() 추가
└── board/BoardController.java            [설명] 응답 타입 DTO로 교체
```
**실습 요약**: 작성 3 / 설명 3 / 참고 1
**주의**: readOnly 제거·`@Transactional` 통일(저자 결정 #2). import 전환은 설명하지 않음

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 3-1 | GEMINI PROMPT | 엔티티 직접 노출의 위험 vs DTO 경계 |
| 그림 3-2 | HTML 다이어그램 | 예외 발생 → 전파 → @RestControllerAdvice → JSON 흐름 |
| 그림 3-3 | CAPTURE NEEDED | 없는 글 조회 시 404 JSON 응답 |

---

## Part 3: 지키고 잇는다

### Ch.4: 인증과 인가 : 로그인한 본인만 — v0.3

**핵심 개념**: 인증 vs 인가 / Stateless vs Stateful(세션의 한계) / JWT 구조(간단) / 해싱 vs 암호화(한 줄) / 필터=인증 / 인터셉터=인가 / 소유자 검증 / 연관관계(@ManyToOne) / Bean Validation
**기술**: `java-jwt`, BCrypt(사용법), `OncePerRequestFilter`, `HandlerInterceptor`, `WebMvcConfig`, `@Valid`
**버전 성과**: 로그인하면 JWT 발급, 남의 글 수정 시 403
**예상 분량**: ~28p

**절 구성**:
- 4.1 완전히 공개된 게시판 — 로그인도, 주인 확인도 없다
- 4.2 인증과 인가는 다르다 — 인증("너 누구야?") vs 인가("그걸 할 권한이 있어?"). 이 장의 필터=인증·인터셉터=인가의 밑그림 (개념)
- 4.3 세션 대신 왜 JWT인가 — Stateless vs Stateful, 쿠키·세션의 한계, 토큰이 상태를 대체 (개념, v1 세션개념 → JWT)
- 4.4 회원 도메인과 연관관계 — `User` 엔티티, `Board.user @ManyToOne(EAGER)`, `findByIdJoinUser`(이름만, 이론은 CH5로 유보)
- 4.5 [실습] 회원가입과 로그인 — BCrypt로 비밀번호 해싱(단방향 해시 vs 암호화 한 줄, 내부 알고리즘 제외), 로그인 성공 시 JWT 발급
- 4.6 JWT 구조와 검증 — 토큰이 무엇을 담나(간단), `JwtUtil.create/verify`, `JwtProvider`
- 4.7 [실습] 필터 = 인증 — `JwtAuthenticationFilter`가 토큰을 확인해 정보만 심는다(차단 안 함)
- 4.8 [실습] 인터셉터 = 인가 — `AuthInterceptor`가 필요한 요청을 실제로 막는다, `WebMvcConfig` 등록(+CORS 한 줄)
- 4.9 소유자 검증과 검증 실패 — 본인 글만(403), `@Valid` 실패(400)를 예외 구조로 확장
- 4.10 이것만은 기억하자 + "그런데 글에 댓글을 달고 싶다"

**코드 실습 분류**:
```
v0.3 (spring-ch04)/  (신규·변경)
├── user/User.java, UserRepository.java   [설명] 회원 도메인
├── user/UserService.java                 [실습] 회원가입(BCrypt)·로그인(JWT)
├── user/UserController.java              [실습] /join, /login
├── user/UserRequest.java                 [설명] @Valid DTO
├── core/util/JwtUtil.java                [실습] JWT 발급·검증
├── core/util/JwtProvider.java            [실습] 토큰 추출·유저 복원
├── core/util/PasswordEncoder.java        [참고] BCrypt 래핑(내부 알고리즘 제외)
├── core/filter/JwtAuthenticationFilter.java [실습] 인증 필터
├── core/interceptor/AuthInterceptor.java [실습] 인가 인터셉터
├── core/config/WebMvcConfig.java         [설명] 인터셉터 등록 + CORS
├── core/handler/ex/Exception401,403.java [설명] 인증·인가 예외
├── board/Board.java                      [설명] @ManyToOne User 추가
└── board/BoardService.java               [설명] 소유자 검증 추가
```
**실습 요약**: 작성 6 / 설명 6 / 참고 1
**주의**: Spring Security 미사용(제거). 필터·인터셉터 직접 구현. `@AuthenticationPrincipal`·`UserDetails`·`hasRole` 등 Security 개념 안 씀
**집필 가드**: (1) 4.5 로그인 실습이 `JwtUtil.create`를 먼저 호출한다(전방 참조) → 코드블록 위에 "내부 구조는 4.6에서 본다" 예고 한 줄. (2) CH4는 분할하지 않는다(v0.3 1:1 대응·서사 완결). 대신 4.6 JWT 구조는 header/payload/signature 3분해를 그림에 위임하고 본문은 압축해 28p 상한 방어

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 4-1 | GEMINI PROMPT | Stateless(가방) vs Stateful(락커) 비유 |
| 그림 4-2 | HTML 다이어그램 | JWT 발급 → 헤더 재전송 → 필터 검증 → 인터셉터 인가 흐름 |
| 그림 4-3 | HTML 다이어그램 | 필터(인증)와 인터셉터(인가) 실행 시점 분리 |
| 그림 4-4 | CAPTURE NEEDED | 로그인 JWT 응답 / 남의 글 수정 시 403 |

---

### Ch.5: 댓글과 JPA 심화 : 잇고, 빨라진다 — v0.4

**핵심 개념**: 양방향 매핑(@OneToMany·mappedBy·연관관계 주인) / cascade(영속성 전이) / 지연 로딩과 프록시 / N+1 문제 / fetch join(회수 서사)
**기술**: `@OneToMany`, `FetchType.LAZY`, `join fetch`, `spring.jpa.show-sql`
**버전 성과**: 게시글 상세에 댓글 목록 동반, 댓글 작성·삭제, N+1 해결
**예상 분량**: ~20p

**절 구성**:
- 5.1 댓글은 글에 딸린다 — 양방향 매핑, 연관관계 주인, `@OneToMany(mappedBy, cascade=REMOVE)`. 게시글을 지우면 댓글도 지워지는 이유(영속성 전이) (개념, v1 챕터5-1)
- 5.2 [실습] 댓글 CRUD — 작성·삭제(목록은 게시글 상세에 내장), 소유자 검증 재사용(CH4 회수)
- 5.3 조회 한 번에 쿼리가 폭증한다 — 지연 로딩은 프록시로 동작한다("왜 `getUser()` 하는 순간 쿼리가?"). `Board.user`를 EAGER↔LAZY 토글하며 N+1을 관찰. **콘솔 출력은 EAGER·LAZY가 동일하니 차이는 `show-sql` SQL 로그로 본다**(같은 출력에서 막히지 않게 실습 안내에 명시)
- 5.4 [실습] fetch join으로 해결 — `findByIdJoinUserAndReply`. CH4에서 이름만 썼던 그 메서드의 정체를 이제 이해
- 5.5 이것만은 기억하자 — 게시판 완성. 책 전체를 닫으며 CH1의 "마법의 정체"를 회수

**코드 실습 분류**:
```
v0.4 (spring-ch05)/  (신규·변경)
├── reply/Reply.java                      [설명] 댓글 엔티티(@ManyToOne user/board)
├── reply/ReplyController.java            [실습] 작성·삭제 엔드포인트
├── reply/ReplyService.java               [실습] 댓글 저장·삭제(소유자 검증)
├── reply/ReplyRepository.java            [설명] EntityManager 기반
├── reply/ReplyRequest/Response.java      [참고] DTO
├── board/Board.java                      [실습] @OneToMany replies, user EAGER→LAZY
├── board/BoardRepository.java            [실습] findByIdJoinUserAndReply(fetch join)
├── board/BoardResponse.java              [설명] DetailDTO에 replies·isOwner
└── test/BoardRepositoryTest.java         [실습] fetch 5단계(EAGER 토글 포함)
```
**실습 요약**: 작성 5 / 설명 3 / 참고 1

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 5-1 | GEMINI PROMPT | Board ↔ Reply 양방향 연관관계(연관관계 주인) |
| 그림 5-2 | HTML 다이어그램 | N+1 발생(1 + N 쿼리) vs fetch join(1 쿼리) 비교 |
| 그림 5-3 | CAPTURE NEEDED | show-sql 로그: LAZY N+1 vs join fetch |

---

## 갭 분석 결과

| 누락 주제 | 우선순위 | 반영 여부 | 비고 |
|----------|---------|----------|------|
| 통합 테스트(MockMvc) | 권장 | 생략 | 저자 결정: 단위 테스트만 |
| Spring Security | 선택 | 생략 | 완성코드가 제거. JWT 직접 구현으로 대체 |
| 관리자 역할/권한(RBAC) | 선택 | 생략 | 완성코드에 없음, 의도 밖 |
| API 문서 자동화(REST Docs)·바이브코딩 | 선택 | 생략 | 의도 밖 |
| 유저네임 중복체크 | 선택 | 생략 | 완성코드에 엔드포인트 없음 |
| DI/빈 컨테이너 원리 | 권장 | 반영(개념) | CH1.6에서 "객체 자동 생성=빈·DI" 개념만. 빈 스코프·주입 방식 등 깊은 메커니즘은 유보 |
| 엔티티 생명주기·트랜잭션 경계 | 권장 | 반영 | CH2.5 신설 (비영속·영속·준영속·삭제 + @Transactional 경계) |
| HTTP 상태 코드·예외 종류(Unchecked) | 권장 | 반영 | CH3.4 신설 |
| 인증 vs 인가(개념) | 권장 | 반영 | CH4.2 신설 (필터·인터셉터 분리의 밑그림) |
| 지연 로딩과 프록시 | 권장 | 반영 | CH5.3에 프록시 원리 보강 |
| Lombok | 권장 | 반영 | CH2.6에서 처음 등장 시 짧게 |
| 트랜잭션 롤백·격리수준 | 선택 | 생략 | 경계·더티체킹까지만(CH2) |
| REST URI 설계 규범 | 선택 | 생략 | CH2.1에서 "REST란" 짧게만 |

## 여정 맵

```
Ch.1 리플렉션(어려움·개념 봉우리) → Ch.2 CRUD(보통·손에 잡힘) →
Ch.3 예외·DTO(쉬어가기) → Ch.4 인증(어려움·최대 봉우리) →
Ch.5 댓글·JPA심화(전환점! N+1) → 완성
```
두 전환점: Ch.1 착지(마법=리플렉션), Ch.5 N+1(심은 게 돌아온다).

## 기술 매핑

| 챕터 | 버전 | 핵심 기술 | 완성 코드와 다르게 갈 점 |
|------|------|----------|------------------------|
| Ch.1 | — | 리플렉션·어노테이션·클래스로더·빈/DI(개념) | 없음(그대로). DI는 개념만 가볍게 |
| Ch.2 | v0.1 | JPA(EntityManager)·더티체킹·3계층·단위테스트 | 패키지 `com.metacoding.spring`, @Transactional 통일(readOnly 제거) |
| Ch.3 | v0.2 | DTO·Optional·전역 예외처리 | import 전환 설명 안 함 |
| Ch.4 | v0.3 | JWT·필터(인증)·인터셉터(인가)·연관관계·검증 | Security 미사용. findByIdJoinUser는 이름만(N+1 이론은 CH5) |
| Ch.5 | v0.4 | 양방향 매핑·지연로딩·N+1·fetch join | EAGER 토글 실습(관찰은 show-sql 로그). fetch join 회수 서사 |
