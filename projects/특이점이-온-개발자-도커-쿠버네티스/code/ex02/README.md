# ex02 — 사용자 정의 네트워크로 컨테이너 2대 로드밸런싱

사용자 정의 네트워크를 만들고 같은 이미지의 서버 2대(app1-1, app1-2)를 띄운 뒤, nginx(lb)가 컨테이너 이름으로 두 대를 로드밸런싱합니다.

## 실행

### 사용자 정의 네트워크 생성

```bash
docker network create ex02-network
```

### 서버(app1) 컨테이너 2대 생성

```bash
docker build -t app1 ex02/app1
docker run -dit --name app1-1 --network ex02-network app1
docker run -dit --name app1-2 --network ex02-network app1
```

### nginx (로드밸런서)

```bash
docker build -t lb ex02/lb
docker run -dit --name lb --network ex02-network -p 80:80 lb
```

## 접속

- http://localhost:80/app1

## 정리

```bash
docker rm -f app1-1 app1-2 lb
docker network rm ex02-network
```
