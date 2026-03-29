#!/bin/sh
set -e

# 1. 시작 로그 출력
echo "[entrypoint] RabbitMQ starting..."

# 2. 기본 엔트리포인트로 위임
exec docker-entrypoint.sh "$@"
