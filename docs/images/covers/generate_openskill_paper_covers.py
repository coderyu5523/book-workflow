#!/usr/bin/env python3
"""오픈스킬 IT 입문 시리즈 종이책 표지 펼침면 생성 (46배판 188x254mm, 날개 없는 무선제본)

앞표지는 전자책 표지(generate_openskill_covers.py)와 같은 디자인을 종이책 크기로 다시 그린다.
뒷표지·책등·ISBN 바코드·재단 가이드는 여기서 새로 그린다.

사용법:
    PYTHONUTF8=1 python docs/images/covers/generate_openskill_paper_covers.py --book Springboot [--spine-mm 9.0]

펼침면 가로 = 도련3 + 뒷표지188 + 책등 + 앞표지188 + 도련3, 세로 = 도련3 + 254 + 도련3 (mm). 300dpi.
책등 두께: --spine-mm 로 직접 주거나, 생략하면 .build/pdf-b5/*(B5).pdf 쪽수로 추정한다
  (쪽수/2 x --leaf-mm, 기본 0.1mm = 80g 모조지 가정). 인쇄소가 알려 주는 값으로 교체할 것.

출력(projects/<책>/assets/paper-cover/):
  cover-paper-spread.png        인쇄용 펼침면(가이드 없음)
  cover-paper-spread.pdf        같은 그림을 실제 mm 크기 쪽으로 만든 PDF
  cover-paper-spread-guide.png  재단선·책등선·치수를 덧그린 확인용

뒷표지 문구는 book/출판등록-책소개.txt(첫 줄=한 줄 요약, 나머지=소개)가 있으면 그것을 쓰고,
없으면 아래 DRAFT_BLURBS 의 초안을 쓴다. ISBN·정가는 book/colophon.json 에서 읽는다.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/pub-studio/references/scripts"))
sys.path.insert(0, str(HERE))
import cover_generator as cg  # noqa: E402

TRIM_W_MM, TRIM_H_MM, BLEED_MM = 188, 254, 3
DPI = 300
DEFAULT_SPINE_MM = 9.0

DARK, MID, GRAY, LIGHT = (30, 30, 30), (90, 90, 90), (120, 120, 120), (170, 170, 170)

# 출판 등록용 책소개 초안. book/출판등록-책소개.txt 가 생기면 그 파일이 우선한다.
DRAFT_BLURBS = {
    "특이점이-온-개발자-Springboot": (
        "게시판을 만들며 배우는 Spring Boot 입문서",
        #  (줄바꿈 금지 공백)로 영문 용어가 줄 끝에서 갈라지지 않게 한다
        "이 책은 자바는 배웠지만 Spring Boot는 처음인 입문자를 위한 책이다. "
        "리플렉션으로 스프링이 동작하는 뼈대를 직접 구현해 본 뒤, 게시판을 만들며 "
        "REST API와 JPA, 예외 처리와 DTO, JWT 인증, 연관관계 매핑까지 다룬다. "
        "개념은 이야기와 비유로 먼저 풀고, 단계마다 코드를 직접 작성하며 확인한다. "
        "책을 마치면 하나의 웹 서비스가 완성되는 전체 흐름을 이해할 수 있다.",
    ),
}


def px(mm: float) -> int:
    return round(mm * DPI / 25.4)


def set_geometry(spine_mm: float) -> None:
    """엔진(cover_generator)의 치수 상수를 이번 규격으로 바꾼다. 엔진 함수들은 호출 때마다
    모듈 전역을 읽으므로, 엔진을 쓰는 모듈(generate_openskill_covers)을 import 하기 전에 호출한다."""
    cg.FLAP = 0
    cg.BACK = cg.FRONT = px(TRIM_W_MM)
    cg.SPINE = px(spine_mm)
    cg.BLEED = px(BLEED_MM)
    cg.W = cg.BLEED + cg.BACK + cg.SPINE + cg.FRONT + cg.BLEED
    cg.H = px(TRIM_H_MM) + 2 * cg.BLEED
    cg.X_FRONT = cg.BLEED + cg.BACK + cg.SPINE


# ---------------------------------------------------------------- 글 배치

def wrap(d, text: str, font, max_w: int) -> list[str]:
    """어절 단위로 줄바꿈한다. 한 어절이 한 줄보다 길면 글자 단위로 자른다."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if cg._tw(d, trial, font) <= max_w:
            cur = trial
            continue
        if cur:
            lines.append(cur)
        cur = ""
        for ch in word:
            if cg._tw(d, cur + ch, font) > max_w and cur:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- EAN-13 바코드

_L = ["0001101", "0011001", "0010011", "0111101", "0100011",
      "0110001", "0101111", "0111011", "0110111", "0001011"]
_G = ["0100111", "0110011", "0011011", "0100001", "0011101",
      "0111001", "0000101", "0010001", "0001001", "0010111"]
_R = ["1110010", "1100110", "1101100", "1000010", "1011100",
      "1001110", "1010000", "1000100", "1001000", "1110100"]
_PARITY = ["LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG",
           "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"]


def ean13_check(d12: str) -> int:
    s = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(d12))
    return (10 - s % 10) % 10


def ean13_modules(d13: str) -> str:
    """95모듈 비트열(1=검은 막대)."""
    parity = _PARITY[int(d13[0])]
    bits = "101"
    for i, ch in enumerate(d13[1:7]):
        bits += (_L if parity[i] == "L" else _G)[int(ch)]
    bits += "01010"
    for ch in d13[7:13]:
        bits += _R[int(ch)]
    return bits + "101"


def draw_barcode(img, d, isbn: str, right: int, bottom: int):
    """오른쪽 아래 모서리(right, bottom)에 맞춰 ISBN 바코드(흰 바탕)를 그린다. 영역 (x0,y0,x1,y1) 반환."""
    digits = isbn.replace("-", "")
    if len(digits) != 13 or ean13_check(digits[:12]) != int(digits[12]):
        raise ValueError(f"ISBN 검증 실패(체크숫자 불일치): {isbn}")
    mod = 4                                  # 1모듈 4px = 0.339mm (표준 0.33mm의 약 103%)
    bar_h, guard_ext = px(21), px(1.5)
    quiet_l, quiet_r = 11 * mod, 7 * mod
    num_h = px(3.4)
    f_num = cg._font(3.4)
    pad = px(2)
    w = quiet_l + 95 * mod + quiet_r
    h = bar_h + guard_ext + num_h + pad * 2
    x0, y0 = right - w - pad, bottom - h
    d.rectangle([x0, y0, right, bottom], fill=(255, 255, 255))
    bx, by = x0 + pad + quiet_l, y0 + pad
    bits = ean13_modules(digits)
    guards = set(range(0, 3)) | set(range(45, 50)) | set(range(92, 95))
    for i, b in enumerate(bits):
        if b == "1":
            hh = bar_h + (guard_ext if i in guards else 0)
            d.rectangle([bx + i * mod, by, bx + (i + 1) * mod - 1, by + hh - 1], fill=(0, 0, 0))
    ty = by + bar_h + guard_ext
    d.text((bx - quiet_l // 2 - cg._tw(d, digits[0], f_num) // 2, ty), digits[0], fill=(0, 0, 0), font=f_num)
    for half, (a, b2) in enumerate([(1, 7), (7, 13)]):
        s = digits[a:b2]
        x_start = bx + (3 if half == 0 else 50) * mod
        span = 42 * mod
        step = span / 6
        for k, ch in enumerate(s):
            cx = x_start + step * (k + 0.5)
            d.text((cx - cg._tw(d, ch, f_num) / 2, ty), ch, fill=(0, 0, 0), font=f_num)
    return (x0, y0, right, bottom)


# ---------------------------------------------------------------- 패널 그리기

def draw_back(img, d, headline: str, body: str, isbn: str, price: str):
    left = cg.BLEED                       # 뒷표지 재단선 왼쪽
    right = cg.BLEED + cg.BACK            # 뒷표지 재단선 오른쪽(책등 쪽)
    top = cg.BLEED
    bottom = cg.H - cg.BLEED
    lm, rm = left + px(12), right - px(12)   # 앞표지(엔진)의 좌우 12mm 격자와 맞춘다
    max_w = rm - lm

    d.text((lm, top + px(24)), "OPENSKILL  IT  STARTER", fill=MID, font=cg._font(5, True))
    d.text((lm, top + px(32)), "오픈스킬 IT 입문", fill=LIGHT, font=cg._font(4.2, True))
    d.rectangle([lm, top + px(41), lm + px(22), top + px(41) + px(0.9)], fill=DARK)

    y = top + px(52)
    head_mm = 8.2                          # 한 줄에 들어갈 때까지 줄인다(6.8mm 아래로는 줄바꿈)
    while head_mm > 6.8 and cg._tw(d, headline, cg._font(head_mm, True)) > max_w:
        head_mm = round(head_mm - 0.2, 1)
    f_head = cg._font(head_mm, True)
    for line in wrap(d, headline, f_head, max_w):
        d.text((lm, y), line, fill=DARK, font=f_head)
        y += px(head_mm * 1.35)

    y += px(8)
    f_body = cg._font(4.3)
    for para in body.split("\n"):
        for line in wrap(d, para, f_body, max_w):
            d.text((lm, y), line, fill=(70, 70, 70), font=f_body)
            y += px(4.3 * 1.85)
        y += px(3)

    # 하단 좌: 출판사(앞표지 하단 문구와 같은 높이·크기) / 우: 정가 + 바코드
    d.text((lm, cg.H - px(25)), "OPENSKILL BOOKS", fill=(160, 160, 160), font=cg._font(7, True))
    d.text((lm, cg.H - px(17)), "오픈스킬북스", fill=(180, 180, 180), font=cg._font(6))

    bc = draw_barcode(img, d, isbn, rm, bottom - px(14))
    f_price = cg._font(4.4, True)
    pt = f"정가 {price}"
    d.text((rm - cg._tw(d, pt, f_price), bc[1] - px(9)), pt, fill=(60, 60, 60), font=f_price)
    return bc


def draw_spine(img, spine_title: str, spine_sub: str, publisher: str):
    """책등 글씨는 위에서 아래로 읽는다(시계 방향 90도)."""
    sp = cg.SPINE
    tmp = Image.new("RGBA", (cg.H, sp), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    f_t = cg._font(3.5, True)
    f_s = cg._font(3.3)
    f_p = cg._font(2.9, True)
    y_mid = sp // 2
    x = cg.BLEED + px(20)
    td.text((x, y_mid), spine_title, fill=DARK, font=f_t, anchor="lm")
    x += int(td.textlength(spine_title, font=f_t)) + px(4)
    td.text((x, y_mid), spine_sub, fill=GRAY, font=f_s, anchor="lm")
    pw = int(td.textlength(publisher, font=f_p))
    td.text((cg.H - cg.BLEED - px(18) - pw, y_mid), publisher, fill=(150, 150, 150), font=f_p, anchor="lm")
    rot = tmp.rotate(-90, expand=True)
    img.paste(rot, (cg.X_FRONT - cg.SPINE, 0), rot)


def dashed(d, p0, p1, color, dash=14, gap=10, width=2):
    (x0, y0), (x1, y1) = p0, p1
    if x0 == x1:
        for y in range(int(y0), int(y1), dash + gap):
            d.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
    else:
        for x in range(int(x0), int(x1), dash + gap):
            d.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)


def guide_overlay(img, spine_mm: float, spine_note: str, barcode_box):
    """재단선(파랑)·책등선(초록)·안전선(연한 점선)·치수를 덧그린 확인용 이미지(아래에 설명 띠를 붙인다)."""
    g = img.copy()
    d = ImageDraw.Draw(g)
    B, W, H = cg.BLEED, cg.W, cg.H
    blue, green, safe = (40, 70, 200), (30, 160, 60), (225, 150, 150)
    dashed(d, (B, 0), (B, H), blue); dashed(d, (W - B, 0), (W - B, H), blue)
    dashed(d, (0, B), (W, B), blue); dashed(d, (0, H - B), (W, H - B), blue)
    xs1, xs2 = B + cg.BACK, B + cg.BACK + cg.SPINE
    dashed(d, (xs1, 0), (xs1, H), green); dashed(d, (xs2, 0), (xs2, H), green)
    s = px(6)
    for x0, x1 in [(B + s, xs1 - s), (xs2 + s, W - B - s)]:
        dashed(d, (x0, B + s), (x0, H - B - s), safe, 8, 8, 1)
        dashed(d, (x1, B + s), (x1, H - B - s), safe, 8, 8, 1)
    dashed(d, (B + s, B + s), (xs1 - s, B + s), safe, 8, 8, 1)
    dashed(d, (B + s, H - B - s), (xs1 - s, H - B - s), safe, 8, 8, 1)
    dashed(d, (xs2 + s, B + s), (W - B - s, B + s), safe, 8, 8, 1)
    dashed(d, (xs2 + s, H - B - s), (W - B - s, H - B - s), safe, 8, 8, 1)
    if barcode_box:
        d.rectangle(barcode_box, outline=(200, 60, 60), width=3)
    f = cg._font(4.2, True)
    d.text((B + px(6), B + px(6)), "뒷표지 (Back)", fill=blue, font=f)
    d.text((xs2 + px(6), B + px(6)), "앞표지 (Front)", fill=blue, font=f)

    strip = px(16)
    out = Image.new("RGB", (W, H + strip), (255, 255, 255))
    out.paste(g, (0, 0))
    od = ImageDraw.Draw(out)
    fs = cg._font(3.6)
    total_w = 2 * BLEED_MM + 2 * TRIM_W_MM + spine_mm
    od.text((B, H + px(3)),
            f"펼침면 {total_w:g} x {TRIM_H_MM + 2 * BLEED_MM}mm = 도련 {BLEED_MM} + 뒷표지 {TRIM_W_MM} + 책등 {spine_mm:g} + 앞표지 {TRIM_W_MM} + 도련 {BLEED_MM}"
            f"  |  재단 {TRIM_W_MM} x {TRIM_H_MM}mm (46배판, 날개 없음)  |  파랑=재단선 초록=책등선 연한점선=안전선(재단선 6mm 안쪽) 빨강=바코드",
            fill=(60, 60, 60), font=fs)
    od.text((B, H + px(9.5)), spine_note, fill=(200, 60, 60), font=fs)
    return out


# ---------------------------------------------------------------- 메인

def estimate_spine(project: Path, leaf_mm: float):
    pdfs = sorted((project / ".build" / "pdf-b5").glob("*(B5).pdf"))
    if not pdfs:
        return DEFAULT_SPINE_MM, f"책등 {DEFAULT_SPINE_MM}mm는 임시값(내지 PDF 없음). 인쇄소 값으로 교체"
    import fitz
    with fitz.open(str(pdfs[-1])) as doc:
        pages = doc.page_count
    mm_ = round(pages / 2 * leaf_mm, 1)
    return mm_, f"책등 {mm_}mm는 추정값(내지 {pages}쪽 / 2 x 쪽당 {leaf_mm}mm). 용지·인쇄소 계산값으로 교체"


def load_text(project: Path):
    name = project.name
    f = project / "book" / "출판등록-책소개.txt"
    if f.exists():
        parts = [p.strip() for p in f.read_text(encoding="utf-8").strip().split("\n\n")]
        return parts[0], "\n".join(parts[1:]), f"출판등록-책소개.txt"
    if name in DRAFT_BLURBS:
        return *DRAFT_BLURBS[name], "초안(DRAFT_BLURBS)"
    raise SystemExit(f"[!] 뒷표지 문구 없음: {f} 를 만들거나 DRAFT_BLURBS 에 추가하세요")


def main() -> int:
    ap = argparse.ArgumentParser(description="오픈스킬 IT 입문 종이책 표지 펼침면(46배판, 날개 없음)")
    ap.add_argument("--book", required=True, help="책 폴더 이름의 일부(예: Springboot)")
    ap.add_argument("--spine-mm", type=float, default=None, help="책등 두께(mm). 생략하면 쪽수로 추정")
    ap.add_argument("--leaf-mm", type=float, default=0.1, help="추정용 종이 한 장 두께(mm), 기본 0.1")
    args = ap.parse_args()

    cands = [p for p in (ROOT / "projects").iterdir() if p.is_dir() and args.book in p.name]
    if len(cands) != 1:
        print(f"[!] --book '{args.book}' 에 맞는 책이 {len(cands)}권: {[c.name for c in cands]}")
        return 1
    project = cands[0]

    if args.spine_mm is not None:
        spine_mm, spine_note = args.spine_mm, f"책등 {args.spine_mm:g}mm는 지정값"
    else:
        spine_mm, spine_note = estimate_spine(project, args.leaf_mm)

    set_geometry(spine_mm)
    import generate_openskill_covers as eb  # noqa: E402  (치수 설정 뒤에 import: 모듈 상수가 그 값을 따른다)

    spec = eb.BOOKS[project.name]
    colophon = json.loads((project / "book" / "colophon.json").read_text(encoding="utf-8"))
    headline, body, text_src = load_text(project)

    img = Image.new("RGB", (cg.W, cg.H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # 앞표지: 전자책과 같은 디자인을 원본 해상도(188x254mm)로 그려 붙인다. 도련은 흰 바탕이라 흰색 그대로 둔다
    front = cg._render_single(eb._cfg(colophon["authors"]), spec["main"], shadow_map=spec["shadow"])
    eb.draw_series(front)
    eb.draw_subtitle(front, spec["subtitle"])
    spec["emblem"](front, eb.band_center(front))
    img.paste(front, (cg.X_FRONT, cg.BLEED))

    bc = draw_back(img, d, headline, body, colophon["isbn"], colophon["price"])
    draw_spine(img, "오픈스킬 IT 입문", spec["subtitle"], "오픈스킬북스")

    out_dir = project / "assets" / "paper-cover"
    out_dir.mkdir(parents=True, exist_ok=True)
    img.save(out_dir / "cover-paper-spread.png", dpi=(DPI, DPI))
    img.save(out_dir / "cover-paper-spread.pdf", "PDF", resolution=float(DPI))
    guide_overlay(img, spine_mm, spine_note, bc).save(out_dir / "cover-paper-spread-guide.png", dpi=(DPI, DPI))

    print(f"[OK] {out_dir}")
    print(f"     펼침면 {cg.W}x{cg.H}px = {cg.W * 25.4 / DPI:.1f}x{cg.H * 25.4 / DPI:.1f}mm ({DPI}dpi)")
    print(f"     {spine_note}")
    print(f"     뒷표지 문구: {text_src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
