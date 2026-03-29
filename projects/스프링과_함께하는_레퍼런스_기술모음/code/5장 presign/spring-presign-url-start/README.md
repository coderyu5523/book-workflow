# Presign URL 설정 가이드

## 환경 변수 설정

1. 프로젝트 루트에 `.env` 파일을 생성하고 아래 값을 입력합니다.

```properties
# ---------------------------
# AWS 환경변수
# ---------------------------
CLOUD_AWS_CREDENTIALS_ACCESS_KEY=YOUR_ACCESS_KEY
CLOUD_AWS_CREDENTIALS_SECRET_KEY=YOUR_SECRET_KEY
CLOUD_AWS_REGION=ap-northeast-2
CLOUD_AWS_S3_BUCKET=YOUR_BUCKET_NAME
```

2. Spring 설정에서 `.env`를 로드하고 환경 변수를 매핑합니다.

```properties
spring.config.import=optional:file:.env[.properties]

cloud.aws.credentials.access-key=${CLOUD_AWS_CREDENTIALS_ACCESS_KEY}
cloud.aws.credentials.secret-key=${CLOUD_AWS_CREDENTIALS_SECRET_KEY}
cloud.aws.region=${CLOUD_AWS_REGION}
cloud.aws.s3.bucket=${CLOUD_AWS_S3_BUCKET}
```

> 참고: 실제 키는 절대 저장소에 커밋하지 마세요.
