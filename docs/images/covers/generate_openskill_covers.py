#!/usr/bin/env python3
"""오픈스킬 IT 입문 시리즈 전자책 표지 생성 (Spring Boot · MSA · Docker & Kubernetes)

사용법:
    PYTHONUTF8=1 python docs/images/covers/generate_openskill_covers.py [출력폴더]

출력폴더를 주지 않으면 각 책의 projects/<책>/assets/cover.jpg 에 바로 저장한다.
엔진은 .claude/skills/pub-studio/references/scripts/cover_generator.py 를 쓴다.
750×1110px, 72ppi JPEG.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/pub-studio/references/scripts"))
import cover_generator as cg  # noqa: E402

DARK = (30, 30, 30)
GRAY = (120, 120, 120)
MID = (90, 90, 90)

SERIES_EN = "OPENSKILL  IT  STARTER"
SERIES_KO = "오픈스킬 IT 입문"
LABEL_MM = 8          # 하단 부제 크기 (세 권 공통, 가장 긴 도커 부제 기준)

LM = cg._mm(12)
RM = cg.FRONT - cg._mm(12)
TOP = cg._mm(50) - cg.BLEED
KX = cg.FRONT / 750.0                     # 750 좌표 -> 원본 가로
KY = (cg.H - 2 * cg.BLEED) / 1110.0       # 1110 좌표 -> 원본 세로


def _cfg():
    return {"title": "", "subtitle": "", "cover_data": {
        "series": "", "series_sub": "", "authors": "최주호, 류재성, 김주혁",
        "publisher": "오픈스킬북스", "accent_color": GRAY}}


# 엠블럼 (750×1110 좌표로 설계)
def _circ(d, cx, cy, r, outline, fill=(255, 255, 255), w=3):
    d.ellipse([cx * KX - r * KX, cy * KY - r * KX, cx * KX + r * KX, cy * KY + r * KX],
              outline=outline, fill=fill, width=w)


def _line(d, a, b, col, w=3):
    d.line([a[0] * KX, a[1] * KY, b[0] * KX, b[1] * KY], fill=col, width=w)


def emblem_msa(img, cy):
    """육각 서비스 네트워크 (중심 허브 + 6노드)"""
    d = ImageDraw.Draw(img); cx, r = 375, 71
    nodes = [(cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)))
             for a in range(0, 360, 60)]
    for i, n in enumerate(nodes):
        _line(d, n, nodes[(i + 1) % 6], (205, 205, 205))
        _line(d, (cx, cy), n, (205, 205, 205))
    for n in nodes:
        _circ(d, n[0], n[1], 9, (150, 150, 150))
    _circ(d, cx, cy, 11, (140, 140, 140))


def emblem_docker(img, cy):
    """배 키 (림 + 8살 + 손잡이)"""
    d = ImageDraw.Draw(img); cx = 375
    pts = [(cx + 83 * math.sin(math.radians(a)), cy - 83 * math.cos(math.radians(a)))
           for a in range(0, 360, 45)]
    for p in pts:
        _line(d, (cx, cy), p, (165, 165, 165))
    _circ(d, cx, cy, 61, (165, 165, 165), fill=None)
    for p in pts:
        _circ(d, p[0], p[1], 9, (165, 165, 165))
    _circ(d, cx, cy, 15, (150, 150, 150), fill=(150, 150, 150))


def emblem_spring(img, cy):
    """3계층 (컨트롤러·서비스·리포지토리 상자 세 개)"""
    d = ImageDraw.Draw(img); cx, w, h, gap = 375, 70, 18, 50
    ys = [cy - gap, cy, cy + gap]
    for i, y in enumerate(ys):
        d.rounded_rectangle([(cx - w) * KX, y * KY - h * KX, (cx + w) * KX, y * KY + h * KX],
                            radius=8 * KX, outline=(160, 160, 160), width=3, fill=(255, 255, 255))
        _circ(d, cx - w + 18, y, 5, (150, 150, 150),
              fill=(150, 150, 150) if i == 1 else (255, 255, 255))
        _line(d, (cx - w + 34, y), (cx + w - 18, y), (205, 205, 205))
        if i < 2:
            _line(d, (cx, y + h * KX / KY), (cx, ys[i + 1] - h * KX / KY), (165, 165, 165))


# 상단 시리즈 블록 · 하단 부제
def draw_series(img):
    d = ImageDraw.Draw(img)
    fe, fb = cg._font(6, True), cg._font(19, True)
    d.text((LM, TOP - cg._mm(6)), SERIES_EN, fill=MID, font=fe)
    y = TOP + cg._mm(1)
    d.text((LM, y), SERIES_KO, fill=DARK, font=fb)
    bb = d.textbbox((LM, y), SERIES_KO, font=fb)
    d.rectangle([LM, bb[3] + cg._mm(7), LM + cg._mm(22), bb[3] + cg._mm(8.5)], fill=DARK)


def draw_subtitle(img, text):
    d = ImageDraw.Draw(img); f = cg._font(LABEL_MM, True)
    y0 = cg.H - cg.BLEED - cg._mm(46) + cg._mm(16) - cg._mm(LABEL_MM * 1.25)
    d.rectangle([(RM - cg._mm(40), y0 - cg._mm(3)), (RM, y0 - cg._mm(2.2))], fill=GRAY)
    d.text((RM - cg._tw(d, text, f), y0), text, fill=GRAY, font=f)


def band_center(img):
    """큰 제목 아래 ~ 부제 선 위, 빈 띠의 세로 중앙 (1110 좌표)"""
    a = np.array(img.convert("L").resize((750, 1110)))
    rows = [y for y in range(500, 1000) if (a[y] < 160).any()]
    top, bot = max(((rows[i], rows[i + 1]) for i in range(len(rows) - 1)),
                   key=lambda g: g[1] - g[0])
    return (top + bot) / 2


RESERVE = (" ", 24, True, "L", -2, DARK)   # 시리즈 블록 자리
BOOKS = {
    "특이점이-온-개발자-Springboot": dict(
        main=[RESERVE, ("Spring", 82, True, "L", -2, DARK), ("Boot", 25, True, "R", 0, GRAY)],
        shadow={"Spring": ((212, 212, 212), 3.0)},
        subtitle="처음 시작하는 Spring Boot", emblem=emblem_spring),
    "특이점이-온-개발자-MSA": dict(
        main=[RESERVE, ("MSA", 60, True, "L", -2, DARK), (" ", 6, True, "L", 0, GRAY),
              ("Microservices Architecture", 18, True, "R", 0, GRAY)],
        shadow={"MSA": ((210, 210, 210), 3.5)},
        subtitle="단계별로 시작하는 MSA", emblem=emblem_msa),
    "특이점이-온-개발자-도커-쿠버네티스": dict(
        main=[RESERVE, ("Docker", 82, True, "L", -2, DARK), ("& Kubernetes", 25, True, "R", 0, GRAY)],
        shadow={"Docker": ((212, 212, 212), 3.0)},
        subtitle="개념으로 시작하는 Docker & Kubernetes", emblem=emblem_docker),
}


def render(spec):
    img = cg._render_single(_cfg(), spec["main"], shadow_map=spec["shadow"])
    draw_series(img)
    draw_subtitle(img, spec["subtitle"])
    spec["emblem"](img, band_center(img))
    return img.resize((750, 1110), Image.LANCZOS)


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    for book, spec in BOOKS.items():
        dst = (out_dir / f"{book}.jpg") if out_dir else ROOT / "projects" / book / "assets" / "cover.jpg"
        dst.parent.mkdir(parents=True, exist_ok=True)
        render(spec).save(dst, "JPEG", quality=92, dpi=(72, 72))
        print(f"saved {dst} ({dst.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
