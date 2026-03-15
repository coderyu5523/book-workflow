#!/usr/bin/env python3
"""사내AI비서_v2 — Typst 기반 PDF 빌드 스크립트

실행:
    cd projects/사내AI비서_v2
    python3 book/build_pdf_typst.py
"""

import sys
from pathlib import Path

# 스킬 엔진 경로 추가
SKILL_SCRIPTS = Path(__file__).resolve().parents[3] / ".claude" / "skills" / "pub-build" / "references" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

import typst_builder

# ── 프로젝트 경로 ──
BASE = Path(__file__).resolve().parent.parent  # projects/사내AI비서_v2
BOOK = BASE / "book"
CHAPTERS = BOOK / "body_v2"
FRONT = BOOK / "front"
BACK = BOOK / "back"
ASSETS = BASE / "assets"

CONFIG = {
    "title": "사내 AI 비서",
    "base": BASE,
    "assets_dir": ASSETS,
    "mermaid_out": BOOK / "mermaid_output",
    "template": BOOK / "templates" / "book.typ",
    "font_path": Path.home() / "Library" / "Fonts",
    "front": [
        FRONT / "prologue.md",
    ],
    "chapters": [
        CHAPTERS / "00-들어가며.md",
        CHAPTERS / "01-환각과-RAG의-첫-만남.md",
        CHAPTERS / "02-일단-사내-시스템부터.md",
        CHAPTERS / "03-어떤-문서를-넣을까.md",
        CHAPTERS / "04-문서를-지식으로-바꾸다.md",
        CHAPTERS / "05-드디어-답해준다.md",
        CHAPTERS / "06-연차도-규정도-한번에.md",
        CHAPTERS / "07-실제로-써보니.md",
        CHAPTERS / "08-엉뚱한-문서를-가져온다.md",
        CHAPTERS / "09-질문을-제대로-이해-못한다.md",
        CHAPTERS / "10-PDF-이미지까지-잡아라.md",
    ],
    "back": [
        BACK / "epilogue.md",
        BACK / "appendix.md",
    ],
    "output_md": BOOK / "ConnectHR_통합본.md",
    "output_typ": BOOK / "ConnectHR_통합본.typ",
    "output_pdf": BOOK / "ConnectHR_통합본.pdf",
}

if __name__ == "__main__":
    typst_builder.build(CONFIG)
