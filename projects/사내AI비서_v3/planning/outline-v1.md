# 뼈대 — 사내AI비서_v3

## 목차

---

### CH01: 엉뚱한 대답

#### 구성

LLM에게 사내 규정을 물었더니 그럴듯한 거짓말을 돌려준다. 팀장의 "AI 비서 만들어봐"라는 지시와 주인공의 막연한 기대로 시작하여, 환각을 직접 목격하는 장면을 그린다.

사전 준비 섹션에서 Ollama 설치 + 모델(deepseek-r1:8b, llama3.1:8b) pull을 일괄 안내한다. 이 챕터의 코드는 LangChain 0.1 스타일(RetrievalQA)로 작성되어 있으며, CH05부터 LCEL 방식으로 전환되는 점을 명시한다.

기술 파트에서는 네 단계를 밟는다. (1) LLM 단독 질문으로 환각을 체험한다. (2) 프롬프트에 규정 텍스트를 직접 삽입(Context Injection)하여 정답이 나오는 것을 확인한다. (3) 더미 3건으로 최소 RAG 파이프라인을 만들고, 청킹 유무를 비교하여 "왜 잘라야 하는지" 체감한다. (4) 추론이 필요한 복잡한 질문을 던져 RAG의 현재 한계를 확인한다.

마무리에서 "이걸 여러 사람이 쓰려면 서버가 필요하다"는 다음 챕터의 동기를 심는다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| step1_fail.py | [실습] | 15줄. LLM 단독 호출 -> 환각 체험 |
| step2_context.py | [실습] | 28줄. 프롬프트에 context_data 삽입 |
| step3_rag.py | [실습] | 67줄. RetrievalQA + ChromaDB 최소 RAG |
| step3_rag_no_chunking.py | [설명] | step3_rag.py와 구조 유사. 통짜 Document 1건의 비효율을 보여주는 핵심 차이만 발췌 |
| step4_rag.py | [설명] | step3_rag.py와 구조 동일. 질문만 바뀜(추론 질문). 질문 변경점과 결과 해석만 발췌 |
| requirements.txt | [참고] | 의존성 목록 표로 요약 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| step1 실행 후 | 터미널 캡처 | step1_fail.py 실행 결과 — LLM이 지어낸 법률 조항 | 단독 |
| step2 실행 후 | 터미널 캡처 | step2_context.py 실행 결과 — 올바른 답변 | 단독 |
| step3 비교 | 터미널 캡처 2장 | step3_rag.py vs step3_rag_no_chunking.py 결과 비교 | 2열 배치 |
| RAG 개념도 | 다이어그램 (Mermaid) | 질문 -> Retriever -> Context -> LLM -> 답변 흐름도 | 단독 |

---

### CH02: 기반을 닦다

#### 구성

"연차가 며칠 남았어?"처럼 숫자 데이터를 물어보면 문서 검색으로는 답할 수 없다는 문제를 드러낸다. 정형 데이터를 다루는 시스템이 먼저 있어야 나중에 AI 비서가 이 데이터에 접근할 수 있다는 동기를 전달한다.

기술 파트에서는 FastAPI + PostgreSQL CRUD 시스템을 만든다. (1) Docker Compose로 PostgreSQL을 띄운다. (2) DDL + 시드 데이터로 테이블을 초기화한다. (3) dataclass로 도메인 모델을 정의한다. (4) psycopg2 컨텍스트 매니저로 DB 연결을 관리한다. (5) CRUD 핵심 함수를 작성한다. (6) FastAPI 라우터로 REST API를 노출한다. (7) Swagger UI에서 테스트한다.

CRUD 함수 18개를 전부 나열하지 않는다. 직원 CRUD의 create/read 흐름을 완성하면, 연차와 매출은 같은 패턴이므로 "전체 코드는 code/ex02/ 참조"로 안내한다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| database.py | [실습] | 99줄. get_connection 컨텍스트 매니저 전체 |
| models.py | [실습] | 88줄. 4개 dataclass 전체 |
| crud.py | [설명] | 589줄. create_employee + get_all_employees 발췌 (약 50줄). 나머지는 같은 패턴 |
| api.py | [설명] | 393줄. api_get_employees + api_create_employee 발췌 (약 40줄). 나머지 16개 엔드포인트는 표로 요약 |
| main.py | [설명] | 75줄. FastAPI 앱 생성 + 라우터 등록 흐름 발췌 |
| schemas.py | [참고] | Pydantic 스키마 목록을 메서드 표로 요약 |
| views.py | [참고] | Admin UI 라우터 존재만 언급 |
| data/schema.sql | [설명] | DDL + 시드 데이터 핵심 발췌 |
| docker-compose.yml | [참고] | 실행 명령만 안내 |
| run.py | [참고] | uvicorn 실행 한 줄만 언급 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 챕터 도입부 | 다이어그램 (Mermaid) | FastAPI + PostgreSQL 아키텍처 (라우터 -> CRUD -> DB) | 단독 |
| Swagger 테스트 | 브라우저 캡처 | Swagger UI에서 직원 조회 API 실행 화면 | 단독 |
| 서버 기동 | 터미널 캡처 | uvicorn 서버 시작 + /docs 접속 로그 | 단독 |

---

### CH03: 문서를 모으다

#### 구성

코드가 없는 개념 챕터. "쓰레기를 넣으면 쓰레기가 나온다"는 원칙을 전달한다.

(1) 사내 문서가 PDF/DOCX/XLSX로 뒤섞여 있고, 파일명도 제각각인 현실을 보여준다. (2) 문서 종류별 수집 전략(HR, Finance, Ops, Security)을 설계한다. (3) 파일명 규칙, 메타데이터 표준, 섹션 헤더 규칙을 정한다. (4) data/docs/ 디렉토리 구조를 정리한다.

이야기 전환의 쉼터 역할을 하면서, 다음 챕터에서 파싱/청킹을 할 때 "왜 이렇게 정리해야 하는지" 맥락을 잡아준다.

#### 코드 배치

코드 없음.

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 문서 수집 전략 | 개념도 (Gemini) | 문서 수집 -> 분류 -> 라벨링 -> 디렉토리 정리 흐름 | 단독 |
| 디렉토리 구조 | 다이어그램 (Mermaid) | data/docs/ 하위 4개 부서 폴더 + 파일 유형 트리 | 단독 |

---

### CH04: 기계가 읽는 법

#### 구성

PDF/DOCX/XLSX를 그대로 LLM에 넣을 수 없다는 문제를 환기한다. 텍스트를 추출하고, 적절한 크기로 자르고, 벡터로 변환해서 검색 가능하게 만드는 3단계 파이프라인을 만든다.

기술 파트. (1) 형식별 텍스트 추출 — pypdf, python-docx, openpyxl. (2) Fixed-size 청킹(500자, 100자 오버랩) + 메타데이터 부착. (3) ko-sroberta-multitask 임베딩 + ChromaDB 저장. (4) CLI 검색(cli_search.py)으로 품질 검증.

파이프라인 오케스트레이터(main.py)는 Step1(파싱) -> Step2(임베딩+저장)의 흐름을 보여준다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| extractor.py | [설명] | 327줄. extract_text 분기 + extract_from_pdf 핵심 흐름 발췌. 나머지 형식은 같은 패턴 |
| chunker.py | [실습] | 264줄. split_text_into_chunks + build_text_chunk + chunk_extract_result 전체 |
| store.py | [실습] | 310줄. load_embedding_model + store_chunks_to_chroma + search_chroma 전체 |
| main.py | [설명] | 306줄. step1_python_parsing + step2_embed_and_store 흐름 발췌 |
| cli_search.py | [설명] | 316줄. run_single_query 핵심 흐름 발췌 |
| extract_pdf.py 등 | [참고] | extractor.py 내부에서 호출하는 형식별 함수. 별도 설명 불필요 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 파이프라인 개요 | 다이어그램 (Mermaid) | 원본 문서 -> 텍스트 추출 -> 청킹 -> 임베딩 -> ChromaDB 흐름 | 단독 |
| 청킹 개념 | 개념도 (Gemini) 2장 | (1) 문서 텍스트를 고정 크기로 자르는 과정 (2) 오버랩이 문맥 손실을 방지하는 원리 | 2열 배치 |
| CLI 검색 결과 | 터미널 캡처 | cli_search.py로 "연차 규정" 검색 — 유사도 점수 + 출처 표시 | 단독 |
| 파이프라인 실행 | 터미널 캡처 | main.py 실행 로그 — 문서 N개 추출, 청크 N개 생성, ChromaDB 저장 완료 | 단독 |

---

### CH05: 질문에 답하다

#### 구성

벡터 검색은 관련 청크를 꺼내줄 뿐, 사용자가 원하는 "답변"이 아니라는 문제를 제기한다. 검색 결과를 LLM에게 넘겨 자연어 답변을 생성하는 RAG 체인을 조립한다.

기술 파트. (1) LCEL 파이프 연산자(|)로 Retriever | Prompt | LLM | Parser 체인을 조립한다. (2) 출처 강제 프롬프트로 근거 없는 답변을 차단한다. (3) WindowMemory(k=5)로 멀티턴 대화를 지원한다. (4) LLM 팩토리로 Ollama/OpenAI를 전환한다. (5) FastAPI 채팅 API를 만들고 웹 UI에서 테스트한다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| rag_chain.py | [실습] | 85줄. build_rag_chain LCEL 파이프 전체 |
| llm_factory.py | [실습] | LLM 분기 팩토리 전체 |
| conversation.py | [실습] | 30줄. WindowMemory 전체 |
| vectorstore.py | [설명] | 168줄. build_retriever 흐름 발췌 |
| response_parser.py | [설명] | parse_answer_text + build_response 핵심 발췌 |
| session_manager.py | [참고] | ConversationManager TTL 관리. 메서드 표 요약 |
| chat_api.py | [설명] | chat_endpoint 핵심 흐름 발췌 |
| session.py | [참고] | 세션 ID 생성 유틸. 메서드 표 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| LCEL 체인 구조 | 다이어그램 (Mermaid) | question -> Retriever -> context + prompt -> LLM -> Parser -> 답변 | 단독 |
| 웹 채팅 UI | 브라우저 캡처 | 채팅 화면에서 질문-답변-출처 표시 | 단독 |
| 멀티턴 대화 | 터미널 캡처 | 2턴 연속 대화 — 맥락 유지 확인 | 단독 |

---

### CH06: 하나로 합치다

#### 구성

CH02의 DB 조회와 CH05의 문서 검색이 따로 논다는 문제를 보여준다. "홍길동 연차 몇 일이야?"와 "출장비 정산 절차가 뭐야?"를 같은 창에서 물어보고 싶다는 욕구에서 통합 에이전트를 만든다.

기술 파트. (1) QueryRouter — 규칙 기반 키워드 매칭 -> DB 스키마 컬럼명 매칭 -> LLM 판단의 3단계 분류. (2) @tool 데코레이터로 4개 도구 정의. (3) create_tool_calling_agent + AgentExecutor로 ReAct 에이전트 구성. (4) IntegratedAgent.run() 실행 흐름.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| router.py | [실습] | 148줄. QueryRouter 전체 (3단계 classify_query) |
| mcp_tools.py | [실습] | 145줄. @tool 4종 전체 |
| agent.py | [실습] | 116줄. IntegratedAgent 전체 |
| agent_helpers.py | [설명] | parse_agent_result, clean_think_tags 핵심 발췌 |
| db_helper.py | [참고] | PostgreSQL + ChromaDB 연결 헬퍼. 메서드 표 |
| chat_api.py | [참고] | IntegratedAgent 호출로 바뀐 차이점만 언급 |
| tests/test_scenarios.py | [참고] | 18개 시나리오 테스트. 테스트 항목 표로 요약 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 에이전트 아키텍처 | 다이어그램 (Mermaid) | 질문 -> QueryRouter -> [정형: Tool] / [비정형: RAG] / [복합: Agent] -> 답변 | 단독 |
| 3단계 라우팅 | 개념도 (Gemini) 2장 | (1) 규칙 -> 스키마 -> LLM 판단 흐름 (2) ReAct Agent의 Tool Calling 루프 | 2열 배치 |
| 통합 테스트 | 터미널 캡처 | 정형 질문 + 비정형 질문 + 복합 질문 3건의 실행 결과 | 단독 |

---

### CH07: 믿고 쓸 수 있게

#### 구성

같은 질문에 매번 수 초씩 대기하고, LLM이 실패하면 에러가 그대로 노출되고, 토큰 비용도 추적이 안 되는 문제를 드러낸다. "다음 달 전사 시연"이라는 마감 압박 속에서 운영 안정화를 진행한다.

기술 파트. (1) ResponseCache(TTL 인메모리) — 동일 질문 캐시. (2) 재시도 로직(3회, 2초 간격) — 일시적 장애 흡수. (3) TokenTracker — 모델별 비용 추적. (4) JsonFormatter — 구조화 로깅. (5) ConnectHRAgent 클래스로 전체 통합. (6) @tool을 개별 파일(tools/)로 모듈화.

EmbeddingCache와 Langfuse 연동은 존재만 언급한다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| agent_config.py | [실습] | 215줄. ConnectHRAgent 전체 |
| cache.py | [실습] | 168줄. ResponseCache 전체. EmbeddingCache는 존재만 언급 |
| monitoring.py | [설명] | 218줄. JsonFormatter + TokenTracker 발췌. LangfuseMonitor는 존재만 언급 |
| router.py | [참고] | ex06과 동일. 변경 없음 |
| tools/*.py | [설명] | 4개 도구 파일 분리. leave_balance.py 하나만 발췌, 나머지는 같은 패턴 |
| agent_helpers.py | [참고] | build_rag_chain + classify_route 메서드 표 |
| llm_factory.py | [참고] | ex05와 동일 패턴 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 운영 안정화 구조 | 다이어그램 (Mermaid) | ConnectHRAgent 내부 — 캐시 -> 라우터 -> 재시도 -> Agent/RAG -> 모니터링 | 단독 |
| 캐시 동작 | 개념도 (Gemini) 2장 | (1) 캐시 미스 -> LLM 호출 -> 캐시 저장 흐름 (2) 캐시 히트 -> 즉시 반환 흐름 | 2열 배치 |
| 캐시 통계 | 터미널 캡처 | 캐시 적중률, 토큰 사용량 통계 출력 | 단독 |

---

### CH08: 엉뚱한 문서를 가져온다

#### 구성

전사 배포 후 "보안 정책을 물었는데 인사규정이 나왔다"는 피드백이 올라온다. 검색 품질을 개선하기 위한 세 가지 실험을 진행한다.

이 챕터부터 실험 모듈은 `code/ex08/tuning/step1_chunk_experiment/` 등 독립 디렉토리에서 실행한다. 각 실험의 진입 명령(`python -m step1_chunk_experiment.main` 등)을 먼저 제시한다.

기술 파트. (1) 청킹 전략 실험 — Fixed vs Recursive vs Semantic, 크기/오버랩 조합 비교. (2) Cross-Encoder 리랭킹 — 검색 결과를 다시 정렬하여 관련성을 높인다. (3) 하이브리드 검색 — BM25(키워드) + Vector(의미) 앙상블.

각 실험은 "문제 -> 실험 -> 결과 해석" 구조를 따른다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| step1_chunk_experiment/strategies.py | [실습] | 114줄. 3가지 청킹 전략 전체 |
| step1_chunk_experiment/experiments.py | [설명] | 5가지 실험 실행기 핵심 흐름 발췌 |
| step1_chunk_experiment/retriever.py | [참고] | InMemoryRetriever. 메서드 표 |
| step1_chunk_experiment/data.py | [참고] | 샘플 문서 + 테스트 쿼리 상수 |
| step1_chunk_experiment/display.py | [참고] | Rich 출력 유틸 |
| step1_chunk_experiment/analysis.py | [참고] | 청크 통계 분석 |
| step2_reranker/reranker.py | [실습] | 98줄. CrossEncoderReranker + SimpleReranker 전체 |
| step2_reranker/experiments.py | [설명] | 검색 품질 비교 핵심 흐름 발췌 |
| step2_reranker/data.py | [참고] | 테스트 데이터 상수 |
| step3_hybrid_search/retrievers.py | [실습] | 196줄. BM25 + Vector + Ensemble 전체 |
| step3_hybrid_search/experiments.py | [설명] | 비교 핵심 흐름 발췌 |
| step3_hybrid_search/data.py | [참고] | 테스트 데이터 상수 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 청킹 실험 결과 | 터미널 캡처 | 5가지 청킹 조합의 비교 테이블 | 단독 |
| 시맨틱 청킹 원리 | 개념도 (Gemini) | 의미 단위로 텍스트를 분할하는 과정 | 단독 |
| 리랭커 결과 | 터미널 캡처 | Cross-Encoder 리랭킹 전후 순위 변화 | 단독 |
| 하이브리드 검색 | 개념도 (Gemini) 2장 | (1) BM25와 Vector 검색의 차이 (2) 앙상블 결합(alpha 가중치) 원리 | 2열 배치 |
| 하이브리드 실험 결과 | 터미널 캡처 | BM25 vs Vector vs Ensemble 비교 테이블 | 단독 |

---

### CH09: 검색의 한계를 넘다

#### 구성

기본 Retriever로는 풀 수 없는 세 가지 문제를 제시한다. (1) 긴 문서에서 맥락을 잃는다. (2) 메타데이터 필터가 필요하다. (3) "WFH"같은 약어를 이해하지 못한다. 각 문제에 맞는 기법을 도입한다.

실험 모듈은 `code/ex09/tuning/step1_advanced_retriever/`, `step2_query_rewrite/` 디렉토리에서 독립 실행한다.

기술 파트. (1) 고급 Retriever 3종 — ParentDocumentRetriever, SelfQueryRetriever, ContextualCompressionRetriever. (2) Query Rewrite 3종 — 약어/동의어 확장, HyDE, Multi-Query.

"백과사전식 나열" 위험을 피하기 위해, 각 기법이 "어떤 유형의 질문"을 해결하는지 먼저 제시한다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| step1_advanced_retriever/retrievers.py | [실습] | 220줄. 3종 Retriever 전체 |
| step1_advanced_retriever/experiments.py | [설명] | 3가지 비교 핵심 흐름 발췌 |
| step1_advanced_retriever/data.py | [참고] | 부모/자식 문서 테스트 데이터 |
| step2_query_rewrite/rewriters.py | [실습] | 272줄. 3종 Query Rewrite 전체 |
| step2_query_rewrite/experiments.py | [설명] | 변환 전후 비교 핵심 흐름 발췌 |
| step2_query_rewrite/data.py | [참고] | ABBREVIATION_MAP, SYNONYM_MAP, HYDE_TEMPLATES |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 고급 Retriever 비교 | 개념도 (Gemini) 2장 | (1) ParentDoc — 작은 청크로 검색, 큰 문서 반환 (2) SelfQuery — 쿼리에서 필터 추출 + 필터링 검색 | 2열 배치 |
| ContextualCompression | 다이어그램 (Mermaid) | 검색 -> 전체 문서 -> 압축(관련 문장만) -> 반환 | 단독 |
| HyDE 원리 | 개념도 (Gemini) | 질문 -> 가상 답변 생성 -> 가상 답변으로 검색 -> 실제 문서 반환 | 단독 |
| 고급 Retriever 실험 결과 | 터미널 캡처 | 3종 Retriever 비교 테이블 | 단독 |
| Query Rewrite 실험 결과 | 터미널 캡처 | 약어확장/HyDE/Multi-Query 전후 비교 | 단독 |

---

### CH10: 끝까지 의심하다

#### 구성

"검색 품질의 천장은 결국 파싱 품질"이라는 근본적 질문을 던진다. 이미지 기반 PDF에서 텍스트가 누락되고, 표가 깨지는 문제를 확인한다.

실험 모듈은 `code/ex10/tuning/step1_document_parser/`, `step2_hybrid_parser/`, `step3_eval_framework/` 디렉토리에서 독립 실행한다.

기술 파트. (1) 문서 파싱 비교 — EasyOCR vs Vision LLM(qwen2.5vl:7b). (2) 하이브리드 파싱 — OCR 결과가 짧으면 Vision LLM으로 보완하는 폴백 전략. (3) 평가 프레임워크 — Precision@K, Recall@K, MRR, Hallucination Rate로 RAG 전체 품질을 정량 측정.

마무리에서 "파싱 -> 검색 -> 답변 -> 평가"의 순환 개선 체계가 완성되었음을 보여준다.

#### 코드 배치

| 파일 | 태그 | 비고 |
|------|------|------|
| step1_document_parser/parser.py | [실습] | 149줄. parse_pdf_ocr + parse_pdf_vllm 전체 |
| step1_document_parser/display.py | [참고] | Rich 출력 유틸 |
| step2_hybrid_parser/hybrid_parser.py | [설명] | OCR->Vision 폴백 + 텍스트레이어 우선 핵심 흐름 발췌 |
| step3_eval_framework/metrics.py | [실습] | 74줄. Precision@K + Recall@K + MRR + Hallucination Rate 전체 |
| step3_eval_framework/evaluator.py | [실습] | 267줄. run_evaluation 전체 |
| step3_eval_framework/display.py | [참고] | Rich 출력 유틸 |
| data/test_questions.json | [참고] | 평가용 질문 세트. 구조만 설명 |

#### 이미지 배치

| 위치 | 종류 | 설명 | 비고 |
|------|------|------|------|
| 파싱 비교 | 개념도 (Gemini) 2장 | (1) OCR 파이프라인 (PDF -> 이미지 -> EasyOCR -> 텍스트) (2) Vision LLM 파이프라인 (PDF -> 이미지 -> qwen2.5vl -> Markdown) | 2열 배치 |
| 파싱 결과 비교 | 터미널 캡처 | OCR vs Vision LLM — 같은 페이지의 추출 텍스트 비교 | 단독 |
| 평가 지표 개념 | 개념도 (Gemini) | Precision/Recall/MRR/Hallucination Rate 4개 지표의 의미 | 단독 |
| 평가 실행 결과 | 터미널 캡처 | 카테고리별 Precision, Recall, MRR, 환각률 테이블 | 단독 |
| 순환 개선 체계 | 다이어그램 (Mermaid) | 파싱 -> 청킹 -> 검색 -> 답변 -> 평가 -> 파싱 개선 순환 루프 | 단독 |

---

## 난이도 곡선

| 챕터 | 난이도 | 핵심 개념 |
|------|--------|----------|
| CH01 | 1 | LLM 호출, RAG 개념 |
| CH02 | 2 | FastAPI, PostgreSQL CRUD, dataclass |
| CH03 | 1 | 문서 수집 전략 (코드 없음) |
| CH04 | 3 | 파싱, 청킹, 임베딩, ChromaDB |
| CH05 | 3 | LCEL, Retriever, 대화 메모리 |
| CH06 | 4 | Tool Calling, ReAct Agent, QueryRouter |
| CH07 | 3 | 캐시, 재시도, 모니터링 |
| CH08 | 3 | 청킹 전략, Reranker, 하이브리드 검색 |
| CH09 | 4 | ParentDoc, SelfQuery, HyDE, Multi-Query |
| CH10 | 4 | OCR, Vision LLM, 평가 프레임워크 |

```
난이도
  5 |
  4 |                         *              *    *
  3 |              *    *              *    *
  2 |        *
  1 |  *              *
  0 +----+----+----+----+----+----+----+----+----+----
     CH01 CH02 CH03 CH04 CH05 CH06 CH07 CH08 CH09 CH10
```

곡선 특징.
- CH01/CH03에서 난이도가 낮아지는 "쉼터"가 두 번 존재한다.
- CH04~CH06에서 점진적으로 상승하여 CH06(Agent)에서 첫 번째 정점을 찍는다.
- CH07에서 한 단계 낮아진 뒤, CH09~CH10에서 두 번째 정점을 찍는다.
- 급격한 난이도 점프 없이 "계단식 상승 + 주기적 완화" 패턴을 유지한다.

---

## 갭 분석

### [필수] 반드시 다뤄야 할 개념

| 항목 | 현재 상태 | 챕터 |
|------|----------|------|
| 환각(Hallucination) 개념과 원인 | step1_fail.py로 체험 | CH01 |
| RAG 파이프라인 기본 구조 | step3_rag.py로 구현 | CH01 |
| 임베딩(Embedding) 개념과 코사인 유사도 | store.py에서 사용 | CH04 |
| 청킹(Chunking) 전략과 오버랩 | chunker.py에서 구현 | CH04 |
| 프롬프트 엔지니어링 (출처 강제) | rag_chain.py RAG_SYSTEM_PROMPT | CH05 |
| LCEL 파이프 연산자 | rag_chain.py에서 구현 | CH05 |
| Tool Calling / Agent 개념 | agent.py에서 구현 | CH06 |
| 검색 품질 평가 지표 (Precision, Recall, MRR) | metrics.py에서 구현 | CH10 |

### [권장] 다루면 좋은 개념

| 항목 | 현재 상태 | 챕터 | 권장 이유 |
|------|----------|------|----------|
| 벡터 데이터베이스 선택 기준 | ChromaDB만 사용 | CH04 | 다른 VectorDB와의 차이를 1~2문단으로 언급 |
| 토큰 제한과 컨텍스트 윈도우 | step2_context.py에서 암시 | CH01 | "왜 문서 전체를 프롬프트에 넣을 수 없는지" 명시 |
| 프롬프트 템플릿 버전 관리 | SYSTEM_PROMPT 하드코딩 | CH05/CH06 | 프롬프트를 별도 파일로 분리하는 패턴 짧게 언급 |
| Cross-Encoder vs Bi-Encoder 차이 | reranker.py에서 사용 | CH08 | 두 아키텍처 원리 차이를 개념도로 설명 |
| RAG 평가 자동화 (CI 연동) | evaluator.py는 수동 실행 | CH10 | 자동화 방향성을 마무리에서 짧게 언급 |

### [선택] 있으면 좋지만 없어도 됨

| 항목 | 비고 |
|------|------|
| GraphRAG / Knowledge Graph | 에필로그에서 "다음 단계"로 언급 가능 |
| 스트리밍 응답 (SSE) | 부록에서 짧게 다룰 수 있음 |
| 멀티모달 RAG (이미지 포함 검색) | 에필로그 소재로 적합 |
| Fine-tuning / LoRA | 이 책은 RAG 중심. 별도 주제 |

### [경고] 다루지 않으면 독자 혼란 가능

| 항목 | 위험 | 해결 방안 | 챕터 |
|------|------|----------|------|
| LangChain 버전 차이 (0.1 vs 0.3) | ex01은 langchain-classic, ex05부터 LCEL. "왜 문법이 바뀌지?" 혼란 | CH01에서 레거시 방식임을 명시, CH05에서 전환 동기 설명 | CH01, CH05 |
| Ollama 설치 및 모델 다운로드 | 여러 모델 필요. 누락 시 실습 불가 | CH01 사전 준비에서 설치 + 모델 pull 일괄 안내 | CH01 |
| Docker Compose 필수 여부 | CH02부터 PostgreSQL 필요 | CH02 초반에 3줄로 안내. 로컬 대안도 언급 | CH02 |
| ex08~10 실험 모듈의 독립성 | "어디서 실행하는 거지?" 혼란 | 각 챕터 시작에서 실행 디렉토리 + 명령 먼저 제시 | CH08~10 |
| `<think>` 태그 제거 | deepseek-r1 특성. 미처리 시 추론 과정 노출 | CH05에서 response_parser.py 설명 시 짧게 언급 | CH05 |

---

## 예상 분량

| 챕터 | 예상 페이지 | 근거 |
|------|-----------|------|
| CH01: 엉뚱한 대답 | 8~10 | 스크립트 5개지만 짧음. 환각 체험 + RAG 개념 도입 |
| CH02: 기반을 닦다 | 12~14 | CRUD 전체. 발췌해도 4파일 |
| CH03: 문서를 모으다 | 5~6 | 코드 없음. 전략 + 디렉토리 설계 |
| CH04: 기계가 읽는 법 | 14~16 | extractor + chunker + store 3개 [실습] |
| CH05: 질문에 답하다 | 10~12 | LCEL 체인 + 대화 메모리 + API |
| CH06: 하나로 합치다 | 12~14 | Router + Tool + Agent 3개 [실습] |
| CH07: 믿고 쓸 수 있게 | 10~12 | 캐시 + 모니터링 패턴 |
| CH08: 엉뚱한 문서를 가져온다 | 12~14 | 3가지 실험 x (문제+코드+결과) |
| CH09: 검색의 한계를 넘다 | 12~14 | 6가지 기법. 나열 위험 주의 |
| CH10: 끝까지 의심하다 | 12~14 | 파싱 비교 + 평가 프레임워크 |
| **합계** | **107~126** | 프롤로그/에필로그/부록 제외 본문 기준 |
