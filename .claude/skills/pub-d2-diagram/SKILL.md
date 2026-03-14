---
name: pub-d2-diagram
description: "D2 다이어그램 빌드 스킬 - D2 언어로 다이어그램을 작성하고 PNG 생성"
model: claude-sonnet-4-6
disable-model-invocation: true
---

# D2 다이어그램 빌드 스킬

model: claude-sonnet-4-6
user_invocable: true
trigger: ["D2 빌드", "다이어그램 생성", "/d2"]

## 하는 일

D2 언어로 다이어그램을 작성하고, O'Reilly 모노톤 스타일로 PNG를 생성합니다.

## 디자인 규칙

> 회의 피드백 #8: 옅은 회색 금지. 프라이머리(파란색) + 화이트 2색 체계.

### 색상 — 프라이머리 + 화이트

| 도형 | 용도 | fill | stroke | 텍스트 |
|------|------|------|--------|--------|
| 타원 | 입출력 (시작/끝) | `white` | `#333333` (얇은) | 검정 |
| 직사각형 | 핵심 프로세스 | `#3b82f6` (프라이머리) | `#3b82f6` (2px) | 검정 |
| 실린더 | 데이터 저장소 | `white` | `#333333` (얇은) | 검정 |
| 점선 박스 | 그룹핑/영역 | `transparent` | `#3b82f6` + stroke-dash: 5 | 검정 |
| 다이아몬드 | 분기점 | `white` | `#333333` | 검정 |
| 육각형 | 핵심 분기 | `#3b82f6` | `#3b82f6` (2px) | 검정 |

**핵심: 직사각형(핵심 프로세스)과 육각형(핵심 분기)만 프라이머리 배경. 나머지는 화이트 배경 + 얇은 테두리.**

### 공통 스타일

- `border-radius: 8` — 모든 사각형 노드
- `direction: right` — 가로 흐름 기본 (세로 금지)
- 화살표 색상: `style.stroke: "#3b82f6"` (프라이머리)
- 레이아웃: ELK (`--layout elk`)
- 회색 배경 금지 (`#f0f0f0`, `#eeeeee` 등 사용하지 않음)

### classes 시스템

```d2
classes: {
  phase: { shape: rectangle; style: { fill: transparent; stroke: "#3b82f6"; stroke-width: 2; border-radius: 8; stroke-dash: 5; font-size: 16 } }
  input: { shape: rectangle; style: { fill: white; stroke: "#333333"; stroke-width: 1; border-radius: 8; font-size: 14 } }
  process: { shape: rectangle; style: { fill: "#3b82f6"; stroke: "#3b82f6"; stroke-width: 2; border-radius: 8; font-size: 14 } }
  llm: { shape: hexagon; style: { fill: "#3b82f6"; stroke: "#3b82f6"; stroke-width: 2; font-size: 15 } }
  problem: { shape: rectangle; style: { fill: white; stroke: "#333333"; stroke-width: 1; border-radius: 8; stroke-dash: 4 } }
  db: { shape: cylinder; style: { fill: white; stroke: "#333333"; stroke-width: 1; border-radius: 8 } }
  answer: { shape: rectangle; style: { fill: white; stroke: "#3b82f6"; stroke-width: 2; border-radius: 8 } }
}
```

## 빌드 파이프라인

D2 → SVG → 색상 보정 → PNG

```bash
# 1. D2 → SVG (ELK 레이아웃, 테마 없음)
d2 --layout elk --pad 40 input.d2 output.svg

# 2. 테마 잔여 색상 → 프라이머리+화이트 보정
sed -e 's/#0D32B2/#3b82f6/g' \
    -e 's/#F7F8FE/#FFFFFF/g' \
    -e 's/#EDF0FD/#FFFFFF/g' \
    -e 's/#E3E9FD/#FFFFFF/g' \
    -e 's/#EEF1F8/#FFFFFF/g' \
    -e 's/fill:url(#streaks-bright[^)]*)/fill:#FFFFFF/g' \
    -e 's/fill:url(#streaks-darker[^)]*)/fill:#FFFFFF/g' \
    -e 's/fill:url(#streaks-normal[^)]*)/fill:#FFFFFF/g' \
    -e 's/fill:url(#streaks-dark[^)]*)/fill:#FFFFFF/g' \
    output.svg > output_clean.svg

# 3. SVG → PNG (144 DPI)
rsvg-convert -d 144 -p 144 output_clean.svg -o output.png

# 4. 정리
rm output.svg output_clean.svg
```

## 일괄 빌드

```bash
cd projects/사내AI비서_v2/assets/diagrams
./build_diagrams.sh
```

## 의존성

| 도구 | 설치 | 용도 |
|------|------|------|
| d2 | `brew install d2` | D2 → SVG 컴파일 |
| rsvg-convert | `brew install librsvg` | SVG → PNG 변환 |

## 다이어그램 목록

| 파일 | 챕터 | 내용 |
|------|------|------|
| 01_rag-comparison | CH01 | LLM 단독 vs RAG 비교 |
| 02_api-restaurant | CH02 | API = 웨이터 비유 |
| 03_parser-pipeline | CH03 | 파서 → 청킹 → 벡터DB |
| 04_parser-dispatch | CH04 | 확장자별 파서 분기 |
| 05_rag-qa-flow | CH05 | RAG Q&A 흐름 |
| 05_lcel-pipeline | CH05 | LCEL 파이프 연결 |
| 06_tool-vs-mcp | CH06 | @tool vs MCP 비교 |
| 06_agent-architecture | CH06 | QueryRouter + ReAct |
| 06_sequence-crud | CH06 | CRUD 시퀀스 |
| 09_ch08-vs-ch09 | CH09 | 검색 전/중/후 비교 |
| 09_sequence-pipeline | CH09 | 전체 파이프라인 시퀀스 |
