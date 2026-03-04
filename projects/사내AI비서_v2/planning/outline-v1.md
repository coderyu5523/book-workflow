# 목차

## 코드 실습 분류 기준
| 분류 | 표시 | 의미 | 독자 액션 |
|------|------|------|----------|
| 실습 | [실습] | 챕터 핵심 코드 | 독자가 직접 작성 |
| 설명 | [설명] | 중요하지만 핵심 아닌 코드 | 코드 읽고 이해 |
| 참고 | [참고] | 이 챕터 주제가 아닌 코드 | 파일명 + 한 줄만 |

---

## Part 0. 시작 전에
> PART 0 (미리보기) + PART 0.5 (환경 설정)을 책의 도입부로 구성.
> 독자가 최종 완성본을 먼저 보고 "이걸 만들 수 있구나"를 느끼게 한다.

### 프롤로그: 이 책이 다루는 것 — ~4p
**내용**: 최종 데모 시나리오 + 아키텍처 한 장 요약 + 독자 대상
*(별도 집필 STEP에서 작성 — 여기서는 자리 표시)*

### 부록 (환경 설정): Ollama + Python + Docker — ~4p
*(STEP 7 마무리에서 작성)*

---

## Part 1. AI가 왜 거짓말을 할까

### CH01: "ChatGPT에 물어봤더니…" — 환각과 RAG의 첫 만남 (v0.0)

**핵심 개념**: LLM 환각, Context Injection, RAG 기본
**기술**: Ollama + deepseek-r1:8b, LangChain RetrievalQA, ChromaDB
**버전 성과**: CLI에서 환각 vs RAG 응답 직접 비교
**예상 분량**: ~12p

**코드 실습 분류**:
```
v0.0/
├── step1_fail.py           [실습] LLM 단독 호출 → 환각 체험
├── step2_context.py        [실습] 컨텍스트 직접 주입 → 임시 해결
├── step3_rag.py            [실습] RAG 기본 파이프라인 구성
├── step3_rag_no_chunking.py [설명] 청킹 유무 비교 (읽기만)
└── step4_rag.py            [참고] 추론 심화 (Chain-of-Thought)
```
**실습 요약**: 실습 3개 / 설명 1개 / 참고 1개

---

## Part 2. 사내 시스템 만들기

### CH02: "일단 사내 시스템부터" — FastAPI로 CRUD 만들기 (v0.1)

**핵심 개념**: REST API, Pydantic, psycopg2, CRUD 패턴
**기술**: FastAPI, PostgreSQL 16, psycopg2, Pydantic 2
**버전 성과**: API로 직원/연차/매출 CRUD 동작
**예상 분량**: ~10p

**코드 실습 분류**:
```
v0.1/app/
├── models.py      [실습] 데이터 모델 (dataclass)
├── schemas.py     [실습] Pydantic 요청/응답 스키마
├── database.py    [실습] DB 연결 패턴 (Context Manager)
├── crud.py        [실습] CRUD 함수 + 매개변수화 쿼리
├── api.py         [설명] REST API 라우터
├── main.py        [참고] FastAPI 앱 진입점
└── views.py       (제외) Jinja2 Admin UI
```
**실습 요약**: 실습 4개 / 설명 1개 / 참고 1개

---

### CH03: "어떤 문서를 넣을까" — 사내 문서 수집 전략과 표준 (v0.2)

**핵심 개념**: 문서 품질, 메타데이터, 청킹 전략 사전 설계, 재인덱싱 전략
**기술**: (코드 없음 — 개념 챕터)
**버전 성과**: 문서 표준 규칙 + 폴더 구조 템플릿 + 재인덱싱 운영 가이드 (독자가 직접 적용 가능)
**예상 분량**: ~9p

**코드 실습 분류**:
```
(코드 없음)
- 문서 표준 규칙 예시 (Markdown 템플릿)
- docs/ 폴더 구조 설계
- 메타데이터 설계 가이드
```
**실습 요약**: 설명 0 / 실습 0 / 개념 중심

---

## Part 3. RAG 엔진 만들기

### CH04: "문서를 '지식'으로 바꾸다" — VectorDB 구축 (v0.3)

**핵심 개념**: 문서 파싱, 청킹, 임베딩, 벡터 저장/검색, 임베딩 모델 선택 기준
**기술**: pypdf, python-docx, openpyxl, ko-sroberta-multitask, ChromaDB
**버전 성과**: CLI에서 벡터 검색 결과 + 코사인 유사도 점수 확인
**예상 분량**: ~11p

> **갭 분석 반영**: "왜 ko-sroberta를 썼나?" 섹션 포함 — 한국어 특화 모델 vs 다국어 모델 비교, 선택 기준 설명.

**코드 실습 분류**:
```
v0.3/src/
├── extractor.py    [실습] PDF/DOCX/XLSX 통합 파서
├── chunker.py      [실습] Fixed-size 청킹 (500자+100오버랩)
├── store.py        [실습] ko-sroberta 임베딩 + ChromaDB upsert
├── main.py         [설명] 파이프라인 오케스트레이션
├── cli_search.py   [설명] 벡터 검색 결과 시각화
├── extract_pdf.py  [참고] PDF 파싱 상세
├── extract_docx.py [참고] DOCX 파싱 상세
└── extract_xlsx.py [참고] XLSX 파싱 상세
```
**실습 요약**: 실습 3개 / 설명 2개 / 참고 3개

---

### CH05: "드디어 답해준다" — RAG Q&A 엔진 (v0.4)

**핵심 개념**: LCEL 파이프라인, 출처 강제, 멀티턴 대화
**기술**: LangChain LCEL (Retriever|Prompt|LLM|Parser), WindowMemory, FastAPI
**버전 성과**: API/CLI에서 질문 → 답변 + [출처: 문서명] 표시
**예상 분량**: ~10p

**코드 실습 분류**:
```
v0.4/src/
├── rag_chain.py       [실습] LCEL 파이프라인 + 출처 강제 프롬프트
├── conversation.py    [실습] WindowMemory(k=5) 멀티턴
├── response_parser.py [설명] DeepSeek <think> 제거 + 출처 추출
v0.4/app/
├── chat_api.py        [설명] POST /api/chat
└── session.py         [참고] 세션 쿠키 관리
```
**실습 요약**: 실습 2개 / 설명 2개 / 참고 1개

---

## Part 4. 진짜 비서 만들기

### CH06: "'연차 몇 개, 규정은?' 동시에" — 통합 에이전트 설계 (v0.5)

**핵심 개념**: QueryRouter, MCP 도구, ReAct 에이전트
**기술**: 규칙/스키마/LLM 3단계 라우팅, @tool 데코레이터, AgentExecutor
**버전 성과**: CLI에서 정형+비정형 복합 질문에 통합 응답
**예상 분량**: ~10p

**코드 실습 분류**:
```
v0.5/src/
├── router.py      [실습] 3단계 QueryRouter (규칙→스키마→LLM)
├── mcp_tools.py   [실습] @tool 4개 (leave_balance, sales_sum, list_employees, search_documents)
└── agent.py       [실습] ReAct Agent (create_tool_calling_agent)
v0.5/app/
├── chat_api.py    [설명] 에이전트/RAG 모드 선택 API
└── database.py    [참고] PostgreSQL 연결
```
**실습 요약**: 실습 3개 / 설명 1개 / 참고 1개

---

### CH07: "실제로 써보니" — 운영을 위한 안정화 (v0.6)

**핵심 개념**: 응답 캐시, 임베딩 캐시, 토큰 추적, 에이전트 표준화
**기술**: ResponseCache(TTL), EmbeddingCache, TokenTracker, ConnectHRAgent
**버전 성과**: CLI 데모 모드에서 캐시 히트율 + 토큰 사용량 통계
**예상 분량**: ~8p

**코드 실습 분류**:
```
v0.6/src/
├── agent_config.py  [실습] ConnectHRAgent 표준 구성
├── cache.py         [실습] ResponseCache(TTL) + EmbeddingCache
├── monitoring.py    [설명] TokenTracker + JSON 로깅
├── main.py          [설명] CLI 대화형 + 데모 모드
└── tools/           [참고] @tool 모듈화 (CH06 개선)
```
**실습 요약**: 실습 2개 / 설명 2개 / 참고 1개

---

## Part 5. 더 잘 만들기 — 튜닝과 평가

### CH08: "엉뚱한 문서를 가져온다" — 검색 품질 튜닝 (v0.7)

**핵심 개념**: 청킹 최적화, Retriever 튜닝, 리랭킹, 하이브리드 검색
**기술**: Semantic Chunking, Cross-Encoder ReRanker, BM25+Vector, rank-bm25
**버전 성과**: CLI에서 실험 전/후 검색 품질 수치 비교
**예상 분량**: ~12p

**코드 실습 분류**:
```
v0.7/tuning/
├── chunk_experiment.py     [실습] Fixed vs Semantic, 크기/오버랩 실험
├── retriever_experiment.py [실습] k값, threshold 실험
├── reranker.py             [실습] Cross-Encoder 리랭킹
└── hybrid_search.py        [실습] BM25+Vector, alpha 조정
```
**실습 요약**: 실습 4개

---

### CH09: "질문을 제대로 이해 못한다" — 질문+답변 고급 튜닝 (v0.8)

**핵심 개념**: 고급 Retriever, Query Rewrite, 답변 근거 시스템
**기술**: Parent Document Retriever, HyDE, Multi-Query, EvidencePipeline
**버전 성과**: CLI에서 쿼리 변환 로그 + 이미지/DB 근거 포함 응답
**예상 분량**: ~10p

**코드 실습 분류**:
```
v0.8/tuning/
├── advanced_retriever.py  [실습] Parent/SelfQuery/Compression
├── query_rewrite.py       [실습] HyDE, Multi-Query, 약어 확장
└── evidence_pipeline.py   [실습] 이미지+DB 근거 동시 제공
```
**실습 요약**: 실습 3개

---

### CH10: "PDF 이미지까지 잡아라" — 고급 문서 처리와 평가 (v0.9)

**핵심 개념**: Vision LLM, OCR, 이미지 인덱싱, RAG 평가
**기술**: LLaVA/EasyOCR, 하이브리드 이미지 처리, Precision@k, Hallucination Rate
**버전 성과**: CLI에서 이미지 캡션 + OCR 결과 + 평가 리포트
**예상 분량**: ~10p

**코드 실습 분류**:
```
v0.9/tuning/
├── document_parser.py   [실습] 라이브러리 비교 + vLLM 멀티모달
├── document_capture.py  [실습] OCR 캡처 + 자동 인제스천
└── eval_framework.py    [실습] Precision@k, Recall@k, Hallucination Rate
```
**실습 요약**: 실습 3개

---

## 갭 분석 결과

> 도메인 표준(RAG 입문서) vs 현재 목차 비교. 의도 필터(seed.md) 적용 후.

| 누락 주제 | 우선순위 | 반영 방안 | 저자 결정 |
|----------|---------|----------|----------|
| **임베딩 모델 선택 기준** (ko-sroberta vs OpenAI) | [필수] | CH04에 "임베딩 모델 왜 이걸 썼나?" 섹션 추가 | ✅ 반영 |
| **프롬프트 인젝션 방어** (사내 AI 보안) | [권장] | 사내 직원 전용 → 실질 위협 낮음. RAG 핵심에서 이탈. | ⬛ 생략 |
| **재인덱싱 전략** (새 문서 추가 시) | [권장] | CH03 문서 수집 전략에 운영 관점 추가 | ✅ 반영 |
| **LangChain vs 직접 구현 비교** | [선택] | 더 알아보기 or 생략 (의도 = 이해 중심) | ⬛ 생략 |
| **배포 전략** (Docker/Nginx) | [선택] | 의도 밖 범위 (seed.md) — 생략 | ⬛ 생략 |

---

## 여정 맵

```
CH01(전환점①) → CH02(보통) → CH03(쉬어가기) → CH04(보통) → CH05(보통)
→ CH06(전환점②) → CH07(쉬어가기) → CH08(높음) → CH09(높음) → CH10(전환점③+마무리)

난이도: 낮음 ─ 보통 ─ 높음
CH01[■■□] CH02[■■□] CH03[■□□] CH04[■■□] CH05[■■□]
CH06[■■■] CH07[■□□] CH08[■■■] CH09[■■■] CH10[■■■]
```

---

## 분량 배분

```
Part 0 (도입부): 프롤로그 4p + 부록(환경설정) 4p = 8p
─────────────────────────────────────────────────────
Part 1: CH01(12p)                              = 12p
Part 2: CH02(10p) + CH03(9p)                  = 19p
Part 3: CH04(11p) + CH05(10p)                 = 21p
Part 4: CH06(10p) + CH07(8p)                  = 18p
Part 5: CH08(12p) + CH09(10p) + CH10(10p)     = 32p
─────────────────────────────────────────────────────
총계: 8 + 12 + 19 + 21 + 18 + 32 = 110p
```

> 권장 100p 초과 8p. 허용 범위. 갭 분석 반영 시 약간 추가될 수 있음.

---

## 기술 매핑

| 챕터 | 버전 | 핵심 기술 | 완성 코드 대비 차이 |
|------|------|----------|--------------|
| CH01 | v0.0 | Ollama, LangChain, ChromaDB | 완성 코드와 동일 (교육용 단순화) |
| CH02 | v0.1 | FastAPI, psycopg2, Pydantic | views.py/templates 제외 |
| CH03 | v0.2 | (개념) | 코드 없음 |
| CH04 | v0.3 | pypdf, ko-sroberta, ChromaDB | 완성 코드와 동일 |
| CH05 | v0.4 | LCEL, WindowMemory | templates/session 제외 |
| CH06 | v0.5 | QueryRouter, @tool, AgentExecutor | templates 제외 |
| CH07 | v0.6 | ResponseCache, TokenTracker | Langfuse 상세 제외 |
| CH08 | v0.7 | Cross-Encoder, BM25, rank-bm25 | 완성 코드와 동일 |
| CH09 | v0.8 | Parent Retriever, HyDE, Evidence | 완성 코드와 동일 |
| CH10 | v0.9 | LLaVA, EasyOCR, eval metrics | RAGAS 제외 |
