# 시나리오 + 버전 설계

## 시나리오

### 한 줄 요약
신입 오픈이가 사내 웹 서비스를 맡아 Docker → Compose → K8s를 배워가는 성장기.

### 관통 비유
**칸막이 사무실 / 빌딩**

| 기술 | 비유 |
|------|------|
| 컨테이너 | 칸막이 사무실 (같은 건물인데 서로 독립된 공간) |
| 이미지 / Dockerfile | 사무실 세팅 매뉴얼 (책상, 의자, 모니터 배치도) |
| 포트포워딩 | 사무실 내선 번호 |
| Docker 네트워크 | 층간 내부 통화망 |
| 볼륨 | 파일 캐비닛 (직원이 퇴사해도 문서는 남음) |
| Compose | 층 전체 입주 계획서 (한 층에 3개 팀을 한 번에 배치) |
| K8s | 빌딩 관리 시스템 (유동적으로 층 배정, 고장 나면 자동 이전) |

### 전체 흐름

```
1막: Docker 기초 (v0.1~v0.6)
  시작 — 오픈이는 사내 웹 서비스를 맡는다. 서버에 직접 설치하다 환경 충돌.
         팀장이 "컨테이너 써봐"라고 한마디 던진다.
         팀장이 화이트보드에 도커의 큰 그림을 그려준다.
  전개 — 컨테이너 기초(v0.1) → 이미지 빌드+프록시(v0.2) → 로드밸런싱(v0.3)
         → 캐싱(v0.4) → 네트워크(v0.5) → 데이터 영속화(v0.6)
  위기 — 서비스가 5개로 늘어남. docker run을 5번 치고, 네트워크를 수동 연결하고,
         금요일 저녁 장애 때 30분간 수동 복구.

    ↓ [1차 전환점: 수동의 한계]
    팀장: "이걸 매번 수동으로 할 거야?"

2막: Docker Compose (v0.7~v0.8)
  전환 — Compose를 알게 됨. yaml 한 장으로 전체를 올린다.
  확장 — 프론트+백엔드+DB 3티어 서비스를 Compose로 구성(v0.8).
  위기 — "다른 팀도 쓰게 해달라." 서비스가 10개로 늘어남.
         Compose 파일이 복잡해지고, 한 서비스가 죽으면 수동 재시작.

    ↓ [2차 전환점: 규모의 한계]
    팀장: "이제 건물 하나론 안 돼. 빌딩 관리 시스템이 필요해."

3막: Kubernetes (v0.9~v1.0)
  전환 — 팀장이 화이트보드에 K8s 큰 그림을 그려준다.
  학습 — K8s 리소스를 하나씩 배움(v0.9). Pod, Deployment, Service, ConfigMap, 
         Secret, PV/PVC를 각각 만들어보며 개념 잡기.
  완성 — ex07(Compose)을 K8s로 옮긴다(v1.0). Ingress로 외부 접속까지.
         동료: "이제 진짜 서비스 같은데요."
```

### 최종 결과물
프론트엔드 + 백엔드(Spring Boot) + DB(MySQL) + 캐시(Redis)로 구성된 4티어 웹 서비스가 Kubernetes 위에서 동작. Ingress로 외부 접속, ConfigMap/Secret으로 설정 분리, PV/PVC로 데이터 영속화.

### 3막 구조

```
[1막] Docker 기초         [2막] Compose        [3막] Kubernetes
v0.1 ~ v0.6               v0.7 ~ v0.8          v0.9 ~ v1.0
──────────────────────── ─────────────────── ──────────────────
  큰 그림 → 실습 반복        선언형 전환          큰 그림 → 실전 전환
           ↑                     ↑
     [1차 전환점]           [2차 전환점]
     수동의 한계             규모의 한계
```

---

## 버전 설계

| 버전 | 뭘 만드나 | 시나리오 속 위치 | 끝나면 뭐가 보이나 | 핵심 변경점 | 코드 |
|------|----------|----------------|------------------|------------|------|
| — | **도커의 큰 그림** | 팀장이 화이트보드에 그려줌 | 도커 동작 원리, 네트워크 흐름(bridge, iptables, 포트포워딩) 이해 | 개념 챕터 | — |
| v0.1 | 컨테이너 첫 만남 | 팀장: "컨테이너 써봐" | 컨테이너를 띄우고, 들어가고, 끄는 기본 조작 | docker run/stop/rm, attach/exec, 마운트 | ex00 |
| v0.2 | Dockerfile + Nginx 프록시 | 매번 처음부터 깔기 지침 → 설계도 | Dockerfile로 이미지 빌드 + Nginx 프록시로 앱 2개 연결 | FROM, COPY, ENTRYPOINT, upstream, proxy_pass | ex01 |
| v0.3 | 로드밸런싱 | 사용자가 늘어서 앱 하나로 감당 안 됨 | 같은 앱 2개에 요청 분산 | upstream 복수 서버, round-robin | ex02 |
| v0.4 | 캐싱 | 이미지를 매번 가져와서 느림 | Nginx 캐싱으로 응답 속도 개선 | proxy_cache, X-Cache-Status | ex03 |
| v0.5 | Docker 네트워크 | host.docker.internal로 우회하다가 한계 | 컨테이너끼리 DNS로 직접 통신 | docker network create, 컨테이너명 DNS | ex04 |
| v0.6 | 데이터 영속화 | DB 컨테이너 재시작하면 데이터 날아감 | MySQL 이미지 + 볼륨으로 데이터 유지 | docker-entrypoint-initdb.d, ENV | ex05 |
| v0.7 | **[1차 전환점]** Docker Compose | docker run 5번 치는 게 한계 | Compose 한 줄로 전체 올리기 | docker-compose.yml, services, networks | ex06 |
| v0.8 | 3티어 Compose | 실제 서비스 구성 | 풀스택(프론트+백엔드+DB)이 Compose 한 방으로 뜸 | environment, 서비스명 DNS, 3티어 구조 | ex07 |
| — | **쿠버네티스의 큰 그림** | 팀장이 화이트보드에 K8s 그려줌 | K8s 아키텍처, 리소스 관계, 요청 흐름 이해 | 개념 챕터 | — |
| v0.9 | K8s 리소스 개별 학습 | 리소스를 하나씩 만들어보며 개념 잡기 | Pod, Deployment, Service, ConfigMap, Secret, PV/PVC 각각 동작 확인 | 각 리소스 YAML 작성, kubectl apply | yaml/ |
| v1.0 | **[2차 전환점]** K8s 실전 전환 | Compose 앱을 K8s로 옮김 | 4티어 서비스가 K8s 위에서 동작 + Ingress 외부 접속 | Namespace, Deployment, Service, ConfigMap, Secret, PV/PVC, Ingress 통합 | ex08 |

## 전환점 상세

### 1차 전환점: 수동의 한계 (v0.6 → v0.7)

오픈이는 v0.1~v0.6까지 docker run으로 하나씩 컨테이너를 올려왔다. 서비스가 5개로 늘면서 매번 docker run을 5번 치고, 네트워크를 수동으로 연결하고, 순서를 기억해야 한다. 금요일 저녁 장애가 나서 30분간 수동 복구하는 사건이 터진다.

**독자가 느끼는 것**: "아, 수동으로 하면 안 되겠구나. 선언형이 필요하구나."
**이야기 장치**: 팀장의 한마디 — "이걸 매번 수동으로 할 거야?"
**해결**: Docker Compose — yaml 한 장으로 전체를 선언하고 한 줄로 올린다.

### 2차 전환점: 규모의 한계 (v0.8 → v0.9)

Compose로 3티어 서비스를 잘 돌리고 있었는데, "다른 팀도 쓰게 해달라"는 요청이 온다. 서비스가 10개로 늘어나면서 Compose 파일이 복잡해지고, 한 서비스가 죽어도 자동 복구가 안 되고, 스케일링도 수동이다.

**독자가 느끼는 것**: "아, Compose만으로는 부족하구나. 오케스트레이션이 필요하구나."
**이야기 장치**: 팀장의 비유 — "이제 건물 하나론 안 돼. 빌딩 관리 시스템이 필요해."
**해결**: Kubernetes — 자동 복구, 자동 스케일링, 선언형 인프라 관리.

## 이야기 소재 — 문제→해결 대비 (코드 분석에서 발굴)

| 대비 | 문제 (전) | 해결 (후) | 등장 시점 |
|------|----------|----------|----------|
| host.docker.internal → DNS | ex01: 호스트 경유 우회 | ex04: Docker 네트워크 직접 연결 | v0.2 → v0.5 |
| 수동 docker run → Compose | ex01~ex05: 컨테이너 개별 실행 | ex06: docker-compose up 한 줄 | v0.6 → v0.7 |
| ENV 하드코딩 → Secret | ex05: Dockerfile에 비밀번호 | ex08: K8s Secret으로 분리 | v0.6 → v1.0 |
| Compose environment → ConfigMap | ex07: docker-compose.yml에 설정 | ex08: ConfigMap + Secret | v0.8 → v1.0 |

## 버전별 예제 코드

| 버전 | 폴더 | 핵심 파일 | 비고 |
|------|------|----------|------|
| v0.1 | code/ex00 | 리눅스-도커-기초-명령어-정리.md | 명령어 레퍼런스 (코드 파일 없음) |
| v0.2 | code/ex01 | app1/Dockerfile, lb/nginx.conf | Dockerfile + Nginx 프록시 |
| v0.3 | code/ex02 | app1/Dockerfile, lb/nginx.conf | 로드밸런싱 nginx.conf |
| v0.4 | code/ex03 | api/app.py, nginx/nginx.conf | Flask + Nginx 캐시 |
| v0.5 | code/ex04 | api/app.py, README.md | Docker 네트워크 + Redis |
| v0.6 | code/ex05 | db/Dockerfile, db/init.sql | MySQL 이미지 빌드 |
| v0.7 | code/ex06 | docker-compose.yml, lb/nginx.conf | Compose 기본 |
| v0.8 | code/ex07 | docker-compose.yml, backend/entrypoint.sh | 3티어 Compose |
| v0.9 | code/yaml | hello-pod2.yml ~ volume-pod.yml (10개) | K8s 개념 단위 |
| v1.0 | code/ex08 | k8s/**/*.yml (14개) | K8s 실전 통합 |

## "큰 그림" 개념 챕터 소재

### 도커의 큰 그림 (1막 시작)
- 가상머신 vs 컨테이너 — 왜 컨테이너로 옮겨가는가
- 이미지 vs 컨테이너 — 설계도와 실체
- 도커 아키텍처 — Docker Engine, Docker Daemon, CLI
- 네트워크 흐름 — 호스트↔컨테이너 통신, bridge 네트워크, iptables, 포트포워딩이 실제로 어떻게 동작하는지
- 이야기 장치: 팀장이 화이트보드에 그려주는 장면

### 쿠버네티스의 큰 그림 (3막 시작)
- K8s 아키텍처 — Master(Control Plane) + Worker Node
- 리소스 관계도 — Pod ⊂ Deployment, Service → Pod, ConfigMap/Secret → Pod, PV ↔ PVC → Pod
- 요청 흐름 — 외부 요청 → Ingress → Service → Pod
- Compose와의 비교 — 무엇이 같고 무엇이 다른가
- 이야기 장치: 팀장이 두 번째 화이트보드를 잡는 장면
