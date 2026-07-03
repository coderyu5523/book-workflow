# ex10 — Deployment 롤링 업데이트

replicas 4개와 RollingUpdate 전략(maxSurge:4, maxUnavailable:0)으로 무중단 배포합니다.

## 적용

```bash
kubectl apply -f ex10/deploy-ex02.yml
kubectl get pod
```

이미지 태그를 바꾸면 무중단 롤링 업데이트가 동작합니다.

```bash
kubectl set image deployment/nginx-replica nginx-container=nginx:1.21
kubectl get pod -w
```

## 정리

```bash
kubectl delete -f ex10/deploy-ex02.yml
```
