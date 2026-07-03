# ex06 — Docker Compose 로 로드밸런싱 구성

app1·app2·lb(nginx)를 Docker Compose로 한 번에 올려, 앞단 nginx가 두 서버로 경로를 분기합니다.

## 실행

### 컨테이너 빌드 및 실행

```bash
cd ex06
docker compose up
```

## 접속

- http://localhost/app1
- http://localhost/app2

## 정리

```bash
docker compose down
```
