# 부록 A: 네트워크 전체 그림

이 책에서 만난 🔍 네트워크 돋보기들을 하나의 그림으로 연결합니다.

---

## 3단계 레이어

```
┌─────────────────────────────────────────────────┐
│  4장. Kubernetes                                 │
│  Pod · Service · kube-proxy · CoreDNS · Ingress │
├─────────────────────────────────────────────────┤
│  ▲ K8s는 Docker 위에서 클러스터 네트워킹 구성    │
├─────────────────────────────────────────────────┤
│  2~3장. Docker                                   │
│  docker0 · veth · iptables · Docker DNS · Compose│
├─────────────────────────────────────────────────┤
│  ▲ Docker는 리눅스 네트워크 도구를 활용          │
├─────────────────────────────────────────────────┤
│  리눅스 네트워크 도구                             │
│  Namespace · veth pair · Bridge · iptables       │
└─────────────────────────────────────────────────┘
```

---

## 연결 고리 맵

| 기초 개념 | Docker (2~3장) | Kubernetes (4장) |
|----------|---------------|-----------------|
| Network Namespace | 컨테이너 격리 (2.3 돋보기) | Pod 공유 namespace (4.3 돋보기) |
| veth pair + Bridge | docker0 연결 (2.3 돋보기) | cni0 bridge (Pod 간 통신) |
| iptables DNAT | `-p` 포트매핑 (2.3 돋보기) | kube-proxy Service (4.4 돋보기) |
| DNS | Docker DNS 127.0.0.11 (3.3 돋보기) | CoreDNS svc.cluster.local (4.5 돋보기) |
| 네트워크 자동화 | Compose 자동 네트워크 (3.4 돋보기) | Service + Ingress (4.4, 4.6 돋보기) |

---

## Docker → Kubernetes 진화

| 개념 | Docker | Kubernetes |
|------|--------|-----------|
| 네트워크 격리 | 컨테이너마다 독립 Namespace | Pod마다 공유 Namespace |
| 이름 해석 | Docker DNS (127.0.0.11) | CoreDNS (svc.cluster.local) |
| 포트 포워딩 | `-p 8080:80` (단일 컨테이너) | Service (다중 Pod 로드밸런싱) |
| 로드밸런싱 | NGINX upstream | kube-proxy iptables 분배 |
| 외부 접근 | `-p` 포트 노출 | NodePort → LoadBalancer → Ingress |
| 멀티 컨테이너 | docker-compose up | kubectl apply -f |

---

**한 줄 정리**: Docker와 Kubernetes의 네트워킹은 마법이 아니라, 리눅스 네트워크 도구(Namespace, veth, Bridge, iptables, DNS)의 조합이다. Docker가 단일 호스트에서 조합했고, Kubernetes가 클러스터 전체로 확장했다.
