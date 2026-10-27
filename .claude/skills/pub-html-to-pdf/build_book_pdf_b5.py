#!/usr/bin/env python3
"""
build_book_pdf_b5.py — 종이책 인쇄용 B5(46배판 188x254mm) 내지 PDF 한 권 빌드.

build_book_pdf.py(A4 전자책용)는 건드리지 않는다. 같은 입력(book/pdf-build.json,
dividers.json, colophon.json, authors.json, .build/*.html)을 읽어 B5 내지를
.build/pdf-b5/ 에 만든다. A4 결과물(.build/pdf/)은 덮어쓰지 않는다.

  PYTHONUTF8=1 python .claude/skills/pub-html-to-pdf/build_book_pdf_b5.py \
      --project-root projects/<책폴더>
  # 시험 빌드(한 챕터의 표지+본문만): --only-chapter 1

전제(반드시 먼저): build_html.py 로 .build/*.html 을 만들어 둘 것(A4와 같은 HTML을 쓴다).

A4판과 다른 점
  - 용지 188x254mm(표지 제작 규격의 46배판). 여백 위20·아래22mm, 안쪽22·바깥16mm (홀수 쪽은 왼쪽이 안쪽, 짝수 쪽은 오른쪽이 안쪽)
  - 표지는 내지에 넣지 않는다(표지 펼침면은 인쇄소 규격이 정해진 뒤 별도 작업)
  - 판권지·머릿말·프롤로그·목차·챕터표지·에필로그·맺음말은 홀수(오른쪽) 쪽에서 시작하고
    필요하면 빈 쪽을 끼운다. 챕터 본문은 챕터표지 바로 다음 쪽(짝수)에서 시작한다
  - 총 쪽수가 홀수면 끝에 빈 쪽을 하나 붙여 짝수로 맞춘다
  - 빈 쪽은 번호를 찍지 않되 쪽수에는 포함한다. 머릿말이 1쪽이고, 목차 구간(목차+뒤 빈 쪽)과
    그 앞의 판권지·지은이 소개는 쪽수에 넣지 않는다(홀수 쪽 = 홀수 번호가 유지되는 구간)
  - 판권지·챕터표지·목차의 mm 치수는 B5 본문 영역(150x212mm)에 맞춰 조정

설정 파일(선택 키): projects/<책>/book/pdf-build.json 의 "output_b5" = 출력 파일명
  (없으면 "output" 이름에 " (B5)"를 붙인다)
  "b5_start_left" = 오른쪽 시작 규칙을 풀 머릿말·프롤로그류 파트 이름 목록(예: ["afterword"]).
  앞 파트가 홀수 쪽에서 끝나면 그 다음 짝수(왼쪽) 쪽에서 바로 시작해 빈 쪽을 줄인다.
  1쪽짜리 에필로그 뒤 마치며에 쓰면 중간 빈 쪽과 끝 빈 쪽이 함께 사라진다(2쪽 절약)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_book_pdf import (  # noqa: E402  A4 빌더와 공유하는 크기 무관 함수
    DEFAULT_TOP_LABELS,
    _chapter_headings,
    _find_heading_offsets,
    _load_dividers,
)

PAGE_W_MM, PAGE_H_MM = 188, 254
MARGIN_TOP_MM, MARGIN_BOTTOM_MM = 20, 22
MARGIN_INNER_MM, MARGIN_OUTER_MM = 22, 16


def _page_css() -> str:
    """홀수(오른쪽) 쪽은 왼쪽이 안쪽, 짝수(왼쪽) 쪽은 오른쪽이 안쪽.
    print.css의 `@page { size: A4 }`보다 뒤에 주입되어 덮어쓴다."""
    return (
        f"@page {{ size: {PAGE_W_MM}mm {PAGE_H_MM}mm;"
        f" margin-top: {MARGIN_TOP_MM}mm; margin-bottom: {MARGIN_BOTTOM_MM}mm; }}"
        f"@page :right {{ margin-left: {MARGIN_INNER_MM}mm;"
        f" margin-right: {MARGIN_OUTER_MM}mm; }}"
        f"@page :left {{ margin-left: {MARGIN_OUTER_MM}mm;"
        f" margin-right: {MARGIN_INNER_MM}mm; }}"
    )


class Renderer:
    """Chromium 한 번만 띄워 여러 HTML을 B5 PDF로 굽는다."""

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        return self

    def __exit__(self, *exc):
        self._browser.close()
        self._pw.stop()

    def render(self, html_path: Path, pdf_path: Path, side: str = "right") -> None:
        """side="left"는 첫 쪽이 짝수(왼쪽) 쪽으로 찍혀야 하는 파트.
        Chromium은 항상 첫 쪽을 오른쪽으로 보므로 빈 쪽을 하나 앞에 두고 구운 뒤 그 쪽을 지운다."""
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        ctx = self._browser.new_context(
            viewport={"width": 1240, "height": 1754}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.add_style_tag(content=_page_css())
        if side == "left":
            page.evaluate(
                "() => { const d = document.createElement('div');"
                " d.style.cssText = 'height:1px;break-after:page';"
                " document.body.insertBefore(d, document.body.firstChild); }")
        page.emulate_media(media="print")
        page.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
        ctx.close()
        if side == "left":
            _drop_first_page(pdf_path)


def _drop_first_page(pdf_path: Path) -> None:
    import fitz
    doc = fitz.open(str(pdf_path))
    first = doc[0].get_text().strip()
    if doc.page_count < 2 or (first and not first.isdigit()):  # 숫자만 있으면 푸터
        doc.close()
        raise RuntimeError(f"앞 빈 쪽이 생기지 않았다(짝수 쪽 시작 렌더 실패): {pdf_path.name}")
    doc.delete_page(0)
    tmp = pdf_path.with_suffix(".tmp.pdf")
    doc.save(str(tmp))
    doc.close()
    os.replace(tmp, pdf_path)


def _page_count(pdf: Path) -> int:
    import fitz
    with fitz.open(str(pdf)) as d:
        return d.page_count


# ---------------------------------------------------------------- 보조 페이지 HTML (B5 치수)

_HEAD = (
    '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">'
    '<link rel="stylesheet" href="./styles/fonts.css">'
    '<link rel="stylesheet" href="./styles/tokens.css">'
    '<link rel="stylesheet" href="./tokens.css">'
)


def _divider_html(data: dict) -> str:
    sub_html = f'<div class="sub">{data["sub"]}</div>' if data.get("sub") else ""
    goal_items = "".join(f"<li>{g}</li>" for g in data.get("goal", []))
    goal_html = ""
    if goal_items:
        goal_html = (
            '<div class="goal"><div class="gh">이번 챕터가 끝나면</div>'
            f"<ul>{goal_items}</ul></div>"
        )
    return f"""{_HEAD}
<style>
* {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
html,body {{ margin:0; font-family:var(--font-body,"Pretendard",sans-serif); }}
.s1 {{ min-height:194mm; display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center;
  padding:0 8mm; box-sizing:border-box; }}
.s1 .label {{ letter-spacing:.34em; font-size:14px; font-weight:700;
  color:var(--color-accent,#4f46e5); margin-bottom:6px; }}
.s1 .num {{ font-size:120px; font-weight:800; line-height:1;
  color:var(--color-accent,#4f46e5); }}
.s1 .rule {{ width:60px; height:3px; border-radius:2px;
  background:var(--color-accent-warm,#ff7849); margin:24px 0 28px; }}
.s1 .title {{ font-size:32px; font-weight:800;
  color:var(--color-text-heading,#0f172a); }}
.s1 .sub {{ font-size:17px; font-weight:500;
  color:var(--color-text-muted,#64748b); margin-top:12px; }}
.goal {{ margin-top:44px; width:min(28em,94%); text-align:left; box-sizing:border-box;
  border:1px solid var(--color-accent-border,#c7d2fe); border-radius:14px; padding:20px 22px; }}
.goal .gh {{ font-size:13px; font-weight:700; letter-spacing:.04em;
  color:var(--color-accent-text,#3730a3); margin-bottom:10px; text-align:center; }}
.goal ul {{ margin:0; padding:0; list-style:none; }}
.goal li {{ position:relative; padding-left:20px; margin:8px 0;
  font-size:14px; line-height:1.7; color:#374151; }}
.goal li::before {{ content:""; position:absolute; left:2px; top:10px;
  width:7px; height:7px; border-radius:50%; background:var(--color-accent,#4f46e5); }}
.goal b {{ color:var(--color-text-heading,#0f172a); font-weight:700; }}
</style></head><body>
<div class="s1">
  <div class="label">CHAPTER</div>
  <div class="num">{data["n"]}</div>
  <div class="rule"></div>
  <div class="title">{data["title"]}</div>
  {sub_html}
  {goal_html}
</div>
</body></html>
"""


def _colophon_html(d: dict) -> str:
    rows = "".join(
        f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>'
        for k, v in [
            (d.get("edition", "초판 1쇄 발행"), d.get("pubdate", "")),
            ("지은이", d.get("authors", "")),
            ("펴낸이", d.get("founder", "")),
            ("펴낸곳", d.get("publisher", "")),
            ("등록", d.get("registration", "")),
            ("주소", d.get("address", "")),
            ("전화", d.get("phone", "")),
            ("이메일", d.get("email", "")),
            ("ISBN", d.get("isbn", "")),
            ("정가", d.get("price", "")),
        ]
        if v)
    notices = "".join(f"<p>{n}</p>" for n in d.get("notices", []))
    css = (
        "* { -webkit-print-color-adjust: exact !important;"
        " print-color-adjust: exact !important; }"
        "html,body { margin:0; font-family:var(--font-body,'Pretendard',sans-serif);"
        " color:#1a202c; word-break:keep-all; overflow-wrap:break-word; }"
        ".wrap { min-height:194mm; display:flex; flex-direction:column;"
        " justify-content:flex-end; padding:16mm 12mm 22mm; box-sizing:border-box; }"
        ".ctitle { font-size:20px; font-weight:800; margin-bottom:12px; }"
        ".rule { height:2px; width:58px; background:var(--color-accent,#4f46e5);"
        " margin-bottom:20px; }"
        ".meta { border-collapse:collapse; font-size:13px; margin-bottom:18px; }"
        ".meta td { padding:4px 0; vertical-align:top; }"
        ".meta .k { color:#64748b; width:110px; font-weight:600; padding-left:0; }"
        ".meta .v { color:#1a202c; }"
        ".copy { font-size:13px; color:#334155; font-weight:600; margin-bottom:22px; }"
        ".notice { font-size:11px; color:#94a3b8; line-height:1.7;"
        " border-top:1px solid #e2e8f0; padding-top:14px; }"
        ".notice p { margin:3px 0; }")
    return (
        f"{_HEAD}<style>{css}</style></head><body><div class=\"wrap\">"
        f'<div class="ctitle">{d.get("title", "")}</div>'
        '<div class="rule"></div>'
        f'<table class="meta">{rows}</table>'
        f'<div class="copy">© {d.get("year", "")} {d.get("authors", "")}</div>'
        f'<div class="notice">{notices}</div>'
        "</div></body></html>")


def _authors_html(d: dict) -> str:
    blocks = ""
    for a in d.get("authors", []):
        career = "".join(f"<li>{c}</li>" for c in a.get("career", []))
        books = ""
        if a.get("books"):
            items = "".join(f"<li>{b}</li>" for b in a["books"])
            books = f'<div class="bk-h">저서</div><ul class="bk">{items}</ul>'
        blocks += (f'<div class="author"><div class="name">{a.get("name", "")}</div>'
                   f'<ul class="career">{career}</ul>{books}</div>')
    css = (
        "* { -webkit-print-color-adjust: exact !important;"
        " print-color-adjust: exact !important; }"
        "html,body { margin:0; font-family:var(--font-body,'Pretendard',sans-serif);"
        " color:#1a202c; word-break:keep-all; overflow-wrap:break-word; }"
        ".wrap { padding:8mm 8mm 0; box-sizing:border-box; }"
        ".atitle { font-size:20px; font-weight:800; margin-bottom:12px; }"
        ".rule { height:2px; width:58px; background:var(--color-accent,#4f46e5);"
        " margin-bottom:26px; }"
        ".author { margin-bottom:24px; }"
        ".name { font-size:15px; font-weight:800; margin-bottom:8px; }"
        "ul { list-style:none; margin:0; padding:0; }"
        ".career li { font-size:12.5px; color:#334155; line-height:1.75; }"
        ".bk-h { font-size:12px; font-weight:700; color:#64748b; margin:8px 0 3px; }"
        ".bk li { font-size:12px; color:#475569; line-height:1.7; }")
    return (
        f"{_HEAD}<style>{css}</style></head><body><div class=\"wrap\">"
        f'<div class="atitle">{d.get("title", "지은이 소개")}</div>'
        '<div class="rule"></div>'
        f"{blocks}</div></body></html>")


def _toc_html(entries) -> str:
    """entries: (level, label, page). 계층 목차 HTML."""
    rows = "".join(
        f'<div class="trow l{lvl}"><span class="tl">{lbl}</span>'
        f'<span class="td"></span><span class="tp">{pg}</span></div>'
        for lvl, lbl, pg in entries)
    css = (
        "* { -webkit-print-color-adjust: exact !important;"
        " print-color-adjust: exact !important; }"
        "html,body { margin:0; font-family:var(--font-body,'Pretendard',sans-serif);"
        " color:#1a202c; }"
        ".wrap { padding: 2mm 8mm 14mm; }"
        ".tt { font-size:28px; font-weight:800; margin:0 0 24px; letter-spacing:-0.5px; }"
        ".trow { display:flex; align-items:baseline; }"
        ".tl { white-space:nowrap; }"
        ".td { flex:1; border-bottom:1px dotted #c8ccd4; margin:0 8px; }"
        ".tp { white-space:nowrap; }"
        ".l1 { margin:16px 0 6px; font-size:14.5px; }"
        ".l1 .tl { font-weight:700; } .l1 .tp { color:var(--color-accent,#4f46e5);"
        " font-weight:700; }"
        ".l2 { margin:5px 0 5px 16px; font-size:12.5px; }"
        ".l2 .tl { font-weight:600; color:#2d3748; } .l2 .tp { color:#4a5568; }"
        ".l3 { margin:3px 0 3px 34px; font-size:11.5px; }"
        ".l3 .tl { color:#5a6678; } .l3 .tp { color:#8a93a3; }")
    return (
        f"{_HEAD}<style>{css}</style></head><body><div class=\"wrap\">"
        '<div class="tt">목차</div>'
        f"{rows}</div></body></html>")


# ---------------------------------------------------------------- 쪽 배치 계산

def _layout(parts, toc_pages, blank_pdf):
    """파트 순서대로 물리 위치와 쪽번호를 계산한다.

    - need_right 파트는 홀수(오른쪽) 쪽에서 시작한다. 직전 파트가 홀수 쪽에서 끝나면 빈 쪽을 끼운다.
    - 쪽번호는 counted 쪽만 센다. 빈 쪽도 counted 구간 안에서는 센다(번호만 안 찍는다).
      단 목차 바로 뒤의 빈 쪽과 첫 counted 파트(머릿말) 앞의 빈 쪽은 세지 않는다.
      (목차+뒤 빈 쪽은 항상 짝수 쪽이라, 세지 않아도 홀수 쪽=홀수 번호가 유지된다)
    반환: segs [(pdf, 쪽수, counted, blank)], starts {파트 인덱스: {phys, num, side}}
    """
    segs, starts = [], {}
    pos = n = 0
    counting = after_toc = False
    for i, p in enumerate(parts):
        cnt = toc_pages if p["kind"] == "toc" else p["count"]
        if p["need_right"] and pos % 2 == 1:
            pad_counted = counting and not after_toc
            segs.append((blank_pdf, 1, pad_counted, True))
            pos += 1
            if pad_counted:
                n += 1
        starts[i] = {"phys": pos + 1,
                     "num": n + 1 if p["counted"] else None,
                     "side": "right" if pos % 2 == 0 else "left"}
        segs.append((p["pdf"], cnt, p["counted"], False))
        pos += cnt
        if p["counted"]:
            n += cnt
            counting = True
        after_toc = p["kind"] == "toc"
    if pos % 2 == 1:  # 인쇄는 장(앞뒤 2쪽) 단위라 총 쪽수를 짝수로 맞춘다
        segs.append((blank_pdf, 1, False, True))
    return segs, starts


def _toc_entries(parts, starts):
    entries = []
    for i, p in enumerate(parts):
        num = starts[i]["num"]
        if num is None:
            continue
        if p["label"]:
            entries.append((p["lvl"], p["label"], num))
        for lvl, text, off in p["sub"] or []:
            entries.append((lvl, text, num + off))
    return entries


def _finalize(src, dst, page_flags, toc_phys, toc_entries):
    """챕터별 푸터 숫자를 가리고 전체 기준 번호(머릿말=1)를 찍는다. 빈 쪽·표지류는 번호 없음.
    계층 PDF 북마크도 추가한다."""
    import fitz
    doc = fitz.open(str(src))

    body_to_phys, body = {}, 0
    for i, page in enumerate(doc):
        ph, pw = page.rect.height, page.rect.width
        for b in page.get_text("blocks"):
            x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
            if y0 > ph - 58 and txt.strip().isdigit():
                page.draw_rect(fitz.Rect(x0 - 6, y0 - 3, x1 + 6, y1 + 3),
                               color=(1, 1, 1), fill=(1, 1, 1))
        counted, blank = page_flags[i]
        if counted:
            body += 1
            body_to_phys[body] = i + 1
            if not blank:
                page.insert_textbox(
                    fitz.Rect(pw / 2 - 40, ph - 42, pw / 2 + 40, ph - 22),
                    str(body), fontsize=9, align=1, color=(0.35, 0.35, 0.35))

    # 문서 등장 순서(seq)를 보존해 정렬한다(소절과 다음 절이 같은 쪽에 걸릴 때 번호가 뒤집히지 않게).
    raw, seq = [], 0
    if toc_phys:
        raw.append((1, "목차", toc_phys, seq)); seq += 1
    for lvl, label, bp in toc_entries:
        if bp in body_to_phys:
            raw.append((lvl, label, body_to_phys[bp], seq)); seq += 1
    raw.sort(key=lambda e: (e[2], e[3]))
    outline, prev = [], 0
    for lvl, label, pno, _ in raw:
        lvl = min(lvl, prev + 1)  # 레벨 점프 방지(set_toc 요구)
        outline.append([lvl, label, pno])
        prev = lvl
    doc.set_toc(outline)
    doc.save(str(dst))
    doc.close()


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="HTML 다이어그램 책의 B5 종이책 내지 PDF 빌드")
    ap.add_argument("--project-root", required=True, help="projects/<책폴더> 경로")
    ap.add_argument("--only-chapter", type=int, default=None,
                    help="시험 빌드: 해당 번호 챕터의 표지+본문만 굽는다(판권지·목차 없음)")
    args = ap.parse_args()

    project = Path(args.project_root).resolve()
    if not project.exists():
        print(f"[!] 프로젝트 경로 없음: {project}")
        return 1
    build_dir = project / ".build"
    pdf_dir = build_dir / "pdf-b5"
    cfg_path = project / "book" / "pdf-build.json"
    if not cfg_path.exists():
        print(f"[!] 설정 파일 없음: {cfg_path}")
        print("    book/pdf-build.json 에 {\"chapters\": [...]} 를 만들어 주세요.")
        return 1
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    chapters = cfg.get("chapters", [])
    if not chapters:
        print("[!] pdf-build.json 의 chapters 가 비어 있음")
        return 1
    top_labels = {**DEFAULT_TOP_LABELS, **cfg.get("top_labels", {})}
    start_left = set(cfg.get("b5_start_left", []))
    base_out = cfg.get("output", f"{project.name}.pdf")
    out_name = cfg.get("output_b5") or f"{Path(base_out).stem} (B5).pdf"
    test_mode = args.only_chapter is not None
    if test_mode:
        prefix = f"{args.only_chapter:02d}-"
        chapters = [c for c in chapters if c.startswith(prefix)]
        if not chapters:
            print(f"[!] {prefix} 로 시작하는 챕터가 pdf-build.json 에 없음")
            return 1
        out_name = f"_test-ch{args.only_chapter}.pdf"

    pdf_dir.mkdir(parents=True, exist_ok=True)
    dividers = _load_dividers(project / "book" / "dividers.json")

    def new_part(kind, html, pdf, *, need_right, counted, side="right",
                 label=None, lvl=None, sub=None):
        return {"kind": kind, "html": html, "pdf": pdf, "need_right": need_right,
                "counted": counted, "side": side, "label": label, "lvl": lvl,
                "sub": sub, "count": 0}

    front, body_parts = [], []
    # 1) 파트 목록 구성 (HTML 준비까지만, 렌더는 아래에서 한 번에)
    if not test_mode:
        cj = project / "book" / "colophon.json"
        if cj.exists():
            colophon = json.loads(cj.read_text(encoding="utf-8"))
            pj = project / "book" / "colophon-paper.json"   # 종이책은 ISBN·정가가 전자책과 달라 덮어쓴다
            if pj.exists():
                colophon.update({k: v for k, v in json.loads(pj.read_text(encoding="utf-8")).items()
                                 if not k.startswith("_")})
            h = build_dir / "_b5-colophon.html"
            h.write_text(_colophon_html(colophon), encoding="utf-8")
            front.append(new_part("colophon", h, pdf_dir / "_colophon.pdf",
                                  need_right=True, counted=False))
        aj = project / "book" / "authors.json"
        if aj.exists():
            h = build_dir / "_b5-authors.html"
            h.write_text(_authors_html(json.loads(aj.read_text(encoding="utf-8"))),
                         encoding="utf-8")
            front.append(new_part("authors", h, pdf_dir / "_authors.pdf",
                                  need_right=False, counted=False,
                                  side="left" if front else "right"))

    for name in chapters:
        html = build_dir / f"{name}.html"
        if not html.exists():
            print(f"[!] HTML 없음: {html}")
            continue
        if name[:2].isdigit():
            n = str(int(name[:2]))
            data = dividers.get(n)
            if data:
                h = build_dir / f"_b5-divider-ch{n}.html"
                h.write_text(_divider_html(data), encoding="utf-8")
                body_parts.append(new_part(
                    "divider", h, pdf_dir / f"_divider-ch{n}.pdf",
                    need_right=True, counted=True,
                    label=f"챕터 {n}. {data['title']}", lvl=1))
            body_parts.append(new_part(
                "chapter", html, pdf_dir / f"{name}.pdf",
                need_right=not data, counted=True,
                side="left" if data else "right"))
        else:
            body_parts.append(new_part(
                "front_back", html, pdf_dir / f"{name}.pdf",
                need_right=name not in start_left, counted=True,
                side="left" if name in start_left else "right",
                label=top_labels.get(name), lvl=1))

    if len(body_parts) < (1 if test_mode else 2):
        print("[!] 변환할 파트 부족")
        return 1

    toc_part = None
    if not test_mode:
        toc_part = new_part("toc", build_dir / "_b5-toc.html", pdf_dir / "_toc.pdf",
                            need_right=True, counted=False)
        parts = front + body_parts[:2] + [toc_part] + body_parts[2:]
    else:
        parts = front + body_parts

    with Renderer() as r:
        # 2) 목차를 뺀 모든 파트 렌더
        for p in parts:
            if p["kind"] == "toc":
                continue
            print(f"[>] {p['pdf'].stem} → B5 PDF ({p['side']})")
            r.render(p["html"], p["pdf"], p["side"])
            p["count"] = _page_count(p["pdf"])
            if p["kind"] in ("divider", "colophon", "authors") and p["count"] != 1:
                print(f"[!] {p['pdf'].stem} 가 {p['count']}쪽으로 넘침 → 쪽 배치가 어긋날 수 있음")
            if p["kind"] == "chapter":
                p["sub"] = _find_heading_offsets(
                    p["pdf"], _chapter_headings(p["html"]))

        # 빈 쪽은 실제 렌더된 쪽 크기에 맞춘다
        import fitz
        with fitz.open(str(parts[0]["pdf"])) as d0:
            w_pt, h_pt = d0[0].rect.width, d0[0].rect.height
        blank_pdf = pdf_dir / "_blank.pdf"
        bd = fitz.open()
        bd.new_page(width=w_pt, height=h_pt)
        bd.save(str(blank_pdf))
        bd.close()

        # 3) 쪽 배치. 시작 쪽(홀/짝)이 렌더 가정과 다른 파트는 맞는 쪽으로 다시 굽는다
        toc_count = 0
        for _ in range(4):
            segs, starts = _layout(parts, toc_count, blank_pdf)
            redo = [i for i, p in enumerate(parts)
                    if p["kind"] != "toc" and starts[i]["side"] != p["side"]]
            if not redo:
                break
            for i in redo:
                p = parts[i]
                p["side"] = starts[i]["side"]
                print(f"[>] {p['pdf'].stem} 시작 쪽이 달라 다시 렌더 ({p['side']})")
                r.render(p["html"], p["pdf"], p["side"])
                p["count"] = _page_count(p["pdf"])
        else:
            print("[!] 쪽 배치가 수렴하지 않음")
            return 1

        # 4) 목차: 번호는 목차 쪽수와 무관하므로 한 번 굽고 쪽수만 반영해 다시 배치
        if toc_part:
            entries = _toc_entries(parts, starts)
            toc_part["html"].write_text(_toc_html(entries), encoding="utf-8")
            print("[>] 목차 → B5 PDF")
            r.render(toc_part["html"], toc_part["pdf"], "right")
            toc_count = _page_count(toc_part["pdf"])
            segs, starts = _layout(parts, toc_count, blank_pdf)
            if _toc_entries(parts, starts) != entries:
                print("[!] 목차 쪽번호가 배치 후 달라짐 → 목차 재생성 필요")
                return 1

    # 5) 병합 + 쪽번호 + 북마크
    from pypdf import PdfWriter
    writer = PdfWriter()
    page_flags = []
    for pdf, cnt, counted, blank in segs:
        if cnt == 0:
            continue
        writer.append(str(pdf))
        page_flags += [(counted, blank)] * cnt
    tmp = pdf_dir / "_merged_tmp.pdf"
    with open(tmp, "wb") as f:
        writer.write(f)
    writer.close()

    toc_idx = parts.index(toc_part) if toc_part else None
    toc_phys = starts[toc_idx]["phys"] if toc_idx is not None else None
    merged = pdf_dir / out_name
    _finalize(tmp, merged, page_flags, toc_phys, _toc_entries(parts, starts))
    tmp.unlink(missing_ok=True)

    with fitz.open(str(merged)) as m:
        print(f"[OK] B5 병합 완료: {merged}")
        print(f"     {m.page_count}쪽, 쪽 크기 {m[0].rect.width:.1f}x{m[0].rect.height:.1f}pt "
              f"(46배판 {PAGE_W_MM}x{PAGE_H_MM}mm = {PAGE_W_MM * 72 / 25.4:.1f}x{PAGE_H_MM * 72 / 25.4:.1f}pt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
