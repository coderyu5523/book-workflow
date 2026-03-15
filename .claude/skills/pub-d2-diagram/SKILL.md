---
name: pub-d2-diagram
description: "D2 다이어그램 빌드 스킬 - D2 언어로 다이어그램을 작성하고 PNG 생성"
model: claude-sonnet-4-6
# disable-model-invocation: true
---

# D2 다이어그램 빌드 스킬

model: claude-sonnet-4-6
user_invocable: true
trigger: ["D2 빌드", "다이어그램 생성", "/d2"]

## 하는 일

D2 언어로 다이어그램을 작성하고, O'Reilly 모노톤 스타일로 PNG를 생성합니다.

## 디자인 토큰

### 색상 팔레트

| 토큰 | 값 | 용도 |
|------|-----|------|
| `primary` | `#2563eb` | stroke, 화살표, 강조 테두리 |
| `primary-bg` | `#eef2ff` | 핵심 프로세스 배경 |
| `primary-text` | `#1e40af` | 핵심 프로세스 텍스트 |
| `neutral-text` | `#374151` | 일반 텍스트 |
| `neutral-border` | `#c5cee0` | 입출력/저장소 테두리 |
| `group-text` | `#1e3a5f` | 그룹 박스 텍스트 |
| `storage-bg` | `#f8fafc` | 저장소(실린더) 배경 |
| `white` | `#ffffff` | 입출력/그룹 배경 |

### 공통 스타일

- `shadow: true` — 모든 노드
- `border-radius: 8` — 모든 사각형 노드
- `bold: true` — 모든 노드 텍스트
- `font-size: 18~20` — 노드 텍스트 (step형은 20, 흐름형은 18)
- `direction: right` — 가로 흐름 기본 (세로 금지)
- 화살표: `stroke: "#2563eb"`, `stroke-width: 2`
- 레이아웃: ELK (`--layout elk`)
- 명시적 `width`/`height` 지정 권장

### classes 시스템

```d2
classes: {
  step: {
    shape: rectangle
    style: {
      fill: "#ffffff"
      stroke: "#2563eb"
      stroke-width: 2
      border-radius: 8
      shadow: true
      font-size: 20
      font-color: "#374151"
      bold: true
    }
    width: 220
    height: 70
  }
  start-end: {
    shape: oval
    style: {
      fill: "#ffffff"
      stroke: "#c5cee0"
      stroke-width: 2
      shadow: true
      font-size: 18
      font-color: "#374151"
    }
    width: 150
    height: 70
  }
  process: {
    shape: rectangle
    style: {
      fill: "#eef2ff"
      font-color: "#1e40af"
      stroke: "#2563eb"
      stroke-width: 2
      border-radius: 8
      shadow: true
      font-size: 18
      bold: true
    }
    width: 150
    height: 60
  }
  decision: {
    shape: diamond
    style: {
      fill: "#ffffff"
      stroke: "#2563eb"
      stroke-width: 2
      shadow: true
      font-size: 16
      font-color: "#374151"
      bold: true
    }
    width: 160
    height: 80
  }
  storage: {
    shape: cylinder
    style: {
      fill: "#f8fafc"
      stroke: "#c5cee0"
      stroke-width: 2
      shadow: true
      font-size: 18
      font-color: "#374151"
      bold: true
    }
    width: 140
    height: 80
  }
  group-box: {
    style: {
      stroke: "#2563eb"
      stroke-width: 2
      stroke-dash: 5
      fill: "#ffffff"
      font-size: 22
      bold: true
      font-color: "#1e3a5f"
    }
  }
}
```

### 다이어그램 유형별 사용 가이드

| 유형 | 사용 class | 예시 |
|------|-----------|------|
| 실습 흐름도 (exercise-flow) | `step` | 단계 나열: step1 → step2 → step3 |
| 아키텍처도 | `start-end` + `process` + `storage` + `group-box` | Client → Server → DB |
| 분기 흐름도 | `start-end` + `decision` + `process` | 입력 → 분기 → 처리A / 처리B |

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

## 디자인 레퍼런스 규칙

D2 작성 시 기존 프로젝트의 .d2 파일을 디자인 레퍼런스로 참조하라. SKILL.md의 classes보다 실제 산출물의 스타일이 우선한다 → why-log.md#2026-03-15-8

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
