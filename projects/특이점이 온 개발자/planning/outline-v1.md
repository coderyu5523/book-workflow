# 목차

## 챕터 구조

이야기 파트 / 기술 파트를 분리하지 않는다. **스토리텔링 안에서 실습을 풀어가는 통합 흐름**.

### 서술 규칙

- **서술 중심** — 소설처럼 ~습니다 체로 서술한다. 대사는 포인트에만 사용하고 전체의 20% 이하로 유지한다
- **스토리 논리적 흐름 필수** — 문제 → 시도 → 실패/한계 인식 → 해결책 등장의 자연스러운 인과가 있어야 한다. 뜬금없는 전개 금지
- **예시 먼저 → 개념은 참고 표** — 모든 개념은 예시(스토리/비유)로 먼저 풀고, 정식 개념 정의는 참고 박스(`> **참고: 제목**`)에 간결하게 정리한다
- **구체적 버전/프레임워크 명시 X** — "Python 3.11", "Flask" 같은 특정 기술명을 스토리에 넣지 않는다. "언어 버전이 달랐다", "라이브러리가 충돌했다" 등 범용적으로 서술한다

### 이미지 규칙

**핵심: 하나의 개념 = 하나의 그림. 절대 합치지 않는다.**

개념을 설명할 때 반드시 단계별로 그림을 넣는다. 하나의 이미지에 여러 개념을 합치면 안 된다.

**예시:**
```
"첫 번째 방법은 주방을 통째로 나누는 것입니다." → 그림 1 (VM 구조)
"두 번째 방법은 칸막이를 치는 것입니다." → 그림 2 (컨테이너 구조)
```

**개념 유형별 시각 요소:**

| 개념 유형 | 설명 | 시각 요소 | 도구 |
|----------|------|----------|------|
| **구조** | 내부가 어떻게 생겼는가 | 구조도 (각각 개별 그림) | GEMINI or D2 |
| **흐름** | 어떤 순서로 동작하는가 | 단계별 다이어그램 (한 단계 = 한 그림) | D2 |
| **비교** | 두 가지가 어떻게 다른가 | 각각의 그림 + 비교표 | GEMINI + 표 |
| **관계** | 무엇이 무엇을 만드는가 | 관계도 | D2 |

**구조/흐름/비교/관계 중 하나에 해당하면 반드시 그림이 있어야 한다.** 글로만 설명하는 것은 허용하지 않는다.

**임의 판단 금지:** "이건 서사가 충분하니 그림이 필요 없다" 같은 판단을 AI가 하지 않는다. 개념 설명이 있으면 무조건 그림을 넣는다. 그림을 넣을지 말지 판단이 필요한 경우 사용자에게 질문한다.

**그림 도구:**
- **D2 다이어그램** — 흐름/관계/구조 (박스+화살표로 표현 가능한 것). 항상 가로(`direction: right`). 단계별로 분리
- **GEMINI PROMPT** — 개념 비교도/인포그래픽 (계층 구조, 비유 시각화 등 D2로 표현이 어려운 것)
- **Mermaid 코드블록 사용 금지** — 독자가 이해 못한다. 실제 이미지로 넣어야 한다

## 코드 실습 분류 기준

| 분류 | 표시 | 의미 | 독자 액션 |
|------|------|------|----------|
| 실습 | [실습] | 챕터 핵심 코드 | 독자가 직접 작성 |
| 설명 | [설명] | 중요하지만 핵심 아닌 코드 | 코드 읽고 이해 |
| 참고 | [참고] | 이 챕터 주제가 아닌 코드 | 파일명 + 한 줄만 |

---

## Part 1: Docker 기초

### Ch.1: 컨테이너가 뭐길래

**핵심 개념**: 가상머신 vs 컨테이너, 도커 아키텍처(Engine/Daemon/CLI), 네트워크 흐름(bridge, iptables, 포트포워딩), 이미지 vs 컨테이너
**기술**: Docker 동작 원리, 네트워크 흐름, Docker Hub
**버전 성과**: 도커가 왜 필요하고 어떻게 동작하는지 큰 그림 이해
**예상 분량**: ~12p

**코드 실습 분류**: 없음 (순수 개념 챕터)

**이미지 계획** (하나의 개념 = 하나의 그림):

| 순번 | 유형 | 개념 유형 | 설명 |
|------|------|----------|------|
| 그림 1-1 | GEMINI | 비교 | 해운 컨테이너 → 소프트웨어 컨테이너 대응 |
| 그림 1-2 | GEMINI | 구조 | 공유 주방 문제 (하나의 주방에 요리사 3명 충돌) |
| 그림 1-3 | GEMINI | 구조 | VM 방식 — 주방을 통째로 나누기 (Guest OS 포함 계층) |
| 그림 1-4 | GEMINI | 구조 | 컨테이너 방식 — 칸막이 치기 (커널 공유 계층) |
| 그림 1-5 | D2 | 구조 | Docker 아키텍처 (CLI → Daemon → Image/Container) |
| 그림 1-6 | D2 | 관계 | 이미지 → 컨테이너 관계 (하나의 이미지 → 여러 컨테이너) |
| 그림 1-7 | D2 | 흐름 | docker run ① CLI → Daemon 명령 전달 |
| 그림 1-8 | D2 | 흐름 | docker run ② 이미지 확인 / Hub 다운로드 |
| 그림 1-9 | D2 | 흐름 | docker run ③ 컨테이너 생성 (파일시스템+네트워크+프로세스) |
| 그림 1-10 | D2 | 흐름 | 네트워크 ① 요청 → iptables 포트 매핑 |
| 그림 1-11 | D2 | 흐름 | 네트워크 ② bridge → veth → 컨테이너 도달 |

**이야기 장치**: 로컬에서 되는데 서버에서 안 되는 상황 → 환경 차이 인식 → 팀장: "환경을 묶어서 가져가면?" → 컨테이너

---

### Ch.2: 상자 하나 띄워보기 — v0.1

**핵심 개념**: 컨테이너 생명주기, docker run/stop/rm, attach vs exec, 바인드 마운트, 볼륨 마운트, docker commit
**기술**: Docker CLI 기본
**버전 성과**: 컨테이너를 띄우고, 들어가고, 끄는 기본 조작
**예상 분량**: ~9p

**코드 실습 분류**:
```
ex00/
└── 리눅스-도커-기초-명령어-정리.md    [설명] Docker CLI + Linux 기초 명령어 모음
```

**실습 요약**: 코드 파일 없음. CLI 명령어를 터미널에서 직접 실행하는 실습.
- docker pull / run / ps / stop / rm
- -d, -dit, -p, --name 옵션
- attach vs exec 차이
- 바인드 마운트 / 볼륨 마운트
- docker commit (Dockerfile 이전 단계)

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 2-1 | GEMINI PROMPT | 컨테이너 생명주기 흐름도 (create → run → stop → rm) |
| 그림 2-2 | CAPTURE NEEDED | docker run + docker ps 실행 결과 |
| 그림 2-3 | GEMINI PROMPT | 바인드 마운트 vs 볼륨 마운트 비교도 |
| 그림 2-4 | CAPTURE NEEDED | attach vs exec 실행 결과 비교 |

---

### Ch.3: 매번 처음부터 깔 순 없잖아 — v0.2

**핵심 개념**: Dockerfile 작성(FROM, COPY, ENTRYPOINT), 이미지 빌드, Nginx 리버스 프록시
**기술**: Dockerfile, docker build, Nginx upstream/proxy_pass
**버전 성과**: Dockerfile로 이미지 빌드 + Nginx 프록시로 앱 2개 연결
**예상 분량**: ~10p

**코드 실습 분류**:
```
ex01/
├── app1/Dockerfile       [실습] Nginx 기반 앱 이미지 (FROM nginx + COPY index.html)
├── app1/index.html       [참고] 정적 HTML
├── app2/Dockerfile       [실습] app2용 Nginx 이미지
├── app2/index.html       [참고] 정적 HTML
├── lb/Dockerfile         [실습] 로드밸런서 이미지 (FROM nginx + COPY nginx.conf)
├── lb/nginx.conf         [설명] upstream + proxy_pass 리버스 프록시 설정
└── README.md             [참고] 빌드+실행 명령어
```

**실습 요약**: 작성 3개, 설명 1개, 참고 3개

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 3-1 | GEMINI PROMPT | Dockerfile → Image → Container 빌드 흐름 |
| 그림 3-2 | GEMINI PROMPT | ex01 아키텍처 (LB → app1/app2) |
| 그림 3-3 | CAPTURE NEEDED | docker build + docker run 실행 결과 |
| 그림 3-4 | CAPTURE NEEDED | 브라우저에서 /app1, /app2 접속 결과 |


---

### Ch.4: 혼자선 감당이 안 된다 — v0.3

**핵심 개념**: 수평 스케일링, 로드밸런싱(round-robin), 같은 이미지 복수 실행
**기술**: Nginx upstream 복수 서버, round-robin
**버전 성과**: 같은 앱 2개 인스턴스에 요청이 분산됨
**예상 분량**: ~8p

**코드 실습 분류**:
```
ex02/
├── app1/Dockerfile       [실습] 로드밸런싱 대상 앱 이미지
├── app1/index.html       [참고] 정적 HTML
├── lb/Dockerfile         [실습] 로드밸런서 이미지
├── lb/nginx.conf         [실습] upstream에 서버 2개 → round-robin 분산
└── README.md             [참고] 동일 이미지 2개 실행 명령어
```

**실습 요약**: 작성 3개, 참고 2개

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 4-1 | GEMINI PROMPT | ex01(프록시) vs ex02(로드밸런싱) 구조 비교 |
| 그림 4-2 | CAPTURE NEEDED | 브라우저 새로고침 → 번갈아 응답 확인 |

**이야기 대비**: ex01(2개 다른 앱 라우팅) → ex02(1개 앱 2개 인스턴스 분산). "앱을 늘리는 게 아니라 같은 앱을 복제한다"

---

### Ch.5: 한 번 가져온 건 저장해두자 — v0.4

**핵심 개념**: Nginx 캐싱 동작 원리, 캐시 히트/미스, Python 앱 이미지 빌드
**기술**: proxy_cache, X-Cache-Status, Flask Dockerfile(FROM python:3.10-alpine)
**버전 성과**: 이미지 요청이 캐싱되어 응답 속도 개선
**예상 분량**: ~8p

**코드 실습 분류**:
```
ex03/
├── api/Dockerfile        [실습] Python Flask 앱 이미지 (FROM python:3.10-alpine + pip install)
├── api/app.py            [참고] Flask 앱 코드
├── api/image.png         [참고] 캐싱 테스트용 이미지
├── nginx/Dockerfile      [실습] 캐싱 Nginx 이미지
├── nginx/nginx.conf      [실습] proxy_cache_path + proxy_cache 설정
└── README.md             [참고] 빌드+실행 명령어
```

**실습 요약**: 작성 3개, 참고 3개

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 5-1 | GEMINI PROMPT | 캐시 동작 흐름 (MISS → 저장 → HIT) |
| 그림 5-2 | CAPTURE NEEDED | curl -I 결과 (X-Cache-Status: MISS → HIT 변화) |

---

### Ch.6: 이름만 부르면 연결된다 — v0.5

**핵심 개념**: Docker 브릿지 네트워크, 컨테이너 DNS, host.docker.internal의 한계와 해결
**기술**: docker network create, --network, 컨테이너명 DNS 통신
**버전 성과**: 컨테이너끼리 이름만으로 직접 통신
**예상 분량**: ~8p

**코드 실습 분류**:
```
ex04/
├── api/Dockerfile        [설명] Redis 연동 Flask 앱 이미지
├── api/app.py            [참고] Flask + Redis 연결 코드 (host='redis' DNS)
└── README.md             [실습] docker network create + --network 명령어 시퀀스
```

**실습 요약**: 작성 0개(파일), 설명 1개, 참고 1개. **명령어 시퀀스 + 다이어그램 중심 실습**

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 6-1 | GEMINI PROMPT | host.docker.internal(ex01) vs Docker network(ex04) 비교도 |
| 그림 6-2 | GEMINI PROMPT | 컨테이너 DNS 동작 원리 (bridge 네트워크 내부) |
| 그림 6-3 | CAPTURE NEEDED | docker network create + 컨테이너 실행 + 통신 확인 |

**보충 요소**: 네트워크 종류(bridge / host / none) 비교표. 코드 파일이 적은 대신 다이어그램 + 명령어 실습 + 전후 비교로 채움.

---

### Ch.7: 꺼져도 남아야 할 것들 — v0.6

**핵심 개념**: 데이터 영속화, MySQL 커스텀 이미지, docker-entrypoint-initdb.d, ENV 환경변수 주입
**기술**: Dockerfile ENV, COPY init.sql, 볼륨 마운트로 데이터 유지
**버전 성과**: 컨테이너가 죽어도 DB 데이터가 살아남음
**예상 분량**: ~8p

**코드 실습 분류**:
```
ex05/
├── db/Dockerfile         [실습] MySQL 커스텀 이미지 (COPY init.sql + ENV)
├── db/init.sql           [참고] 초기화 SQL (user_tb + 샘플 데이터)
└── README.md             [참고] 빌드+실행 명령어
```

**실습 요약**: 작성 1개, 참고 2개

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 7-1 | GEMINI PROMPT | 볼륨 없는 컨테이너(데이터 소멸) vs 볼륨 마운트(데이터 유지) |
| 그림 7-2 | CAPTURE NEEDED | 컨테이너 삭제 → 재생성 → 데이터 확인 |

**이야기 대비**: ENV로 비밀번호 하드코딩 → CH12(K8s)에서 Secret으로 분리. "지금은 이렇게 하지만, 나중에 문제가 된다"를 암시.

---

## Part 2: Docker Compose

### Ch.8: 한 줄이면 전부 올라간다 — v0.7 [1차 전환점]

**핵심 개념**: Docker Compose 기본(services, build, networks, ports), 선언형 인프라, Compose 네트워크 DNS
**기술**: docker-compose.yml, docker-compose up/down
**버전 성과**: docker run 3번 → docker-compose up 한 줄로 전체 실행
**예상 분량**: ~10p

**코드 실습 분류**:
```
ex06/
├── docker-compose.yml    [실습] 3서비스(app1/app2/lb) + 네트워크 정의
├── app1/Dockerfile       [설명] ex01과 동일 (이전 챕터에서 작성)
├── app1/index.html       [참고] 정적 HTML
├── app2/Dockerfile       [설명] ex01과 동일
├── app2/index.html       [참고] 정적 HTML
├── lb/Dockerfile         [설명] Nginx 이미지
├── lb/nginx.conf         [설명] 서비스명(app1, app2)으로 upstream — DNS 변화 포인트
└── README.md             [참고] docker-compose up 명령어
```

**실습 요약**: 작성 1개, 설명 4개, 참고 3개

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 8-1 | GEMINI PROMPT | docker run × 3 vs docker-compose up 비교 (전환점 시각화) |
| 그림 8-2 | GEMINI PROMPT | docker-compose.yml 구조도 (services/networks 관계) |
| 그림 8-3 | CAPTURE NEEDED | docker-compose up 실행 결과 |

**전환점 장면**: 금요일 저녁 장애. 컨테이너 5개 수동 복구 30분. 팀장: "이걸 매번 수동으로 할 거야?"

---

### Ch.9: 진짜 서비스를 올려보자 — v0.8

**핵심 개념**: 3티어 아키텍처(frontend+backend+db), Compose environment로 설정 주입, 서비스명 DNS
**기술**: docker-compose.yml environment, 3티어 구조
**버전 성과**: 풀스택 서비스(프론트+백엔드+DB)가 Compose 한 방으로 뜸
**예상 분량**: ~9p

**코드 실습 분류**:
```
ex07/
├── docker-compose.yml        [실습] 3티어 서비스 + environment 주입
├── frontend/Dockerfile       [설명] Nginx + HTML + nginx.conf
├── frontend/index.html       [참고] 정적 HTML (앱 화면)
├── frontend/nginx.conf       [설명] /api/ → backend:8080 프록시
├── backend/Dockerfile        [참고] JDK + git clone + gradlew build
├── backend/entrypoint.sh     [참고] 앱 빌드 스크립트
├── db/Dockerfile             [설명] MySQL 커스텀 이미지 (CH07에서 작성)
├── db/init.sql               [참고] 초기화 SQL
└── README.md                 [참고] docker-compose up 명령어
```

**실습 요약**: 작성 1개, 설명 3개, 참고 5개

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 9-1 | GEMINI PROMPT | 3티어 아키텍처 (frontend ↔ backend ↔ db) |
| 그림 9-2 | CAPTURE NEEDED | docker-compose up 후 브라우저 접속 결과 |
| 그림 9-3 | CAPTURE NEEDED | 사용자 목록이 표시되는 화면 |

**주의**: backend 첫 실행 시 git clone → gradlew build로 수분 소요. 챕터에서 반드시 안내.

---

## Part 3: Kubernetes

### Ch.10: 건물 하나론 안 된다

**핵심 개념**: K8s 아키텍처(Control Plane + Worker Node), 리소스 관계도, 요청 흐름(외부 → Ingress → Service → Pod), Compose와의 비교
**기술**: K8s 동작 원리, 리소스 관계, Minikube 설치
**버전 성과**: K8s가 왜 필요하고 어떻게 동작하는지 큰 그림 이해
**예상 분량**: ~14p

**코드 실습 분류**: 없음 (순수 개념 챕터)

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 10-1 | GEMINI PROMPT | Compose vs K8s — 무엇이 같고 무엇이 다른가 |
| 그림 10-2 | GEMINI PROMPT | K8s 아키텍처 (Control Plane: API Server, etcd, Scheduler, Controller Manager + Worker Node: kubelet, kube-proxy, Pod) |
| 그림 10-3 | GEMINI PROMPT | K8s 리소스 관계도 (Pod ⊂ Deployment, Service → Pod, ConfigMap/Secret → Pod, PV ↔ PVC → Pod) |
| 그림 10-4 | GEMINI PROMPT | 외부 요청 흐름 (Client → Ingress → Service → Pod) |
| 그림 10-5 | GEMINI PROMPT | K8s 리소스 전체 맵 (Namespace 안에 모든 리소스 배치) |

**이야기 장치**: 팀장이 두 번째 화이트보드를 잡는 장면. "이번엔 좀 더 큰 그림이야."
**전환점 장면**: "다른 팀도 쓰게 해달라." Compose로는 관리가 안 되는 상황.

---

### Ch.11: 부품을 하나씩 만져보자 — v0.9

**핵심 개념**: Pod, Deployment, RollingUpdate, Service(NodePort/ClusterIP), ConfigMap, Secret, PV/PVC, Namespace
**기술**: kubectl apply, kubectl get, YAML 작성
**버전 성과**: K8s 리소스를 각각 만들고 동작 확인
**예상 분량**: ~12p

**코드 실습 분류**:
```
yaml/
├── hello-pod2.yml        [실습] Pod 기본 (kind, metadata, spec.containers)
├── deploy-ex01.yml       [실습] Deployment 기본 (replicas:1, selector, template)
├── deploy-ex02.yml       [실습] Deployment + RollingUpdate (maxSurge, maxUnavailable)
├── deploy-ex03.yml       [실습] Deployment + envFrom (ConfigMap/Secret 주입)
├── service-ex01.yml      [실습] Service (NodePort, selector 매핑)
├── configmap-conn.yml    [실습] ConfigMap (data 필드)
├── secret-password.yml   [실습] Secret (stringData → Base64 자동 변환)
├── volume-pv.yml         [실습] PersistentVolume (hostPath, capacity)
├── volume-pvc.yml        [실습] PersistentVolumeClaim (volumeName, resources)
└── volume-pod.yml        [실습] Pod + PVC volumeMounts 연결
```

**실습 요약**: 작성 10개 (전체 [실습])

**학습 순서**:
1. Pod (hello-pod2) → "K8s의 최소 단위"
2. Deployment (deploy-ex01) → "Pod를 관리하는 컨트롤러"
3. Deployment + RollingUpdate (deploy-ex02) → "무중단 배포"
4. Service (service-ex01) → "Pod에 접근하는 문"
5. ConfigMap (configmap-conn) → "설정을 밖으로 빼기"
6. Secret (secret-password) → "비밀번호는 따로 보관"
7. Deployment + envFrom (deploy-ex03) → "ConfigMap/Secret을 Pod에 주입"
8. PV/PVC (volume-pv, volume-pvc, volume-pod) → "데이터 영속화 (K8s 버전)"

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 11-1 | CAPTURE NEEDED | kubectl apply + kubectl get pods 결과 |
| 그림 11-2 | GEMINI PROMPT | Deployment → ReplicaSet → Pod 관계도 |
| 그림 11-3 | CAPTURE NEEDED | RollingUpdate 진행 중 kubectl get pods 변화 |
| 그림 11-4 | GEMINI PROMPT | Service → Pod 연결 (selector 매칭) |
| 그림 11-5 | CAPTURE NEEDED | minikube service로 NodePort 접속 |

**권장 언급**: Service 비교표 (ClusterIP / NodePort / LoadBalancer), Namespace 개념 (CH12 전 사전 설명)

---

### Ch.12: 같은 앱, 다른 세상 — v1.0 [2차 전환점]

**핵심 개념**: Compose → K8s 전환, 전체 리소스 통합 배포, Namespace, Ingress
**기술**: kubectl apply -f, Namespace, Deployment, Service, ConfigMap, Secret, PV/PVC, Ingress
**버전 성과**: 4티어 서비스(frontend+backend+db+redis)가 K8s 위에서 동작 + Ingress 외부 접속
**예상 분량**: ~11p

**코드 실습 분류**:
```
ex08/
├── k8s/namespace.yml                    [실습] Namespace: metacoding
├── k8s/db/db-secret.yml                 [실습] DB 인증정보 Secret
├── k8s/db/db-pv.yml                     [실습] PersistentVolume (hostPath)
├── k8s/db/db-pvc.yml                    [실습] PersistentVolumeClaim
├── k8s/db/db-deploy.yml                 [실습] DB Deployment + PVC 마운트
├── k8s/db/db-service.yml                [실습] DB ClusterIP Service
├── k8s/backend/backend-configmap.yml    [실습] Backend ConfigMap (DB URL, Redis host)
├── k8s/backend/backend-secret.yml       [실습] Backend Secret (DB 인증정보)
├── k8s/backend/backend-deploy.yml       [실습] Backend Deployment (replicas:2, envFrom)
├── k8s/backend/backend-service.yml      [실습] Backend ClusterIP Service
├── k8s/redis/redis-deploy.yml           [실습] Redis Deployment
├── k8s/redis/redis-service.yml          [실습] Redis ClusterIP Service
├── k8s/frontend/frontend-deploy.yml     [실습] Frontend Deployment
├── k8s/frontend/frontend-service.yml    [실습] Frontend ClusterIP Service
├── k8s/frontend/frontend-ingress.yml    [실습] Ingress (외부 → frontend)
├── backend/Dockerfile                   [참고] JDK + entrypoint.sh
├── backend/entrypoint.sh                [참고] git clone → build
├── frontend/Dockerfile                  [참고] Nginx + HTML
├── frontend/index.html                  [참고] 정적 HTML
├── frontend/nginx.conf                  [참고] /api/ 프록시
├── db/Dockerfile                        [참고] MySQL 이미지
├── db/init.sql                          [참고] 초기화 SQL
├── redis/Dockerfile                     [설명] Redis 7.4-alpine (2줄)
└── README.md                            [참고] minikube + kubectl 명령어
```

**실습 요약**: 작성 15개, 설명 1개, 참고 8개

**적용 순서 (서사 흐름)**:
1. Namespace 생성 → "건물 이름 짓기"
2. DB (Secret → PV → PVC → Deployment → Service) → "지하 창고 + 데이터베이스"
3. Backend (ConfigMap → Secret → Deployment → Service) → "사무실 입주"
4. Redis (Deployment → Service) → "임시 메모장"
5. Frontend (Deployment → Service → Ingress) → "입구 열기"

**이미지 계획**:
| 순번 | 유형 | 설명 |
|------|------|------|
| 그림 12-1 | GEMINI PROMPT | ex07(Compose) vs ex08(K8s) 전환 비교도 |
| 그림 12-2 | GEMINI PROMPT | ex08 전체 K8s 아키텍처 (Namespace 안 4서비스 배치) |
| 그림 12-3 | CAPTURE NEEDED | kubectl get all -n metacoding 결과 |
| 그림 12-4 | CAPTURE NEEDED | Ingress로 브라우저 접속 + 방문 횟수 표시 |

**대비 소재**:
- Compose environment → ConfigMap + Secret
- ENV 하드코딩(ex05) → Secret(ex08)
- Compose 네트워크 → K8s Service

**주의**: `minikube addons enable ingress` 선행 필요. backend 첫 실행 수분 소요.

---

## 갭 분석 결과

| 누락 주제 | 우선순위 | 반영 여부 | 비고 |
|----------|---------|----------|------|
| Namespace | 필수 | 반영 | CH11에서 개념 설명, CH12에서 실습 |
| Rolling Update | 필수 | 반영 | CH11 deploy-ex02.yml에서 실습 |
| Docker Hub/Registry | 권장 | 반영 | CH01에서 아키텍처 설명 시 1단락 |
| Multi-stage build | 권장 | 생략 | 개념서 범위 밖 |
| Image layer 캐시 | 권장 | 생략 | 개념서 범위 밖 |
| LoadBalancer Service | 권장 | 반영 | CH11에서 Service 비교표 |
| StatefulSet | 권장 | 생략 | 개념서 범위 밖 |
| HPA | 권장 | 생략 | 개념서 범위 밖 |
| Environment variables | 권장 | 반영 | CH07~CH08에서 자연스럽게 등장 |
| .dockerignore | 선택 | 생략 | 개념서 범위 밖 |
| Docker security | 선택 | 생략 | 개념서 범위 밖 |
| ReplicaSet | 선택 | 생략 | Deployment 설명 시 1줄 언급으로 충분 |
| DaemonSet | 선택 | 생략 | 개념서 범위 밖 |
| Job/CronJob | 선택 | 생략 | 개념서 범위 밖 |
| RBAC | 선택 | 생략 | 개념서 범위 밖 |
| Helm | 선택 | 생략 | 개념서 범위 밖 |

## 여정 맵

```
Ch.1(개념)  → Ch.2(쉬움) → Ch.3(보통) → Ch.4(보통) → Ch.5(보통)
     ↓
 큰 그림 이해     첫 실습     Dockerfile    로드밸런싱    캐싱

→ Ch.6(보통) → Ch.7(보통) → Ch.8(전환점!) → Ch.9(어려움)
   네트워크      영속화        Compose        3티어

→ Ch.10(개념) → Ch.11(보통) → Ch.12(전환점!)
   K8s 큰 그림    리소스 학습     K8s 실전
```

난이도 곡선: 쉬움 → 보통 유지 → [1차 전환점 상승] → 개념으로 리셋 → 보통 → [2차 전환점 상승]

## 기술 매핑

| 챕터 | 버전 | 핵심 기술 | 완성 코드와 다른 점 |
|------|------|----------|-------------------|
| Ch.1 | — | Docker 동작 원리, 네트워크 | 없음 (개념) |
| Ch.2 | v0.1 | docker run/stop/rm, mount | ex00 그대로 |
| Ch.3 | v0.2 | Dockerfile, Nginx proxy | ex01 그대로 |
| Ch.4 | v0.3 | Nginx load balancing | ex02 그대로 |
| Ch.5 | v0.4 | Nginx cache, Flask Dockerfile | ex03 그대로 |
| Ch.6 | v0.5 | Docker network, DNS | ex04 그대로 |
| Ch.7 | v0.6 | MySQL image, volume | ex05 그대로 |
| Ch.8 | v0.7 | Docker Compose | ex06 그대로 |
| Ch.9 | v0.8 | Compose 3-tier, environment | ex07 그대로 |
| Ch.10 | — | K8s 아키텍처, 리소스 관계 | 없음 (개념) |
| Ch.11 | v0.9 | K8s 리소스 개별 (10개 YAML) | yaml/ 그대로 |
| Ch.12 | v1.0 | K8s 통합 (15개 YAML) | ex08 그대로 |
