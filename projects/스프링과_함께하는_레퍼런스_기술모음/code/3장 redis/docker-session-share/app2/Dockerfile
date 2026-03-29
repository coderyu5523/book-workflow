# 1. OpenJDK 21 기반의 Eclipse Temurin 이미지 사용
FROM eclipse-temurin:21-jdk

# 2. Git 설치
# - 컨테이너 내부에서 Git 클론을 수행하기 위함
RUN apt-get update && apt-get install -y git

# 3. 작업 디렉터리 설정
# - 이후 실행 명령어의 기준 경로를 /app으로 고정
WORKDIR /app

# 4. entrypoint.sh 스크립트 복사
# - 호스트의 entrypoint.sh를 컨테이너 내부로 복사
COPY ./entrypoint.sh ./entrypoint.sh

# 5. 스크립트 실행 권한 부여
RUN chmod +x ./entrypoint.sh

# 6. 컨테이너 실행 시 entrypoint.sh 자동 실행
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]