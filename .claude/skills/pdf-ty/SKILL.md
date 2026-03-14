# PDF 빌드 스킬 (Typst)

model: claude-sonnet-4-6
user_invocable: true
trigger: ["PDF 빌드", "pdf 생성", "/pdf-ty"]

## 하는 일

프로젝트 마크다운 파일들을 통합하여 Typst 기반 출판 품질 PDF를 생성합니다.

## 파이프라인

```
Markdown (14개 파일)
  → 전처리 (주석 제거, 이미지 경로, Mermaid PNG)
  → Pandoc (MD → Typst)
  → 후처리 (이미지/라벨/표 수정)
  → 템플릿 병합
  → Typst 컴파일 → PDF
```

## 실행 방법

```bash
cd projects/사내AI비서_v2
python book/build_pdf_typst.py
```

## 의존성

| 도구 | 설치 | 용도 |
|------|------|------|
| typst | `brew install typst` | Typst → PDF 컴파일 |
| pandoc | `brew install pandoc` | Markdown → Typst 변환 |
| npx @mermaid-js/mermaid-cli | Node.js 필요 | Mermaid → PNG 렌더링 |

## 주요 파일

| 파일 | 역할 |
|------|------|
| `book/build_pdf_typst.py` | 빌드 스크립트 |
| `book/templates/book.typ` | Typst 조판 템플릿 |
| `book/ConnectHR_통합본.typ` | 생성된 Typst 소스 |
| `book/book_ConnectHR_통합본_typst.pdf` | 최종 PDF |

## WeasyPrint 버전과의 차이

기존 `build_pdf.py`(WeasyPrint)는 별도로 보존됩니다.

| 항목 | WeasyPrint | Typst |
|------|-----------|-------|
| 코드 하이라이팅 | 단색 | 구문별 색상 |
| 자동 목차 | 불가 | `outline()` 내장 |
| 교차참조 | 불가 | `@label` 지원 |
| 페이지 나눔 | CSS 부분 지원 | 정밀 제어 |
| 폰트 | file:// 절대경로 | --font-path 플래그 |
| 빌드 속도 | 느림 | 빠름 |

## 참고

상세 가이드: `references/build-guide.md`
