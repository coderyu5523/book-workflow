# ex01 — nginx 리버스 프록시로 두 서버 라우팅

두 개의 nginx 서버를 각각 호스트 포트로 띄우고, 앞단 nginx(lb)가 `/app1`·`/app2` 경로를 각 서버로 프록시합니다.

## 실행

### 서버 1

```bash
docker build -t app1 ex01/app1
docker run -dit -p 8000:80 app1
```

### 서버 2

```bash
docker build -t app2 ex01/app2
docker run -dit -p 9000:80 app2
```

### nginx (로드밸런서)

```bash
docker build -t lb ex01/lb
docker run -dit -p 80:80 lb
```

## 접속

- http://localhost:80/app1
- http://localhost:80/app2
