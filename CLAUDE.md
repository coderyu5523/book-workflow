# 집필에이전트 v4

기술 서적(100페이지 권장)을 이야기처럼 쓰는 에이전트 시스템.
저자(도메인 전문가)와 AI 에이전트 팀이 대화하며 책을 완성한다.
**코드를 따라치는 튜토리얼이 아니라, "왜 이게 필요한지"를 이야기로 전달하는 개념서.**

> **코드 워크플로우**는 완성 코드를 **만드는** 단계 (별도 설계).
> 이 워크플로우의 STEP 2에서 분석하는 완성 코드 = 코드 워크플로우의 산출물.

---

## 아키텍처

```
메타코딩 (오케스트레이터) — STEP 디스패치 + progress.json 관리
├── 설계분석관 (Analyst-Architect) ← A 시리즈 5개 + B 시리즈 6개
├── 작가 (Writer)                 ← C 시리즈 5개 + humanizer
├── 편집장 (Editor)               ← D 시리즈 6개 + 검토 모드 3개
├── 일러스트레이터 (Illustrator)    ← visual + screenshot + diagram
└── 인쇄소 (Publisher)            ← pub 계열 6개 + pdf-ty

메타코딩 직접 호출 스킬:
└── why-분석기                    ← 실패 분석 → "하지 마라" 규칙 추가
```

| 개념 | 정체 | 역할 |
|------|------|------|
| **STEP** | 흐름 | 1~7번까지 순서대로 진행하는 워크플로우 단계 |
| **에이전트** | 전문가 | 역할별 규칙과 스킬을 가진 서브 에이전트 (6개, `.claude/agents/`) |
| **스킬** | 도구 | 하나의 작업만 수행하고 결과를 돌려주는 원자적 도구 (`.claude/skills/`) |
| **검토 모드** | 체크리스트 | 산출물 품질을 검증하는 관점과 질문 목록 (3개, 편집장 소유) |

**상세**: `.claude/agents/meta/AGENT.md` (디스패치 테이블), `.claude/STRUCTURE.md` (파일 구조 맵)

---

## 전체 워크플로우 (7 STEP)

```
Phase 1 ── 의도 확립
  STEP 1. 씨앗              "이 책은 뭐다"

Phase 2 ── 재료 파악
  STEP 2. 코드 해부          "재료가 뭐가 있지"

Phase 3 ── 이야기 설계
  STEP 3. 시나리오 + 버전     "어떤 순서로 이야기하지"
  STEP 4. 뼈대 세우기         "목차와 코드 실습 배치"

Phase 4 ── 집필
  STEP 5. 챕터 집필 (반복)    "쓴다"

Phase 5 ── 완성
  STEP 6. 프롤로그            "숲을 보여준다"
  STEP 7. 마무리              "에필로그, 부록"
```

---

## 명령어 라우팅

사용자가 명령어를 입력하면 메타코딩이 디스패치 테이블을 참조하여 에이전트를 순서대로 호출한다.

| 명령어 | STEP | 디스패치 순서 | 산출물 |
|--------|------|-------------|--------|
| `새 책 만들기` | — | 메타코딩 단독 | 프로젝트 디렉토리 |
| `씨앗 심기` | 1 | 설계분석관 → 작가 → 편집장 | `planning/seed.md` |
| `코드 분석` | 2 | 설계분석관(+Context7) → 편집장 | `planning/code-analysis.md` |
| `시나리오 설계` | 3 | 설계분석관 → 일러스트레이터 → 편집장 | `planning/scenario.md` + `versions/` |
| `뼈대 세우기` | 4 | 설계분석관(+Context7) → 일러스트레이터 → 작가 → 편집장 | `planning/outline.md` |
| `챕터 작성 [N]` | 5 | 작가 → 일러스트레이터 → 편집장 → FAIL 시 why-분석기 스킬 | `chapters/NN-제목.md` |
| `검토 [챕터]` | — | 편집장 단독 | `review/feedback-log.md` |
| `프롤로그 생성` | 6 | 작가 → 편집장 | `book/front/prologue.md` |
| `마무리` | 7 | 작가 → 편집장 → 인쇄소 | `book/back/` |

**상세 절차**: 각 에이전트의 `.claude/agents/*/AGENT.md` 참조

### `새 책 만들기` 상세

프로젝트 디렉토리 생성 시 brace expansion 사용 금지. 각 디렉토리를 개별 생성:
```bash
mkdir -p projects/[책이름]/planning
mkdir -p projects/[책이름]/chapters
mkdir -p projects/[책이름]/book/front
mkdir -p projects/[책이름]/book/body
mkdir -p projects/[책이름]/book/back
mkdir -p projects/[책이름]/versions
mkdir -p projects/[책이름]/questions/pending
mkdir -p projects/[책이름]/questions/done
mkdir -p projects/[책이름]/assets
mkdir -p projects/[책이름]/code
mkdir -p projects/[책이름]/review
```
`.claude/progress-template.json` → `projects/[책이름]/progress.json` 복사. 완성 코드를 `code/`에 넣으라고 안내.

### `현재 상태` 출력 포맷

```
[프로젝트명] — [제목]
   현재: STEP N. [이름] (in_progress)

── STEP 진행 ──────────────────────
[x] STEP 1. 씨앗           → seed-v2.md (pass)
[~] STEP 5. 챕터 집필       → 2/5 완료
[ ] STEP 6. 프롤로그

── 챕터 상태 ──────────────────────
[x] CH01 제목 (ex01) — pass
[~] CH02 제목 (ex02) — 작성 중

진행률: ████████░░░░░░░ 45%
```

---

## 스타일 가드레일

상세 규칙은 `.claude/rules/` (자동 로드) 참조. 핵심만 요약:

- **전체 존댓말**: 캐릭터 대화/독백만 구어체
- **내면 독백**: 괄호 `()` 사용 (이탤릭 금지)
- **이모지 전면 금지**
- **"## 이야기 파트" 대문 제거**, 기술파트 대문 유지
- **볼드** 양쪽 띄어쓰기 필수, 문맥 전환 시 빈 줄 삽입
- **금지 패턴**: 설교, 반복 강조, 정의 전 용어
- **이야기 파트에 코드 없음**. 기술 파트에서만, 10~15줄 이내
- **의도가 필터다**: seed.md의 의도가 모든 결정의 기준

---

## 규칙 체계

| 범위 | 위치 | 로딩 |
|------|------|------|
| 글로벌 (모든 에이전트 공통) | `.claude/rules/style.md`, `code.md`, `structure.md` | 세션 시작 시 자동 로드 |
| 에이전트별 | 각 `agents/*/AGENT.md`의 `## 규칙` 섹션 | 서브 에이전트 컨텍스트에서만 로드 |
| 스킬 상세 | `skills/*/references/*.md` | 스킬 실행 시에만 로드 |

**서브 에이전트 컨텍스트 격리**: 작가 에이전트는 작가 규칙만, 인쇄소 에이전트는 인쇄소 규칙만 로드. 글로벌 규칙 3개만 공통.

---

## 프로젝트 인프라

### 폴더 구조

```
projects/[책이름]/
├── progress.json          ← 상태 관리
├── answers.md             ← 모든 답변 누적
├── planning/              ← STEP 1~4 산출물
├── chapters/              ← STEP 5 산출물
├── book/front|body|back/  ← 프롤로그, 본문, 에필로그
├── versions/exNN/         ← 버전별 예제 코드
├── questions/pending|done/← 인사이트 질문 장바구니
├── assets/CHNN/           ← 챕터별 이미지 (diagram/, terminal/, gemini/)
├── code/                  ← 완성 코드 (진실의 원천)
└── review/                ← 피드백 로그
```

### 산출물 버전 관리

파일명에 `-vN` 접미사. 절대 덮어쓰지 않는다: `seed-v1.md → seed-v2.md → ...`

### progress.json 운영

1. STEP 시작 → `in_progress`, `current_step` 업데이트
2. 산출물 생성 → artifact 경로·버전 업데이트
3. 검토 완료 → review 결과 업데이트
4. STEP 완료 → `done`
5. 챕터 추가 → `step_5_chapters.chapters`에 push
6. 세션 재개 → progress.json 읽고 미완료 항목부터 이어가기

---

## 워크플로우 진행 규칙

1. **한 STEP씩 진행**: 산출물 완성 후 다음 STEP
2. **질문은 하나씩, 선택형 UI로**: `AskUserQuestion` 사용, 최대 4개 선택지, AI 추천은 첫 번째에 `(Recommended)`
3. **답변 즉시 저장**: `answers.md`에 기록
4. **STEP 완료 안내**: 다음 STEP 명령어 안내
5. **되돌아가기**: 이전 산출물 수정 시 새 버전 생성
6. **상수는 질문하지 않는다**: 톤, 스타일, 챕터 구조, 코드 분류 등 자동 적용
7. **의도가 필터다**: seed.md의 의도가 이후 모든 결정의 기준

### 출력 형식

- Markdown 형식, 파일명은 번호 접두사 (예: `01-시작하기.md`)
- 코드 블록 언어 태그 필수
- 이미지: `![설명](경로)` 플레이스홀더

### 프로젝트 관리

- 현재 프로젝트: `projects/` 아래 가장 최근 수정 폴더로 자동 감지
- 여러 프로젝트 시 사용자에게 확인
