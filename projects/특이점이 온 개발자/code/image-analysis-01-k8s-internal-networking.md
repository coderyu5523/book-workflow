# 이미지 분석 1: Kubernetes 내부 네트워킹 구조 (손그림)

## 다이어그램 개요

손으로 그린 스타일의 Kubernetes 클러스터 내부 네트워킹 구조도입니다. 외부 요청이 클러스터에 진입하여 Pod에 도달하기까지의 전체 흐름을 보여줍니다.

---

## 구성 요소 분석

### 1. 로컬호스트 (Host)
- 다이어그램 왼쪽 끝에 위치
- 외부에서 클러스터로 요청을 보내는 출발점

### 2. 클러스터 입구 — NodePort Service
- **NodePort 4000** 포트로 외부 요청을 수신
- NodePort Service에 의해 **kube-proxy가 처리**
- 그 결과 **Ingress Pod로 라우팅** (L7 로드밸런싱)

### 3. 쿠버네티스 가상세계 (클러스터 내부)

#### Ingress Controller Pod
- 클러스터 입구에서 들어온 요청을 받는 첫 번째 Pod
- L7(애플리케이션 계층) 라우팅 수행
- URL 경로, 호스트 헤더 등을 기반으로 적절한 Service로 분배

#### Kube Proxy
- 각 노드(Node1, Node2)마다 존재
- **Endpoints 참조**: Service에 연결된 Pod 목록을 확인
- **ClusterIP의 요청을 가로채서 L4 로드밸런싱** 수행
- iptables 규칙을 통해 실제 트래픽 전달

#### Endpoint Controller
- Pod를 지정하면 **IP 주소 시 감시** (Pod의 IP 변화를 감시)
- Service와 Pod 사이의 매핑 정보(Endpoints)를 유지/갱신

#### ClusterIP Service (S:A, S:B)
- **S:A** — ClusterIP Service, Label: A
- **S:B** — ClusterIP Service, Label: B
- 클러스터 내부에서만 접근 가능한 가상 IP 제공
- Pod 그룹에 대한 안정적인 진입점 역할

#### Node1, Node2
- 각 노드에 Kube Proxy가 동작
- Pod(P:A)가 분산 배치됨

#### Deployment
- **Pod의 상태를 유지하는 컨트롤러**
- P:A Pod 여러 개를 관리
- 원하는 개수(replicas)만큼 Pod를 자동 유지

---

## 트래픽 흐름 요약

```
Host
  → NodePort:4000 (kube-proxy가 처리)
    → Ingress Controller Pod (L7 라우팅)
      → ClusterIP Service S:A 또는 S:B (L4 로드밸런싱)
        → kube-proxy가 Endpoints 참조하여 실제 Pod로 전달
          → P:A (Node1 또는 Node2에 분산)
```

---

## 핵심 포인트

| 계층 | 담당 컴포넌트 | 역할 |
|------|-------------|------|
| L7 로드밸런싱 | Ingress Controller | URL/Host 기반 라우팅 |
| L4 로드밸런싱 | Kube-Proxy + ClusterIP | IP:Port 기반 트래픽 분배 |
| Pod 관리 | Deployment | 원하는 상태(replicas) 유지 |
| Endpoints 관리 | Endpoint Controller | Pod IP 변화 감시 및 갱신 |

---

## 이 다이어그램이 강조하는 것

1. **NodePort → Ingress → Service → Pod** 순서의 계층적 트래픽 흐름
2. **kube-proxy**가 두 곳에서 등장 — NodePort 처리와 ClusterIP 처리 모두 담당
3. **Endpoint Controller**가 Pod의 IP 변화를 감시하여 Service 매핑을 최신 상태로 유지
4. **Deployment**가 Pod 수를 자동으로 유지하는 컨트롤러 역할
