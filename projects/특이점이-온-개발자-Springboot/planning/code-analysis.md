# 코드 분석

## 완성 코드 정보

- 경로: `code/spring-ch01` ~ `code/spring-ch05`
- 언어/프레임워크: Java 21, Spring Boot 4.0.3, Gradle (`io.spring.dependency-management` 1.1.7)
- `spring-ch01`은 Spring 의존성이 전혀 없는 순수 Java 프로젝트입니다(`build.gradle` 없음). ch02부터 Spring Boot 프로젝트로 전환됩니다.
- DB: H2 인메모리 (`spring.datasource.url=jdbc:h2:mem:test`), `ddl-auto=create` + `data.sql`로 매 실행마다 초기화
- 패키지 루트: `com.metacoding.springv3` (ch02~ch05), `com.reflection` (ch01)

## 전체 구조

```
code/
├── spring-ch01/  (순수 Java, Spring 없음)
│   └── src/main/java/com/reflection/
│       ├── ex01/  하드코딩 if-else 분기
│       ├── ex02/  커스텀 @RequestMapping + 리플렉션 invoke
│       └── ex03/  커스텀 @Controller + 클래스로더 스캔
├── spring-ch02/  (Spring Boot 시작 — 게시판 CRUD)
│   └── src/main/java/com/metacoding/springv3/
│       ├── board/           Board, BoardController, BoardService, BoardRepository, BoardRequest
│       └── core/util/       Resp (공통 응답 래퍼)
├── spring-ch03/  (+ 전역 예외 처리)
│   └── + core/handler/      GlobalExceptionHandler, ex/Exception404
│   └── + board/BoardResponse (DTO 분리)
├── spring-ch04/  (+ JWT 인증)
│   └── + user/               User, UserController, UserService, UserRepository, UserRequest
│   └── + core/util/          JwtProvider, JwtUtil, PasswordEncoder
│   └── + core/filter/        JwtAuthenticationFilter
│   └── + core/interceptor/   AuthInterceptor
│   └── + core/config/        WebMvcConfig
│   └── + core/handler/ex/    Exception401, Exception403
└── spring-ch05/  (+ 댓글)
    └── + reply/               Reply, ReplyController, ReplyService, ReplyRepository, ReplyRequest, ReplyResponse
    └── board/Board             @OneToMany replies 연관관계 추가
```

챕터마다 이전 챕터 프로젝트를 통째로 복사한 뒤 위 파일들을 얹는 구조입니다. `spring-ch05`가 최종 완성본(게시판 + 인증 + 댓글)입니다.

---

## 챕터별 해부

### ch01 리플렉션

Spring 의존성이 없는 순수 Java 프로젝트로, `main()`만 실행되는 3단계 진화입니다. 세 버전 모두 `BoardController`의 `insert/delete/update/select` 메서드를 호출하는 목적은 같고, "어떻게 호출 대상을 찾는가"만 달라집니다.

| 버전 | 파일 | 핵심 동작 | 대응하는 스프링 실제 기능 |
|------|------|----------|--------------------------|
| ex01 | `App.java`, `BoardController.java` | `if(uri.equals("/insert"))` 형태로 문자열 비교 후 직접 메서드 호출 | 어노테이션 매핑 이전의 "수작업 라우팅" — Spring이 해결하기 이전 상태 |
| ex02 | `App.java`, `BoardController.java`, `RequestMapping.java` | `@RequestMapping(uri=...)` 커스텀 어노테이션 정의(`@Retention(RUNTIME)`, `@Target(METHOD)`) 후, `getDeclaredMethods()`로 전체 메서드를 순회하며 `getDeclaredAnnotation()`으로 uri 일치 여부 확인, `method.invoke()`로 리플렉션 호출 | Spring의 `RequestMappingHandlerMapping`이 컨트롤러 메서드의 `@RequestMapping`/`@GetMapping` 등을 읽어 URI와 매칭시키고, `HandlerAdapter`가 리플렉션으로 해당 메서드를 호출하는 과정의 축소판 |
| ex03 | `App.java`, `BoardController.java`, `Controller.java`, `RequestMapping.java` | `@Controller`(TYPE 대상) 마커 어노테이션 추가. `Thread.currentThread().getContextClassLoader()`로 패키지 폴더의 `.class` 파일을 나열(`File.listFiles()`) → `Class.forName()`으로 클래스 로딩 → `isAnnotationPresent(Controller.class)`로 필터링 → `newInstance()`로 인스턴스 생성 → 리스트에 저장 → `findUri()`로 ex02와 동일한 방식의 리플렉션 호출 | Spring의 컴포넌트 스캔(`@ComponentScan`)이 클래스패스를 뒤져 `@Controller`/`@Service` 등이 붙은 클래스를 찾아 빈으로 등록하는 과정 + `DispatcherServlet`이 등록된 컨트롤러들 중에서 URI에 맞는 핸들러를 찾아 호출하는 전체 흐름의 축소판 |

ex01→ex02→ex03은 "이 클래스만 호출할 수 있음(하드코딩)" → "어노테이션으로 대상을 표시하면 리플렉션으로 찾아 호출할 수 있음" → "여러 클래스 중 마커 어노테이션이 붙은 것만 자동으로 찾아 등록·호출할 수 있음"으로 확장되며, 각각 스프링의 라우팅과 컴포넌트 스캔이 실제로 무엇을 하는지 손으로 재현합니다.

### ch02 게시판 CRUD

Spring Boot 프로젝트가 시작되는 챕터입니다. `@RestController`, `@Entity`, `EntityManager` 기반 CRUD 전체가 처음 등장합니다.

| 파일 | 역할 |
|------|------|
| `Springv3Application.java` | `@SpringBootApplication` 진입점 |
| `board/Board.java` | `@Entity` `@Table(name="board_tb")`. `@Id @GeneratedValue(IDENTITY)`, `@CreationTimestamp`로 생성시각 자동 기록. Lombok `@Data`만 사용(빌더 없음) |
| `board/BoardController.java` | `@RestController @RequestMapping("/api/boards")`. `GET /`, `GET /{boardId}`, `POST /`, `PUT /{boardId}`, `DELETE /{boardId}` 5개 REST 엔드포인트. 반환값은 `Resp.ok(...)`로 감싼 `ResponseEntity` |
| `board/BoardService.java` | `boardRepository`만 의존. 저장·수정·삭제 메서드에 `@Transactional`(`jakarta.transaction.Transactional`) |
| `board/BoardRepository.java` | Spring Data JPA 인터페이스가 아니라 `EntityManager`를 직접 주입받아 `find/persist/remove`를 호출하는 순수 JPA 방식. `update()` 메서드가 없음 |
| `board/BoardRequest.java` | `SaveDTO`, `UpdateDTO` record. 아직 `toEntity()` 없음(컨트롤러/서비스에서 setter로 직접 채움) |
| `core/util/Resp.java` | `record Resp<T>(status, msg, body)`. `Resp.ok(body)`/`Resp.fail(status, msg)` 정적 팩토리 |
| `resources/db/data.sql` | `board_tb`에 시드 데이터 2건 |

**데이터 흐름**: `BoardController` → `BoardService` → `BoardRepository`(EntityManager) → H2. 조회는 `em.find`/JPQL, 저장은 `em.persist`, 삭제는 `em.remove`.

**더티체킹이 코드에 직접 드러나는 지점**: `BoardService.게시글수정()`은 `boardRepository.findById()`로 영속 상태의 `Board`를 가져온 뒤 `board.setTitle()/setContent()`만 호출하고 별도 `save()`나 `update()` 호출이 없습니다. 메서드 끝의 주석 `// 트랜잭션 종료시 flush()`가 명시하듯, `@Transactional` 메서드 종료 시점에 영속성 컨텍스트가 변경을 감지해 자동으로 UPDATE 쿼리를 날리는 흐름입니다. `BoardRepositoryTest.update_test()`는 `em.flush()` + `em.clear()`로 이 시점을 강제로 눈에 보이게 만듭니다.

**테스트**: `BoardControllerTest`(`@SpringBootTest` + `@AutoConfigureMockMvc` + `@Transactional`, API 전체를 MockMvc로 검증하는 통합 테스트), `BoardRepositoryTest`(`@DataJpaTest`, 리포지토리 단위에 가까운 테스트, `System.out.println`으로 결과를 눈으로 확인하는 "eye" 패턴).

### ch03 전역 예외처리

| 구분 | 파일 | ch02 대비 변경 |
|------|------|----------------|
| 신규 | `core/handler/GlobalExceptionHandler.java` | `@RestControllerAdvice`. `Exception404`를 404 JSON으로, 그 외 `Exception`을 500 JSON으로 변환하는 `@ExceptionHandler` 2개 |
| 신규 | `core/handler/ex/Exception404.java` | `RuntimeException` 상속, 메시지만 담는 커스텀 예외 |
| 신규 | `board/BoardResponse.java` | `DTO`, `DetailDTO` record 추가. 엔티티를 그대로 노출하던 ch02와 달리 응답 전용 DTO로 분리 |
| 변경 | `board/BoardRepository.java` | `findById()`가 `Board` 대신 `Optional<Board>` 반환 |
| 변경 | `board/BoardService.java` | `boardRepository.findById(id).orElseThrow(() -> new Exception404(...))` 패턴으로 통일. (원천 코드는 클래스 레벨 `@Transactional(readOnly=true)` + 쓰기 메서드 재선언 조합이나, 완성본 rag-end에서는 **저자 결정 #2**에 따라 readOnly 제거·`org.springframework...Transactional`로 통일) |
| 변경 | `board/BoardRequest.java` | `SaveDTO.toEntity()` 추가 (Board.builder() 사용) |
| 변경 | `board/Board.java` | `@NoArgsConstructor` + `@Builder` 생성자 추가 (toEntity()가 사용) |
| 변경 | `board/BoardController.java` | 응답 타입을 `BoardResponse.DTO`/`DetailDTO`로 교체 |
| 테스트 | `BoardControllerTest` | `detail_notfound_test()` 추가 (404 + Resp 에러 포맷 검증) |

**핵심 변화**: (1) 엔티티를 API 응답에 직접 노출하지 않고 DTO로 감싸는 계층 분리, (2) `null` 체크 대신 `Optional` + `orElseThrow`로 예외를 던지고 `@RestControllerAdvice`가 일괄 JSON 변환하는 예외 기반 흐름 제어. (원천 코드에는 조회/쓰기를 `readOnly` 클래스·메서드 레벨로 나눈 조합도 있으나, 완성본은 **저자 결정 #2**로 제거·통일하므로 이 책에서는 다루지 않음)

### ch04 JWT 인증

Spring Security를 쓰지 않고 필터·인터셉터·JWT 유틸을 직접 구현합니다. `JwtProvider.java`, `JwtUtil.java` 주석에 "Spring Security 제거 후"라는 표현이 그대로 남아 있어, 이 프로젝트가 원래 Spring Security 기반이었던 것을 걷어내고 원리를 손으로 재구현한 버전임을 코드가 스스로 밝히고 있습니다.

| 구분 | 파일 | 역할 |
|------|------|------|
| 신규 | `user/User.java` | `@Entity`. `username`(unique), `password`, `email` |
| 신규 | `user/UserController.java` | `POST /join`(회원가입), `POST /login`(JWT 발급) |
| 신규 | `user/UserService.java` | 클래스 `@Transactional(readOnly=true)`. `회원가입()`: 유저네임 중복 체크 → BCrypt 암호화 → 저장. `로그인()`: 유저 조회 → 비밀번호 검증 → `JwtUtil.create()` |
| 신규 | `user/UserRepository.java`, `UserRequest.java` | `EntityManager` 기반 repository, `@Valid` 검증 어노테이션이 붙은 record DTO |
| 신규 | `core/util/PasswordEncoder.java` | `at.favre.lib:bcrypt` 라이브러리 래핑. `encode()`/`matches()` 2개 메서드만 노출 (BCrypt 내부 알고리즘은 다루지 않음) |
| 신규 | `core/util/JwtUtil.java` | `com.auth0:java-jwt`. `create(User)`로 `HMAC512` 서명 토큰 발급(subject=username, claim id=userId, 만료 7일), `verify(jwt)`로 토큰 복원 |
| 신규 | `core/util/JwtProvider.java` | 요청 헤더(`Authorization: Bearer ...`)에서 토큰을 꺼내는 `resolveToken()`, 토큰을 검증해 `User`를 반환하되 실패 시 `null`을 반환하는 `getUser()` |
| 신규 | `core/filter/JwtAuthenticationFilter.java` | `OncePerRequestFilter`. 토큰이 유효하면 `request.setAttribute("sessionUser", user)`만 하고 항상 다음 필터로 통과시킴(차단하지 않음) |
| 신규 | `core/interceptor/AuthInterceptor.java` | `HandlerInterceptor`. GET/OPTIONS는 통과, 그 외 메서드인데 `sessionUser` 속성이 없으면 `Exception401` 발생(여기서 실제 차단) |
| 신규 | `core/config/WebMvcConfig.java` | `AuthInterceptor`를 `/api/boards`, `/api/boards/**`에 등록 + CORS 허용 설정 |
| 신규 | `core/handler/ex/Exception401.java`, `Exception403.java` | 인증(401)/인가(403) 예외 |
| 변경 | `core/handler/GlobalExceptionHandler.java` | `ex401`, `ex403`, `exValid`(`MethodArgumentNotValidException` → 400) 핸들러 추가 |
| 변경 | `board/Board.java` | `@ManyToOne(fetch=EAGER) @JoinColumn(name="user_id") User user` 추가(작성자 연관관계) |
| 변경 | `board/BoardRequest.java` | `SaveDTO`에 `@NotEmpty`/`@Size` 검증 추가, `toEntity(User user)`로 작성자 연결 |
| 변경 | `board/BoardResponse.java` | `DetailDTO`에 `userId`, `username` 추가 |
| 변경 | `board/BoardRepository.java` | `findByIdJoinUser()` 추가 (`join fetch b.user`로 즉시 로딩, N+1 방지) |
| 변경 | `board/BoardService.java` | `게시글추가`가 `User sessionUser`를 받아 작성자 연결. `게시글수정`/`게시글삭제`는 `board.getUser().getId().equals(sessionUserId)`로 작성자 본인 확인 후 아니면 `Exception403` |
| 변경 | `board/BoardController.java` | 쓰기 메서드들이 `HttpServletRequest`에서 `sessionUser` attribute를 꺼내 서비스로 전달 |
| build.gradle | 추가 의존성 | `spring-boot-starter-validation`, `com.auth0:java-jwt:4.3.0`, `at.favre.lib:bcrypt:0.10.2` |
| data.sql | 추가 | `user_tb` 시드 2건, `board_tb`에 `user_id` 컬럼 값 추가 |

**데이터 흐름(인증)**: 클라이언트가 `Authorization: Bearer <jwt>` 헤더로 요청 → `JwtAuthenticationFilter`가 토큰을 검증해 유효하면 `request`에 `sessionUser`를 심어둠(차단 없음) → `AuthInterceptor`가 쓰기 요청에 한해 `sessionUser`가 없으면 401 발생(여기서 실질적 차단) → 컨트롤러가 `request.getAttribute("sessionUser")`로 로그인 유저를 꺼내 서비스에 전달 → 서비스가 게시글의 `board.getUser().getId()`와 비교해 본인이 아니면 403.

**필터와 인터셉터의 역할 분리가 코드로 명확히 드러남**: 필터는 "인증"(토큰이 유효한 사용자인지 확인해 정보만 심어둠), 인터셉터는 "인가"(그 정보가 있어야 하는 요청인지 판단해 실제로 막음)로 나뉘어 있습니다.

### ch05 댓글

| 구분 | 파일 | 역할 |
|------|------|------|
| 신규 | `reply/Reply.java` | `@Entity`. `comment`, `@ManyToOne(LAZY) User user`, `@ManyToOne(LAZY) Board board` |
| 신규 | `reply/ReplyController.java` | `POST /api/replies`(작성), `DELETE /api/replies/{replyId}`(삭제). 목록/수정 엔드포인트 없음(목록은 게시글 상세 응답에 내장) |
| 신규 | `reply/ReplyService.java` | 클래스 `@Transactional(readOnly=true)`. `댓글쓰기()`: `boardId`로 게시글 조회 후 `Reply` 생성·저장. `댓글삭제()`: 작성자 본인 확인 후 `Exception403`/삭제 (ch04 게시글 소유자 검증과 동일 패턴 재사용) |
| 신규 | `reply/ReplyRepository.java`, `ReplyRequest.java`, `ReplyResponse.java` | `EntityManager` 기반 repository, 검증 DTO, 응답 DTO |
| 변경 | `board/Board.java` | `@OneToMany(mappedBy="board", fetch=LAZY, cascade=CascadeType.REMOVE) List<Reply> replies` 추가. 게시글 삭제 시 댓글도 함께 삭제(cascade). **`user` 필드의 `fetch`가 ch04의 `EAGER`에서 `LAZY`로 변경됨** |
| 변경 | `board/BoardRepository.java` | `findByIdJoinUserAndReply()` 추가 (`join fetch b.user left join fetch b.replies`) |
| 변경 | `board/BoardService.java` | `게시글상세()`가 `sessionUserId`를 추가로 받아 `findByIdJoinUserAndReply()` 호출 |
| 변경 | `board/BoardResponse.java` | `DetailDTO`에 `isOwner`(로그인 사용자가 작성자인지), `List<ReplyDTO> replies`(각 댓글도 자체 `isOwner` 포함) 추가. `checkOwner()` 정적 헬퍼로 판단 |
| 변경 | `board/BoardController.java` | `detail()`이 더는 로그인을 요구하지 않고, `sessionUser`가 있으면 `sessionUserId`를 계산해 서비스에 전달(비로그인 시 `null`) → 목록·상세는 계속 공개, `isOwner` 계산만 선택적으로 이루어짐 |
| 변경 | `core/config/WebMvcConfig.java` | 인터셉터 경로에 `/api/replies`, `/api/replies/**` 추가 |
| data.sql | 추가 | `reply_tb` 시드 4건 |

**N+1과 fetch join을 실습으로 유도하는 구조**: `BoardRepositoryTest`(ch05)에는 `findByIdEager_test`, `findByIdLazy_test`, `findByIdLazyLoading_test`(글만 조회 후 `board.getUser().getUsername()`을 호출해 지연 로딩이 이 시점에 추가 쿼리를 발생시키는 것을 확인), `findByIdJoinUser_test`, `findByIdJoinUserAndReply_test`가 순서대로 배치되어 있습니다. `Board.user`의 fetch 전략을 ch04의 `EAGER`에서 ch05에 `LAZY`로 바꾼 뒤 이 테스트들로 "즉시 로딩 → 지연 로딩 → 지연 로딩의 N+1 문제 → `join fetch`로 해결"까지 손으로 확인하도록 설계되어 있습니다. 이는 코드에 실제로 존재하는, 매우 구체적인 JPA 성능 실습 소재입니다.

> **실습 설계 주의 (STEP 3에서 반드시 반영)**: ch05에서는 `Board.user`가 `LAZY`로 고정돼 있습니다. 그래서 `findByIdEager_test`와 `findByIdLazy_test`는 본문(둘 다 `getId()`만 출력, user 미접근)과 결과가 **동일**해서, 그대로 순서대로 실행하면 "즉시 로딩"이 눈에 드러나지 않습니다. 즉시 로딩을 실제로 관찰하려면 실습 시나리오에 "`Board.user`를 잠시 `EAGER`로 되돌려 실행 → 다시 `LAZY`로" 하는 **어노테이션 토글 단계**를 명시해야 합니다. N+1은 `findByIdLazyLoading_test`(`board.getUser().getUsername()` 호출 시점)에서 발생합니다. 이 단서를 실습 흐름에 넣지 않으면 독자가 "왜 EAGER와 LAZY가 똑같지?"에서 막힙니다.

---

## 핵심 기능 (의도 안)

| 기능 | 관련 코드 | 주요 기술 |
|------|-----------|-----------|
| URI-메서드 하드코딩 라우팅 | ch01 ex01 `App`, `BoardController` | 순수 Java, if-else |
| 커스텀 어노테이션 + 리플렉션 호출 | ch01 ex02 `RequestMapping`, `App.main` (리플렉션 순회 루프가 main 안에 있음. `findUri`는 ex03에만 존재) | `java.lang.annotation`, `java.lang.reflect.Method.invoke` |
| 컴포넌트 스캔 재구현 | ch01 ex03 `Controller`, `App.main` | `ClassLoader`, `Class.forName`, `isAnnotationPresent`, `newInstance` |
| 게시글 CRUD REST API | ch02~ch05 `board/*` | `@RestController`, `@GetMapping` 등, `ResponseEntity` |
| 순수 JPA 방식 Repository (EntityManager 직접 사용) | ch02~ch05 `BoardRepository`, `UserRepository`, `ReplyRepository` | `EntityManager.find/persist/remove`, JPQL |
| 영속성 컨텍스트와 더티체킹 | ch02 `BoardService.게시글수정`, ch02 `BoardRepositoryTest.update_test` | JPA 1차 캐시, `@Transactional` flush 시점 |
| 트랜잭션 경계 (`@Transactional`) | ch03~ch05 각 Service. 완성본은 readOnly 없이 `org.springframework...Transactional`로 통일 (저자 결정 #2) | Spring 선언적 트랜잭션 |
| 전역 예외 처리 + 커스텀 예외 계층 | ch03~ch05 `GlobalExceptionHandler`, `Exception401/403/404` | `@RestControllerAdvice`, `@ExceptionHandler` |
| 요청/응답 DTO 분리 | ch03~ch05 `BoardRequest`, `BoardResponse`, `UserRequest`, `ReplyRequest/Response` | Java record, 빌더 패턴 |
| Bean Validation | ch04~ch05 `UserRequest`, `BoardRequest` | `@NotEmpty`, `@Size`, `@Email`, `@Valid`, `MethodArgumentNotValidException` |
| JWT 발급/검증 | ch04~ch05 `JwtUtil`, `JwtProvider` | `com.auth0:java-jwt`, HMAC512 서명 |
| 비밀번호 해싱 (사용법) | ch04~ch05 `PasswordEncoder` | `at.favre.lib:bcrypt` |
| 필터 기반 인증 (차단 없이 정보만 심음) | ch04~ch05 `JwtAuthenticationFilter` | `OncePerRequestFilter`, `request.setAttribute` |
| 인터셉터 기반 인가 (실제 차단) | ch04~ch05 `AuthInterceptor`, `WebMvcConfig` | `HandlerInterceptor`, `InterceptorRegistry` |
| 리소스 소유자 검증 | ch04 게시글, ch05 댓글 | 도메인 로직(`board.getUser().getId().equals(sessionUserId)`) |
| 연관관계 매핑 (`@ManyToOne`, `@OneToMany`, cascade) | ch04~ch05 `Board.user`, `Board.replies`, `Reply.user/board` | JPA 연관관계, `CascadeType.REMOVE` |
| Fetch 전략과 N+1 문제 | ch05 `Board.user`(EAGER→LAZY 변경), `BoardRepository.findByIdJoinUser*`, `BoardRepositoryTest` 5종 실습 | `FetchType`, `join fetch` |
| 단위/통합 테스트 | 전 챕터 `*Test.java` | JUnit5, `@SpringBootTest`+`MockMvc`(통합), `@DataJpaTest`(단위에 가까움) |
| 댓글 CRUD (작성/삭제, 목록은 게시글 상세에 내장) | ch05 `reply/*` | 위 기술들의 조합 응용 |

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|-----------|-----------|
| BCrypt 해시 알고리즘 내부 동작(salt 생성, cost factor 연산 원리) | `core/util/PasswordEncoder.java` (`BCrypt.withDefaults().hashToString()`) | seed.md 의도 밖. `encode()`/`matches()` 사용법까지만 다루고 내부 알고리즘은 다루지 않음 |
| Gradle 빌드 설정 상세 (`plugins`, `toolchain`, `dependency-management` 동작 원리) | 각 챕터 `build.gradle` | 의존성 "추가" 수준까지만 다룸. 플러그인 내부 동작은 의도 밖 |
| H2 이외 실제 DB(MySQL 등) 전환 | 없음 (전 챕터 `application.properties`가 H2 인메모리 고정) | 코드 자체에 존재하지 않음. 로컬 H2 실행까지만 다룸 |
| 프론트엔드·화면 렌더링 (JSP·타임리프) | 없음 (전 챕터 `templates/` 디렉토리 없음, `@RestController`만 존재) | 코드 자체에 존재하지 않음. API·백엔드에 집중 |
| 배포·운영 (Docker, 클라우드) | 없음 (`Dockerfile`, CI/CD 설정 없음) | 코드 자체에 존재하지 않음. 로컬 실행까지만 다룸 |

> CORS 설정(`WebMvcConfig.addCorsMappings`)은 **저자 결정 #3**에 따라 이 책에 **포함**한다(제외 아님). `WebMvcConfig`에서 인터셉터 등록과 함께 등장하므로, 깊이(한 줄 언급 vs 상세)는 ch04 집필 시 결정한다.

## 기술 스택 정리

| 기술 | 버전 | 용도 |
|------|------|------|
| Java | 21 (toolchain) | 언어 |
| Spring Boot | 4.0.3 | 웹 프레임워크 (ch02부터) |
| Spring Web (`spring-boot-starter-web`) | Boot 관리 버전 | REST 컨트롤러, MVC 인프라(필터·인터셉터) |
| Spring Data JPA (`spring-boot-starter-data-jpa`) | Boot 관리 버전 | JPA/Hibernate 구동, `EntityManager` 제공 (Repository 인터페이스 자체는 사용 안 함) |
| Spring Validation (`spring-boot-starter-validation`) | Boot 관리 버전 | `@Valid`, Bean Validation 어노테이션 (ch04부터) |
| H2 Database | Boot 관리 버전 (runtime) | 로컬 인메모리 DB |
| Lombok | compileOnly | `@Data`, `@Builder`, `@NoArgsConstructor`, `@RequiredArgsConstructor` |
| java-jwt (auth0) | 4.3.0 | JWT 생성/검증 (ch04부터) |
| bcrypt (at.favre.lib) | 0.10.2 | 비밀번호 해싱 (ch04부터) |
| JUnit 5 + Spring Test | `spring-boot-starter-test` | 단위/통합 테스트, MockMvc |
| `spring-boot-data-jpa-test`, `spring-boot-webmvc-test` | Boot 관리 버전 | `@DataJpaTest`, `@AutoConfigureMockMvc` 슬라이스 테스트 |

## 기술 의존성 메모

실제 코드에서 확인된 선후행 개념만 기록합니다.

- **리플렉션 → 어노테이션 → 스프링 매핑/스캔**: ch01 ex02(리플렉션 `invoke`)를 이해해야 ex03(스캔)이 자연스럽고, ex03을 거쳐야 ch02의 `@RestController`/`@RequestMapping`이 "마법이 아니라 리플렉션 기반 프레임워크 코드"로 읽힙니다. ch01 3단계를 건너뛰고 ch02로 가면 이 책의 차별점(마법을 벗겨낸다)이 성립하지 않습니다.
- **`EntityManager`를 먼저 이해해야 더티체킹이 이해됨**: ch02 `BoardRepository`가 Spring Data JPA 인터페이스가 아니라 `EntityManager`를 직접 씁니다. `em.find()`로 가져온 엔티티가 영속 상태라는 것, 영속성 컨텍스트가 스냅샷을 들고 있다는 개념이 먼저 서야 `BoardService.게시글수정()`에 왜 `save()` 호출이 없는지 설명이 가능합니다.
- **더티체킹 → `@Transactional` 경계**: 더티체킹은 트랜잭션이 끝나는 시점(`flush()`)에 일어납니다. `BoardRepositoryTest.update_test()`가 `em.flush()` + `em.clear()`를 명시적으로 호출하는 이유(영속성 컨텍스트를 강제로 비워 DB에 실제로 반영됐는지 확인)를 설명하려면 트랜잭션 경계와 영속성 컨텍스트의 생명주기(보통 트랜잭션과 함께 시작·종료)를 먼저 짚어야 합니다.
- **`Optional` + `orElseThrow` → 전역 예외 처리**: ch03에서 `findById()`가 `Optional<Board>`로 바뀌고 서비스에서 `orElseThrow(() -> new Exception404(...))`가 등장합니다. `@RestControllerAdvice`를 설명하기 전에 "예외가 어디서 발생해 어떻게 컨트롤러까지 전파되는가"의 그림이 먼저 필요합니다.
- **필터 → 인터셉터 순서 의존**: `JwtAuthenticationFilter`는 서블릿 필터 체인(스프링 컨텍스트 진입 전)에서 동작하고, `AuthInterceptor`는 `DispatcherServlet` 내부(핸들러 결정 후)에서 동작합니다. 필터가 먼저 실행되어 `sessionUser`를 세팅해 둬야 인터셉터가 그 값을 읽을 수 있는 순서 의존 관계입니다. 이 둘의 실행 시점 차이(서블릿 필터 vs 스프링 MVC 인터셉터)를 그림으로 짚어야 "왜 두 개로 나눴는지"가 설명됩니다.
- **JWT 발급/검증 → 인증 정보 전달 경로**: `UserService.로그인()`이 `JwtUtil.create()`로 토큰을 만들고, 클라이언트가 그 토큰을 헤더에 담아 재요청하면 `JwtProvider.resolveToken()` → `JwtUtil.verify()` → 필터의 `request.setAttribute()` → 컨트롤러의 `request.getAttribute()` 순서로 흘러갑니다. 토큰이 세션을 대체하는 무상태(stateless) 인증이라는 개념이 이 흐름 설명의 전제입니다.
- **소유자 검증 패턴의 반복**: ch04 게시글 수정/삭제와 ch05 댓글 삭제가 동일한 `resource.getUser().getId().equals(sessionUserId)` 패턴을 반복합니다. ch05를 쓸 때 ch04에서 이미 설명한 패턴이라는 것을 명시적으로 회수하면 좋습니다.
- **연관관계 매핑 → fetch 전략 → N+1**: `@ManyToOne`/`@OneToMany`를 먼저 이해해야 `FetchType.EAGER`/`LAZY` 차이가 의미를 가지고, fetch 전략을 이해해야 ch05의 `findByIdEager_test`~`findByIdJoinUserAndReply_test` 5종 테스트가 보여주는 "지연 로딩이 추가 쿼리를 유발한다 → join fetch로 한 번에 가져온다"는 흐름이 설명됩니다. ch04(EAGER)에서 ch05(LAZY로 변경)로 넘어가는 지점이 N+1 문제를 도입하기에 가장 자연스러운 자리입니다.
- **Bean Validation → 전역 예외 처리 확장**: `@Valid`가 실패하면 `MethodArgumentNotValidException`이 발생하고, 이것도 ch03에서 만든 `GlobalExceptionHandler`에 핸들러 하나만 추가하는 형태로 확장됩니다. 즉 ch04의 검증 실패 처리는 새 개념이 아니라 ch03 예외 처리 구조의 재사용입니다.

---

## 저자 결정 (확정)

STEP 2 확인 사항에 대한 저자 결정입니다. 이후 STEP 3~5는 이 결정을 기준으로 진행합니다.

1. **레포명·패키지**: 완성본 레포 `spring-end`, 예제 레포 `spring-start`. 패키지에서 `springv3`를 제거하여 `com.metacoding.springv3` → **`com.metacoding.spring`** 으로 전 챕터 일괄 리네임. (실제 코드 반영은 rag-end/rag-start 생성 시점)
2. **`@Transactional` / readOnly**: `readOnly=true`를 **제거**하고 전 챕터를 `org.springframework.transaction.annotation.Transactional`로 **통일**한다. 클래스 레벨 읽기전용 선언 제거, 쓰기 메서드에 `@Transactional`. ch02~05 import가 하나로 맞춰지므로 "import가 왜 바뀌나" 설명은 다루지 않는다(개념 하나 축소).
3. **CORS(`WebMvcConfig.addCorsMappings`)**: 일단 포함한다. 깊이(한 줄 언급 vs 상세)는 ch04 집필 시 결정.
4. **ch05 fetch 5단계 실습**: `findByIdEager_test` → `findByIdLazy_test` → `findByIdLazyLoading_test`(N+1 재현) → `findByIdJoinUser_test` → `findByIdJoinUserAndReply_test`를 실습으로 그대로 따라가게 한다. 이 책 JPA 파트의 하이라이트.
5. **ch01 실행 방식**: 순수 자바(`build.gradle` 없음)이므로, IDE(인텔리제이)에서 각 `App.java`의 `main()`을 실행하는 방식으로 안내한다.
