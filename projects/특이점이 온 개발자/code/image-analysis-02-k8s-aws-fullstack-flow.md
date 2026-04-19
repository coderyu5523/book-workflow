# 이미지 분석 2: Kubernetes 풀스택 트래픽 흐름 (AWS 환경)

## 다이어그램 개요

파란색 테마의 정교한 다이어그램으로, AWS 환경에서 외부 트래픽이 Kubernetes 클러스터를 통과하여 Spring 애플리케이션 Pod에 도달하는 전체 과정을 보여줍니다. L4/L7 로드밸런싱의 차이, 라벨-셀렉터 매칭, kube-proxy의 역할을 시각적으로 설명합니다.

---

## 구성 요소 분석

### 1. 외부 트래픽 (Internet)
- `GET /web` 요청이 인터넷을 통해 들어옴

### 2. AWS L4 로드밸런서 (속도 최우선)
- **검증 항목**: IP/Port만 확인
- **역할**: 여러 노드로 분산
- L4 계층이므로 패킷 내용(URL, JSON 등)은 해석하지 않음
- 빠른 속도가 장점

### 3. Kubernetes Ingress (L7 복잡한 안내소)
- **URL 확인**: `/web` → Web 서비스로 라우팅
- **상세한 연결 정보** 기반으로 판단
- JSON 파싱은 하지 않음
- L7 계층에서 Host/Path 기반 라우팅 수행

### 4. 서비스 (Service: Web)
- **Label**: `app=web`
- **Selector**: `app=web`
- 라벨이 `app=web`인 Pod를 자동으로 찾아 연결
- 클러스터 내부 가상 IP 제공

### 5. 서비스 (Service: API)
- **Label**: `app=api`
- API 전용 서비스
- Web Pod에서 내부적으로 호출

### 6. 노드 (Node) + 큐브 프록시 (kube-proxy)
- **서비스 정의(라벨) 기반으로 실제 네트워크 규칙(iptables) 등록**
- Kube-proxy Traffic Redirection 수행
- 서비스의 가상 IP를 실제 Pod IP로 변환

### 7. 파드 (Pod) A — `app=web`
- **Spring 애플리케이션** 실행 중
- 드디어 JSON 파싱, `user_id` 검증 등 비즈니스 로직 처리
- `data` 수신 및 처리
- **디플로이먼트로 항상 3개 유지**

### 8. 파드 (Pod) C — `app=api`
- API 서비스 Pod
- **디플로이먼트로 항상 3개 유지**

---

## 트래픽 흐름 요약

```
외부 (GET /web)
  → AWS L4 로드밸런서          [IP/Port만 확인, 노드 분산]
    → Kubernetes Ingress       [URL 확인: /web → Service:Web]
      → Service (app=web)      [Selector로 Pod 매칭]
        → kube-proxy           [iptables 규칙으로 실제 Pod 전달]
          → Pod A (Spring)     [JSON 파싱, 비즈니스 로직 처리]
            → Service (app=api) [내부 API 호출]
              → Pod C (API)
```

---

## L4 vs L7 비교 (이 다이어그램의 핵심)

| 구분 | AWS L4 로드밸런서 | Kubernetes Ingress (L7) |
|------|-------------------|------------------------|
| **확인 항목** | IP/Port만 | URL 경로, Host 헤더 |
| **속도** | 빠름 (최우선) | 상대적으로 느림 |
| **판단 능력** | 단순 분산 | /web → Web, /api → API 라우팅 |
| **JSON 파싱** | 안 함 | 안 함 |
| **비유** | 고속도로 톨게이트 | 건물 안내 데스크 |

> **JSON 파싱은 누가?** → Pod 안의 애플리케이션(Spring)이 처리. 네트워크 계층에서는 하지 않음.

---

## 라벨-셀렉터 매칭 흐름

```
Service (Selector: app=web)
        ↓ 매칭
Pod A (Label: app=web)  ← 연결됨
Pod B (Label: app=api)  ← 연결 안 됨

Service (Selector: app=api)
        ↓ 매칭
Pod C (Label: app=api)  ← 연결됨
```

---

## 핵심 포인트

1. **계층별 역할 분리**: L4(속도) → L7(라우팅) → Service(매칭) → Pod(비즈니스 로직)
2. **라벨과 셀렉터**: Service가 Pod를 찾는 유일한 방법은 라벨 매칭
3. **kube-proxy**: 서비스 정의를 iptables 규칙으로 변환하여 실제 네트워크 경로 생성
4. **Deployment**: Pod 수를 항상 3개로 유지 (자동 복구)
5. **JSON 파싱 시점**: 네트워크 장비가 아닌, 최종 목적지인 Pod의 애플리케이션이 처리
