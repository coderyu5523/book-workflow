#!/usr/bin/env python3
"""ConnectHR — 사내 AI 비서 만들기 PDF 빌드 스크립트 (Typst)"""

import sys
from pathlib import Path

# 스킬 엔진 경로
SKILL_SCRIPTS = Path(__file__).resolve().parent.parent.parent.parent / ".claude/skills/pub-build/references/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from typst_builder import build  # noqa: E402

BASE = Path(__file__).resolve().parent.parent  # projects/사내AI비서_v2

config = {
    "title": "ConnectHR — 사내 AI 비서 만들기",
    "base": BASE,
    "assets_dir": BASE / "assets",
    "mermaid_out": BASE / "book" / "_mermaid_out",
    "template": BASE / "book" / "templates" / "book.typ",
    "font_path": None,

    "front": [
        BASE / "book/body_v2/00-들어가며.md",
    ],
    "chapters": [
        BASE / "book/body_v2/01-환각과-RAG의-첫-만남.md",
        BASE / "book/body_v2/02-일단-사내-시스템부터.md",
        BASE / "book/body_v2/03-어떤-문서를-넣을까.md",
        BASE / "book/body_v2/04-문서를-지식으로-바꾸다.md",
        BASE / "book/body_v2/05-드디어-답해준다.md",
        BASE / "book/body_v2/06-연차도-규정도-한번에.md",
        BASE / "book/body_v2/07-실제로-써보니.md",
        BASE / "book/body_v2/08-엉뚱한-문서를-가져온다.md",
        BASE / "book/body_v2/09-질문을-제대로-이해-못한다.md",
        BASE / "book/body_v2/10-PDF-이미지까지-잡아라.md",
    ],
    "back": [
        BASE / "book/body_v2/11-에필로그.md",
        BASE / "book/body_v2/12-부록.md",
    ],

    "output_md": BASE / "book" / "ConnectHR_통합본.md",
    "output_typ": BASE / "book" / "ConnectHR_통합본.typ",
    "output_pdf": BASE / "book" / "book_ConnectHR_통합본_typst.pdf",

    "layout_checker": str(BASE / "book" / "pdf_layout_checker.py"),
}

if __name__ == "__main__":
    build(config)
