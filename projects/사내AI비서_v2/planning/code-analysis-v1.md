# 코드 분석

## 완성 코드 정보
- 경로: `projects/사내AI비서/code/`
- 언어: Python 3.x
- 프레임워크: FastAPI + LangChain + ChromaDB

## 전체 구조

```
code/
├── CH03_LLM의_한계와_RAG의_필요성/  ← LLM 실패 체험 + RAG 발견
│   ├── step1_fail.py              ← LLM에게 사내 질문 → 환각 확인
│   ├── step2_context.py           ← 문서를 통째로 넣기 → 토큰 한계
│   ├── step3_rag.py               ← RAG로 해결
│   ├── step3_rag_no_chunking.py   ← 청킹 없는 RAG (비교)
│   ├── step4_rag.py               ← 개선된 RAG
│   └── requirements.txt
│
├── CH04_FastAPI_기본_시스템/       ← 정형 데이터 CRUD + Admin UI
│   ├── app/
│   │   ├── main.py               ← FastAPI 진입점
│   │   ├── database.py           ← psycopg2 PostgreSQL 연결
│   │   ├── models.py             ← Employee, LeaveBalance, Sale dataclass
│   │   ├── schemas.py            ← Pydantic 요청/응답 모델
│   │   ├── crud.py               ← SQL CRUD 함수 (직원/휴가/매출)
│   │   ├── views.py              ← Jinja2 Admin UI 라우터
│   │   └── api.py                ← REST JSON API 라우터
│   ├── templates/                 ← Admin 대시보드 HTML
│   ├── static/css/               ← 스타일
│   ├── docker-compose.yml         ← PostgreSQL 16 컨테이너
│   └── requirements.txt
│
├── CH06_VectorDB_구축/            ← 문서 파싱 + 청킹 + 벡터DB
│   ├── src/
│   │   ├── main.py               ← 파이프라인 오케스트레이션
│   │   ├── extractor.py          ← PDF/DOCX/XLSX 파싱 공통
│   │   ├── extract_pdf.py        ← pypdf PDF 파싱
│   │   ├── extract_docx.py       ← python-docx DOCX 파싱
│   │   ├── extract_xlsx.py       ← openpyxl XLSX 파싱
│   │   ├── chunker.py            ← 500자 청킹 + 100자 오버랩
│   │   ├── store.py              ← ko-sroberta 임베딩 + ChromaDB
│   │   └── cli_search.py         ← CLI 검색 도구
│   ├── data/
│   │   ├── docs/                  ← HR/FIN/OPS/SEC 원본 문서 6개
│   │   ├── markdown/              ← 파싱 결과
│   │   └── chroma_db/             ← ChromaDB 저장소
│   └── requirements.txt
│
├── CH07_RAG_QA_엔진/              ← LLM + RAG 체인 + 채팅 UI
│   ├── app/
│   │   ├── main.py               ← FastAPI 웹 앱
│   │   ├── chat_api.py           ← POST /api/chat 엔드포인트
│   │   └── session.py            ← 세션 관리
│   ├── src/
│   │   ├── rag_chain.py          ← LCEL 파이프라인 + 프롬프트
│   │   ├── response_parser.py    ← 답변 + 출처 파싱
│   │   └── conversation.py       ← 멀티턴 히스토리
│   ├── templates/                 ← 채팅 UI
│   ├── static/                    ← CSS + JS
│   └── requirements.txt
│
├── CH08_통합_에이전트_설계/        ← 정형+비정형 라우팅
│   ├── src/
│   │   ├── router.py             ← 3단계 QueryRouter (규칙→스키마→LLM)
│   │   ├── mcp_tools.py          ← 4개 도구 (DB 쿼리 + 문서 검색)
│   │   └── agent.py              ← ReAct 에이전트
│   ├── app/                       ← 채팅 UI (에이전트 모드)
│   ├── tests/test_scenarios.py    ← 18개 테스트
│   ├── data/schema.sql            ← DDL + 샘플 데이터
│   └── docker-compose.yml
│
├── CH09_LangChain_연결/           ← 에이전트 프레임워크 표준화
│   ├── src/
│   │   ├── main.py               ← CLI 진입점 (대화형 + 데모)
│   │   ├── agent_config.py       ← LLM + Router + AgentExecutor
│   │   ├── monitoring.py         ← JSON 로깅 + Langfuse
│   │   ├── cache.py              ← TTL 응답 캐시
│   │   ├── router.py             ← QueryRouter
│   │   └── tools/                 ← @tool 데코레이터 4개
│   └── requirements.txt
│
└── CH10_RAG_튜닝/                 ← 성능 최적화 10개 실험
    ├── src/                        ← 에이전트 (CH09 기반)
    ├── tuning/
    │   ├── chunk_experiment.py    ← Fixed vs Semantic 청킹
    │   ├── retriever_experiment.py ← k값, threshold 튜닝
    │   ├── reranker.py            ← Cross-Encoder 재정렬
    │   ├── hybrid_search.py       ← BM25 + Vector 앙상블
    │   ├── advanced_retriever.py  ← Parent/SelfQuery
    │   ├── query_rewrite.py       ← HyDE, Multi-Query
    │   ├── document_parser.py     ← 라이브러리 vs vLLM 비교
    │   ├── document_capture.py    ← PDF→PNG→LLaVA 파이프라인
    │   └── evidence_pipeline.py   ← 근거 추적
    ├── data/test_questions.json   ← 평가 질문 30개
    └── outputs/                    ← 실험 결과 + 평가 보고서
```

## 핵심 기능 (의도 안)

| # | 기능 | 관련 코드 | 주요 기술 | 비유 소재 |
|---|------|----------|----------|----------|
| 0a | LLM 환각 체험 | CH03/step1_fail.py | OpenAI API 직접 호출 | 똑똑하지만 우리 회사를 모르는 외부 컨설턴트 |
| 0b | 컨텍스트 스터핑 한계 | CH03/step2_context.py | 토큰 한도 실험 | 편지봉투에 백과사전을 넣으려는 것 |
| 0c | RAG 기초 체험 | CH03/step3_rag.py, step4_rag.py | RAG 파이프라인 기초 | 필요한 페이지만 찾아서 건네주기 |
| 0d | 청킹 유무 비교 | CH03/step3_rag_no_chunking.py | 청킹 없는 RAG | 책 통째로 vs 색인 카드 |
| 1 | 정형 데이터 CRUD | CH04/app/crud.py, api.py | FastAPI, PostgreSQL, Pydantic | 회사 인사/매출 장부 |
| 2 | Admin 대시보드 | CH04/app/views.py, templates/ | Jinja2, HTML/CSS | 관리자 사무실 |
| 3 | 문서 텍스트 추출 | CH06/src/extractor.py, extract_*.py | pypdf, python-docx, openpyxl | 서류함에서 문서 꺼내기 |
| 4 | 텍스트 청킹 | CH06/src/chunker.py | Fixed-size 500자 + 오버랩 100자 | 책을 색인 카드로 잘라내기 |
| 5 | 벡터 임베딩 + DB 저장 | CH06/src/store.py | ko-sroberta, ChromaDB | 도서관 분류 번호 붙이기 |
| 6 | CLI 검색 | CH06/src/cli_search.py | ChromaDB retriever | 도서관에서 책 찾기 |
| 7 | RAG 체인 | CH07/src/rag_chain.py | LCEL, 프롬프트 엔지니어링 | 비서가 자료 찾아서 대답 |
| 8 | 답변 + 출처 파싱 | CH07/src/response_parser.py | OutputParser | 비서가 근거 문서도 같이 제출 |
| 9 | 멀티턴 대화 | CH07/src/conversation.py | WindowMemory | 비서가 이전 대화 기억 |
| 10 | 채팅 웹 UI | CH07/app/, templates/, static/ | FastAPI, Jinja2, Fetch API | 비서와 대화하는 창구 |
| 11 | 질문 라우팅 | CH08/src/router.py | 3단계 (규칙→스키마→LLM) | 안내데스크 — 어디로 보낼지 |
| 12 | MCP 도구 4개 | CH08/src/mcp_tools.py | DB 쿼리 + 문서 검색 | 비서의 연장통 |
| 13 | ReAct 에이전트 | CH08/src/agent.py | LangChain Agent | 비서가 스스로 판단하고 행동 |
| 14 | 에이전트 표준 구성 | CH09/src/agent_config.py | AgentExecutor, Router | 비서 매뉴얼 완성 |
| 15 | 캐시 + 모니터링 | CH09/src/cache.py, monitoring.py | TTL 캐시, Langfuse | 비서 업무 일지 + 빠른 응답 |
| 16 | 청킹 실험 | CH10/tuning/chunk_experiment.py | Fixed vs Semantic | 색인 카드 크기 실험 |
| 17 | Retriever 튜닝 | CH10/tuning/retriever_experiment.py | k값, threshold | 검색 범위 조절 |
| 18 | ReRanker | CH10/tuning/reranker.py | Cross-Encoder | 검색 결과 재정렬 |
| 19 | Hybrid Search | CH10/tuning/hybrid_search.py | BM25 + Vector | 키워드 + 의미 동시 검색 |
| 20 | Query Rewrite | CH10/tuning/query_rewrite.py | HyDE, Multi-Query | 질문을 다시 써보기 |
| 21 | 문서 캡처 파이프라인 | CH10/tuning/document_capture.py | PyMuPDF, OCR, LLaVA | 사진 찍어서 읽기 |
| 22 | 평가 프레임워크 | CH10/src/eval_framework.py | Precision@k, RAGAS | 비서 성적표 |

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|----------|----------|
| 파인튜닝 | (코드 없음) | seed.md 의도 밖 |
| 자체 LLM 학습 | (코드 없음) | seed.md 의도 밖 |
| 프로덕션 배포/운영 | (코드 없음) | seed.md 의도 밖 |

## 기술 스택 정리

| 분류 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **웹** | FastAPI | 0.115+ | REST API + 웹 UI |
| **DB** | PostgreSQL | 16 | 정형 데이터 (직원/휴가/매출) |
| **DB 드라이버** | psycopg2-binary | 2.9.9+ | PostgreSQL 연결 |
| **템플릿** | Jinja2 | 3.1+ | Admin/채팅 UI |
| **검증** | Pydantic | 2.10+ | 요청/응답 스키마 |
| **문서 파싱** | pypdf, python-docx, openpyxl | 각 최신 | PDF/DOCX/XLSX 텍스트 추출 |
| **임베딩** | sentence-transformers (ko-sroberta) | 3.3+ | 768차원 벡터 변환 |
| **벡터DB** | ChromaDB | 1.5+ | 벡터 저장/검색 |
| **LLM 프레임워크** | LangChain | 0.3+ | RAG 체인, 에이전트, 도구 |
| **LLM** | Ollama / OpenAI | - | 텍스트 생성 (선택) |
| **검색 보조** | rank-bm25 | 0.2+ | 키워드 기반 검색 (Hybrid) |
| **ReRanker** | BAAI/bge-reranker-v2-m3 | - | 검색 결과 재정렬 |
| **OCR** | easyocr | 1.7+ | 이미지 텍스트 추출 |
| **PDF 이미지화** | PyMuPDF | 1.24+ | 페이지별 PNG 변환 |
| **모니터링** | Langfuse (선택) | 2.60+ | LLM 호출 추적 |

## 기술 의존성 메모

```
LLM 한계 + RAG 필요성 (CH03) ← 왜 RAG가 필요한지 체험
  ↓ RAG 동기부여
FastAPI (CH04)
  ↓ 웹 프레임워크 기반
문서 파싱 + 청킹 + ChromaDB (CH06)
  ↓ 벡터DB가 준비되어야
RAG 체인 (CH07) ← LCEL, 프롬프트 엔지니어링 이해 필요
  ↓ RAG가 있어야
라우팅 + 에이전트 (CH08) ← 정형(CH04) + 비정형(CH06~07) 통합
  ↓ 에이전트 구조가 잡혀야
LangChain 표준 (CH09) ← 도구, 캐시, 모니터링 추가
  ↓ 표준 구성이 있어야
RAG 튜닝 (CH10) ← 기존 파이프라인 위에서 실험
```

**선행 개념 (독자가 알아야 할 것)**:
- Python 기초 (함수, 클래스, 데코레이터)
- 터미널/CLI 사용
- Docker 기본 (docker-compose up 수준)
- REST API 개념 (GET/POST 수준)

**책에서 설명해야 할 개념** (독자가 모를 것):
- LLM의 한계 (환각, 토큰 한도, 보안) — CH03에서 실패 체험으로
- RAG가 뭔지 (왜 LLM만으로 안 되는지) — CH03에서 해결 과정으로
- 임베딩이 뭔지 (벡터가 뭔지)
- 청킹이 뭔지 (왜 잘라야 하는지)
- 프롬프트 엔지니어링 기초
- 에이전트/도구 패턴
- 벡터 유사도 검색 원리
