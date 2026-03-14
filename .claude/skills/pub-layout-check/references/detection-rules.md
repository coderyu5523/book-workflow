# 레이아웃 감지 규칙 상세

## 페이지 설정 상수

| 항목 | 값 | 비고 |
|------|-----|------|
| 용지 | A4 (210 × 297mm) | 841.89pt 높이 |
| 상단 여백 | 28mm (79.37pt) | 헤더 공간 포함 |
| 하단 여백 | 25mm (70.87pt) | 푸터 공간 포함 |
| 좌우 여백 | 22mm (62.36pt) | — |
| 콘텐츠 영역 높이 | ~691.65pt | 상하 여백 제외 |

## 헤더/푸터 필터링

PyMuPDF(fitz)의 `get_text("dict")`는 헤더/푸터 텍스트도 블록으로 반환.
콘텐츠 영역 내 블록만 분석 대상:

```python
content_top = TOP_MARGIN_PT      # 79.37pt
content_bottom = A4_HEIGHT_PT - BOTTOM_MARGIN_PT  # 771.02pt

# ±5pt 허용오차로 필터링
text_blocks = [b for b in blocks
    if b["type"] == 0
    and b["bbox"][1] >= content_top - 5
    and b["bbox"][3] <= content_bottom + 5]
```

## 건너뛸 페이지

표지(p1)와 목차(p2)는 분석 제외. `SKIP_PAGES = {1, 2}`

## 감지 규칙 상세

### 1. 빈 페이지 (severity: high)

**조건**: 콘텐츠 영역 내 텍스트·이미지 블록이 하나도 없음
**원인**:
- `pagebreak(weak: true)` 중복 (heading show rule + 수동 pagebreak)
- `#heading`이 heading show rule을 트리거 (TOC 등)
**해결**: heading show rule에서 pagebreak 조건 확인, 불필요한 수동 pagebreak 제거

### 2. 고아 콘텐츠 (severity: high)

**조건**: 텍스트 ≤4줄 AND 하단 빈 공간 50%+ AND 이미지 없음
**원인**:
- 이전 섹션의 마지막 1~3줄이 다음 페이지로 넘어감
- 다음 섹션이 pagebreak로 시작하여 고아 줄 뒤에 빈 공간 발생
**해결 전략** (page-fit 스킬 참조):
1. 이전 페이지 콘텐츠를 약간 줄여서 고아 줄을 이전 페이지로 당기기
2. 다음 섹션의 pagebreak를 제거하여 이어붙이기
3. 이전 페이지의 이미지/코드 크기를 약간 줄여 공간 확보

### 3. 낮은 사용률 (severity: medium)

**조건**: 콘텐츠 사용률 45% 미만 AND 텍스트 4줄 초과
**원인**: 큰 이미지나 코드 블록이 다음 페이지로 밀림
**해결**: image-optimize 스킬로 이미지 크기 조절, 또는 코드 블록 앞뒤 텍스트 조정

### 4. 과대 이미지 (severity: medium)

**조건**: 단일 이미지가 콘텐츠 영역의 70%+ 차지
**원인**: auto-image의 max-width가 너무 큼, 또는 이미지 자체가 세로로 긺
**해결**: `_detect_image_max_width()`의 해당 유형 max-width 축소

### 5. 밀림 패턴 (severity: medium)

**조건**: 이전 페이지 55% 미만 사용 AND 다음 페이지에 이미지 시작
**원인**: 이미지가 이전 페이지의 남은 공간에 안 들어가서 다음 페이지로 이동
**해결**: auto-image의 `layout()` 함수가 자동 축소하거나, max-width 조절

## 심각도 기준

| 심각도 | 마커 | 의미 | 자동 수정 가능 |
|--------|------|------|:------------:|
| high | `[!]` | 반드시 수정 필요 | 일부 |
| medium | `[~]` | 개선 권장 | 가능 |
| low | `[.]` | 참고 사항 | — |
