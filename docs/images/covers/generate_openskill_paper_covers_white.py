#!/usr/bin/env python3
"""오픈스킬 IT 입문 종이책 표지 펼침면 - 흰 바탕 + 기술 색 한 가지 + 흰 책등 안 (46배판 188x254mm, 날개 없음)

paper-cover-samples/spread_options.py 의 G1(흰 책등)을 책별 설정으로 받게 일반화한 것이다.
앞표지 큰 단어와 포인트는 기술 색 한 가지, 나머지는 검정이다. 뒷표지는 소개 + 항목 5줄 카드 + 난이도·QR·바코드·정가.
ISBN·정가는 book/colophon-paper.json(종이책 전용)에서 읽는다. 없으면 그 책은 건너뛴다(전자책 ISBN을 대신 쓰지 않는다).

사용법:
    PYTHONUTF8=1 python docs/images/covers/generate_openskill_paper_covers_white.py [--book Springboot|MSA|도커] [--spine-mm 9.0]

출력(projects/<책>/assets/paper-cover/):
  cover-paper-spread-흰책등.jpg   펼침면 (300dpi, 품질 95)
책등 두께: --spine-mm 로 주거나, 생략하면 내지 쪽수로 추정한다(쪽수/2 x 0.1mm, 80g 모조지 가정).
  B5 내지 PDF(.build/pdf-b5)가 있으면 그 쪽수, 없으면 A4 전자책 PDF 쪽수 x 1.27(스프링 142쪽 -> 180쪽 비율).
  인쇄소가 알려 주는 값으로 반드시 교체한다.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/pub-studio/references/scripts"))
sys.path.insert(0, str(HERE))
import cover_generator as cg  # noqa: E402
import generate_openskill_paper_covers as pc  # noqa: E402

pc.set_geometry(pc.DEFAULT_SPINE_MM)         # eb 를 import 하기 전에 엔진 치수를 46배판으로 맞춘다
import generate_openskill_covers as eb  # noqa: E402

BLACK = (30, 30, 30)
GRAY = (105, 105, 105)
GREEN = (76, 160, 56)           # 스프링 초록(로고 색 #6DB33F보다 조금 짙게)
BLUE = (30, 125, 215)           # 도커 파랑(로고 색 #2496ED보다 조금 짙게)
ORANGE = (244, 114, 56)         # MSA는 대표색이 없어 오픈스킬 보조색(주황)

B = 3                           # 도련 mm
TW, TH = 188, 254               # 재단 mm
A4_TO_B5 = 1.27                 # A4 전자책 쪽수 -> B5 내지 쪽수 (스프링 142 -> 180)


def mix(color, f):
    """흰색에 color 를 f 만큼 섞는다(연한 바탕색)."""
    return tuple(round(255 - (255 - c) * f) for c in color)


# 책별 설정. rows 는 (항목 이름, 한 줄 설명) 5개. 문구는 저자 확인 전 초안이다
BOOKS = {
    "Springboot": dict(
        dir="특이점이-온-개발자-Springboot", accent=GREEN,
        shadow=(214, 236, 206), soft=(190, 225, 180), card=(238, 247, 240),
        head1="게시판을 만들며 배우는", head2="Spring Boot 입문서",
        intro=("자바는 배웠지만 Spring Boot는 처음인 입문자를 위한 책입니다. "
               "스프링의 뼈대를 직접 구현해 본 뒤, 게시판 하나를 인증까지 만들며 핵심 개념을 익힙니다."),
        rows=[("스프링 동작 원리", "리플렉션과 컴포넌트 스캔으로 스프링의 뼈대를 직접 구현합니다"),
              ("REST API와 JPA", "게시판 CRUD를 만들며 JPA와 3계층 구조를 익힙니다"),
              ("예외 처리와 DTO", "요청·응답 DTO와 전역 예외 처리를 적용합니다"),
              ("JWT 인증", "JWT를 발급하고 검증해 로그인한 사용자를 식별합니다"),
              ("연관관계 매핑", "게시글과 댓글을 양방향으로 연결하고 로딩 방식을 비교합니다")],
        qr="https://github.com/metacoding-06-springboot-v1/start"),
    "MSA": dict(
        dir="특이점이-온-개발자-MSA", accent=ORANGE,
        head1="서비스를 나누고 연결하며 배우는", head2="MSA 입문서",
        intro=("Spring Boot로 API는 만들어 봤지만 MSA는 처음인 개발자를 위한 책입니다. "
               "쇼핑몰 주문 시스템을 마이크로서비스로 바꿔 가며 핵심 구조를 만들어 봅니다."),
        rows=[("모놀리식과 MSA", "모놀리식의 한계와 서비스를 나누는 이유를 알아봅니다"),
              ("서비스 연결과 보상 트랜잭션", "REST로 서비스를 호출하고 실패하면 앞 작업을 되돌립니다"),
              ("DDD와 클린 아키텍처", "도메인 중심으로 구조를 바꾸고 쿠버네티스에 배포합니다"),
              ("Kafka와 Saga 패턴", "메시지로 서비스를 분리하고 분산 트랜잭션을 조율합니다"),
              ("WebSocket 실시간 알림", "주문 완료를 사용자에게 실시간으로 전달합니다")],
        qr="https://github.com/metacoding-12-msa/start"),
    "도커": dict(
        dir="특이점이-온-개발자-도커-쿠버네티스", accent=BLUE,
        head1="컨테이너 개념부터 배우는", head2="Docker & Kubernetes 입문서",
        intro=("배포와 운영 환경이 낯선 개발자를 위한 책입니다. 컨테이너가 환경 차이를 푸는 원리부터 "
               "쿠버네티스가 컨테이너를 자동으로 운영하는 흐름까지 익힙니다."),
        rows=[("컨테이너와 이미지", "환경 차이를 컨테이너로 해결하는 원리를 이해합니다"),
              ("Dockerfile과 Compose", "환경 구성을 코드로 만들고 여러 컨테이너를 한 번에 실행합니다"),
              ("Kubernetes 시작하기", "Pod를 자동으로 복구하고 무중단으로 배포합니다"),
              ("Kubernetes 네트워킹", "Service와 Ingress로 외부에서 접속할 주소를 만듭니다"),
              ("설정과 데이터 관리", "비밀번호와 데이터를 Pod 밖에 두고 전체 서비스를 배포합니다")],
        qr="https://github.com/metacoding-10-linux-docker/start"),
}
for _s in BOOKS.values():
    _s.setdefault("shadow", mix(_s["accent"], 0.22))
    _s.setdefault("soft", mix(_s["accent"], 0.34))
    _s.setdefault("card", mix(_s["accent"], 0.09))


def X(v): return pc.px(B + v)          # 재단 기준 mm -> 캔버스 px
def F(size, bold=False): return cg._font(size, bold)


# ---------------------------------------------------------------- 앞표지
def emblem_spring(img, cy, accent, soft):
    d = ImageDraw.Draw(img)
    cx, w, h, gap = 375, 70, 18, 50
    ys = [cy - gap, cy, cy + gap]
    for i, y in enumerate(ys):
        d.rounded_rectangle([(cx - w) * eb.KX, y * eb.KY - h * eb.KX, (cx + w) * eb.KX, y * eb.KY + h * eb.KX],
                            radius=8 * eb.KX, outline=accent, width=5, fill=(255, 255, 255))
        eb._circ(d, cx - w + 18, y, 5, accent, fill=accent if i == 1 else (255, 255, 255))
        eb._line(d, (cx - w + 34, y), (cx + w - 18, y), soft, w=4)
        if i < 2:
            eb._line(d, (cx, y + h * eb.KX / eb.KY), (cx, ys[i + 1] - h * eb.KX / eb.KY), accent, w=4)


def emblem_msa(img, cy, accent, soft):
    """육각 서비스 네트워크(중심 허브 + 6노드)"""
    d = ImageDraw.Draw(img)
    cx, r = 375, 71
    nodes = [(cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a))) for a in range(0, 360, 60)]
    for i, n in enumerate(nodes):
        eb._line(d, n, nodes[(i + 1) % 6], soft, w=4)
        eb._line(d, (cx, cy), n, soft, w=4)
    for n in nodes:
        eb._circ(d, n[0], n[1], 9, accent, w=5)
    eb._circ(d, cx, cy, 11, accent, fill=accent, w=5)


def emblem_docker(img, cy, accent, soft):
    """배 키(림 + 8살 + 손잡이)"""
    d = ImageDraw.Draw(img)
    cx = 375
    pts = [(cx + 83 * math.sin(math.radians(a)), cy - 83 * math.cos(math.radians(a))) for a in range(0, 360, 45)]
    for p in pts:
        eb._line(d, (cx, cy), p, soft, w=4)
    eb._circ(d, cx, cy, 61, accent, fill=None, w=5)
    for p in pts:
        eb._circ(d, p[0], p[1], 9, accent, w=5)
    eb._circ(d, cx, cy, 15, accent, fill=accent, w=5)


EMBLEMS = {"Springboot": emblem_spring, "MSA": emblem_msa, "도커": emblem_docker}


def render_front(key, spec, authors):
    base = eb.BOOKS[spec["dir"]]
    accent = spec["accent"]
    # 큰 단어는 기술 색, 보조 단어는 검정(전자책 표지의 DARK/GRAY 를 바꿔 끼운다)
    main = [(t, s, b, al, ls, accent if c == eb.DARK else BLACK if c == eb.GRAY else c)
            for (t, s, b, al, ls, c) in base["main"]]
    shadow = {k: (spec["shadow"], w) for k, (_, w) in base["shadow"].items()}
    img = cg._render_single(eb._cfg(authors), main, shadow_map=shadow)
    d = ImageDraw.Draw(img)
    # 시리즈 블록
    d.text((eb.LM, eb.TOP - cg._mm(6)), eb.SERIES_EN, fill=accent, font=F(6, True))
    y = eb.TOP + cg._mm(1)
    fb = F(19, True)
    d.text((eb.LM, y), eb.SERIES_KO, fill=BLACK, font=fb)
    bb = d.textbbox((eb.LM, y), eb.SERIES_KO, font=fb)
    d.rectangle([eb.LM, bb[3] + cg._mm(7), eb.LM + cg._mm(22), bb[3] + cg._mm(8.5)], fill=accent)
    # 부제
    f = F(eb.LABEL_MM, True)
    y0 = cg.H - cg.BLEED - cg._mm(46) + cg._mm(16) - cg._mm(eb.LABEL_MM * 1.25)
    d.rectangle([(eb.RM - cg._mm(40), y0 - cg._mm(3)), (eb.RM, y0 - cg._mm(2.2))], fill=accent)
    d.text((eb.RM - cg._tw(d, base["subtitle"], f), y0), base["subtitle"], fill=BLACK, font=f)
    EMBLEMS[key](img, eb.band_center(img), accent, spec["soft"])
    return img


# ---------------------------------------------------------------- 뒷표지
def qr_image(url, size_mm):
    m = cv2.QRCodeEncoder.create().encode(url)
    m = np.pad(m, 2, constant_values=255)                       # 여백(quiet zone) 2모듈
    return Image.fromarray(m).convert("RGB").resize((pc.px(size_mm), pc.px(size_mm)), Image.NEAREST)


def text(d, x, y, s, size, color, bold=False, anchor="ls"):
    d.text((X(x), X(y)), s, font=F(size, bold), fill=color, anchor=anchor)


def rrect(d, x0, y0, x1, y1, r, fill):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=pc.px(r), fill=fill)


def fit_size(d, s, size, bold, max_mm, min_size=7.0):
    """한 줄이 max_mm 안에 들어올 때까지 글자 크기를 줄인다."""
    while size > min_size and cg._tw(d, s, F(size, bold)) > pc.px(max_mm):
        size = round(size - 0.2, 1)
    assert cg._tw(d, s, F(size, bold)) <= pc.px(max_mm), f"한 줄에 안 들어감: {s}"
    return size


def render_back(spec, isbn, price):
    accent, card = spec["accent"], spec["card"]
    img = Image.new("RGB", (pc.px(TW + 2 * B), pc.px(TH + 2 * B)), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text(d, 14, 24, "OPENSKILL  IT  STARTER", 4.8, accent, True)
    s1 = fit_size(d, spec["head1"], 9.4, True, 160)
    s2 = fit_size(d, spec["head2"], 13.5, True, 160)
    text(d, 14, 46, spec["head1"], s1, BLACK, True)
    text(d, 14, 63, spec["head2"], s2, accent, True)
    lines = pc.wrap(d, spec["intro"], F(4.4), pc.px(160))
    for k, ln in enumerate(lines):
        text(d, 14, 78 + k * 7.2, ln, 4.4, GRAY)
    top = 78 + (len(lines) - 1) * 7.2 + 8
    pitch = 16.4
    bottom = top + 5 + 4 * pitch + 12 + 5
    assert bottom <= 194, f"체크 카드가 푸터와 겹침: {bottom}"
    rrect(d, 14, top, 174, bottom, 8, card)
    y = top + 5
    for name, desc in spec["rows"]:
        assert cg._tw(d, desc, F(3.8)) <= pc.px(174 - 6 - 39), f"설명이 카드 밖으로 나감: {desc}"
        cx, cy = X(28), X(y + 6)
        r = pc.px(4.2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
        d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.4), (cx + r * 0.5, cy - r * 0.35)],
               fill=(255, 255, 255), width=pc.px(1.1), joint="curve")
        text(d, 39, y + 3.6, name, 5.2, BLACK, True, "lm")
        text(d, 39, y + 10, desc, 3.8, GRAY, False, "lm")
        y += pitch
    rrect(d, 14, 200, 174, 247, 8, card)
    # 카드 안 푸터(좌: 난이도·출판사 / 우: QR·바코드·정가)
    right, bot = X(TW - 18), X(241)
    bc = pc.draw_barcode(img, d, isbn, right, bot)
    pt = f"정가 {price}"
    f = F(4.2, True)
    d.text((right - cg._tw(d, pt, f), bc[1] - pc.px(1.6)), pt, font=f, fill=(60, 60, 60), anchor="ls")
    qr = qr_image(spec["qr"], 19)
    qx, qy = bc[0] - pc.px(5) - qr.width, bot - qr.height - pc.px(3.5)
    img.paste(qr, (qx, qy))
    d.text((qx + qr.width // 2, qy + qr.height + pc.px(3)), "실습 코드", font=F(3.2), fill=(130, 130, 130), anchor="mm")
    text(d, 22, 214, "난이도", 3.6, (120, 96, 84), True, "lm")
    for i in range(4):
        r = pc.px(1.4)
        c = (X(22 + 14 + i * 5.2), X(214))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=accent if i == 0 else (255, 255, 255),
                  outline=accent if i == 0 else (200, 200, 200), width=3)
    text(d, 22 + 14 + 4 * 5.2 + 1, 214, "입문", 3.6, accent, True, "lm")
    text(d, 22, 232, "OPENSKILL BOOKS", 6, (170, 170, 170), True)
    text(d, 22, 239, "오픈스킬북스", 5, (190, 190, 190))
    return img


# ---------------------------------------------------------------- 책등(흰 바탕, 위에서 아래로 읽음)
def draw_spine(img, subtitle):
    sp = cg.SPINE
    x0 = cg.X_FRONT - sp
    d = ImageDraw.Draw(img)
    d.rectangle([x0, 0, cg.X_FRONT - 1, cg.H], fill=(255, 255, 255))
    tmp = Image.new("RGBA", (cg.H, sp), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    f_t, f_s, f_p = F(3.5, True), F(3.3), F(2.9, True)
    y_mid = sp // 2
    x = cg.BLEED + pc.px(20)
    td.text((x, y_mid), "오픈스킬 IT 입문", fill=BLACK, font=f_t, anchor="lm")
    x += int(td.textlength("오픈스킬 IT 입문", font=f_t)) + pc.px(4)
    td.text((x, y_mid), subtitle, fill=GRAY, font=f_s, anchor="lm")
    pw = int(td.textlength("오픈스킬북스", font=f_p))
    td.text((cg.H - cg.BLEED - pc.px(18) - pw, y_mid), "오픈스킬북스", fill=(140, 140, 140), font=f_p, anchor="lm")
    rot = tmp.rotate(-90, expand=True)
    img.paste(rot, (x0, 0), rot)


# ---------------------------------------------------------------- 책등 두께 추정 + 메인
def estimate_spine(project: Path):
    import fitz
    b5 = sorted((project / ".build" / "pdf-b5").glob("*(B5).pdf"))
    if b5:
        with fitz.open(str(b5[-1])) as doc:
            pages, src = doc.page_count, "B5 내지"
    else:
        a4 = sorted((project / ".build" / "pdf").glob("오픈스킬 IT 입문*.pdf"))
        if not a4:
            return pc.DEFAULT_SPINE_MM, f"책등 {pc.DEFAULT_SPINE_MM}mm는 임시값(내지 PDF 없음)"
        with fitz.open(str(a4[-1])) as doc:
            pages, src = int(math.ceil(doc.page_count * A4_TO_B5 / 2) * 2), f"A4 {doc.page_count}쪽 x {A4_TO_B5}"
    mm_ = round(pages / 2 * 0.1, 1)
    return mm_, f"책등 {mm_}mm는 추정값({src} -> 내지 {pages}쪽 / 2 x 0.1mm)"


def main() -> int:
    ap = argparse.ArgumentParser(description="오픈스킬 IT 입문 종이책 표지 펼침면(흰 책등 안)")
    ap.add_argument("--book", help="Springboot | MSA | 도커 (생략하면 세 권 모두)")
    ap.add_argument("--spine-mm", type=float, default=None, help="책등 두께(mm). 생략하면 쪽수로 추정")
    args = ap.parse_args()
    keys = [k for k in BOOKS if not args.book or args.book in k or args.book in BOOKS[k]["dir"]]
    if not keys:
        print(f"[!] --book '{args.book}' 에 맞는 책이 없음: {list(BOOKS)}")
        return 1
    failed = 0
    for key in keys:
        spec = BOOKS[key]
        project = ROOT / "projects" / spec["dir"]
        pj = project / "book" / "colophon-paper.json"
        if not pj.exists():     # 종이책 ISBN을 전자책 것으로 대신 찍지 않는다
            print(f"[!] {key}: {pj.relative_to(ROOT)} 없음. 종이책 ISBN·정가를 넣어 만든 뒤 다시 실행하세요")
            failed += 1
            continue
        spine_mm, note = (args.spine_mm, f"책등 {args.spine_mm:g}mm는 지정값") if args.spine_mm else estimate_spine(project)
        pc.set_geometry(spine_mm)
        colo = json.loads((project / "book" / "colophon.json").read_text(encoding="utf-8"))
        colo.update({k: v for k, v in json.loads(pj.read_text(encoding="utf-8")).items() if not k.startswith("_")})
        canvas = Image.new("RGB", (cg.W, cg.H), (255, 255, 255))
        back = render_back(spec, colo["isbn"], colo["price"])
        canvas.paste(back.crop((0, 0, cg.BLEED + cg.BACK, cg.H)), (0, 0))
        canvas.paste(render_front(key, spec, colo["authors"]), (cg.X_FRONT, cg.BLEED))
        draw_spine(canvas, eb.BOOKS[spec["dir"]]["subtitle"])
        out = project / "assets" / "paper-cover"
        out.mkdir(parents=True, exist_ok=True)
        dst = out / "cover-paper-spread-흰책등.jpg"
        canvas.save(dst, "JPEG", quality=95, subsampling=0, optimize=True, dpi=(pc.DPI, pc.DPI))
        print(f"[OK] {key}: {dst}")
        print(f"     {cg.W}x{cg.H}px = {cg.W * 25.4 / pc.DPI:.1f}x{cg.H * 25.4 / pc.DPI:.1f}mm, {note}")
        print(f"     ISBN {colo['isbn']}  정가 {colo['price']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
