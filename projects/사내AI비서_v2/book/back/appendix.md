# 부록

---

## A. 환경 설정

### Python 설치

이 책의 모든 예제는 Python **3.12** 를 기준으로 작성됐습니다. 3.10~3.12에서 동작하며, 3.13 이상에서는 일부 패키지 호환성 문제가 있을 수 있습니다.

**macOS**

```bash
# Homebrew로 설치
brew install python@3.12
```

**Windows**

공식 사이트(https://www.python.org/downloads/)에서 Python 3.12를 다운로드합니다. 설치 시 **"Add Python to PATH"** 체크박스를 반드시 선택하세요.

**Linux (Ubuntu/Debian)**

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

### 가상환경 설정

예제마다 패키지 버전이 다를 수 있으므로, **반드시 가상환경을 만들어서 진행하세요.**

```bash
# 가상환경 생성
python3 -m venv .venv

# 활성화 (macOS/Linux)
source .venv/bin/activate

# 활성화 (Windows)
.venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

가상환경이 활성화되면 터미널 프롬프트 앞에 `(.venv)` 가 표시됩니다.

### 자주 만나는 오류

**`python` 명령어가 안 될 때**

macOS/Linux에서는 `python` 대신 `python3` 를 사용해야 할 수 있습니다.

```bash
# python이 안 되면
python3 --version
python3 -m venv .venv
```

**`pip install` 에서 권한 오류**

가상환경 없이 시스템 Python에 설치하려고 하면 권한 오류가 발생합니다. 가상환경을 먼저 활성화하세요.

```bash
# 이렇게 하면 안 됩니다
pip install langchain  # PermissionError 또는 externally-managed-environment

# 이렇게 하세요
source .venv/bin/activate  # 먼저 가상환경 활성화
pip install -r requirements.txt
```

**`pip` 대신 `pip3`**

`pip` 명령이 안 되면 `pip3` 를 사용하세요. 가상환경 안에서는 둘 다 동일합니다.

**psycopg2-binary 설치 실패 (macOS Apple Silicon)**

M1/M2/M3 Mac에서 psycopg2-binary 설치가 실패할 수 있습니다.

```bash
# libpq 먼저 설치
brew install libpq
pip install psycopg2-binary
```

### LLM 설정

이 책은 두 가지 LLM 백엔드를 지원합니다.

| 옵션 | 장점 | 환경 변수 |
|------|------|----------|
| **Ollama (로컬)** | 무료, 오프라인 가능 | `OLLAMA_BASE_URL`, `OLLAMA_MODEL` |
| **OpenAI (클라우드)** | 품질 우수, 설치 불필요 | `OPENAI_API_KEY`, `OPENAI_MODEL` |

CH06 이후 에이전트 기능(Tool Calling)을 사용하려면 Ollama의 경우 `llama3.1:8b` 이상 모델이 필요합니다.

### .env 파일 예시

각 예제 폴더의 `.env.example` 을 `.env` 로 복사한 뒤 값을 채워넣으세요.

```bash
# LLM 설정
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# OpenAI 사용 시
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o-mini

# PostgreSQL (ex02 이후)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=rag_password

# 벡터DB + 임베딩
CHROMA_PERSIST_DIR=./data/chroma_db
EMBEDDING_MODEL=jhgan/ko-sroberta-multitask
```

### Docker (PostgreSQL)

ex02 이후 예제는 PostgreSQL이 필요합니다. Docker Compose로 실행합니다.

```bash
docker-compose up -d
```

PostgreSQL 16 Alpine 이미지를 사용하며, `data/schema.sql` 이 자동으로 초기화됩니다.

### 핵심 패키지 요약

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `langchain` | 0.3.x | RAG 파이프라인, 에이전트 |
| `chromadb` | 1.5.x | 벡터 데이터베이스 |
| `fastapi` | 0.115.x | API 서버 |
| `sentence-transformers` | 3.3.x | 한국어 임베딩 모델 |
| `psycopg2-binary` | 2.9.x | PostgreSQL 연결 |
| `pypdf` | 4.3.x | PDF 파싱 |
| `python-docx` | 1.1.x | DOCX 파싱 |
| `openpyxl` | 3.1.x | XLSX 파싱 |
| `rank-bm25` | 0.2.x | 하이브리드 검색 (CH08) |
| `easyocr` | 1.7.x | OCR (CH10) |

각 예제 폴더의 `requirements.txt` 로 한 번에 설치할 수 있습니다.

```bash
pip install -r requirements.txt
```

---

## B. 참고 자료

이 책에서 사용한 라이브러리의 공식 문서입니다.

| 라이브러리 | 공식 문서 |
|-----------|----------|
| **LangChain** | https://python.langchain.com/docs |
| **ChromaDB** | https://docs.trychroma.com |
| **FastAPI** | https://fastapi.tiangolo.com |
| **sentence-transformers** | https://www.sbert.net |
| **OpenAI Python SDK** | https://platform.openai.com/docs/libraries/python-library |

---

## C. 더 알고 싶다면

RAG와 LLM 응용에 관심이 생겼다면, 아래 주제를 찾아보세요.

- **Graph RAG** — 단순 청크 검색이 아니라 지식 그래프로 문서 관계를 표현하는 방식
- **멀티모달 RAG** — 텍스트뿐 아니라 이미지, 표, 차트를 함께 다루는 RAG
- **Agentic RAG** — 에이전트가 검색 전략을 스스로 결정하는 방식

ConnectHR에서 한 단계 더 나아가는 방향들입니다.
