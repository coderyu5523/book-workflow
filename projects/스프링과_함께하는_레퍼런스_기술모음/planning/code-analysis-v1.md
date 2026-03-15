# 코드 분석 — 스프링과 함께하는 레퍼런스 기술 모음

## 분석 대상

기존 노션 콘텐츠 (`projects/4 스프링과 함께 하는 레퍼런스 기술 모음 (집필 - 김주혁)/`) 기반 분석. code/ 폴더는 비어 있으며, 장별 개별 GitHub 레포를 참조합니다.

---

## 장별 핵심 기능 목록

| 장 | 핵심 기능 | 난이도 |
|---|---|---|
| 1장 Docker | Dockerfile 작성, docker-compose.yml 구성, entrypoint.sh 자동 빌드/실행 | 하 |
| 2장 OAuth2.0/OIDC | 카카오 인가코드 요청, Access Token 발급, OIDC ID Token 검증(JWKS/RSA), JWT 인증필터 | 중상 |
| 3장 Redis 세션 | Spring Session + Redis, Nginx 리버스 프록시, 2대 서버 세션 공유 | 중 |
| 4장 Base64 업로드 | Base64 인코딩/디코딩, UUID 파일명, 정적 리소스 매핑, React 연동 | 하 |
| 5장 Presigned URL | AWS S3 Presigned URL 발급, Lambda 이미지 리사이즈, 3단계 반복 실습 | 중상 |
| 6장 Polling/SSE/WebSocket | Polling(Ajax 2초), SSE(SseEmitter), WebSocket/STOMP 비교 구현 | 중 |
| 7장 스트리밍 | FFmpeg HLS 인코딩(720p/1080p), HLS 정적 매핑, 기술 선택 가이드 | 중상 |
| 8장 Elasticsearch | Docker ES+Kibana, RDB+ES 이중 저장, multi_match 가중치, Fuzzy 검색, 한글 분석기(nori) | 중 |
| 9장 RabbitMQ | GitHub 폴링 감지(Producer), Exchange/Queue/Routing, Consumer 파일 반영 | 중 |

---

## 전체 기술 스택

| 분류 | 기술 | 사용 장 |
|------|------|--------|
| 프레임워크 | Spring Boot (Java, JDK 21) | 전 장 |
| 빌드 | Gradle | 전 장 |
| 템플릿 | Mustache | 2, 3, 6장 |
| ORM/DB | Spring Data JPA, H2 | 2, 4, 6, 7, 8장 |
| 인프라 | Docker, Docker Compose | 1, 3, 8, 9장 |
| 웹서버 | Nginx (리버스 프록시) | 3장 |
| 캐시/세션 | Redis, Spring Session Data Redis | 3장 |
| 인증 | OAuth 2.0, OIDC, JWT (nimbus-jose-jwt) | 2장 |
| HTTP 클라이언트 | RestTemplate | 2장 |
| 클라우드 | AWS S3, AWS Lambda (Python 3.11), IAM | 5장 |
| 영상 처리 | FFmpeg (Java wrapper) | 7장 |
| 스트리밍 | HLS (m3u8/ts) | 7장 |
| 검색 엔진 | Elasticsearch 8.x, Kibana | 8장 |
| ORM (ES) | Spring Data Elasticsearch | 8장 |
| 메시지 브로커 | RabbitMQ (AMQP) | 9장 |
| 메시징 | spring-boot-starter-amqp | 9장 |
| 실시간 통신 | SSE (SseEmitter), WebSocket/STOMP | 6장 |
| 프론트 | Vanilla JS, React | 4, 6장 |
| API 테스트 | Postman | 2, 4, 5, 7장 |

---

## 참조 Git 레포 목록

GitHub 조직: **metacoding-11-spring-reference** (주요), **kjh5848** (1장)

| 장 | 레포 | 용도 |
|---|---|---|
| 1장 | `kjh5848/spring-app` | 실습용 Spring 서버 |
| 1장 | `kjh5848/spring-docker` | Dockerfile + docker-compose |
| 2장 | `metacoding-11-spring-reference/kakao-oauth-code-ssr-start` | SSR OAuth 시작 코드 |
| 2장 | `metacoding-11-spring-reference/kakao-oauth-code-ssr-end` | SSR OAuth 완성 코드 |
| 2장 | `metacoding-11-spring-reference/kakao-oauth-code-oidc-start` | OIDC 시작 코드 |
| 2장 | `metacoding-11-spring-reference/kakao-oauth-code-oidc-end` | OIDC 완성 코드 |
| 3장 | `metacoding-11-spring-reference/docker-session-share` | Redis 세션 공유 |
| 4장 | `metacoding-11-spring-reference/spring-base64` | Base64 업로드 서버 |
| 4장 | `metacoding-11-spring-reference/react-base64` | React 프론트 |
| 5장 | `metacoding-11-spring-reference/spring-presign-url-start` | Presigned URL 시작 |
| 5장 | `metacoding-11-spring-reference/spring-presign-url-end` | Presigned URL 완성 |
| 6장 | `metacoding-11-spring-reference/spring-polling` | Polling 구현 |
| 6장 | `metacoding-11-spring-reference/spring-sse` | SSE 구현 |
| 6장 | `metacoding-11-spring-reference/spring-websoket` | WebSocket/STOMP |
| 7장 | `metacoding-11-spring-reference/spring-polling` | 스트리밍 실습 기반 코드 |
| 7장 | `BtbN/FFmpeg-Builds` (외부) | FFmpeg 바이너리 다운로드 |
| 8장 | `metacoding-11-spring-reference/docker-elasticsearch` | ES + Kibana + Spring |
| 9장 | `metacoding-11-spring-reference/rabbitmq-producer` | Producer |
| 9장 | `metacoding-11-spring-reference/rabbitmq-consumer` | Consumer |
| 9장 | `metacoding-11-spring-reference/rabbitmq-docker` | RabbitMQ Docker |

**실습 패턴**: start/end 구조 (시작 코드 clone → 챕터 따라 구현 → end 레포로 확인)

---

## 장 간 의존성

```
1장 Docker ──────┐
                 ├── 3장 Redis (docker-compose 전제)
                 ├── 8장 Elasticsearch (docker-compose 전제)
                 └── 9장 RabbitMQ (docker-compose 전제)

4장 Base64 업로드 ──→ 5장 Presigned URL (로컬 → 클라우드 업로드 확장)

6장 Polling/SSE/WebSocket ──→ 7장 스트리밍 (실시간 통신 개념 연장)

2장 OAuth: 독립
```

---

## 의도 필터 — 안/밖 분류

**의도**: "주니어 개발자가 실무 주변 기술의 두려움을 없앤다"

### 의도 안 (부합)

모든 9개 장이 의도에 부합합니다. 각 장이 "들어는 봤지만 직접 해본 적 없는" 기술을 다루며, 핵심 흐름을 구현하는 구조입니다.

### 주의 필요 (깊이 조절)

| 항목 | 현재 상태 | 권장 |
|------|----------|------|
| 2장 JWT 보안 심화 | Access/Refresh Token 전략, 저장 위치 비교까지 상세 | 짧게 언급, 심화는 부록 |
| 5장 AWS 콘솔 설정 | IAM/S3/Lambda 설정 캡처 과다 | 핵심 흐름 집중, 콘솔 설정은 부록 |
| 7장 FFmpeg 세부 구현 | 특수 도메인이나 유지 결정 | 기술 선택 가이드 중심으로 비중 조절 |
| 5장 AWS 클라우드 의존 | seed에서 "로컬에서 동작하는 수준까지"라고 명시 | S3/Lambda는 클라우드 필수. 로컬 대안(LocalStack) 언급하거나, "클라우드 입문"으로 예외 명시 |
