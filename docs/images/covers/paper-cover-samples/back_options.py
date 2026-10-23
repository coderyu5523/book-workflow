"""뒷표지 시안(46배판 188x254mm 재단 + 도련 3mm 패널). 시안용 스크립트이며 최종 표지는 generate_openskill_paper_covers.py가 만든다.

실행: PYTHONUTF8=1 python docs/images/covers/paper-cover-samples/back_options.py  ->  back-options.png(시안 3 이전/보강 비교)
spread_options.py가 option3b()를 가져다 쓴다(색 인자로 바탕·포인트·제목·카드 색을 바꾼다).
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/pub-studio/references/scripts"))
sys.path.insert(0, str(ROOT / "docs/images/covers"))
import cover_generator as cg  # noqa: E402
import generate_openskill_paper_covers as pc  # noqa: E402  (바코드 그리기 재사용)

PROJ = ROOT / "projects/특이점이-온-개발자-Springboot"
colo = json.loads((PROJ / "book/colophon.json").read_text(encoding="utf-8"))
ISBN, PRICE = colo["isbn"], colo["price"]
QR_URL = "https://github.com/metacoding-06-springboot-v1/start"

DPI = 300
px = pc.px
B = 3                       # 도련 mm
TW, TH = 188, 254           # 재단 mm
CW, CH = px(TW + 2 * B), px(TH + 2 * B)

HEAD1, HEAD2 = "게시판을 만들며 배우는", "Spring Boot 입문서"
SUB = "자바는 배웠지만 Spring Boot는 처음인 입문자를 위한 책"
CHAPTERS = ["스프링 동작 원리", "REST API와 JPA", "예외 처리와 DTO", "JWT 인증", "연관관계 매핑"]


def X(v): return px(B + v)          # 재단 기준 mm -> 캔버스 px
def F(size, bold=False): return cg._font(size, bold)


def text(d, x, y, s, size, color, bold=False, anchor="ls"):
    d.text((X(x), X(y)), s, font=F(size, bold), fill=color, anchor=anchor)


def tw(d, s, size, bold=False):
    return cg._tw(d, s, F(size, bold)) / px(1)


def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, width=3):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=px(r), fill=fill, outline=outline, width=width)


def qr_image(url, size_mm):
    enc = cv2.QRCodeEncoder.create()
    m = enc.encode(url)                                   # 0/255 모듈 배열
    m = np.pad(m, 2, constant_values=255)                 # 여백(quiet zone) 2모듈
    img = Image.fromarray(m).convert("RGB")
    return img.resize((px(size_mm), px(size_mm)), Image.NEAREST)


def difficulty(d, x, y, accent, label_color):
    text(d, x, y, "난이도", 3.6, label_color, True, "lm")
    cx = x + 14
    for i in range(4):
        r = px(1.4)
        c = (X(cx + i * 5.2), X(y))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=accent if i == 0 else (255, 255, 255),
                  outline=accent if i == 0 else (200, 200, 200), width=3)
    text(d, cx + 4 * 5.2 + 1, y, "입문", 3.6, accent, True, "lm")


def footer(img, d, accent, label_color, mark_y=None, on_card=False):
    """하단 메타: 우측 QR + 바코드 + 정가, 좌측 난이도 + 출판사."""
    right = X(TW - 12)
    bottom = X(TH - 12)
    bc = pc.draw_barcode(img, d, ISBN, right, bottom)
    pt = f"정가 {PRICE}"
    f = F(4.4, True)
    d.text((right - cg._tw(d, pt, f), bc[1] - px(2.2)), pt, font=f, fill=(60, 60, 60), anchor="ls")
    qs = 20
    qr = qr_image(QR_URL, qs)
    qx = bc[0] - px(6) - qr.width
    qy = bottom - qr.height - px(3.5)
    img.paste(qr, (qx, qy))
    d.text((qx + qr.width // 2, qy + qr.height + px(3)), "실습 코드", font=F(3.2), fill=(130, 130, 130), anchor="mm")
    my = mark_y if mark_y is not None else TH - 22
    difficulty(d, 14, my - 8, accent, label_color)
    text(d, 14, my + 4, "OPENSKILL BOOKS", 7, (160, 160, 160), True)
    text(d, 14, my + 12, "오픈스킬북스", 6, (180, 180, 180))


# ------------------------------------------------------------------ 시안 1: 초록 색면 + 번호 행
def option1():
    green, dgreen, tint = (47, 158, 68), (24, 98, 44), (233, 247, 236)
    img = Image.new("RGB", (CW, CH), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, CW, X(112)], fill=green)
    text(d, 14, 26, "OPENSKILL  IT  STARTER", 4.8, (205, 238, 212), True)
    text(d, 14, 52, HEAD1, 9.6, (225, 246, 230), True)
    text(d, 14, 70, HEAD2, 13.2, (255, 255, 255), True)
    text(d, 14, 92, SUB, 4.5, (225, 246, 230))
    # 우측 장식: 3계층 상자(앞표지 엠블럼을 흰 선으로). 헤드라인 오른쪽 끝(약 x=132)과 겹치지 않게 x=140부터
    for i, yy in enumerate((22, 34, 46)):
        d.rounded_rectangle([X(140), X(yy), X(174), X(yy + 8)], radius=px(2), outline=(255, 255, 255), width=5)
        r = px(1.2)
        d.ellipse([X(144) - r, X(yy + 4) - r, X(144) + r, X(yy + 4) + r], fill=(255, 255, 255) if i == 1 else None,
                  outline=(255, 255, 255), width=3)
        d.line([X(149), X(yy + 4), X(170), X(yy + 4)], fill=(190, 230, 200), width=3)
    text(d, 14, 127, "이 책에서 배우는 것", 4.6, dgreen, True)
    y = 133
    for i, name in enumerate(CHAPTERS, 1):
        rrect(d, 14, y, 174, y + 11.5, 4, fill=tint)
        cx, cy = X(23), X(y + 5.75)
        r = px(3.7)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=green)
        d.text((cx, cy), str(i), font=F(4.2, True), fill=(255, 255, 255), anchor="mm")
        text(d, 32, y + 5.75, name, 5, (30, 40, 34), True, "lm")
        y += 14.5
    footer(img, d, green, dgreen)
    return img


# ------------------------------------------------------------------ 시안 2: 인디고 말풍선 + 3칸
def option2():
    ind, tint, dark = (79, 70, 229), (238, 242, 255), (28, 27, 60)
    img = Image.new("RGB", (CW, CH), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text(d, 14, 24, "OPENSKILL  IT  STARTER", 4.8, ind, True)
    rrect(d, 14, 32, 174, 100, 12, fill=ind)
    d.polygon([(X(34), X(99)), (X(54), X(99)), (X(30), X(114))], fill=ind)
    text(d, 26, 58, "“이런 걸 처음부터", 9, (255, 255, 255), True)
    text(d, 26, 73, "직접 만드는 사람은 없어요.”", 9, (255, 255, 255), True)
    text(d, 162, 90, "- 선배", 4.4, (205, 205, 255), False, "rs")
    text(d, 14, 134, HEAD1, 9, dark, True)
    text(d, 14, 151, HEAD2, 12.5, ind, True)
    steps = [("1", "스프링 뼈대\n만들기"), ("2", "게시판 CRUD\n완성하기"), ("3", "인증과\n연관관계")]
    x = 14
    for n, label in steps:
        rrect(d, x, 164, x + 50, 200, 6, fill=tint)
        cx, cy = X(x + 9), X(173)
        r = px(4.2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ind)
        d.text((cx, cy), n, font=F(4.6, True), fill=(255, 255, 255), anchor="mm")
        for k, line in enumerate(label.split("\n")):
            text(d, x + 6, 183 + k * 7, line, 5, dark, True, "lm")
        x += 55
    footer(img, d, ind, ind)
    return img


# ------------------------------------------------------------------ 시안 3: 피치 배경 + 흰 카드 체크 목록
def option3():
    orange, tint, dark = (244, 114, 56), (255, 243, 235), (60, 40, 30)
    img = Image.new("RGB", (CW, CH), tint)
    d = ImageDraw.Draw(img)
    text(d, 14, 24, "OPENSKILL  IT  STARTER", 4.8, orange, True)
    text(d, 14, 48, HEAD1, 9.4, dark, True)
    text(d, 14, 65, HEAD2, 13.5, orange, True)
    text(d, 14, 82, SUB, 4.4, (120, 96, 84))
    rrect(d, 14, 94, 174, 186, 8, fill=(255, 255, 255))
    y = 99
    for name in CHAPTERS:
        cx, cy = X(28), X(y + 7)
        r = px(4.4)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=orange)
        d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.4), (cx + r * 0.5, cy - r * 0.35)],
               fill=(255, 255, 255), width=px(1.1), joint="curve")
        text(d, 39, y + 7, name, 5.4, dark, True, "lm")
        y += 16.5
    rrect(d, 14, 196, 174, 247, 8, fill=(255, 255, 255))
    # 카드 안 푸터(좌: 난이도·출판사 / 우: QR·바코드)
    footer_card(img, d, orange)
    return img


# ------------------------------------------------------------------ 시안 3 보강: 소개 문단 + 항목별 한 줄 설명
INTRO = ("자바는 배웠지만 Spring Boot는 처음인 입문자를 위한 책입니다. "
         "스프링의 뼈대를 직접 구현해 본 뒤, 게시판 하나를 인증까지 만들며 핵심 개념을 익힙니다.")
ROWS = [("스프링 동작 원리", "리플렉션과 컴포넌트 스캔으로 스프링의 뼈대를 직접 구현합니다"),
        ("REST API와 JPA", "게시판 CRUD를 만들며 JPA와 3계층 구조를 익힙니다"),
        ("예외 처리와 DTO", "요청·응답 DTO와 전역 예외 처리를 적용합니다"),
        ("JWT 인증", "JWT를 발급하고 검증해 로그인한 사용자를 식별합니다"),
        ("연관관계 매핑", "게시글과 댓글을 양방향으로 연결하고 로딩 방식을 비교합니다")]


def option3b(orange=(244, 114, 56), tint=(255, 243, 235), dark=(60, 40, 30), subc=(120, 96, 84),
             card=(255, 255, 255)):
    """orange=포인트색(이름만 그대로), tint=바탕색, dark=제목색, subc=보조 글자색, card=카드 바탕색"""
    img = Image.new("RGB", (CW, CH), tint)
    d = ImageDraw.Draw(img)
    text(d, 14, 24, "OPENSKILL  IT  STARTER", 4.8, orange, True)
    text(d, 14, 46, HEAD1, 9.4, dark, True)
    text(d, 14, 63, HEAD2, 13.5, orange, True)
    lines = pc.wrap(d, INTRO, F(4.4), px(160))
    for k, ln in enumerate(lines):
        text(d, 14, 78 + k * 7.2, ln, 4.4, subc)
    top = 78 + (len(lines) - 1) * 7.2 + 8
    pitch = 16.4
    bottom = top + 5 + 4 * pitch + 12 + 5
    assert bottom <= 194, f"체크 카드가 푸터와 겹침: {bottom}"
    rrect(d, 14, top, 174, bottom, 8, fill=card)
    y = top + 5
    for name, desc in ROWS:
        cx, cy = X(28), X(y + 6)
        r = px(4.2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=orange)
        d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.4), (cx + r * 0.5, cy - r * 0.35)],
               fill=(255, 255, 255), width=px(1.1), joint="curve")
        text(d, 39, y + 3.6, name, 5.2, dark, True, "lm")
        text(d, 39, y + 10, desc, 3.8, subc, False, "lm")
        y += pitch
    rrect(d, 14, 200, 174, 247, 8, fill=card)
    footer_card(img, d, orange)
    return img


def footer_card(img, d, accent):
    right = X(TW - 18)
    bottom = X(241)
    bc = pc.draw_barcode(img, d, ISBN, right, bottom)
    pt = f"정가 {PRICE}"
    f = F(4.2, True)
    d.text((right - cg._tw(d, pt, f), bc[1] - px(1.6)), pt, font=f, fill=(60, 60, 60), anchor="ls")
    qr = qr_image(QR_URL, 19)
    qx = bc[0] - px(5) - qr.width
    qy = bottom - qr.height - px(3.5)
    img.paste(qr, (qx, qy))
    d.text((qx + qr.width // 2, qy + qr.height + px(3)), "실습 코드", font=F(3.2), fill=(130, 130, 130), anchor="mm")
    difficulty(d, 22, 214, accent, (120, 96, 84))
    text(d, 22, 232, "OPENSKILL BOOKS", 6, (170, 170, 170), True)
    text(d, 22, 239, "오픈스킬북스", 5, (190, 190, 190))


def main():
    out_dir = HERE
    panels = [("3  이전 (글 최소)", option3()), ("3  보강 (소개 + 항목별 설명)", option3b())]
    tw_, label_h = 1100, 110
    th_ = round(CH * tw_ / CW)
    sheet = Image.new("RGB", (tw_ * len(panels) + 40 * (len(panels) + 1), th_ + label_h + 40), (225, 225, 228))
    sd = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(panels):
        x = 40 + i * (tw_ + 40)
        small = im.resize((tw_, th_), Image.LANCZOS)
        sheet.paste(small, (x, label_h))
        sd.rectangle([x, label_h, x + tw_ - 1, label_h + th_ - 1], outline=(150, 150, 150), width=2)
        sd.text((x, 28), f"시안 {name}", font=F(3.6, True), fill=(40, 40, 40))
    sheet.save(out_dir / "back-options.png")
    print("saved", out_dir / "back-options.png", sheet.size)


if __name__ == "__main__":
    main()
