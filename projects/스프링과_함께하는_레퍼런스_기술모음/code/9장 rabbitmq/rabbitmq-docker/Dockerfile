# 1. RabbitMQ Management 이미지 사용
# - Management UI가 포함된 공식 이미지입니다.
FROM rabbitmq:3.13-management

# 2. entrypoint.sh 복사
# - 컨테이너 시작 시 실행될 스크립트입니다.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# 3. 실행 권한 부여
RUN chmod +x /usr/local/bin/entrypoint.sh

# 4. 컨테이너 시작 시 entrypoint 실행
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# 5. RabbitMQ 서버 실행
CMD ["rabbitmq-server"]
