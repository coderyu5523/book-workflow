# ex04 — Redis 공유 저장소와 Flask API 2대

Redis를 공유 저장소로 두고 Flask API 2대(api1, api2)가 같은 데이터를 읽고 씁니다. 한쪽에서 저장한 값을 다른 쪽에서 조회할 수 있습니다.

## 실행

### 네트워크 만들기

```bash
docker network create ex04-network
```

### redis 실행

```bash
docker run -d --name redis --network ex04-network -p 6379:6379 redis
```

### api 실행

```bash
docker build -t api ex04/api
docker run -d --name api1 --network ex04-network -p 5001:5000 api
docker run -d --name api2 --network ex04-network -p 5002:5000 api
```

## 접속

- http://localhost:5001/save
- http://localhost:5002/read

## 포트 충돌(tcp 오류) 발생 시

```bash
netsh interface ipv4 show excludedportrange protocol=tcp
net stop winnat
```

## 정리

```bash
docker rm -f redis api1 api2
docker network rm ex04-network
```
