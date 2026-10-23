"""앞표지 후보를 보강한 뒷표지(시안 3)와 합친 펼침면 시안. 시안용 스크립트이며 최종 표지는 generate_openskill_paper_covers.py가 만든다.

실행: PYTHONUTF8=1 python docs/images/covers/paper-cover-samples/spread_options.py
  ->  spread-G1.png(흰 책등) / spread-G2.png(초록 책등) 전체 펼침면, front-options.png(두 안 비교 시트)
render_front()의 variant: A 흰 바탕+주황 / B 흰 바탕+Spring 주황 / C 피치 바탕 / D 피치 바탕+검정 Boot / G 흰 바탕+스프링 초록.
spread(variant, spine, back_kwargs)로 다른 조합도 만든다(earlier/ 의 이미지가 이전 조합).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/pub-studio/references/scripts"))
sys.path.insert(0, str(ROOT / "docs/images/covers"))
sys.path.insert(0, str(HERE))
import cover_generator as cg  # noqa: E402
import generate_openskill_paper_covers as pc  # noqa: E402

pc.set_geometry(9.0)                         # 엔진 치수를 46배판/날개 없음으로(책등 9mm 추정)
import generate_openskill_covers as eb  # noqa: E402  (치수 설정 뒤에 import)
import back_options as bo  # noqa: E402

NAME = "특이점이-온-개발자-Springboot"
PROJ = ROOT / "projects" / NAME
authors = json.loads((PROJ / "book/colophon.json").read_text(encoding="utf-8"))["authors"]

ORANGE = (244, 114, 56)
PEACH = (255, 243, 235)
WARM_DARK = (60, 40, 30)
WARM_GRAY = (120, 96, 84)
GREEN = (76, 160, 56)            # 스프링 초록(로고 색 #6DB33F보다 조금 짙게)
BLACK = (30, 30, 30)


def draw_series(img, en, ko, bar):
    d = ImageDraw.Draw(img)
    fe, fb = cg._font(6, True), cg._font(19, True)
    d.text((eb.LM, eb.TOP - cg._mm(6)), eb.SERIES_EN, fill=en, font=fe)
    y = eb.TOP + cg._mm(1)
    d.text((eb.LM, y), eb.SERIES_KO, fill=ko, font=fb)
    bb = d.textbbox((eb.LM, y), eb.SERIES_KO, font=fb)
    d.rectangle([eb.LM, bb[3] + cg._mm(7), eb.LM + cg._mm(22), bb[3] + cg._mm(8.5)], fill=bar)


def draw_subtitle(img, text, color, bar):
    d = ImageDraw.Draw(img)
    f = cg._font(eb.LABEL_MM, True)
    y0 = cg.H - cg.BLEED - cg._mm(46) + cg._mm(16) - cg._mm(eb.LABEL_MM * 1.25)
    d.rectangle([(eb.RM - cg._mm(40), y0 - cg._mm(3)), (eb.RM, y0 - cg._mm(2.2))], fill=bar)
    d.text((eb.RM - cg._tw(d, text, f), y0), text, fill=color, font=f)


def emblem(img, cy, line, node, soft):
    """앞표지 3계층 엠블럼(컨트롤러·서비스·리포지토리)을 색을 바꿔 다시 그린다."""
    d = ImageDraw.Draw(img)
    cx, w, h, gap = 375, 70, 18, 50
    ys = [cy - gap, cy, cy + gap]
    for i, y in enumerate(ys):
        d.rounded_rectangle([(cx - w) * eb.KX, y * eb.KY - h * eb.KX, (cx + w) * eb.KX, y * eb.KY + h * eb.KX],
                            radius=8 * eb.KX, outline=line, width=5, fill=(255, 255, 255))
        eb._circ(d, cx - w + 18, y, 5, node, fill=node if i == 1 else (255, 255, 255))
        eb._line(d, (cx - w + 34, y), (cx + w - 18, y), soft, w=4)
        if i < 2:
            eb._line(d, (cx, y + h * eb.KX / eb.KY), (cx, ys[i + 1] - h * eb.KX / eb.KY), line, w=4)


def render_front(variant):
    reserve = eb.RESERVE
    if variant == "B":      # 흰 바탕, Spring 주황
        main = [reserve, ("Spring", 82, True, "L", -2, ORANGE), ("Boot", 25, True, "R", 0, WARM_GRAY)]
        shadow = {"Spring": ((253, 222, 204), 3.0)}
        en, ko, bar, sub, sbar = ORANGE, WARM_DARK, ORANGE, WARM_GRAY, ORANGE
        e_line, e_node, e_soft = ORANGE, ORANGE, (250, 200, 170)
    elif variant == "G":    # 흰 바탕 + 스프링 초록 한 색. Spring만 초록, Boot·제목·소제목은 검정
        main = [reserve, ("Spring", 82, True, "L", -2, GREEN), ("Boot", 25, True, "R", 0, BLACK)]
        shadow = {"Spring": ((214, 236, 206), 3.0)}
        en, ko, bar, sub, sbar = GREEN, BLACK, GREEN, BLACK, GREEN
        e_line, e_node, e_soft = GREEN, GREEN, (190, 225, 180)
    elif variant == "D":    # 피치 바탕. Boot와 소제목은 검정, 나머지 포인트(라벨·선·엠블럼)만 주황
        black = (20, 20, 20)
        main = [reserve, ("Spring", 82, True, "L", -2, WARM_DARK), ("Boot", 25, True, "R", 0, black)]
        shadow = {"Spring": ((236, 222, 212), 3.0)}
        en, ko, bar, sub, sbar = ORANGE, WARM_DARK, ORANGE, black, ORANGE
        e_line, e_node, e_soft = ORANGE, ORANGE, (250, 200, 170)
    else:                   # A: 흰 바탕 / C: 피치 바탕. Spring은 짙은 갈색, 포인트만 주황
        main = [reserve, ("Spring", 82, True, "L", -2, WARM_DARK), ("Boot", 25, True, "R", 0, ORANGE)]
        shadow = {"Spring": ((236, 222, 212), 3.0)}
        en, ko, bar, sub, sbar = ORANGE, WARM_DARK, ORANGE, ORANGE, ORANGE
        e_line, e_node, e_soft = ORANGE, ORANGE, (250, 200, 170)
    front = cg._render_single(eb._cfg(authors), main, shadow_map=shadow)
    draw_series(front, en, ko, bar)
    draw_subtitle(front, eb.BOOKS[NAME]["subtitle"], sub, sbar)
    emblem(front, eb.band_center(front), e_line, e_node, e_soft)
    if variant in ("C", "D"):   # 흰색을 피치로(곱하기). 글자 가장자리의 안티앨리어싱이 그대로 유지된다
        front = ImageChops.multiply(front, Image.new("RGB", front.size, PEACH))
    return front


def draw_spine(img, bg, c1, c2, c3):
    sp = cg.SPINE
    x0 = cg.X_FRONT - sp
    d = ImageDraw.Draw(img)
    d.rectangle([x0, 0, cg.X_FRONT - 1, cg.H], fill=bg)
    tmp = Image.new("RGBA", (cg.H, sp), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    f_t, f_s, f_p = cg._font(3.5, True), cg._font(3.3), cg._font(2.9, True)
    y_mid = sp // 2
    x = cg.BLEED + pc.px(20)
    td.text((x, y_mid), "오픈스킬 IT 입문", fill=c1, font=f_t, anchor="lm")
    x += int(td.textlength("오픈스킬 IT 입문", font=f_t)) + pc.px(4)
    td.text((x, y_mid), eb.BOOKS[NAME]["subtitle"], fill=c2, font=f_s, anchor="lm")
    pw = int(td.textlength("오픈스킬북스", font=f_p))
    td.text((cg.H - cg.BLEED - pc.px(18) - pw, y_mid), "오픈스킬북스", fill=c3, font=f_p, anchor="lm")
    rot = tmp.rotate(-90, expand=True)
    img.paste(rot, (x0, 0), rot)


def spread(variant, spine, back_kwargs=None):
    W, H = cg.W, cg.H
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    back = bo.option3b(**(back_kwargs or {}))
    canvas.paste(back.crop((0, 0, cg.BLEED + cg.BACK, H)), (0, 0))
    bg = PEACH if variant in ("C", "D") else (255, 255, 255)
    fr = Image.new("RGB", (cg.FRONT + cg.BLEED, H), bg)
    fr.paste(render_front(variant), (0, cg.BLEED))
    canvas.paste(fr, (cg.X_FRONT, 0))
    draw_spine(canvas, *spine)
    return canvas


# 흰 바탕 + 초록 한 색 안: 뒷표지 색 인자, 책등 후보 2종 (배경, 제목, 부제, 출판사 글자색)
BACK_G = dict(orange=GREEN, tint=(255, 255, 255), dark=BLACK, subc=(105, 105, 105), card=(238, 247, 240))
SPINES = {
    "A  흰 책등 + 검정 글씨 (앞뒤 표지와 같은 흰색)": ((255, 255, 255), BLACK, (105, 105, 105), (140, 140, 140)),
    "B  초록 책등 + 흰 글씨 (한 색을 책등까지)": (GREEN, (255, 255, 255), (222, 242, 214), (205, 232, 196)),
}


def main():
    out_dir = HERE
    sheets = []
    for i, (name, spine) in enumerate(SPINES.items(), 1):
        sp_img = spread("G", spine, BACK_G)
        sp_img.save(HERE / f"spread-G{i}.png", dpi=(300, 300))
        sheets.append((name, sp_img))
    tw_ = 1150
    th_ = round(cg.H * tw_ / cg.W)
    label_h = 80
    cols = 2
    rows = (len(sheets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw_ + 40) + 40, rows * (th_ + label_h) + 40), (225, 225, 228))
    sd = ImageDraw.Draw(sheet)
    for k, (name, im) in enumerate(sheets):
        x = 40 + (k % cols) * (tw_ + 40)
        y = 20 + (k // cols) * (th_ + label_h)
        sd.text((x, y + 20), f"책등 {name}", font=cg._font(3.6, True), fill=(40, 40, 40))
        sheet.paste(im.resize((tw_, th_), Image.LANCZOS), (x, y + label_h))
    sheet.save(out_dir / "front-options.png")
    print("saved", out_dir / "front-options.png", sheet.size)


if __name__ == "__main__":
    main()
