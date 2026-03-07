# 집필에이전트 v3

기술 서적(100페이지 권장)을 이야기처럼 쓰는 워크플로우 시스템.
저자(도메인 전문가)와 하나의 AI(Claude)가 대화하며 책을 완성한다.
**코드를 따라치는 튜토리얼이 아니라, "왜 이게 필요한지"를 이야기로 전달하는 개념서.**

> **코드 워크플로우**는 완성 코드를 **만드는** 단계 (별도 설계).
> 이 워크플로우의 STEP 2에서 분석하는 완성 코드 = 코드 워크플로우의 산출물.

| 개념 | 정체 | 역할 |
|------|------|------|
| **STEP** | 흐름 | 1~7번까지 순서대로 진행하는 워크플로우 단계 |
| **스킬** | 도구 | 하나의 작업만 수행하고 결과를 돌려주는 원자적 도구 (22개, `.claude/skills/CATALOG.md`) |
| **검토 모드** | 체크리스트 | 산출물 품질을 검증하는 관점과 질문 목록 (3개, review 스킬 참조) |

에이전트는 없다. 하나의 AI가 STEP을 따라가며 스킬을 쓰고, 검토 모드로 점검한다.

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
  STEP 6. 프롤로그 + 로드맵   "숲을 보여준다"
  STEP 7. 마무리              "서문, 에필로그, 부록"
```

---

## 명령어 라우팅

사용자가 명령어를 입력하면 워크플로우 파일을 읽고, 해당 스킬을 로드하여 실행한다.

| 명령어 | STEP | 워크플로우 | 스킬 | 산출물 |
|--------|------|-----------|------|--------|
| `새 책 만들기` | — | — | — | 프로젝트 디렉토리 |
| `씨앗 심기` | 1 | `workflow/step1-씨앗.md` | code | `planning/seed.md` |
| `코드 분석` | 2 | `workflow/step2-코드해부.md` | code | `planning/code-analysis.md` |
| `시나리오 설계` | 3 | `workflow/step3-시나리오.md` | code, planning | `planning/scenario.md` + `versions/` |
| `뼈대 세우기` | 4 | `workflow/step4-뼈대.md` | code, planning, visual | `planning/outline.md` |
| `챕터 작성 [N]` | 5 | `workflow/step5-챕터집필.md` | writing, code, visual, review | `chapters/NN-제목.md` |
| `검토 [챕터]` | — | `workflow/review-guide.md` | review | `review/feedback-log.md` |
| `프롤로그 생성` | 6 | `workflow/step6-프롤로그.md` | writing | `book/front/prologue.md` |
| `마무리` | 7 | `workflow/step7-마무리.md` | writing, planning | `book/front/preface.md` 등 |

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
📖 [프로젝트명] — [제목]
   현재: STEP N. [이름] (in_progress)

── STEP 진행 ──────────────────────
[x] STEP 1. 씨앗           → seed-v2.md (pass)
[~] STEP 5. 챕터 집필       → 2/5 완료
[ ] STEP 6. 프롤로그+로드맵

── 챕터 상태 ──────────────────────
[x] CH01 제목 (ex01) — pass
[~] CH02 제목 (ex02) — 작성 중

진행률: ████████░░░░░░░ 45%
```

---

## 스타일 가드레일

항상 적용되는 핵심 규칙 (상세 규칙 + 예시는 writing 스킬 참조):

- **전체 존댓말**: 내러티브·설명문 모두. 캐릭터 대화/독백만 구어체 유지
- **대화 표기**: `**팀장**: "대사"` / `**나**: "대사"` / LLM 대화: `> **나**: 질문`
- **내면 독백**: `*이탤릭*`으로. 괄호 `()` 사용 금지
- **등장인물**: 역할명(**팀장**/**나**/**동료**), 조회 대상(A 사원, B 팀원)
- **금지 패턴**: 설교("이것이야말로..."), 반복 강조("이것이 바로...이유"), 정의 전 용어
- **이모지 금지** (박스 스타일에서만 허용). **볼드** 양쪽 띄어쓰기 필수
- **영어 용어**: 처음 등장 시 `한국어(English)` 형태. 이후 한국어만
- **이미지 플레이스홀더**: `[GEMINI PROMPT]`(개념도) / `[CAPTURE NEEDED]`(실습 캡처)
- **이야기 파트에 코드 없음**. 기술 파트에서만, 10~15줄 이내

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
├── versions/ex01~N/       ← 버전별 예제 코드
├── questions/pending|done/← 인사이트 질문 장바구니
├── assets/                ← 챕터별 이미지
├── code/                  ← 완성 코드
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
