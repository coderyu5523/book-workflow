# ex07 — Docker Compose 풀스택 (backend · db · frontend)

Spring 백엔드 + MySQL + nginx 프론트엔드를 Docker Compose로 한 번에 구동합니다. 프론트에서 `/api/users`로 사용자 목록을 조회합니다.

## 실행

### 컨테이너 빌드 및 실행

```bash
cd ex07
docker compose up
```

## 접속

- http://localhost:80/

## 정리

```bash
docker compose down
```

### db 데이터 삭제

```bash
rm -rf ex07/db/store
```
