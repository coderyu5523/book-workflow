# 답변 기록

## STEP 1 — 씨앗 심기

### Q1. 책의 핵심 의도
**A**: Spring Boot를 쓰는 개발자가 실무에서 마주치는 기술들을 하나씩 직접 구현해보며 두려움을 없애는 책

### Q2. 독자 설정
**A**: 1~2년차 주니어 개발자 — Spring Boot로 간단한 CRUD는 하지만 Docker나 메시징 등은 안 써본 수준

### Q3. 실시간 통신 구성
**A**: 기존처럼 Polling/SSE/WebSocket을 한 장에서 비교. 대규모 스트리밍은 별도 장

### Q4. 파일 업로드 구성
**A**: 기존처럼 2개 장 분리 (Base64 업로드 / Presigned URL+S3+Lambda)

## STEP 2 — 코드 분석

### Q5. 7장 스트리밍 포함 여부
**A**: 유지. 영상 서비스도 실무에서 만날 수 있으니까

### Q6. 레포 구조
**A**: 장별 개별 레포 유지 (metacoding-11-spring-reference/*)
