# 코드 분석

## 완성 코드 정보
- 경로: projects/특이점이 온 개발자/code/
- 구성: ex00~ex08 (단계별 예제) + yaml/ (K8s 개념 학습용)
- 기술 스택: Docker, Docker Compose, Kubernetes(Minikube), Nginx, Flask(Python), Spring Boot(Java), MySQL, Redis

## 전체 구조

```
code/
├── ex00/                              ← 리눅스/도커 기초 명령어 레퍼런스
│   └── 리눅스-도커-기초-명령어-정리.md
├── ex01/                              ← Nginx 리버스 프록시 (2앱 + LB)
│   ├── app1/ (Dockerfile, index.html)
│   ├── app2/ (Dockerfile, index.html)
│   ├── lb/   (Dockerfile, nginx.conf)
│   └── README.md
├── ex02/                              ← 로드밸런싱 (1앱 × 2 인스턴스)
│   ├── app1/ (Dockerfile, index.html)
│   ├── lb/   (Dockerfile, nginx.conf)
│   └── README.md
├── ex03/                              ← 리버스 프록시 + 캐싱 (Flask API)
│   ├── api/  (app.py, Dockerfile)
│   ├── nginx/ (Dockerfile, nginx.conf)
│   └── README.md
├── ex04/                              ← Docker 네트워크 DNS (Flask + Redis)
│   ├── api/  (app.py, Dockerfile)
│   └── README.md
├── ex05/                              ← MySQL 커스텀 이미지 (init.sql)
│   ├── db/   (Dockerfile, init.sql)
│   └── README.md
├── ex06/                              ← Docker Compose (ex01 → Compose 전환)
│   ├── app1/, app2/, lb/
│   ├── docker-compose.yml
│   └── README.md
├── ex07/                              ← Compose 3티어 (Spring Boot + MySQL + Nginx)
│   ├── backend/ (Dockerfile, entrypoint.sh)
│   ├── db/      (Dockerfile, init.sql)
│   ├── frontend/ (Dockerfile, index.html, nginx.conf)
│   ├── docker-compose.yml
│   └── README.md
├── ex08/                              ← K8s 전환 (ex07 → Kubernetes)
│   ├── backend/, db/, frontend/, redis/
│   ├── k8s/
│   │   ├── namespace.yml
│   │   ├── backend/ (configmap, secret, deploy, service)
│   │   ├── db/      (secret, pv, pvc, deploy, service)
│   │   ├── frontend/ (deploy, service, ingress)
│   │   └── redis/   (deploy, service)
│   └── README.md
└── yaml/                              ← K8s 개념 단위 학습
    ├── hello-pod2.yml                 (Pod 기본)
    ├── deploy-ex01.yml                (Deployment 기본)
    ├── deploy-ex02.yml                (RollingUpdate)
    ├── deploy-ex03.yml                (envFrom ConfigMap/Secret)
    ├── service-ex01.yml               (NodePort Service)
    ├── configmap-conn.yml             (ConfigMap)
    ├── secret-password.yml            (Secret)
    ├── volume-pv.yml                  (PersistentVolume)
    ├── volume-pvc.yml                 (PersistentVolumeClaim)
    └── volume-pod.yml                 (Pod + PVC 마운트)
```

## 핵심 기능 (의도 안)

| 기능 | 관련 코드 | 주요 기술 | 예제 |
|------|----------|----------|------|
| 컨테이너 생명주기 | ex00 명령어 정리 | docker run/stop/rm, attach/exec, exit vs detach | ex00 |
| 바인드/볼륨 마운트 | ex00 명령어 정리 | --mount type=bind/volume | ex00 |
| docker commit | ex00 명령어 정리 | 컨테이너 → 이미지 (Dockerfile 이전 단계) | ex00 |
| Dockerfile 작성 | ex01~ex07 모든 Dockerfile | FROM, COPY, ENTRYPOINT, CMD, ENV, RUN | ex01~ex07 |
| 포트포워딩 | ex01~ex07 | -p 호스트:컨테이너 | ex01~ex07 |
| Nginx 리버스 프록시 | ex01/lb/nginx.conf | upstream, proxy_pass, location | ex01 |
| Nginx 로드밸런싱 | ex02/lb/nginx.conf | upstream 복수 서버, round-robin | ex02 |
| Nginx 캐시 동작 원리 | ex03/nginx/nginx.conf | proxy_cache, X-Cache-Status | ex03 |
| Docker 브릿지 네트워크 | ex04 README | docker network create, --network | ex04 |
| 컨테이너 DNS | ex04/api/app.py, ex06/lb/nginx.conf | 컨테이너명으로 통신 | ex04, ex06 |
| host.docker.internal → DNS 전환 | ex01 vs ex04 비교 | 우회 → 직접 연결 (문제→해결) | ex01→ex04 |
| MySQL 이미지 초기화 | ex05/db/Dockerfile | docker-entrypoint-initdb.d, ENV | ex05 |
| Docker Compose 기본 | ex06/docker-compose.yml | services, build, networks, ports | ex06 |
| Compose 환경변수 주입 | ex07/docker-compose.yml | environment | ex07 |
| Compose 3티어 구조 | ex07 전체 | frontend + backend + db | ex07 |
| K8s Pod | yaml/hello-pod2.yml | kind: Pod, containers | yaml/ |
| K8s Deployment | yaml/deploy-ex01~03.yml, ex08/k8s/ | replicas, selector, template | yaml/, ex08 |
| K8s RollingUpdate | yaml/deploy-ex02.yml | strategy, maxSurge, maxUnavailable | yaml/ |
| K8s Service (NodePort) | yaml/service-ex01.yml | type: NodePort | yaml/ |
| K8s Service (ClusterIP) | ex08/k8s/*-service.yml | type: ClusterIP | ex08 |
| K8s ConfigMap | yaml/configmap-conn.yml, ex08/backend/ | data, envFrom | yaml/, ex08 |
| K8s Secret | yaml/secret-password.yml, ex08/*/secret | stringData, Opaque | yaml/, ex08 |
| K8s PV/PVC | yaml/volume-*.yml, ex08/db/ | hostPath, PVC 바인딩 | yaml/, ex08 |
| K8s Ingress | ex08/frontend/frontend-ingress.yml | rules, pathType, backend | ex08 |
| K8s Namespace | ex08/k8s/namespace.yml | namespace 분리 | ex08 |
| ENV → Secret 전환 | ex05 vs ex08 비교 | 하드코딩 → Secret 분리 (문제→해결) | ex05→ex08 |
| Compose → K8s 전환 | ex07 vs ex08 비교 | environment → ConfigMap/Secret | ex07→ex08 |

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|----------|----------|
| Linux 명령어 심화 | ex00 (vim, ps, kill, find, tail, apt) | 의도 밖 명시 |
| Flask/Python 앱 코드 상세 | ex03/api/app.py, ex04/api/app.py | 앱은 "컨테이너에 올리는 대상"으로만 |
| Spring Boot/Java 코드 상세 | ex07~08/backend/entrypoint.sh | 빌드 과정은 블랙박스 |
| Nginx 설정 심화 | ex03/nginx/nginx.conf 문법 상세 | 캐시 개념만, 설정 문법 제외 |
| MySQL 운영/쿼리 | ex05~08/db/ | 의도 밖 명시 |
| Redis 운영/데이터 구조 | ex04, ex08/redis/ | DNS 연결 예시로만 활용 |
| Docker Hub push | ex00 | 이미지 배포 과정 제외 |
| K8s 클러스터 구축 | ex08 README (minikube 관련) | Minikube 설치/구성 상세 제외 |
| CI/CD | (미구현) | 의도 밖 명시 |
| 모니터링/로깅 | (미구현) | 의도 밖 명시 |

## 기술 스택 정리 (의도 안)

| 분류 | 기술 | 역할 |
|------|------|------|
| 컨테이너 | Docker | 이미지 빌드, 컨테이너 실행 |
| 오케스트레이션 | Docker Compose | 멀티 컨테이너 선언형 관리 |
| 오케스트레이션 | Kubernetes (Minikube) | 프로덕션급 컨테이너 오케스트레이션 |
| 웹서버/프록시 | Nginx | 리버스 프록시, 로드밸런싱, 캐싱 |
| 앱 (블랙박스) | Flask (Python) | ex03~04 백엔드 |
| 앱 (블랙박스) | Spring Boot (Java) | ex07~08 백엔드 |
| DB (블랙박스) | MySQL | 데이터 영속화 대상 |
| 캐시 (블랙박스) | Redis | 네트워크 연결 대상 |

## 기술 의존성 메모

### 예제 간 선행 관계
```
ex00 (컨테이너 CLI, 마운트)
  └→ ex01 (Dockerfile + Nginx 프록시) ← host.docker.internal 사용
       └→ ex02 (로드밸런싱 — ex01 변형)
            └→ ex03 (캐시 — ex02 변형 + Flask)
                 └→ ex04 (Docker 네트워크 DNS) ← host.docker.internal 문제 해결
                      └→ ex05 (MySQL 이미지 — ENV 하드코딩)
                           └→ ex06 (Compose — ex01+ex04 통합)
                                └→ ex07 (3티어 Compose — ex05+ex06 통합)
                                     └→ yaml/ (K8s 개념 단위 학습)
                                          └→ ex08 (K8s 실전 — ex07 전환)
```

### 독자 배경지식 (알고 있다고 가정)
- HTTP 요청/응답 기본
- 포트 번호 개념
- 프로세스 개념
- IP 주소 기본 (localhost)
- YAML 문법 기초

### 책이 설명해야 할 것 (배경지식에 없음)
- 가상머신 vs 컨테이너 차이
- 이미지 vs 컨테이너 차이
- DNS 동작 원리 (컨테이너 맥락)
- 도커의 기본 동작 원리 & 도커 관련 네트워크 흐름(ex. 호스트pc - 컨테이너 통신, iptables 같이 요청이 왔을 때 어떤 흐름으로 되는지 등)
- 쿠버네티스의 기본 동작 원리 & 쿠버네티스 기본 흐름(ex. 쿠버네티스 리소스간 큰 그림, 리소스간 요청 흐름 등)

## 이야기 소재 — 문제→해결 대비 구조

| 대비 | 문제 (전) | 해결 (후) | 교훈 |
|------|----------|----------|------|
| host.docker.internal → DNS | ex01: 호스트 경유 우회 | ex04: 컨테이너 네트워크 직접 연결 | Docker 네트워크가 왜 필요한가 |
| 수동 docker run → Compose | ex01: 컨테이너 3개 각각 실행 | ex06: docker-compose up 한 줄 | 선언형이 왜 편한가 |
| ENV 하드코딩 → Secret | ex05: Dockerfile에 비밀번호 | ex08: K8s Secret으로 분리 | 설정 분리가 왜 필요한가 |
| Compose → K8s | ex07: environment로 설정 주입 | ex08: ConfigMap + Secret | 대규모에서 왜 K8s인가 |

## 교재 작성 시 주의사항

1. **ex07/ex08 backend 빌드 시간**: entrypoint.sh에서 git clone → gradlew build. 첫 실행에 수분 소요. 독자에게 반드시 안내
2. **ex08 Ingress 선행 조건**: `minikube addons enable ingress` 필요. README 누락
3. **host.docker.internal OS 제한**: Docker Desktop(Win/Mac) 전용. Linux에서 미지원. 교재에서 명확히 언급
4. **ex08 db-pv storageClassName**: 수동 바인딩 방식. StorageClass 자동 할당과의 차이를 간단히 언급
