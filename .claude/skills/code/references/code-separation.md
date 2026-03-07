# 코드 분리 패턴: 실습 / 설명 / 참고 파일 분류

> 출처: CH05~CH06 리팩토링 사례에서 추출한 패턴
> 적용 시점: STEP 4(뼈대) 코드 태깅 후, STEP 5(챕터 집필) 기술 파트 작성 시

---

## 원칙

1. 모든 코드 파일은 **[실습] / [설명] / [참고]** 중 하나로 분류한다.
2. 한 파일에 [실습]+[참고] 코드가 혼재하면 **파일 수준에서 분리**한다.
3. [실습] 파일에는 해당 챕터의 **핵심 교육 개념만** 남긴다.
4. [참고] 파일에는 인프라/유틸리티/보일러플레이트를 옮긴다.
5. [실습] 파일은 [참고] 파일에서 `import`한다.
6. 챕터 마크다운에서 각 분류별 작성 방식이 다르다 (아래 참조).
7. **실행 가능성 보장**: [참고]/[설명] 파일은 GitHub 완성본(`exNN/`)에 포함된다. 독자가 `git clone` 후 [실습] 파일만 직접 작성하면 **바로 실행 가능**해야 한다. 의존 파일이 없어서 서버가 안 뜨는 상황은 만들지 않는다.
8. **실습 간 빌드업**: 각 실습은 이전 실습 대비 **무엇이 달라졌는지** 비교할 수 있도록 구성한다. 독자가 핵심 코드만 작성하고, 실행 결과를 직접 비교하며 차이를 체감하도록 유도한다.

---

## 3단계 분류 기준

### [실습] — 독자가 직접 타이핑하는 핵심 코드
- 이번 챕터에서 **새로 배우는 개념**을 구현한 코드
- 독자가 "왜 이렇게 하는지" 이해해야 하는 코드
- **챕터에서**: "아래 코드를 `파일명`에 작성합니다"로 시작 → **전체 코드** 표시 → 핵심 설명
- GitHub에는 완성본(`exNN/`)만 제공. 독자는 책을 보고 직접 작성
- 예: LCEL 파이프라인 조립, @tool 데코레이터, ReAct 에이전트 클래스, WindowMemory

### [설명] — 독자가 읽고 이해하되 직접 치지 않는 코드
- 동작 흐름을 이해해야 하지만, 독자가 타이핑할 필요 없는 코드
- API 엔드포인트, 응답 파서, 미들웨어 등 **연결 계층**
- **챕터에서**: 코드 블록으로 보여주되, 핵심 흐름 위주로 설명 (전체 코드 X)
- 예: `chat_api.py` (POST /api/chat 엔드포인트), `response_parser.py` (답변 정제)

### [참고] — 독자가 보지 않아도 되는 인프라 코드
- 이전 챕터에서 **이미 배운 패턴의 반복** (LLM 생성, DB 연결 등)
- 글루 코드 (세션 관리, 싱글턴, TTL 정리, 문서 파싱 등)
- **챕터에서**: 코드 블록 없음. **메서드 표**로만 요약
- 예: `build_llm()`, `run_query()`, `parse_and_chunk_docs()`, `ConversationManager`

### 분류 요약

| 분류 | 독자 행동 | 챕터 표현 | 파일 분리 |
|------|----------|----------|----------|
| [실습] | 직접 타이핑 | 코드 블록 + 상세 설명 | 핵심만 남김 |
| [설명] | 읽고 이해 | 코드 블록 + 흐름 설명 | 분리 불필요 (파일 그대로) |
| [참고] | 안 봐도 됨 | 메서드 표로 요약 | [실습]에서 분리하여 별도 파일 |

---

## 파일 분리 작업 순서

1. 원본 파일의 모든 함수/클래스를 나열한다.
2. 각 항목을 "이번 챕터 핵심 개념?" 기준으로 실습/참고 분류한다.
3. [참고] 항목을 새 파일로 분리한다 (파일명은 역할 기반: `llm_factory.py`, `db_helper.py` 등).
4. [실습] 파일에서 분리된 함수를 `import`한다.
5. `python -c "from src.xxx import yyy"` 로 import 테스트한다.

---

## 챕터 마크다운 작성 규칙

### `# 실행` — 스크립트/서버 실행 명령어에 bash 주석으로 표기

독자가 실제로 실행하는 명령어(스크립트, 서버, curl 등)의 bash 블록 첫 줄에 `# 실행` 주석을 넣는다.
환경 설정(`cd`, `pip install`, `docker compose up`)에는 붙이지 않는다.

```markdown
```bash
# 실행
python step1_fail.py
```
```

- 스크립트 실행(`python script.py`) → 붙임
- 서버 실행(`uvicorn`, `python -m app.main`) → 붙임
- curl/API 호출 → 붙임
- 환경 설정(`cd`, `pip install`, `docker compose up`, `cp .env.example`) → **안 붙임**
- 출력 결과 블록 → **안 붙임**

### [실습] 파일 → 파일 생성 안내 + 전체 코드 + 설명

독자가 직접 타이핑하는 코드. 아래 형식을 따른다:

```markdown
### 실습 N — 파일명.py: 제목

아래 코드를 `exNN/경로/파일명.py`에 작성합니다.

(전체 코드 블록)

(핵심 설명 — 줄별 상세 또는 단계별 흐름)

(실행 명령)

(실행 결과 스크린샷 또는 출력)
```

- **"아래 코드를 `exNN/경로/파일명.py`에 작성합니다"**로 시작 — 디렉토리 경로 포함 (예: `ex05/src/rag_chain.py`, `ex06/src/mcp_tools.py`)
- **전체 코드** 표시 — 독자가 GitHub 없이도 따라칠 수 있어야 함
- GitHub에는 완성본(`exNN/`)만 제공. 예제 파일은 별도 제공하지 않음

### [설명] 파일 → 코드 블록 + 흐름 설명

핵심 흐름(처리 순서)을 코드 블록으로 보여주되, 전체 코드가 아닌 **주요 흐름만** 발췌.
독자가 "이렇게 연결되는구나" 수준으로 이해하면 충분.

```markdown
### [설명] chat_api.py — POST /api/chat

이 라우터가 사서에게 질문을 전달하는 창구입니다.

(핵심 흐름만 발췌한 코드 블록)

전체 흐름이 한 눈에 보입니다. 세션 확인 → 히스토리 조회 → 체인 실행 → 응답 정제.
```

### [참고] 파일 → 메서드 표로 요약 (코드 블록 없음)

```markdown
`rag_chain.py`에서 사용하는 인프라 함수는 별도 모듈로 분리되어 있습니다:

| 파일 | 함수 | 역할 |
|------|------|------|
| `llm_factory.py` | `build_llm()` | Ollama/OpenAI LLM 인스턴스 생성 |
| `vectorstore.py` | `build_retriever()` | ChromaDB Retriever 생성 (DB 없으면 자동 구축) |
```

### 파일 계층 구조 표기

모든 파일에 [실습/설명/참고] 태그를 표시한다.

```markdown
ex05/
├── src/
│   ├── rag_chain.py        [실습] LCEL 파이프라인
│   ├── conversation.py     [실습] WindowMemory
│   ├── llm_factory.py      [참고] LLM 생성
│   ├── vectorstore.py      [참고] ChromaDB Retriever
│   ├── session_manager.py  [참고] 세션별 대화 관리
│   └── response_parser.py  [설명] DeepSeek <think> 제거 + 출처 추출
└── app/
    ├── chat_api.py         [설명] POST /api/chat 엔드포인트
    └── session.py          [참고] 세션 쿠키 관리
```

---

## 적용 사례

### ex05 (CH05: RAG Q&A)

| 원본 | 분리 후 [실습] | 분리된 [참고] |
|------|--------------|-------------|
| rag_chain.py (305줄) | rag_chain.py (124줄): `RAG_SYSTEM_PROMPT`, `_format_docs`, `build_rag_chain` | llm_factory.py: `build_llm()` / vectorstore.py: `build_retriever()`, `_parse_and_chunk_docs()` |
| conversation.py (221줄) | conversation.py (55줄): `WindowMemory` 클래스만 | session_manager.py: `ConversationManager`, `get_conversation_manager()` |

### ex06 (CH06: 통합 에이전트)

| 원본 | 분리 후 [실습] | 분리된 [참고] |
|------|--------------|-------------|
| mcp_tools.py (400줄) | mcp_tools.py (193줄): `@tool` 4개 + `ALL_TOOLS` | db_helper.py: `run_query()`, `build_vectorstore()`, `get_vectorstore()` |
| agent.py (271줄) | agent.py (150줄): `SYSTEM_PROMPT`, `IntegratedAgent` 핵심 | llm_factory.py: `build_llm()` / agent_helpers.py: `parse_agent_result()`, `serialize_steps()`, `fallback_response()` |

---

## 자주 분리되는 [참고] 파일 패턴

| 파일명 | 역할 | 반복 등장 |
|--------|------|----------|
| `llm_factory.py` | LLM 인스턴스 생성 (Ollama/OpenAI 분기) | ex05, ex06, ex07+ |
| `db_helper.py` | DB 연결 + 쿼리 실행 + 벡터스토어 구축 | ex06+ |
| `session_manager.py` | 세션별 대화 관리 (WindowMemory 래핑) | ex05+ |
| `agent_helpers.py` | 에이전트 결과 파싱/직렬화/폴백 | ex06+ |
| `vectorstore.py` | ChromaDB Retriever 생성 + 문서 파싱 | ex05+ |

---

## 체크리스트

- [ ] 각 [실습] 파일의 핵심 교육 개념을 식별했는가?
- [ ] [참고]로 분리한 코드가 [실습] 파일에서 정상 import 되는가?
- [ ] 챕터 마크다운의 파일 계층 구조에 [실습/참고/설명] 태그가 붙어 있는가?
- [ ] [참고] 파일의 함수는 메서드 표로 요약했는가?
- [ ] 분리 후 import 테스트(`python -c "from src.xxx import yyy"`)를 통과했는가?
