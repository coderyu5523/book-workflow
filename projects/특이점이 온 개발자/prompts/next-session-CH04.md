# 다음 세션: CH04 집필

## 프로젝트
- 경로: projects/특이점이 온 개발자/
- progress.json 확인 후 현재 상태 파악

## 워크플로우
- .claude/workflow/step5-챕터집필.md (실행 흐름)
- .claude/workflow/review-guide.md (검토 체크리스트)

## 컨텍스트 파일 (읽어야 할 것)
- planning/seed-v1.md (의도, 핵심 메시지, 의도 밖 범위)
- planning/outline-v1.md (CH04 섹션 — 코드 분류, 이미지 계획)
- planning/scenario-v1.md (v0.3 시나리오)
- chapters/03-매번-처음부터-깔-순-없잖아.md (브릿지 문장 확인)
- answers.md (이전 STEP 답변 누적)

## 이번 챕터 변수
- 제목: 혼자선 감당이 안 된다
- 핵심 개념: 수평 스케일링, 로드밸런싱(round-robin), 같은 이미지 복수 실행
- 버전: v0.3
- 코드: ex02 (실습 3개, 참고 2개)
- 이전 챕터 브릿지: "app1에 사용자가 몰리면 어떻게 될까요? 서버 하나로 감당이 안 될 때, 같은 앱을 여러 개 띄워서 요청을 나누는 방법을 다음 챕터에서 다룹니다."
- 에셋 경로: assets/CH04/{gemini, terminal}/
- 이야기 대비: ex01(2개 다른 앱 라우팅) → ex02(1개 앱 2개 인스턴스 분산). "앱을 늘리는 게 아니라 같은 앱을 복제한다"

## 이미지 계획
- 그림 4-1: GEMINI PROMPT — ex01(프록시) vs ex02(로드밸런싱) 구조 비교
- 그림 4-2: CAPTURE NEEDED — 브라우저 새로고침 → 번갈아 응답 확인

## 에이전트 디스패치 순서
writer → editor (글 작성 → 검토)
이미지 생성(illustrator)은 코드 완성 확인 후 유저가 별도 요청

## 명령
`챕터 작성 4` 실행
