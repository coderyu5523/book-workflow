
# 1. app1 git 클론
git clone "https://github.com/metacoding-11-spring-reference/spring-session-share-app1.git"

# 2. app1 프로젝트 디렉터리로 이동
cd spring-session-share-app1

# 3. Gradle Wrapper 실행 권한 부여
chmod +x ./gradlew

# 4. Spring Boot 실행
./gradlew bootRun --no-daemon