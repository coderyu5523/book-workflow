# ex08 — Pod YAML 첫 적용

nginx 컨테이너 한 개를 가진 Pod를 정의합니다.

## 적용

```bash
kubectl apply -f ex08/hello-pod2.yml
kubectl get pod
```

## 정리

```bash
kubectl delete -f ex08/hello-pod2.yml
```
