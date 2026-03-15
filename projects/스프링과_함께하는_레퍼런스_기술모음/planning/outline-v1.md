# 목차 + 코드 배치 — 스프링과 함께하는 레퍼런스 기술 모음

## 페이지 배분 (100페이지 기준)

| 장 | 제목 | 난이도 | 페이지 | 비고 |
|---|---|---|---|---|
| 1 | Docker로 시작하는 개발 환경 | 하 | 9p | 개념 간결, 실습 단순 |
| 2 | OAuth 2.0 & OIDC (Kakao) | 중상 | 14p | SSR + OIDC 두 실습, JWT 심화 축소 |
| 3 | Redis 세션 공유 | 중 | 10p | docker-compose 활용, 구조 명확 |
| 4 | Base64 이미지 업로드 | 하 | 9p | 코드 직관적, 쉬어가는 장 |
| 5 | Presigned URL + S3 + Lambda | 중상 | 13p | 3단계 반복 실습, AWS 콘솔 설정 부록 이동 |
| 6 | Polling / SSE / WebSocket 비교 | 중 | 12p | 3가지 구현 비교 |
| 7 | 대규모 스트리밍과 기술 선택 | 중상 | 11p | FFmpeg HLS + 기술 선택 가이드 중심 |
| 8 | Elasticsearch 키워드 검색 | 중 | 12p | ES+Kibana, 검색 구현 |
| 9 | RabbitMQ 메시지 큐 | 중 | 10p | Producer/Consumer 구조 |
| **합계** | | | **100p** | |

---

## 난이도 곡선

### 장별 난이도

```
난이도
  상  |
중상  |      *              *         *
  중  |           *              *         *    *
  하  |  *              *
      +----+----+----+----+----+----+----+----+----
         1    2    3    4    5    6    7    8    9
```

**패턴: 파도형**. 어려운 장(2, 5, 7) 다음에 쉬운 장(3, 4, 6)이 와서 숨을 돌릴 틈을 줍니다.

### 장 내부 섹션별 난이도

```
1장  [하─하─하]           평탄 (진입 장벽 최소화)
2장  [하─중─중상─중상─중]  전반 개념 → 후반 구현으로 상승
3장  [하─중─중─하]        중반 피크 → 확인 단계에서 하강
4장  [하─하─중─하]        거의 평탄, 서비스 로직에서만 약간 상승
5장  [하─중─중상─중─중상─중상─하]  3단계 반복 실습, 계단식 상승
6장  [하─중─중─중상─중]   WebSocket에서 피크
7장  [하─중─중상─중─하]   FFmpeg 인코딩이 피크, 기술 선택 가이드에서 하강
8장  [하─중─중─중─중─중─하]  고르게 중, Fuzzy에서 약간 상승
9장  [하─중─중─중─중─하]   균등 분포
```

---

## 장별 세부 목차

---

### 1장 Docker로 시작하는 개발 환경 (9p, 1주차)

**레포**: `kjh5848/spring-docker` (완성), `kjh5848/spring-app` (Spring 서버)

#### 이야기 파트 (2p)
- 입사 첫 날, "Docker로 환경 맞추세요" — 첫 마디에 멈칫하다
- 로컬 설치 버전 충돌 에피소드

#### 기술 파트 (6p)

**1.1 도커는 왜 필요한가** (1p)
- 환경 격리 개념, "통째로 묶어서 실행"

**1.2 Dockerfile + entrypoint.sh** (2p)
- Dockerfile 구조 [설명]
- entrypoint.sh 자동 빌드/실행 [설명]

**1.3 docker-compose로 Spring 서버 실행** (2p)
- docker-compose.yml 구성 [실습]
- `docker compose up` / `docker compose down` [실습]
- 실행 결과 확인 (localhost:8080)

**1.4 도커 명령어 정리** (1p)
- 핵심 명령어 표 [참고]

#### 닫기 (1p)
- "이것만은 기억하자": 환경을 코드로 관리한다
- 다음 예고: "다음 주, 카카오 로그인을 붙여달라는 요청이 옵니다"

#### 파일 트리 + 태그

```
kjh5848/spring-docker/
├── Dockerfile           [설명] 이미지 빌드 설정
├── entrypoint.sh        [설명] 컨테이너 시작 시 자동 실행
└── docker-compose.yml   [실습] 서비스 정의 + 포트 매핑

kjh5848/spring-app/
└── SpringDokerController.java  [참고] health check 엔드포인트
```

---

### 2장 OAuth 2.0 & OIDC — Kakao 소셜 로그인 (14p, 2주차)

**레포**: `kakao-oauth-code-ssr-start/end`, `kakao-oauth-code-oidc-start/end`

#### 이야기 파트 (2p)
- "카카오 소셜 로그인 붙여주세요" — 용어 폭격에 당황하다
- OAuth 흐름도 화살표 앞에서 얼어붙는 장면

#### 기술 파트 (10p)

**2.1 준비** (1p)
- 카카오 디벨로퍼 앱 설정 요약 [참고]
- Redirect URI, REST API 키, Client Secret [참고]

**2.2 SSR: Code 방식 로그인** (4p)
- OAuth 2.0 구성 요소 (Resource Owner, Authorization Server, Client) [설명]
- Authorization Code 방식 프로세스 [설명]
- 인가 코드 요청 → Access Token 교환 → 사용자 정보 조회 [실습]
- 세션 로그인 처리 [실습]

**2.3 REST API: Code + OIDC 검증** (4p)
- 대칭키 vs 공개키 개념 [설명]
- OIDC란 무엇인가 — ID Token = 신분증 [설명]
- OIDC 프로세스 (ID Token 발급 → JWKS 공개키 검증) [설명]
- JWT 인증 필터 구현 [실습]

**2.4 정리** (1p)
- Code 방식 vs Code+OIDC 방식 비교표 [참고]
- JWT 심화 (Access/Refresh Token 전략)는 짧게 언급만

#### 닫기 (2p)
- "이것만은 기억하자": OAuth는 결국 토큰 교환
- 다음 예고: "서버가 2대가 되면서 로그인이 풀리기 시작합니다"

#### 파일 트리 + 태그

```
kakao-oauth-code-ssr-start → end/
├── KakaoController.java        [실습] 인가코드 수신 + Token 교환
├── KakaoService.java           [실습] RestTemplate으로 카카오 API 호출
├── KakaoTokenResponse.java     [설명] 토큰 응답 DTO
├── UserController.java         [실습] 세션 로그인 처리
└── templates/login.mustache    [참고] 카카오 로그인 버튼 UI

kakao-oauth-code-oidc-start → end/
├── OidcController.java         [실습] ID Token 수신
├── JwksService.java            [실습] JWKS 공개키 조회 + RSA 검증
├── JwtAuthFilter.java          [실습] JWT 인증 필터
└── SecurityConfig.java         [설명] 필터 등록
```

---

### 3장 Redis 세션 공유 (10p, 3주차)

**레포**: `docker-session-share`

#### 이야기 파트 (2p)
- 서버 2대로 늘렸더니 로그인이 풀리는 현상
- "누구세요?" 에러 메시지를 보며 당황하는 장면

#### 기술 파트 (7p)

**3.1 전체 아키텍처** (1p)
- Client → Nginx → Spring A/B → Redis 개념도 [설명]

**3.2 Spring Session + Redis 설정** (2p)
- application.properties (Redis 접속 정보) [실습]
- build.gradle (spring-session-data-redis) [실습]
- HomeController (세션 읽기/쓰기) [설명]

**3.3 Nginx 경로 기반 라우팅** (1.5p)
- nginx.conf (upstream + location) [설명]

**3.4 docker-compose 구성** (1p)
- docker-compose.yml (Redis + Nginx + Spring 2대) [실습]

**3.5 실행 & 세션 공유 확인** (1.5p)
- /app1 → /app2 → /app1 요청으로 count 증가 확인 [실습]

#### 닫기 (1p)
- "이것만은 기억하자": 서버를 늘리면 상태를 외부로 분리한다
- 다음 예고: "프로필 사진을 넣어달라는 요청이 옵니다"

#### 파일 트리 + 태그

```
docker-session-share/
├── docker-compose.yml                    [실습] 전체 인프라 구성
├── nginx/nginx.conf                      [설명] 경로 기반 라우팅
├── app1/
│   ├── application.properties            [실습] Redis 세션 설정
│   ├── build.gradle                      [실습] 의존성 추가
│   ├── HomeController.java               [설명] 세션 카운터 로직
│   └── templates/index.mustache          [참고] 서버명 + 카운트 표시
└── app2/
    └── (app1과 동일 구조)                 [참고]
```

---

### 4장 Base64 이미지 업로드 (9p, 4주차)

**레포**: `spring-base64`, `react-base64`

#### 이야기 파트 (1.5p)
- "프로필에 사진 넣어주세요" — 이미지를 서버에 어떻게 보내지?
- 파일 업로드라는 처음 접하는 영역

#### 기술 파트 (6.5p)

**4.1 전체 흐름 한눈에 보기** (1p)
- Postman → Spring → 파일 저장 → DB 기록 → URL 반환 [설명]

**4.2 엔티티 + DTO 설계** (1p)
- ImageEntity (id, uuid, fileName, url) [설명]
- ImageRequest (fileName, fileData) [설명]
- ImageResponse [참고]

**4.3 업로드 API 구현** (2p)
- Base64 디코딩 (Base64.getDecoder().decode) [실습]
- UUID 파일명 생성 [실습]
- 로컬 디스크 저장 (Files.write) [실습]
- DB 저장 [실습]

**4.4 정적 리소스 매핑 + 조회 API** (1.5p)
- WebConfig (/uploads/** → file:uploads/) [설명]
- 목록 조회, 단건 조회 API [참고]

**4.5 React 연동** (1p)
- CORS 설정 [설명]
- 이미지 업로드/목록/상세 확인 [참고]

#### 닫기 (1p)
- "이것만은 기억하자": 이미지도 결국 문자열 (Base64)
- 다음 예고: "이미지가 쌓이면서 서버 디스크가 가득 찹니다"

#### 파일 트리 + 태그

```
spring-base64/
├── ImageController.java      [참고] 엔드포인트 정의
├── ImageService.java         [실습] Base64 디코딩 + UUID + 저장
├── ImageEntity.java          [설명] 엔티티 구조
├── ImageRequest.java         [설명] 요청 DTO (fileName, fileData)
├── ImageResponse.java        [참고] 응답 DTO
├── ImageRepository.java      [참고] JPA Repository
├── WebConfig.java            [설명] 정적 리소스 매핑
├── CorsConfig.java           [설명] CORS 설정
└── application.properties    [참고] 정적 리소스 경로

react-base64/
└── (React 프로젝트)           [참고] 프론트 연동 확인용
```

---

### 5장 Presigned URL + S3 + Lambda (13p, 5주차)

**레포**: `spring-presign-url-start/end`

#### 이야기 파트 (2p)
- 서버 디스크 사용량 90% 알림이 울리다
- 4장에서 로컬에 저장한 게 문제였다는 깨달음
- 이 장은 클라우드 환경(AWS)이 필요한 유일한 장. 실무에서 반드시 마주치는 패턴이므로 포함

#### 기술 파트 (9p)

**5.1 아키텍처 구조** (1.5p)
- Client → Spring(URL 발급) → S3(직접 업로드) → Lambda(리사이즈) [설명]
- Presigned URL이란: 서버를 거치지 않는 업로드 [설명]

**5.2 Spring 서버 구현 1 — Presigned URL 발급** (2p)
- AWS S3 설정 (application.properties) [실습]
- PresignedUrlService (Presigned URL 생성) [실습]
- Postman 실습 1: URL 발급 확인 [실습]

**5.3 Lambda 리사이즈 구현** (2p)
- Lambda 함수 (Python) [설명]
- S3 이벤트 트리거 설정 개요 [참고]

**5.4 Spring 서버 구현 2 — Resized URL 저장** (1.5p)
- S3에서 리사이즈된 이미지 URL 조회 [실습]
- DB 저장 + 응답 [실습]

**5.5 Spring 서버 구현 3 — 전체 흐름 통합** (1p)
- 3단계 통합 실습 [실습]

**5.6 AWS 콘솔 설정 (부록 참조)** (1p)
- IAM/S3 버킷/Lambda 설정 핵심만 요약 [참고]
- 상세 캡처는 부록으로 이동

#### 닫기 (2p)
- "이것만은 기억하자": 서버가 모든 걸 처리할 필요는 없다
- AWS 계정 필요 안내
- 다음 예고: "실시간 알림이 필요해집니다"

#### 파일 트리 + 태그

```
spring-presign-url-start → end/
├── S3Config.java               [실습] AWS S3 클라이언트 설정
├── PresignedUrlService.java    [실습] Presigned URL 생성
├── ImageController.java        [실습] 업로드/조회 엔드포인트
├── ImageService.java           [실습] Resized URL 저장 로직
├── ImageEntity.java            [설명] 엔티티 (원본URL + 리사이즈URL)
├── application.properties      [실습] AWS 접속 정보
└── lambda/
    └── resize_function.py      [설명] Lambda 리사이즈 코드 (Python)
```

---

### 6장 Polling / SSE / WebSocket 실전 비교 (12p, 7주차)

**레포**: `spring-polling`, `spring-sse`, `spring-websoket`

#### 이야기 파트 (2p)
- "새 댓글 알림이 바로 떠야 해요" — 실시간이라는 단어에 막막해지다
- 세 가지 방법이 있다는 걸 알게 되는 장면

#### 기술 파트 (8.5p)

**6.1 실시간 통신이란** (1p)
- Polling vs SSE vs WebSocket 개념 비교표 [설명]
- 언제 무엇을 쓰는가 [설명]

**6.2 Polling 구현 (Ajax)** (2p)
- NotificationController (알림 저장/조회) [설명]
- JS setInterval 2초 간격 Ajax 호출 [설명]
- 동작 확인 [참고]

**6.3 SSE 구현 (Server-Sent Events)** (2.5p)
- SseEmitter 생성 + 이벤트 전송 [실습]
- SseController (구독/발행 엔드포인트) [실습]
- EventSource JS 클라이언트 [설명]
- 동작 확인 [참고]

**6.4 WebSocket 구현 (STOMP)** (2.5p)
- WebSocketConfig (STOMP 엔드포인트 + 메시지 브로커) [설명]
- MessageController (@MessageMapping) [설명]
- SockJS + STOMP 클라이언트 [설명]
- 동작 확인 [참고]

**6.5 세 방식 비교 정리** (0.5p)
- 비교표: 연결 방식, 방향, 적합 시나리오 [참고]

#### 닫기 (1.5p)
- "이것만은 기억하자": 요구사항에 따라 방식을 고른다
- 다음 예고: "영상 콘텐츠 서비스를 준비합니다"

#### 파일 트리 + 태그

```
spring-polling/
├── NotificationController.java   [설명] 알림 CRUD API
├── NotificationService.java      [설명] 인메모리 알림 저장
└── templates/index.mustache      [설명] Ajax setInterval 폴링

spring-sse/
├── SseController.java            [실습] SseEmitter 구독/발행
├── SseService.java               [실습] Emitter 관리
└── templates/index.mustache      [설명] EventSource 클라이언트

spring-websoket/
├── WebSocketConfig.java          [설명] STOMP 설정
├── MessageController.java        [설명] @MessageMapping 핸들러
├── StompInterceptor.java         [설명] 연결 인터셉터
└── templates/index.mustache      [설명] SockJS + STOMP 클라이언트
```

---

### 7장 대규모 스트리밍과 기술 선택 (11p, 8주차)

**레포**: `spring-polling` (스트리밍 기반 코드), `BtbN/FFmpeg-Builds` (외부)

#### 이야기 파트 (2p)
- "영상도 WebSocket으로 되지 않아?" — 차원이 다른 문제
- 1GB 영상 로딩에 몇 분이 걸리는 장면

#### 기술 파트 (7.5p)

**7.1 HLS 스트리밍이란** (1p)
- "잘게 쪼개서 순서대로 보낸다" — m3u8 + ts 구조 [설명]
- 프로젝트 구조 개요 [설명]

**7.2 업로드 API 구현** (1.5p)
- MultipartFile 업로드 컨트롤러 [설명]
- 파일 저장 서비스 [설명]

**7.3 FFmpeg 인코딩 & HLS 조각화** (2p)
- FFmpeg 설치 및 Java 래퍼 [설명]
- 720p/1080p 인코딩 + ts 분할 [설명]
- master.m3u8 생성 [설명]

**7.4 HLS 스트리밍 제공** (1.5p)
- 정적 리소스 매핑 (/hls/**) [설명]
- 클라이언트 HLS.js 재생 [설명]

**7.5 스트리밍 기술 선택 가이드** (1.5p)
- HLS vs DASH vs RTMP 비교 [참고]
- 규모별 아키텍처 판단 기준 [참고]
- CDN 활용 방향 [참고]

#### 닫기 (1.5p)
- "이것만은 기억하자": 영상 스트리밍 = 쪼개기 + 순서 보장
- 다음 예고: "검색이 5초 넘게 걸린다는 버그 리포트가 올라옵니다"

#### 파일 트리 + 태그

```
spring-polling/ (스트리밍 프로젝트)
├── VideoController.java         [설명] 업로드 + 스트리밍 엔드포인트
├── VideoService.java            [설명] FFmpeg 인코딩 호출
├── FfmpegService.java           [설명] FFmpeg 래퍼 (HLS 변환)
├── WebConfig.java               [설명] /hls/** 정적 매핑
├── application.properties       [참고] 저장 경로 설정
└── templates/player.mustache    [참고] HLS.js 플레이어 UI
```

---

### 8장 Elasticsearch 키워드 검색 (12p, 10주차)

**레포**: `docker-elasticsearch`

#### 이야기 파트 (2p)
- "검색이 5초 넘게 걸려요" — LIKE '%키워드%'의 한계
- 검색 엔진이라는 낯선 세계

#### 기술 파트 (8.5p)

**8.1 왜 Elasticsearch가 필요한가** (1.5p)
- LIKE 검색의 한계 (Full Table Scan) [설명]
- 역인덱스(Inverted Index) 원리 [설명]

**8.2 실습 환경 준비** (1p)
- docker-compose.yml (ES + Kibana) [실습]
- Spring 의존성 + 접속 설정 [실습]

**8.3 데이터 모델 설계 (RDB + ES)** (1p)
- JPA Entity + ES Document 매핑 [설명]
- @Document, @Field 어노테이션 [설명]

**8.4 저장 흐름: RDB + ES 이중 저장** (1.5p)
- BoardService (JPA 저장 + ES 저장) [실습]
- ElasticsearchRepository 사용 [실습]

**8.5 검색 흐름: ES 검색 → RDB 재조회** (1.5p)
- multi_match 가중치 검색 (제목 x3, 내용 x1) [실습]
- ES에서 ID 목록 → JPA findAllById [실습]

**8.6 Fuzzy 검색 + nori 한글 분석기** (2p)
- Fuzzy 검색 개념 (편집 거리) [설명]
- nori 분석기 설정 + 인덱스 매핑 [실습]
- Kibana에서 검색 테스트 [참고]

#### 닫기 (1.5p)
- "이것만은 기억하자": 검색 엔진은 왜 따로 있는가
- 다음 예고: "시스템 간 연동을 자동화해야 합니다"

#### 파일 트리 + 태그

```
docker-elasticsearch/
├── docker-compose.yml            [실습] ES + Kibana 구성
├── BoardEntity.java              [설명] JPA 엔티티
├── BoardDocument.java            [설명] ES Document 매핑
├── BoardRepository.java          [참고] JPA Repository
├── BoardSearchRepository.java    [참고] ES Repository
├── BoardService.java             [실습] 이중 저장 + 검색 로직
├── BoardController.java          [참고] 엔드포인트
├── SearchService.java            [실습] multi_match + Fuzzy 검색
└── application.properties        [실습] ES 접속 설정
```

---

### 9장 RabbitMQ 메시지 큐 (10p, 12주차)

**레포**: `rabbitmq-producer`, `rabbitmq-consumer`, `rabbitmq-docker`

#### 이야기 파트 (2p)
- "API 직접 호출하면 되지 않나?" — 결합도의 함정
- GitHub이 느려지면 우리 시스템도 느려지는 문제

#### 기술 파트 (7p)

**9.1 시나리오와 전체 구조** (1p)
- GitHub Polling → Producer → RabbitMQ → Consumer 흐름 [설명]
- Exchange/Queue/Routing Key 개념 [설명]

**9.2 실습 환경** (0.5p)
- docker-compose.yml (RabbitMQ) [실습]
- 관리 콘솔 접속 확인 [참고]

**9.3 Producer 구현** (2p)
- GitHub 파일 Polling 설계 (RestTemplate + @Scheduled) [설명]
- RabbitMQ 메시지 발행 (RabbitTemplate.convertAndSend) [실습]
- Exchange/Queue 설정 (RabbitConfig) [실습]

**9.4 Consumer 구현** (1.5p)
- @RabbitListener로 메시지 수신 [실습]
- 파일 반영 로직 (다운로드 + 저장) [실습]

**9.5 통합 테스트 시나리오** (1p)
- Producer + RabbitMQ + Consumer 전체 실행 [실습]
- 관리 콘솔에서 메시지 흐름 확인 [참고]

**9.6 실무 확장 포인트** (1p)
- Dead Letter Queue, 재시도 정책 [참고]
- 다중 Consumer 구조 [참고]

#### 닫기 (1p)
- "이것만은 기억하자": 직접 호출 vs 메시지 큐 간접 호출
- 에필로그 예고: "3개월 전 얼어붙던 터미널 앞에서..."

#### 파일 트리 + 태그

```
rabbitmq-docker/
└── docker-compose.yml            [실습] RabbitMQ 구성

rabbitmq-producer/
├── GitHubPollingService.java     [설명] @Scheduled GitHub 파일 감지
├── RabbitConfig.java             [실습] Exchange/Queue/Binding 설정
├── MessagePublisher.java         [실습] RabbitTemplate 메시지 발행
└── application.properties        [실습] RabbitMQ 접속 정보

rabbitmq-consumer/
├── MessageConsumer.java          [실습] @RabbitListener 수신
├── FileProcessService.java      [실습] 파일 다운로드 + 저장
└── application.properties        [실습] RabbitMQ 접속 정보
```

---

## 코드 태그 요약

### 태그별 파일 수

| 태그 | 파일 수 | 설명 |
|------|---------|------|
| [실습] | 36개 | 독자가 직접 작성. 전체 코드 제공 |
| [설명] | 36개 | 핵심 흐름만 발췌하여 설명 |
| [참고] | 22개 | 코드 블록 없이 메서드/설정 표로 요약 |

### 장별 태그 분포

| 장 | [실습] | [설명] | [참고] |
|---|---|---|---|
| 1장 Docker | 1 | 3 | 1 |
| 2장 OAuth | 5 | 5 | 4 |
| 3장 Redis | 4 | 3 | 2 |
| 4장 Base64 | 3 | 4 | 5 |
| 5장 S3 | 6 | 2 | 1 |
| 6장 Polling/SSE/WS | 2 | 10 | 4 |
| 7장 스트리밍 | 0 | 5 | 3 |
| 8장 ES | 5 | 3 | 3 |
| 9장 RabbitMQ | 6 | 2 | 3 |

**6장은 SSE를 [실습]으로 직접 구현하고, Polling/WebSocket은 [설명]으로 비교합니다.** 7장은 clone 후 핵심 로직을 파악하는 [설명] 중심입니다. 나머지 장은 start/end 또는 단일 레포에서 [실습] 비중이 높습니다.

---

## 부록 (별도 페이지 불포함)

- **부록 A**: AWS 콘솔 설정 상세 (5장 IAM/S3/Lambda 캡처)
- **부록 B**: JWT Access/Refresh Token 전략 (2장 심화)
