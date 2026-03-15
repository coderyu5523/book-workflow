# 코드 분석 — 사내AI비서_v3

## 프로젝트 트리

### ex01 — RAG 개념 증명 (문제 체험형 도입)

```
ex01/
├── step1_fail.py           # LLM에 직접 질문 -> 할루시네이션 체험
├── step2_context.py        # 프롬프트에 정보를 직접 삽입 -> 정답 확인
├── step3_rag.py            # 첫 번째 RAG 파이프라인 (VectorDB + RetrievalQA)
├── step3_rag_no_chunking.py # 청킹 미적용 RAG (통짜 문서의 비효율 체험)
├── step4_rag.py            # 추론이 필요한 복잡한 질문으로 RAG 테스트
└── requirements.txt        # langchain, langchain-ollama, chromadb 등
```

### ex02 — 사내 CRUD 시스템 (데이터베이스 기반)

```
ex02/
├── app/
│   ├── main.py             # FastAPI 진입점, 라우터 등록
│   ├── database.py         # psycopg2 PostgreSQL 연결 컨텍스트 매니저
│   ├── models.py           # Employee, LeaveBalance, Sale, DeptSummary dataclass
│   ├── crud.py             # 직원/연차/매출 CRUD 함수 (psycopg2 raw SQL)
│   ├── api.py              # REST JSON API 라우터 (/api/*)
│   ├── schemas.py          # Pydantic 요청/응답 스키마
│   └── views.py            # Jinja2 Admin UI 라우터 (/admin/*)
├── data/schema.sql         # PostgreSQL DDL + 시드 데이터 (직원 5명, 매출 10건)
├── docker-compose.yml      # PostgreSQL 16 컨테이너
├── run.py                  # uvicorn 서버 실행
├── requirements.txt
├── static/css/style.css    # Admin UI 스타일시트
└── templates/              # dashboard, employees, leaves, sales HTML
```

### ex04 — VectorDB 구축 파이프라인

```
ex04/
├── src/
│   ├── extractor.py        # PDF/DOCX/XLSX 텍스트 추출
│   ├── chunker.py          # Fixed-size 청킹 (500자, 오버랩 100자) + 메타데이터
│   ├── store.py            # ko-sroberta-multitask 임베딩 + ChromaDB 저장/검색
│   ├── main.py             # 파이프라인 오케스트레이터 (Step1 파싱 -> Step2 임베딩)
│   └── cli_search.py       # ChromaDB CLI 검색 도구
├── data/
│   ├── docs/               # 원본 문서 (HR PDF, 보안 DOCX, 재무 XLSX 등)
│   ├── markdown/           # 파싱 결과 마크다운 (검증용)
│   └── chroma_db/          # ChromaDB 영속 데이터
└── requirements.txt
```

### ex05 — RAG Q&A 엔진 (채팅 웹앱)

```
ex05/
├── app/
│   ├── main.py             # FastAPI 진입점
│   ├── chat_api.py         # 채팅 API (/api/chat) — RAG 체인 호출
│   └── session.py          # 세션 ID 생성/쿠키 관리
├── src/
│   ├── rag_chain.py        # LCEL 파이프라인 (Retriever | Prompt | LLM | Parser)
│   ├── llm_factory.py      # LLM 팩토리 (Ollama/OpenAI 분기)
│   ├── vectorstore.py      # ChromaDB Retriever 생성 (자동 구축 포함)
│   ├── conversation.py     # WindowMemory (슬라이딩 윈도우 대화 메모리)
│   ├── response_parser.py  # <think> 태그 제거 + 출처 추출
│   └── session_manager.py  # ConversationManager (세션별 TTL 관리)
├── data/                   # docs + chroma_db
├── static/css/             # chat.css, style.css
├── templates/              # chat.html, base.html
├── run.py
└── requirements.txt
```

### ex06 — 통합 에이전트 (정형 + 비정형)

```
ex06/
├── app/
│   ├── main.py             # FastAPI 진입점 (chat + admin 통합)
│   ├── chat_api.py         # 채팅 API — IntegratedAgent 호출
│   ├── admin_crud.py       # Admin CRUD 라우터
│   ├── admin_views.py      # Admin Jinja2 뷰
│   └── database.py         # PostgreSQL 연결
├── src/
│   ├── agent.py            # IntegratedAgent (ReAct + Tool Calling)
│   ├── router.py           # QueryRouter (규칙 -> 스키마 -> LLM 3단계 분류)
│   ├── mcp_tools.py        # @tool 정의 (leave_balance, sales_sum, list_employees, search_documents)
│   ├── llm_factory.py      # LLM 팩토리
│   ├── agent_helpers.py    # 에이전트 결과 파싱, <think> 태그 제거
│   └── db_helper.py        # PostgreSQL 쿼리 헬퍼 + ChromaDB 벡터스토어 로드
├── tests/test_scenarios.py # 에이전트 시나리오 테스트
├── data/                   # docs + chroma_db + schema.sql
├── docker-compose.yml
├── static/, templates/     # chat + admin UI
└── requirements.txt
```

### ex07 — 운영 안정화 (캐시, 모니터링, 재시도)

```
ex07/
├── app/
│   ├── main.py             # FastAPI 진입점
│   ├── chat_api.py         # 채팅 API — ConnectHRAgent 호출
│   ├── admin_crud.py       # Admin CRUD
│   ├── admin_views.py      # Admin 뷰 + 통계 페이지
│   └── database.py         # PostgreSQL 연결
├── src/
│   ├── agent_config.py     # ConnectHRAgent (캐시 + 재시도 + Langfuse 통합)
│   ├── router.py           # QueryRouter (3단계 분류)
│   ├── agent_helpers.py    # RAG 체인 구축 + 라우트 분류 헬퍼
│   ├── llm_factory.py      # LLM 팩토리
│   ├── cache.py            # ResponseCache (TTL 인메모리) + EmbeddingCache (파일)
│   ├── monitoring.py       # JsonFormatter + TokenTracker + LangfuseMonitor
│   └── tools/
│       ├── leave_balance.py
│       ├── sales_sum.py
│       ├── list_employees.py
│       └── search_documents.py
├── data/
├── docker-compose.yml
├── static/, templates/     # chat + admin + stats UI
└── requirements.txt
```

### ex08 — RAG 튜닝 실험 (검색 품질 개선)

```
ex08/
├── tuning/
│   ├── step1_chunk_experiment/   # 청킹 실험
│   │   ├── __main__.py           # CLI 진입점
│   │   ├── strategies.py         # Fixed / Recursive / Semantic 청킹 전략
│   │   ├── experiments.py        # 5가지 실험 실행기
│   │   ├── retriever.py          # InMemoryRetriever (실험용)
│   │   ├── analysis.py           # 청크 통계 분석
│   │   ├── data.py               # 샘플 문서 + 테스트 쿼리
│   │   └── display.py            # Rich 테이블 출력
│   ├── step2_reranker/           # Reranker 실험
│   │   ├── __main__.py
│   │   ├── reranker.py           # CrossEncoderReranker + SimpleReranker (폴백)
│   │   ├── experiments.py        # 검색 품질 비교
│   │   ├── data.py
│   │   └── display.py
│   └── step3_hybrid_search/      # 하이브리드 검색 실험
│       ├── __main__.py
│       ├── retrievers.py         # BM25Retriever + VectorRetriever + EnsembleRetriever
│       ├── experiments.py        # BM25 vs Vector vs Ensemble 비교
│       ├── data.py
│       └── display.py
├── data/
├── docker-compose.yml
└── requirements.txt
```

### ex09 — 고급 Retriever + 쿼리 변환

```
ex09/
└── tuning/
    ├── step1_advanced_retriever/
    │   ├── __main__.py
    │   ├── retrievers.py         # ParentDoc, SelfQuery, ContextualCompression
    │   ├── experiments.py        # 3가지 고급 검색기 비교
    │   ├── data.py
    │   └── display.py
    └── step2_query_rewrite/
        ├── __main__.py
        ├── rewriters.py          # 약어확장, HyDE, Multi-Query
        ├── experiments.py        # 쿼리 변환 전후 비교
        ├── data.py
        └── display.py
```

### ex10 — 문서 파싱 고도화 + 평가 프레임워크

```
ex10/
├── tuning/
│   ├── step1_document_parser/    # OCR vs Vision LLM 파싱 비교
│   │   ├── __main__.py
│   │   ├── parser.py             # parse_pdf_ocr (EasyOCR), parse_pdf_vllm (Vision LLM)
│   │   └── display.py
│   ├── step2_hybrid_parser/      # 하이브리드 파싱 전략
│   │   ├── __main__.py
│   │   ├── hybrid_parser.py      # OCR->VisionLLM 폴백 + 텍스트레이어 우선
│   │   └── display.py
│   └── step3_eval_framework/     # RAG 평가 프레임워크
│       ├── __main__.py
│       ├── evaluator.py          # 벡터DB 구축 -> 검색 -> LLM 답변 -> 지표 계산
│       ├── metrics.py            # Precision@K, Recall@K, MRR, 할루시네이션 추정
│       └── display.py
├── app/                          # 웹앱 (chat + admin)
├── src/
│   ├── evidence.py               # 캡처 이미지 경로 -> 웹 URL 변환
│   ├── capture.py                # 문서 캡처 유틸리티
│   └── tools/search_documents.py # 문서 검색 도구
├── data/test_questions.json      # 평가용 질문 세트
├── generate_real_pdfs.py         # 테스트용 PDF 생성 스크립트
├── process_pdfs.py               # PDF 일괄 처리
└── run.py
```


## 기능 목록

### ex01 — RAG 개념 증명

| 파일 | 핵심 함수/로직 | 역할 |
|------|--------------|------|
| step1_fail.py | `llm.invoke(question)` | LLM에 사내 규정 직접 질문 -> 할루시네이션 발생 체험 |
| step2_context.py | 프롬프트에 `context_data` 삽입 | 수동 컨텍스트 주입으로 정답 확인 |
| step3_rag.py | `RetrievalQA.from_chain_type()` | 더미 3건으로 최소 RAG 파이프라인 구현 |
| step3_rag_no_chunking.py | 통짜 Document 1건 | 청킹 미적용 시 검색 비효율 체험 |
| step4_rag.py | 복잡한 추론 질문 | RAG 한계 체험 (단순 검색으로는 추론 불가) |

### ex02 — CRUD 시스템

| 파일 | 핵심 함수/클래스 | 역할 |
|------|----------------|------|
| database.py | `get_connection()` | psycopg2 컨텍스트 매니저 |
| models.py | `Employee`, `LeaveBalance`, `Sale`, `DeptSummary` | dataclass 도메인 모델 |
| crud.py | `create_employee()`, `get_all_employees()`, `update_leave_usage()`, `get_dashboard_stats()` 등 | 직원/연차/매출 CRUD (raw SQL) |
| api.py | `api_get_employees()`, `api_use_leave()` 등 | REST API 엔드포인트 |
| views.py | `view_dashboard()`, `view_employees()` 등 | Jinja2 Admin UI |
| schemas.py | `EmployeeCreate`, `LeaveUsageRequest` 등 | Pydantic 스키마 |

### ex04 — VectorDB 구축

| 파일 | 핵심 함수/클래스 | 역할 |
|------|----------------|------|
| extractor.py | `extract_from_pdf()`, `extract_from_docx()`, `extract_from_xlsx()`, `extract_text()` | 형식별 텍스트 추출 |
| chunker.py | `split_text_into_chunks()`, `chunk_extract_result()`, `build_text_chunk()` | Fixed-size 청킹 + 메타데이터 |
| store.py | `load_embedding_model()`, `store_chunks_to_chroma()`, `search_chroma()` | 임베딩 + ChromaDB 저장/검색 |
| main.py | `step1_python_parsing()`, `step2_embed_and_store()` | 2단계 파이프라인 오케스트레이터 |
| cli_search.py | `run_single_query()`, `run_interactive_mode()` | CLI 벡터 검색 검증 |

### ex05 — RAG Q&A 엔진

| 파일 | 핵심 함수/클래스 | 역할 |
|------|----------------|------|
| rag_chain.py | `build_rag_chain()`, `get_rag_chain()` | LCEL 파이프라인 조립 |
| llm_factory.py | `build_llm()` | LLM 분기 (Ollama/OpenAI) |
| vectorstore.py | `build_retriever()`, `_parse_and_chunk_docs()` | ChromaDB Retriever + 자동 구축 |
| conversation.py | `WindowMemory` | 슬라이딩 윈도우 대화 메모리 |
| response_parser.py | `parse_answer_text()`, `build_response()` | `<think>` 태그 제거, 출처 추출 |
| session_manager.py | `ConversationManager` | 세션별 대화 관리 (TTL) |
| chat_api.py | `chat_endpoint()` | 채팅 API 엔드포인트 |

### ex06 — 통합 에이전트

| 파일 | 핵심 함수/클래스 | 역할 |
|------|----------------|------|
| agent.py | `IntegratedAgent`, `_build_agent_executor()`, `run()` | ReAct 에이전트 (Tool Calling) |
| router.py | `QueryRouter`, `classify_query()` | 3단계 질문 분류 |
| mcp_tools.py | `leave_balance()`, `sales_sum()`, `list_employees()`, `search_documents()` | @tool 도구 4종 |
| agent_helpers.py | `parse_agent_result()`, `clean_think_tags()` | 결과 파싱 |

### ex07 — 운영 안정화

| 파일 | 핵심 함수/클래스 | 역할 |
|------|----------------|------|
| agent_config.py | `ConnectHRAgent`, `_run_with_retry()`, `run()` | 운영급 에이전트 |
| cache.py | `ResponseCache`, `EmbeddingCache` | TTL 캐시 + 파일 임베딩 캐시 |
| monitoring.py | `JsonFormatter`, `TokenTracker`, `LangfuseMonitor` | 로깅 + 토큰 추적 + Langfuse |
| tools/ | 4종 도구 (개별 파일 분리) | leave_balance, sales_sum, list_employees, search_documents |

### ex08 — RAG 튜닝 실험

| 서브모듈 | 핵심 구현 | 역할 |
|---------|----------|------|
| step1_chunk_experiment | `fixed_size_chunking()`, `recursive_character_chunking()`, `semantic_chunking()`, `InMemoryRetriever` | 청크 크기/오버랩/전략 비교 + Retriever 파라미터 실험 |
| step2_reranker | `CrossEncoderReranker`, `SimpleReranker` | Cross-Encoder 리랭킹 vs 키워드 폴백 비교 |
| step3_hybrid_search | `BM25Retriever`, `VectorRetriever`, `EnsembleRetriever` | BM25 + Vector 앙상블 하이브리드 검색 |

### ex09 — 고급 Retriever + 쿼리 변환

| 서브모듈 | 핵심 구현 | 역할 |
|---------|----------|------|
| step1_advanced_retriever | `ParentDocumentRetriever`, `SelfQueryRetriever`, `ContextualCompressionRetriever` | 부모문서, 메타데이터 필터링, 문맥 압축 |
| step2_query_rewrite | `expand_abbreviations()`, `compare_hyde_vs_direct()`, `generate_multi_queries()` | 약어확장, HyDE, Multi-Query |

### ex10 — 문서 파싱 고도화 + 평가

| 서브모듈 | 핵심 구현 | 역할 |
|---------|----------|------|
| step1_document_parser | `parse_pdf_ocr()`, `parse_pdf_vllm()` | OCR vs Vision LLM 파싱 비교 |
| step2_hybrid_parser | `process_image_hybrid()`, `process_image_textlayer()` | OCR->Vision 폴백, 텍스트레이어 우선 |
| step3_eval_framework | `run_evaluation()`, `calculate_precision_at_k()`, `calculate_mrr()`, `estimate_hallucination_rate()` | Precision@K, Recall@K, MRR, 할루시네이션률 |
| src/evidence.py | `resolve_image_url()`, `list_captured_images()` | 캡처 이미지 -> 웹 URL 변환 |


## 기술 스택

### LLM / AI

| 기술 | 버전 | 용도 |
|------|------|------|
| LangChain | 0.3.7~0.3.21 | RAG 체인, Agent, Tool Calling |
| langchain-ollama | 0.2.0~0.2.3 | Ollama LLM 연동 |
| langchain-openai | 0.2.9~0.3.7 | OpenAI LLM 연동 |
| langchain-chroma | 0.2.4~0.2.6 | ChromaDB 통합 |
| langchain-community | 0.3.7~0.3.20 | HuggingFace 임베딩 등 |
| langchain-text-splitters | 0.3.8 | Recursive/Semantic 청킹 |
| langchain-experimental | 0.3.4 | SemanticChunker (ex08) |
| langchain-classic | 0.1.0 | RetrievalQA 레거시 체인 (ex01) |
| sentence-transformers | 3.3.1 | 임베딩 + Cross-Encoder |
| Ollama deepseek-r1:8b | — | 기본 로컬 LLM |
| OpenAI gpt-4o-mini | — | 클라우드 LLM 대안 |
| qwen2.5vl:7b | — | Vision LLM (ex10 파싱) |

### VectorDB / 검색

| 기술 | 버전 | 용도 |
|------|------|------|
| ChromaDB | 1.5.1 | 벡터 데이터베이스 |
| ko-sroberta-multitask | — | 한국어 문장 임베딩 |
| rank-bm25 | 0.2.2 | BM25 키워드 검색 |

### 문서 파싱

| 기술 | 버전 | 용도 |
|------|------|------|
| pypdf | 4.3.1 | PDF 텍스트 추출 |
| python-docx | 1.1.2 | DOCX 추출 |
| openpyxl | 3.1.5 | XLSX 추출 |
| PyMuPDF (fitz) | 1.24.0 | PDF 이미지 렌더링 |
| pdfplumber | 0.11.4 | PDF 정밀 텍스트 추출 |
| EasyOCR | 1.7.2 | OCR 텍스트 인식 |

### 웹 / 데이터베이스 / 운영

| 기술 | 버전 | 용도 |
|------|------|------|
| FastAPI | 0.115.x | REST API + Admin UI |
| PostgreSQL | 16 | 정형 데이터 |
| psycopg2-binary | 2.9.x | PostgreSQL 드라이버 |
| Langfuse | (선택) | LLM 모니터링 |
| Rich | 13.9.4 | 터미널 출력 |
| Docker Compose | — | PostgreSQL 컨테이너 |


## 의존성 맵

### 모듈 간 진화 경로

```
ex01 (문제 체험)
  │  "LLM만으로 안 되는구나"
  ▼
ex02 (CRUD 시스템)
  │  "AI가 쓸 데이터를 만들자"    ── 정형 데이터 기반 구축
  ▼
ex04 (VectorDB)
  │  "비정형 문서도 검색하자"     ── 파싱 -> 청킹 -> 임베딩 -> 저장
  ▼
ex05 (RAG 엔진)
  │  "검색한 문서로 답변하자"     ── LCEL 체인 + 대화 메모리
  ▼
ex06 (통합 에이전트)
  │  "DB도 문서도 한 번에"        ── Tool Calling + QueryRouter
  ▼
ex07 (운영 안정화)
  │  "실서비스급으로 키우자"      ── 캐시 + 재시도 + 모니터링
  ▼
ex08 (RAG 튜닝)                  ── 검색 품질 실험 (사이드 브랜치)
  │  "청킹/Reranker/하이브리드"
  ▼
ex09 (고급 Retriever)            ── 검색 고도화 실험 (사이드 브랜치)
  │  "ParentDoc/SelfQuery/HyDE"
  ▼
ex10 (파싱 고도화 + 평가)        ── 문서 파싱 + 품질 측정 (사이드 브랜치)
     "OCR/Vision/평가 프레임워크"
```

### 공유 컴포넌트

| 컴포넌트 | 등장 모듈 | 설명 |
|---------|----------|------|
| `llm_factory.py` | ex05, ex06, ex07 | Ollama/OpenAI 분기 팩토리 |
| `database.py` | ex02, ex06, ex07, ex10 | psycopg2 PostgreSQL 연결 |
| QueryRouter | ex06, ex07 | 3단계 질문 분류 |
| ChromaDB 벡터스토어 | ex04, ex05, ex06, ex07, ex10 | 동일 컬렉션/임베딩 모델 |
| Tool 4종 | ex06, ex07 | leave_balance, sales_sum, list_employees, search_documents |
| Admin UI 템플릿 | ex02, ex06, ex07, ex10 | dashboard/employees/leaves/sales HTML |
| data/docs/ 원본 문서 | ex04~ex08 | HR PDF, 보안 DOCX, 재무 XLSX |


## 의도 필터

### 의도 안 (핵심, 반드시 다뤄야 할 기능)

| 기능 | 위치 | 이유 |
|------|------|------|
| LLM 할루시네이션 체험 | ex01/step1_fail.py | "문제를 먼저 겪고" — 책의 출발점 |
| 컨텍스트 주입 해결 체험 | ex01/step2_context.py | RAG 필요성의 직관적 이해 |
| 최소 RAG 파이프라인 | ex01/step3_rag.py | "직접 만들어봐야 이해한다" |
| 청킹 유무 비교 | ex01/step3_rag_no_chunking.py | 청킹 필요성 체험 |
| PostgreSQL CRUD | ex02/ 전체 | 에이전트가 사용할 정형 데이터 기반 |
| 문서 파싱 파이프라인 | ex04/extractor, chunker | "데이터를 넣는" 과정 |
| 임베딩 + VectorDB 저장 | ex04/store.py | RAG의 핵심 인프라 |
| LCEL RAG 체인 | ex05/rag_chain.py | LangChain 파이프 연산자 |
| LLM 팩토리 | ex05/llm_factory.py | 로컬/클라우드 LLM 전환 |
| 대화 메모리 | ex05/conversation.py | 대화 맥락 유지 |
| Tool Calling Agent | ex06/agent.py, mcp_tools.py | 정형+비정형 통합 |
| QueryRouter | ex06/router.py | 에이전트 라우팅 |
| 캐시/재시도/모니터링 | ex07/ | 운영 안정화 패턴 |
| 청킹 전략 비교 | ex08/step1 | Fixed vs Recursive vs Semantic |
| Reranker | ex08/step2 | Cross-Encoder 리랭킹 |
| 하이브리드 검색 | ex08/step3 | BM25 + Vector 앙상블 |
| 고급 Retriever | ex09/step1 | ParentDoc, SelfQuery, ContextualCompression |
| 쿼리 변환 | ex09/step2 | HyDE, Multi-Query |
| 문서 파싱 고도화 | ex10/step1~2 | OCR/Vision 처리 |
| RAG 평가 프레임워크 | ex10/step3 | Precision, Recall, MRR, 할루시네이션 |

### 의도 밖 (존재하지만 깊이 다루지 않아도 될 기능)

| 기능 | 위치 | 이유 |
|------|------|------|
| Admin UI 템플릿 (HTML/CSS/JS) | ex02~ex10의 templates/ | 웹 프론트엔드는 주제 밖 |
| Docker Compose 설정 | ex02, ex06~ex08 | 인프라 설정은 부록 수준 |
| Pydantic 스키마 상세 | ex02/schemas.py | API 검증 세부사항 |
| Jinja2 뷰 로직 상세 | ex02/views.py | 서버사이드 렌더링 세부 |
| Langfuse 연동 상세 | ex07/monitoring.py | 선택적 도구 |
| EmbeddingCache | ex07/cache.py | 최적화 세부사항 |
| 테스트 PDF 생성 스크립트 | ex10/ | 데이터 생성용 유틸 |

### 주의 (하지 않으려는 것에 해당하는 패턴)

| 패턴 | 위치 | 설명 |
|------|------|------|
| API 레퍼런스 나열 위험 | ex02/api.py (18개 엔드포인트) | CRUD 전부 나열하면 레퍼런스가 됨. 핵심 흐름만 발췌 필요 |
| 이론 후 방치 위험 | ex08~ex10 실험 모듈 | 실험만 보여주고 해석 없으면 방치 패턴. 문제 -> 실험 -> 결과 해석 흐름 필수 |
| 백과사전식 나열 위험 | ex09 고급 Retriever 3종 | 단순 나열 금지. 각각의 "해결하려는 문제"를 먼저 제시해야 함 |


## 교차 검증 메모

- **ChromaDB 1.5.1**: 전 모듈 통일. 최신 안정 버전, PersistentClient API 사용
- **LangChain 0.3.x**: ex01은 langchain-classic(0.1.0)에서 RetrievalQA 사용, ex05부터 LCEL로 전환. 의도적 진화 경로
- **ko-sroberta-multitask**: 한국어 특화 임베딩. 전 모듈 동일 모델로 일관성 유지
- **Ollama deepseek-r1:8b**: 기본 LLM. `<think>` 태그 제거 로직이 ex05, ex06에 존재
- **psycopg2 vs SQLAlchemy**: requirements에 둘 다 있으나 실제 코드는 raw SQL만 사용. SQLAlchemy는 불필요 의존성
- **langchain-experimental 0.3.4**: SemanticChunker 전용 (ex08). 별도 설치 필요 명시 권장
- **EasyOCR 1.7.2**: GPU 없이 CPU 모드 (`gpu=False`). 독자 환경 호환성 우선
- **ex01 langchain-classic**: 레거시 패키지. RetrievalQA -> LCEL 마이그레이션을 보여주는 의도적 선택
