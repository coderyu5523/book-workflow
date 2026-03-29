# 1. Eclipse Temurin 21 기반 이미지를 사용
# - Temurin은 OpenJDK를 기반으로 한 Eclipse 재단의 공식 배포판입니다.
# - 해당 이미지는 이미 Java 21(JDK)이 설치된 리눅스 환경으로, 별도의 JDK 설치 과정이 필요 없습니다.
# - 경량화된 기본 환경을 제공하므로 빌드 속도가 빠르고 이미지 크기가 상대적으로 작습니다.
FROM eclipse-temurin:21-jdk


# 2. 필수 패키지 설치 (예: git)
# - apt-get update: 패키지 목록을 최신으로 갱신합니다.
# - apt-get install -y git: git을 설치하며, -y 옵션으로 자동 확인을 수행합니다.
RUN apt-get update && apt-get install -y git

# 3. 작업 디렉터리 설정
# - 이후 실행되는 명령어의 기준 경로를 /app으로 고정합니다.
# - 마치 “cd /app” 명령을 미리 수행한 것과 같습니다.
WORKDIR /app

# 4. 로컬 entrypoint.sh 파일을 컨테이너 내부로 복사
# - COPY <호스트경로> <컨테이너경로>
# - 이 예시에서는 현재 폴더의 entrypoint.sh를 컨테이너 /app/entrypoint.sh로 복사합니다.
COPY ./entrypoint.sh ./entrypoint.sh

# 5. entrypoint.sh에 실행 권한 추가
# - chmod +x 명령어로 해당 스크립트를 실행 가능하게 만듭니다.
RUN chmod +x ./entrypoint.sh

# 6. 컨테이너 시작 시 entrypoint.sh 자동 실행
# - ENTRYPOINT는 컨테이너가 실행될 때 반드시 호출되는 명령어를 정의합니다.
# - /bin/bash를 통해 쉘 환경에서 entrypoint.sh 스크립트를 실행합니다.
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]