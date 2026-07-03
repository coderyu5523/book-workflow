# ex03 — nginx 프록시 캐시

nginx가 API 서버 앞에서 프록시 역할을 하며, `/image.png` 요청을 캐싱합니다. 응답 헤더의 `X-Cache-Status`로 HIT/MISS를 확인할 수 있습니다.

## 실행

### 사용자 정의 네트워크 생성 (이미 있으면 생략)

```bash
docker network create ex03-network
```

### api 서버 실행

```bash
docker build -t api ex03/api
docker run -dit --name api --network ex03-network api
```

### nginx 실행

```bash
docker build -t nginx-cache ex03/nginx
docker run -dit --name nginx-cache --network ex03-network -p 80:80 nginx-cache
```

## 접속

- http://localhost:80
- http://localhost:80/image.png

## 정리

```bash
docker rm -f api nginx-cache
docker network rm ex03-network
```
