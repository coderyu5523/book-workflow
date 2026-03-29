#!/usr/bin/env python3
"""표지 자동 생성 — CONFIG에서 데이터를 받아 앞표지 PNG 생성

사용법:
    from cover_generator import generate_front_cover
    cover_path = generate_front_cover(config, output_dir)

CONFIG 필수 키:
    title:    str — 책 제목
    subtitle: str — 부제목

CONFIG 선택 키 (cover_data dict):
    series:      str — 시리즈명 (예: "특이점이 온 개발자")
    series_sub:  str — 시리즈 서브 (예: "개념편")
    authors:     str — 저자 (예: "최주호, 류재성, 김주혁")
    badges:      list[str] — 키워드 배지
    publisher:   str — 출판사명
    accent_color: tuple — RGB 액센트 컬러 (예: (180, 120, 30))
    top_descs:   list[str] — 상단 설명 텍스트
    main_words:  list[tuple] — 메인 타이틀 큰 글씨 [(text, size_mm, bold, align, x_off, color_key), ...]
    back_desc:   list[str] — 뒷표지 설명 텍스트
"""
from __future__ import annotations

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DPI = 300
MM = DPI / 25.4

# B5 기준 치수
FLAP = int(80 * MM)
BACK = int(182 * MM)
SPINE = int(9 * MM)
FRONT = int(182 * MM)
BLEED = int(3 * MM)
W = BLEED + FLAP + BACK + SPINE + FRONT + FLAP + BLEED
H = int(257 * MM) + 2 * BLEED

X_BFLAP = BLEED
X_BACK = BLEED + FLAP
X_SPINE = BLEED + FLAP + BACK
X_FRONT = BLEED + FLAP + BACK + SPINE
X_FFLAP = BLEED + FLAP + BACK + SPINE + FRONT

# 폰트 디렉토리 — generate_spreads_v4_5.py와 같은 위치의 fonts/ 사용
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "docs", "images", "covers", "fonts")
_FONT_DIR = os.path.normpath(_FONT_DIR)


def _mm(v):
    return int(v * MM)


def _font(size_mm, bold=False):
    px = _mm(size_mm)
    if bold:
        names = ["Pretendard-Bold.otf", "Pretendard-SemiBold.otf"]
    else:
        names = ["Pretendard-Regular.otf", "Pretendard-SemiBold.otf"]
    for name in names:
        p = os.path.join(_FONT_DIR, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, px)
            except Exception:
                continue
    for p in ["/System/Library/Fonts/AppleSDGothicNeo.ttc"]:
        try:
            return ImageFont.truetype(p, px, index=(5 if bold else 0))
        except Exception:
            continue
    return ImageFont.load_default()


def _tw(d, text, font):
    bb = d.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


def _th(d, text, font):
    bb = d.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]


def _build_cover_data(config: dict) -> dict:
    """CONFIG에서 표지 데이터 추출. cover_data가 있으면 우선 사용."""
    cd = config.get("cover_data", {})
    title = config.get("title", "")
    subtitle = config.get("subtitle", "")

    # 제목에서 메인 단어 자동 추출 (cover_data에 main_words가 없을 때)
    if "main_words" not in cd:
        # 제목을 2줄로 나눔
        words = title.split()
        if len(words) >= 2:
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            main_words = [
                (line1, 40, True, "L", -2, "dark"),
                (line2, 40, True, "R", 0, "gray"),
            ]
        else:
            main_words = [(title, 50, True, "L", -2, "dark")]
    else:
        main_words = cd["main_words"]

    return {
        "series": cd.get("series", ""),
        "series_sub": cd.get("series_sub", ""),
        "authors": cd.get("authors", ""),
        "badges": cd.get("badges", []),
        "publisher": cd.get("publisher", "오픈스킬북스"),
        "accent_color": cd.get("accent_color", (45, 99, 235)),
        "top_descs": cd.get("top_descs", []),
        "main_words": main_words,
        "tagline": subtitle,
        "back_desc": cd.get("back_desc", []),
        "title": title,
        "subtitle": subtitle,
    }


def _render_front_cover(d, data: dict):
    """앞표지 영역에 콘텐츠 렌더링"""
    c1 = data["accent_color"]
    fx = X_FRONT
    LM = fx + _mm(12)
    RM = fx + FRONT - _mm(12)

    # 상단 설명
    f_top = _font(5.5)
    top_y = _mm(12)
    for desc_line in data["top_descs"]:
        dw = _tw(d, desc_line, f_top)
        d.text((RM - dw, top_y), desc_line, fill=(140, 140, 140), font=f_top)
        top_y += _th(d, desc_line, f_top) + _mm(2)

    # 시리즈 타이포 "특이점이 온 개발자"
    series = data["series"]
    if series:
        f_big = _font(28, bold=True)
        f_mid = _font(16, bold=True)
        f_dev = _font(24, bold=True)

        x_cur = LM
        y_line1 = _mm(35)
        d.text((x_cur, y_line1), "특", fill=(30, 30, 30), font=f_big)
        x_cur += _tw(d, "특", f_big) + _mm(0.5)
        baseline_offset = _mm(28) - _mm(16)
        d.text((x_cur, y_line1 + baseline_offset), "이점이", fill=(80, 80, 80), font=f_mid)
        x_cur += _tw(d, "이점이", f_mid) + _mm(4)
        d.text((x_cur, y_line1), "온", fill=(30, 30, 30), font=f_big)
        y_line2 = y_line1 + _mm(30)
        d.text((LM, y_line2), "개발자", fill=(40, 40, 40), font=f_dev)
        series_bottom = y_line2 + _mm(28)
    else:
        series_bottom = _mm(50)

    # 메인 타이틀
    max_w = RM - LM - _mm(5)
    cur_y = series_bottom
    for text, size, bold_flag, align, x_off, color_key in data["main_words"]:
        cur_size = size
        font = _font(cur_size, bold=bold_flag)
        t_w = _tw(d, text, font)
        while t_w > max_w and cur_size > 10:
            cur_size -= 2
            font = _font(cur_size, bold=bold_flag)
            t_w = _tw(d, text, font)

        fill = (30, 30, 30) if color_key == "dark" else (120, 120, 120)
        if align == "L":
            x = LM + _mm(x_off)
        elif align == "R":
            x = RM - t_w + _mm(x_off)
        else:
            x = fx + (FRONT - t_w) // 2 + _mm(x_off)

        # 그림자
        d.text((x + _mm(2.5), cur_y + _mm(2.5)), text, fill=(235, 235, 235), font=font)
        d.text((x, cur_y), text, fill=fill, font=font)
        cur_y += _mm(cur_size) + _mm(2)

    # 태그라인
    cur_y += _mm(3)
    f_tag = _font(7)
    d.text((LM, cur_y), data["tagline"], fill=(130, 130, 130), font=f_tag)

    # 배지
    badges = data["badges"]
    if badges:
        cur_y += _th(d, data["tagline"], f_tag) + _mm(5)
        f_badge = _font(3.5)
        badge_h = _mm(5)
        badge_pad_x = _mm(2.5)
        badge_gap = _mm(1.5)
        row_gap = _mm(2)
        mid = len(badges) // 2 + len(badges) % 2
        rows = [badges[:mid], badges[mid:]]
        for row in rows:
            bx = LM
            for badge_text in row:
                bw = _tw(d, badge_text, f_badge) + badge_pad_x * 2
                d.rounded_rectangle(
                    [(bx, cur_y), (bx + bw, cur_y + badge_h)],
                    radius=_mm(3), fill=(240, 243, 248), outline=(220, 225, 235),
                )
                bb = d.textbbox((0, 0), badge_text, font=f_badge)
                text_h = bb[3] - bb[1]
                ty = cur_y + (badge_h - text_h) // 2 - bb[1]
                d.text((bx + badge_pad_x, ty), badge_text, fill=(70, 85, 105), font=f_badge)
                bx += bw + badge_gap
            cur_y += badge_h + row_gap

    # 우측 하단: 서브 + 저자
    sub_text = data["series_sub"]
    if sub_text:
        f_sub = _font(16, bold=True)
        sub_w = _tw(d, sub_text, f_sub)
        sub_y = H - _mm(40)
        line_w = _mm(40)
        d.rectangle([(RM - line_w, sub_y - _mm(3)), (RM, sub_y - _mm(3) + _mm(0.8))], fill=c1)
        d.text((RM - sub_w, sub_y), sub_text, fill=c1, font=f_sub)

    f_author = _font(4)
    author_text = data["authors"] + " 지음" if data["authors"] else ""
    if author_text:
        aw = _tw(d, author_text, f_author)
        d.text((RM - aw, H - _mm(18)), author_text, fill=(130, 130, 130), font=f_author)

    # 출판사
    f_pub_name = _font(7, bold=True)
    f_pub_icon = _font(6)
    pub_y = H - _mm(25)
    d.text((LM, pub_y), "OPENSKILL BOOKS", fill=(160, 160, 160), font=f_pub_name)
    d.text((LM, pub_y + _mm(8)), data["publisher"], fill=(180, 180, 180), font=f_pub_icon)


def generate_front_cover(config: dict, output_dir: Path | str) -> Path:
    """CONFIG에서 표지 데이터를 읽어 앞표지 PNG 생성.

    Returns:
        생성된 cover.png 절대 경로
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "cover.png"

    data = _build_cover_data(config)

    # 스프레드 크기로 생성 (앞표지 영역만 사용)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    _render_front_cover(d, data)

    # 앞표지 영역만 추출
    front = img.crop((X_FRONT, BLEED, X_FRONT + FRONT, H - BLEED))
    front.save(str(output_path), dpi=(DPI, DPI))
    print(f"   표지 생성: {output_path.name} ({front.size[0]}x{front.size[1]})")
    return output_path


def generate_spread(config: dict, output_dir: Path | str) -> Path:
    """CONFIG에서 전체 스프레드(POD용) 생성. 가이드 포함.

    Returns:
        생성된 spread.png 절대 경로
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "spread.png"

    data = _build_cover_data(config)

    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    _render_front_cover(d, data)
    # TODO: 뒷표지, 책등, 날개 렌더링 추가 (현재는 앞표지만)

    img.save(str(output_path), dpi=(DPI, DPI))
    return output_path
