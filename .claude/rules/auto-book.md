---
globs: ["projects/*/book/front/*.md", "projects/*/book/body/*.md", "projects/*/book/back/*.md"]
---

# 자동 트리거: book/

프롤로그(front), 본문(body), 에필로그/부록(back) 파일을 수정할 때 자동으로 적용된다.

---

## writer (작가)

### 공통 규칙
- 전체 존댓말, 이모지 금지
- 금지: 설교, 반복 강조, 진부한 표현
- **볼드** 양쪽 띄어쓰기
- 이야기 파트에 코드 없음

### 경로별 추가 규칙
- **front/** (프롤로그): 일기처럼 작성. CH01~CH10을 관통하는 서사
- **body/** (본문): chapters/*.md와 톤/구조 일관성 유지
- **back/** (에필로그/부록): 전체 책 흐름의 마무리. 새로운 개념 도입 금지

### 필수 스킬
- writing (skills/writing/SKILL.md) — 요약/브릿지
- humanizer (skills/humanizer/SKILL.md) — AI 패턴 교정

### 참조
- 작가 규칙 상세: .claude/agents/writer/AGENT.md (프롤로그 섹션)

---

## editor (편집장)

### 점검 항목
- 프롤로그가 전체 챕터 흐름(CH01~CH10)과 일치하는가
- 챕터에 없는 내용이 들어가지 않았는가
- 톤이 챕터 본문과 일관되는가
- 에필로그/부록이 전체 책 구조와 일관되는가

### 참조
- 편집장 규칙 상세: .claude/agents/editor/AGENT.md

---

## publisher (인쇄소)

### 점검 항목
- **body/** 변경 시 PDF 리빌드가 필요한지 판단
- 레이아웃에 영향을 주는 변경(이미지, 표, 코드 블록 추가/삭제) 감지

### 참조
- 인쇄소 규칙 상세: .claude/agents/publisher/AGENT.md
