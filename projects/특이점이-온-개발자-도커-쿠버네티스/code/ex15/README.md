# ex15 — Kubernetes 풀스택 통합 배포

MySQL·Redis·Spring 백엔드·nginx 프론트엔드를 minikube 클러스터에 배포하고, Ingress로 외부 접속까지 연결하는 통합 실습입니다.

## 미니큐브 실행

```bash
minikube start
minikube addons enable ingress
```

## 이미지 빌드

```bash
minikube image build -t metacoding/db:1 ex15/db
minikube image build -t metacoding/backend:1 ex15/backend
minikube image build -t metacoding/frontend:1 ex15/frontend
minikube image build -t metacoding/redis:1 ex15/redis
```

## 배포

```bash
kubectl apply -f ex15/k8s/namespace.yml
kubectl apply -f ex15/k8s/ --recursive
```

## 확인

```bash
kubectl get deploy,pod,service,ingress -n metacoding
kubectl logs -l app=backend -n metacoding --tail=100 --prefix
```

## 외부 접속

별도 터미널에서 터널을 열어 둔 뒤 접속합니다.

```bash
minikube tunnel
```

- http://127.0.0.1

## 정리

```bash
kubectl delete namespace metacoding
kubectl delete pv db-pv
```
