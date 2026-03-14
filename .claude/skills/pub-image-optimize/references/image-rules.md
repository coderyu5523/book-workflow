# 이미지 규칙 상세

## Autocrop 알고리즘

```python
from PIL import Image, ImageChops

img = Image.open(path).convert("RGB")
bg = Image.new("RGB", img.size, (255, 255, 255))  # 흰색 배경 가정
diff = ImageChops.difference(img, bg)
bbox = diff.getbbox()  # 콘텐츠 영역 바운딩 박스
```

### 파라미터

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `padding` | 6px | 잘린 영역 주변에 유지할 여백 |
| 최소 트림 | 20px | 상하 합계 20px 이상일 때만 잘라냄 |

### 주의사항

- 흰색 배경(`#FFFFFF`) 기준으로만 동작. 투명 배경이나 색상 배경 이미지는 효과 없음
- 원본 파일을 **직접 수정**(덮어쓰기). 원본 보존 필요시 백업 후 실행
- PNG 형식만 지원 (JPEG도 가능하지만 재압축 손실 발생)

## auto-image Typst 함수

### 함수 시그니처

```typst
#let auto-image(
  path,              // 이미지 파일 절대경로
  alt: none,         // 캡션 텍스트 (content 타입)
  max-width: 0.7,    // 최대 너비 비율 (0.0 ~ 1.0)
) = ...
```

### 크기 결정 로직

```
1. target-width = 콘텐츠 영역 너비 × max-width
2. 이미지를 target-width로 렌더링했을 때의 높이 측정
3. 필요 높이 = 이미지 높이 + 캡션 높이(28pt) + 여백(24pt)

조건 분기:
  IF 필요 높이 > 남은 공간 AND 남은 공간 > 120pt:
    축소 비율 = (남은 공간 - 캡션 - 여백) / 이미지 높이
    IF 축소 비율 >= 0.5:
      → target-width × 축소 비율로 축소
    ELSE:
      → 원래 크기 유지 (다음 페이지로 이동)
  ELSE:
    → target-width 그대로 사용
```

### Pandoc 출력 → auto-image 변환

빌드 스크립트의 `fix_typst_content()`에서 처리:

| Pandoc 출력 | 변환 결과 |
|------------|----------|
| `!#link("path")[alt]` | `#auto-image("path", alt: [alt], max-width: N)` |
| `#box(image("path"))` | `#auto-image("path", max-width: N)` |

## 이미지 유형 판별

`_detect_image_max_width(path)` 함수가 파일 경로의 **패턴 매칭**으로 유형 결정.
Mermaid 이미지는 `_get_image_aspect_ratio()`로 렌더링된 PNG의 종횡비를 읽어 자동 분기:

```python
def _get_image_aspect_ratio(path: str) -> float | None:
    from PIL import Image
    img = Image.open(path)
    w, h = img.size
    return w / h if h > 0 else None

def _detect_image_max_width(path: str) -> str:
    if 'chapter-opening' in path:    return '0.5'
    elif 'mermaid_' in path:
        ar = _get_image_aspect_ratio(path)
        if ar is not None:
            if ar > 2.0:   return '0.75'  # 가로형 (flowchart LR 등)
            elif ar > 1.0: return '0.55'  # 정사각형~약간 가로
            else:          return '0.45'  # 세로형 (flowchart TD 등)
        return '0.55'  # fallback
    elif any(x in path for x in ['step1', 'step2', 'step3', 'step4']):
        return '0.65'
    else:
        return '0.6'
```

### Mermaid 종횡비 기준

| 종횡비 (W/H) | 분류 | max-width | 예시 |
|-------------|------|-----------|------|
| > 2.0 | 가로형 | 0.75 | `flowchart LR` 5노드, 실습 순서 |
| 1.0 ~ 2.0 | 중간 | 0.55 | `flowchart TD` + `direction LR` subgraph |
| < 1.0 | 세로형 | 0.45 | `flowchart TD` 깊은 트리 |

### 새 유형 추가 방법

1. `_detect_image_max_width()`에 패턴 추가
2. 이미지 파일명에 해당 패턴 포함
3. 예: 관리자 화면 캡처 → `'admin-ui' in path: return '0.55'`
