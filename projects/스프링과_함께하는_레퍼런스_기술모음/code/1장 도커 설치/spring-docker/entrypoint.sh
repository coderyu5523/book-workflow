# 1. Git 리포지토리 주소 설정
git clone "https://github.com/kjh5848/spring-app"

# 2. 프로젝트 디렉터리로 이동
cd spring-app

# 3. gradlew 실행 권한 부여
chmod +x ./gradlew

# 4. Gradle 빌드 (테스트 생략)
./gradlew clean build

# 5. jar 파일 실행 권한 부여
chmod +x build/libs/*.jar

# 6. Spring Boot 실행 (docker 프로필 활성화)
java -jar build/libs/*.jar