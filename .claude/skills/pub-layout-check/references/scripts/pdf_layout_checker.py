#!/usr/bin/env python3
"""PDF 레이아웃 자동 분석기

빌드된 PDF를 페이지별로 분석하여 레이아웃 문제를 감지하고 피드백을 제공합니다.

감지 항목:
  - 빈 페이지 (표지/목차 제외)
  - 고아 콘텐츠 (1~3줄만 넘어간 페이지)
  - 과도한 하단 공백 (40% 이상)
  - 과대 이미지 (페이지의 70% 이상)
  - 연속 빈 공간 패턴 (이미지/코드가 다음 페이지로 밀린 경우)

의존성: pip install PyMuPDF
"""

import sys
from pathlib import Path


# ── 페이지 설정 상수 (book.typ과 일치) ──
A4_HEIGHT_PT = 297 * 72 / 25.4       # 841.89pt
TOP_MARGIN_PT = 28 * 72 / 25.4       # 79.37pt
BOTTOM_MARGIN_PT = 25 * 72 / 25.4    # 70.87pt
LEFT_MARGIN_PT = 22 * 72 / 25.4      # 62.36pt
CONTENT_HEIGHT = A4_HEIGHT_PT - TOP_MARGIN_PT - BOTTOM_MARGIN_PT  # ~691.65pt

# 표지·목차로 간주할 페이지 (분석 제외)
SKIP_PAGES = {1, 2}


def analyze_layout(pdf_path: str, skip_pages: set = None) -> list[dict]:
    """PDF 레이아웃 분석 후 이슈 목록 반환"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("   [경고] PyMuPDF 미설치 → 레이아웃 분석 건너뜀 (pip install PyMuPDF)")
        return []

    if skip_pages is None:
        skip_pages = SKIP_PAGES

    doc = fitz.open(pdf_path)
    issues = []
    page_stats = []  # 페이지별 통계 (연속 패턴 분석용)

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1

        # 표지/목차 건너뛰기
        if page_num in skip_pages:
            page_stats.append({"page": page_num, "usage": 100, "skipped": True})
            continue

        # 블록 추출 (헤더/푸터 영역 제외)
        content_top = TOP_MARGIN_PT
        content_bottom = A4_HEIGHT_PT - BOTTOM_MARGIN_PT
        blocks = page.get_text("dict")["blocks"]
        # 콘텐츠 영역 내 블록만 필터링 (헤더/푸터 제외)
        text_blocks = [
            b for b in blocks
            if b["type"] == 0 and b["bbox"][1] >= content_top - 5 and b["bbox"][3] <= content_bottom + 5
        ]
        image_blocks = [
            b for b in blocks
            if b["type"] == 1 and b["bbox"][1] >= content_top - 5 and b["bbox"][3] <= content_bottom + 5
        ]

        # ── 빈 페이지 감지 ──
        if not text_blocks and not image_blocks:
            issues.append({
                "page": page_num,
                "type": "blank_page",
                "severity": "high",
                "message": f"페이지 {page_num}: 완전히 빈 페이지",
                "suggestion": "불필요한 pagebreak가 삽입되었을 수 있음. heading show rule 또는 수동 pagebreak 확인",
            })
            page_stats.append({"page": page_num, "usage": 0, "skipped": False})
            continue

        # 콘텐츠 영역 계산 (절대 좌표 기준, 상단 여백부터 측정)
        all_blocks = text_blocks + image_blocks
        max_y = max(b["bbox"][3] for b in all_blocks)
        min_y = min(b["bbox"][1] for b in all_blocks)
        content_used = max_y - content_top
        usage_pct = min((content_used / CONTENT_HEIGHT) * 100, 100)

        # 텍스트 줄 수 계산
        total_lines = sum(len(b.get("lines", [])) for b in text_blocks)

        page_stats.append({
            "page": page_num,
            "usage": usage_pct,
            "lines": total_lines,
            "max_y": max_y,
            "min_y": min_y,
            "images": len(image_blocks),
            "skipped": False,
        })

        # ── 고아 콘텐츠 감지 (1~3줄만 있는 페이지) ──
        bottom_space_pct = (A4_HEIGHT_PT - BOTTOM_MARGIN_PT - max_y) / CONTENT_HEIGHT * 100
        if total_lines <= 4 and bottom_space_pct > 50 and len(image_blocks) == 0:
            issues.append({
                "page": page_num,
                "type": "orphan_content",
                "severity": "high",
                "lines": total_lines,
                "message": f"페이지 {page_num}: {total_lines}줄만 있고 하단 {bottom_space_pct:.0f}% 빈 공간",
                "suggestion": "이전 페이지에서 약간만 줄이면 이 줄들이 이전 페이지에 들어갈 수 있음. "
                              "또는 다음 섹션의 pagebreak를 제거하여 이어붙이기",
            })

        # ── 과도한 하단 공백 (내용은 있지만 아래가 비어있음) ──
        elif usage_pct < 45 and total_lines > 4:
            issues.append({
                "page": page_num,
                "type": "low_usage",
                "severity": "medium",
                "usage": usage_pct,
                "message": f"페이지 {page_num}: 콘텐츠가 {usage_pct:.0f}%만 차지",
                "suggestion": "큰 이미지나 코드 블록이 다음 페이지로 밀렸을 수 있음. "
                              "이미지 크기를 줄이거나 콘텐츠 배치 조정",
            })

        # ── 과대 이미지 감지 ──
        for img_block in image_blocks:
            img_height = img_block["bbox"][3] - img_block["bbox"][1]
            img_usage = img_height / CONTENT_HEIGHT * 100
            if img_usage > 70:
                issues.append({
                    "page": page_num,
                    "type": "large_image",
                    "severity": "medium",
                    "img_usage": img_usage,
                    "message": f"페이지 {page_num}: 이미지가 페이지의 {img_usage:.0f}% 차지",
                    "suggestion": "auto-image의 max-width를 줄이거나, 이미지 자체를 리사이즈",
                })

    # ── 연속 패턴 분석 ──
    for i in range(1, len(page_stats)):
        prev = page_stats[i - 1]
        curr = page_stats[i]
        if prev.get("skipped") or curr.get("skipped"):
            continue

        # 패턴: 이전 페이지 하단 40%+ 빈 공간 → 현재 페이지 상단에 큰 이미지/코드
        if prev.get("usage", 100) < 55 and curr.get("images", 0) > 0:
            issues.append({
                "page": prev["page"],
                "type": "push_pattern",
                "severity": "medium",
                "message": f"페이지 {prev['page']}~{curr['page']}: "
                           f"이전 페이지 {prev['usage']:.0f}% 사용 후 다음 페이지에 이미지 시작",
                "suggestion": "이미지가 이전 페이지에 안 들어가서 밀린 패턴. "
                              "auto-image가 자동 축소하거나, 이미지 전 텍스트를 조정",
            })

    doc.close()
    return issues


def print_report(issues: list[dict], pdf_path: str = ""):
    """분석 결과 보고서 출력"""
    if pdf_path:
        print(f"\n   PDF 레이아웃 분석: {Path(pdf_path).name}")

    if not issues:
        print("   레이아웃 이슈 없음")
        return []

    print(f"   {len(issues)}개 이슈 발견")
    print("   " + "-" * 55)

    severity_order = {"high": 0, "medium": 1, "low": 2}
    sorted_issues = sorted(issues, key=lambda x: (severity_order.get(x["severity"], 3), x["page"]))

    for issue in sorted_issues:
        marker = {"high": "[!]", "medium": "[~]", "low": "[.]"}.get(issue["severity"], "[ ]")
        print(f"   {marker} {issue['message']}")
        print(f"       -> {issue['suggestion']}")

    print("   " + "-" * 55)
    high = sum(1 for i in issues if i["severity"] == "high")
    medium = sum(1 for i in issues if i["severity"] == "medium")
    low = sum(1 for i in issues if i["severity"] == "low")
    parts = []
    if high:
        parts.append(f"심각 {high}")
    if medium:
        parts.append(f"주의 {medium}")
    if low:
        parts.append(f"참고 {low}")
    print(f"   요약: {' / '.join(parts)}")

    return sorted_issues


def print_page_usage(pdf_path: str, skip_pages: set = None):
    """전체 페이지 사용률 시각화"""
    try:
        import fitz
    except ImportError:
        return

    if skip_pages is None:
        skip_pages = SKIP_PAGES

    doc = fitz.open(pdf_path)
    print(f"\n   페이지별 사용률 ({len(doc)}페이지)")
    print("   " + "-" * 55)

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1

        if page_num in skip_pages:
            print(f"   p{page_num:02d} [표지/목차]")
            continue

        content_top = TOP_MARGIN_PT
        content_bottom = A4_HEIGHT_PT - BOTTOM_MARGIN_PT
        blocks = page.get_text("dict")["blocks"]
        all_blocks = [
            b for b in blocks
            if b["type"] in (0, 1)
            and b["bbox"][1] >= content_top - 5
            and b["bbox"][3] <= content_bottom + 5
        ]

        if not all_blocks:
            bar = " " * 40
            print(f"   p{page_num:02d} |{bar}|   0%  <<<빈 페이지>>>")
            continue

        max_y = max(b["bbox"][3] for b in all_blocks)
        min_y = min(b["bbox"][1] for b in all_blocks)
        usage = (max_y - min_y) / CONTENT_HEIGHT * 100
        usage = min(usage, 100)

        bar_len = int(usage / 100 * 40)
        bar = "#" * bar_len + "." * (40 - bar_len)

        flag = ""
        if usage < 30:
            flag = "  <<<고아>>>"
        elif usage < 50:
            flag = "  <<빈 공간>>"

        print(f"   p{page_num:02d} |{bar}| {usage:3.0f}%{flag}")

    doc.close()
    print("   " + "-" * 55)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 pdf_layout_checker.py <pdf_path>")
        print("  PDF를 분석하여 레이아웃 문제를 감지합니다.")
        sys.exit(1)

    pdf_file = sys.argv[1]
    if not Path(pdf_file).exists():
        print(f"[오류] 파일 없음: {pdf_file}")
        sys.exit(1)

    # 페이지 사용률 시각화
    print_page_usage(pdf_file)

    # 이슈 분석
    issues = analyze_layout(pdf_file)
    print_report(issues, pdf_file)
