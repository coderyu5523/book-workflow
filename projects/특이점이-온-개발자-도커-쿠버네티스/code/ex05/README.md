# ex05 — MySQL 초기화 이미지

`init.sql`로 테이블과 초기 데이터를 넣은 MySQL 이미지를 빌드하고 실행합니다.

## 실행

### DB 빌드 및 실행

```bash
docker build -t db ex05/db
docker run -dit -p 3306:3306 db
```

## 정리

```bash
docker rm -f $(docker ps -q --filter ancestor=db)
```
