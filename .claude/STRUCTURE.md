# 파일 구조 맵

메타코딩(오케스트레이터)이 세션 시작 시 로드. 모든 에이전트가 참조 가능.

---

## 시스템 (.claude/) — 변경 빈도: 낮음

### 에이전트 (정의 + 규칙 + 절차)

```
.claude/agents/
├── meta/AGENT.md           — 오케스트레이터. 디스패치 테이블
├── analyst/AGENT.md        — 분석관. A 시리즈 스킬 + 규칙
├── architect/AGENT.md      — 설계사. B 시리즈 스킬 + 규칙
├── writer/AGENT.md         — 작가. C 시리즈 + humanizer + 규칙
├── editor/AGENT.md         — 편집장. D 시리즈 + 검토 체크리스트 + 규칙
├── illustrator/AGENT.md    — 일러스트레이터. visual + screenshot + 규칙
├── publisher/AGENT.md      — 인쇄소. pub 계열 PDF 빌드 + 규칙
└── why/
    ├── AGENT.md            — Why Agent. 규칙 업데이트
    └── why-log.md          — 변경 이력 (포인터 대상)
```

### 글로벌 규칙 (자동 로드)

```
.claude/rules/
├── style.md                — 톤, 편집, 포맷
├── code.md                 — 코드 표시 규칙
└── structure.md            — 산출물 구조, 버전 관리
```

### 스킬 (캡슐화 + 포인터 참조)

```
.claude/skills/
├── @analyst/SKILL.md        — 포인터 인덱스 (이름 + 경로만)
├── @architect/SKILL.md      — 포인터 인덱스
├── @editor/SKILL.md         — 포인터 인덱스
├── @illustrator/SKILL.md    — 포인터 인덱스
├── @publisher/SKILL.md      — 포인터 인덱스
├── @writer/SKILL.md         — 포인터 인덱스
├── code/                    — 실제 스킬 (SKILL.md + references/)
├── d2-diagram/              — 실제 스킬 (SKILL.md) [예정]
├── design-doc-mermaid/      — 실제 스킬 (SKILL.md + references/)
├── humanizer/               — 실제 스킬 (SKILL.md + references/)
├── pdf-ty/                  — 실제 스킬 (SKILL.md + references/)
├── planning/                — 실제 스킬 (SKILL.md + references/)
├── pub-build/               — 실제 스킬 (SKILL.md + references/)
├── pub-d2-diagram/          — 실제 스킬 (SKILL.md)
├── pub-image-optimize/       — 실제 스킬 (SKILL.md + references/)
├── pub-layout-check/        — 실제 스킬 (SKILL.md + references/)
├── pub-page-fit/            — 실제 스킬 (SKILL.md + references/)
├── pub-typst-design/        — 실제 스킬 (SKILL.md + references/)
├── review/                  — 실제 스킬 (SKILL.md + references/)
├── screenshot/              — 실제 스킬 (SKILL.md + references/)
├── visual/                  — 실제 스킬 (SKILL.md + references/)
└── writing/                 — 실제 스킬 (SKILL.md + references/)
```

---

## 프로젝트 — 변경 빈도: 높음

```
projects/{책이름}/
├── progress.json           — 상태 관리 (STEP 진행, 챕터 상태)
├── answers.md              — 모든 답변 누적
├── planning/
│   ├── seed-vN.md          — STEP 1 산출물 (의도)
│   ├── code-analysis-vN.md — STEP 2 산출물 (코드 분석)
│   ├── scenario-vN.md      — STEP 3 산출물 (시나리오)
│   └── outline-vN.md       — STEP 4 산출물 (목차)
├── chapters/
│   └── NN-제목.md          — STEP 5 산출물 (챕터)
├── book/
│   ├── front/              — prologue
│   ├── body/               — 본문 (빌드용)
│   └── back/               — epilogue, appendix
├── versions/exNN/          — 버전별 예제 코드
├── code/                   — 완성 코드 (진실의 원천)
├── assets/CHNN/
│   ├── diagram/            — D2/Mermaid 렌더링 PNG
│   ├── terminal/           — rich → SVG → PNG 캡처
│   └── gemini/             — Gemini 생성 개념도
├── questions/pending|done/ — 인사이트 질문 장바구니
└── review/
    ├── feedback-log.md     — 편집장 피드백
    └── why-log.md          — Why Agent 변경 이력
```
