# Mermaid 다이어그램 가이드

> 출처: v1 visual/mermaid
> 관련 스킬: B4.계층-생성기, B5.난이도-곡선기

---

## 기본 원칙

- **노드 최대 7개** — 넘으면 subgraph로 분리
- **`flowchart`** 키워드 사용 (`graph` 아님)

---

## 특수문자 처리

- 괄호/중괄호/대괄호/슬래시가 라벨에 있으면 **큰따옴표 필수**
- 줄바꿈: `<br>` 만 사용 (`\n` 금지)
- 엣지 텍스트: `A -- "텍스트" --> B` 형식 (`-->|텍스트|` 금지)
- 점선: `A -. "텍스트" .-> B`
- 굵은선: `A == "텍스트" ==> B`

---

## Subgraph 규칙

- ID에 공백/특수문자 금지
- `subgraph SubSystem ["시스템 이름"]` 형식

---

## Bold/Italic 절대 금지

Mermaid 안에서 `**` 또는 `*`를 사용하면 **렌더링이 깨진다.**
큰따옴표 안이든 밖이든 절대 사용하지 않는다.

가장 흔한 렌더링 실패 원인이다.

---

## 색상 팔레트 — 프라이머리 + 화이트

모든 Mermaid 다이어그램은 **프라이머리(파란색) + 화이트** 2색 체계. 회색 배경 금지. 가독성 최우선.

| 이름 | 용도 | classDef |
|------|------|----------|
| default | 일반 노드 (화이트 배경) | `fill:#ffffff,stroke:#333,stroke-width:1px,color:#1a1a1a` |
| primary | 핵심 프로세스 (프라이머리 배경) | `fill:#3b82f6,stroke:#3b82f6,stroke-width:2px,color:#1a1a1a` |

**도형 색상 규칙**.
- 타원 (입출력). 화이트 배경 + 얇은 검정/연회색 테두리
- 직사각형 (핵심 프로세스). 프라이머리 배경 + 프라이머리 테두리 + 검정 텍스트
- 실린더 (데이터 저장소). 화이트 배경 + 얇은 검정/연회색 테두리
- 점선 박스 (그룹핑). 화이트 배경 + 프라이머리 점선 테두리

**핵심 프로세스(직사각형)만 프라이머리 배경, 나머지는 화이트 배경 + 얇은 테두리.**

```mermaid
flowchart LR
    A(["사용자 요청"]) --> B["Controller"]
    B --> C["Service"]
    C --> D[("Database")]

    classDef default fill:#ffffff,stroke:#333,stroke-width:1px,color:#1a1a1a
    classDef primary fill:#3b82f6,stroke:#3b82f6,stroke-width:2px,color:#1a1a1a

    class B,C primary
```

---

## 체크리스트

```
□ `flowchart` 키워드 사용했는가?
□ 특수문자 포함 라벨에 큰따옴표를 씌웠는가?
□ 엣지 텍스트가 `-- "텍스트" -->` 형식인가?
□ 노드 7개 이하인가?
□ `**` 또는 `*`가 Mermaid 안에 없는가?
□ 프라이머리+화이트 2색 체계를 지켰는가? (회색 배경 없는가?)
```

---

## 예시

```mermaid
flowchart LR
    A["사용자 요청"] --> B["Controller"]
    B --> C["Service"]
    C --> D["Repository"]
    D --> E["Database"]
```
