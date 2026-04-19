# 다음 세션: CH05 집필

## 프로젝트
- 경로: projects/특이점이 온 개발자/
- progress.json 확인 후 현재 상태 파악

## 워크플로우
- .claude/workflow/step5-챕터집필.md (소제목 템플릿, 번호 규칙, 산출물 형식)
- .claude/workflow/review-guide.md (검토 체크리스트)

## 컨텍스트 파일 (읽어야 할 것)
- planning/seed-v1.md (의도, 핵심 메시지, 의도 밖 범위)
- planning/outline-v1.md (CH05 섹션 — 코드 분류, 이미지 계획)
- planning/scenario-v1.md (v0.4 시나리오)
- chapters/04-혼자선-감당이-안-된다.md (브릿지 문장 확인)
- answers.md (이전 STEP 답변 누적)

## 이번 챕터 변수
- 제목: 한 번 가져온 건 저장해두자
- 핵심 개념: Nginx 캐싱 동작 원리, 캐시 히트/미스, Python 앱 이미지 빌드
- 버전: v0.4
- 코드: ex03 (실습 3개, 참고 3개)
- 이전 챕터 브릿지: "같은 요청이 반복될 때마다 서버가 매번 처음부터 처리하고 있었습니다. 한 번 처리한 결과를 저장해두면 더 빨라지지 않을까요?"
- 에셋 경로: assets/CH05/{gemini, terminal}/

## 이미지 계획
- 그림 5-1: GEMINI PROMPT — 캐시 동작 흐름 (MISS → 저장 → HIT)
- 그림 5-2: CAPTURE NEEDED — curl -I 결과 (X-Cache-Status: MISS → HIT 변화)

## 에이전트 디스패치 순서
writer → editor (글 작성 → 검토)
이미지 생성(illustrator)은 코드 완성 확인 후 유저가 별도 요청

## 명령
`챕터 작성 5` 실행
