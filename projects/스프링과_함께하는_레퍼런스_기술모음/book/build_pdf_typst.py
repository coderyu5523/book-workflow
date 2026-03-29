#!/usr/bin/env python3
"""스프링과 함께하는 레퍼런스 기술모음 — Typst 기반 PDF 빌드 스크립트

실행:
    cd projects/스프링과_함께하는_레퍼런스_기술모음
    python3 book/build_pdf_typst.py           # 통합 PDF
    python3 book/build_pdf_typst.py --chapter 01  # CH01만 개별 빌드
    python3 book/build_pdf_typst.py --all     # 챕터별 개별 PDF 전부
"""

import sys
from pathlib import Path

# 스킬 엔진 경로 추가
SKILL_SCRIPTS = Path(__file__).resolve().parents[3] / ".claude" / "skills" / "pub-build" / "references" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

import typst_builder

# ── 프로젝트 경로 ──
BASE = Path(__file__).resolve().parent.parent  # projects/스프링과_함께하는_레퍼런스_기술모음
BOOK = BASE / "book"
CHAPTERS = BASE / "chapters"
FRONT = BOOK / "front"
BACK = BOOK / "back"
ASSETS = BASE / "assets"

CHAPTER_FILES = [
    CHAPTERS / "01-Docker로-시작하는-개발-환경.md",
    CHAPTERS / "02-OAuth-2.0-OIDC-Kakao-소셜-로그인.md",
    CHAPTERS / "03-Redis-세션-공유.md",
    CHAPTERS / "04-Base64-이미지-업로드.md",
    CHAPTERS / "05-Presigned-URL-S3-Lambda.md",
    CHAPTERS / "06-Polling-SSE-WebSocket.md",
    CHAPTERS / "07-HLS-스트리밍-기술선택.md",
    CHAPTERS / "08-Elasticsearch-키워드-검색.md",
    CHAPTERS / "09-RabbitMQ-메시지-큐.md",
]

CONFIG = {
    "title": "처음 만나는 스프링 주변 기술",
    "subtitle": "Docker부터 RabbitMQ까지 9가지 실습",
    "base": BASE,
    "assets_dir": ASSETS,
    "template": BOOK / "templates" / "book.typ",
    "font_path": Path.home() / "Library" / "Fonts",
    "front": [
        FRONT / "preface.md",
        FRONT / "prologue.md",
    ],
    "chapters": CHAPTER_FILES,
    "back": [
        BACK / "afterword.md",
    ],
    "output_md": BOOK / "처음_만나는_스프링_주변_기술_통합본.md",
    "output_typ": BOOK / "처음_만나는_스프링_주변_기술_통합본.typ",
    "output_pdf": BOOK / "처음_만나는_스프링_주변_기술_통합본.pdf",
    "output_dir": BOOK / "chapter_pdfs",
    "mermaid_out": BOOK / "_mermaid_images",
}


def build_single_chapter(ch_num: str):
    """특정 챕터 하나만 개별 PDF 빌드"""
    for f in CHAPTER_FILES:
        if f.name.startswith(ch_num):
            print(f"챕터 개별 빌드: {f.name}")
            result = typst_builder.build_chapter(f, CONFIG)
            if result:
                print(f"완료: {result}")
            return
    print(f"[오류] 챕터 '{ch_num}'을 찾을 수 없습니다.")


def build_all_chapters():
    """모든 챕터를 개별 PDF로 빌드"""
    print("전체 챕터 개별 빌드")
    print("=" * 50)
    results = []
    for f in CHAPTER_FILES:
        result = typst_builder.build_chapter(f, CONFIG)
        if result:
            results.append(result)
    print(f"\n{'=' * 50}")
    print(f"완료: {len(results)}/{len(CHAPTER_FILES)} 챕터 빌드")


if __name__ == "__main__":
    # --design 인자 처리
    if "--design" in sys.argv:
        idx = sys.argv.index("--design")
        if idx + 1 < len(sys.argv):
            CONFIG["design"] = sys.argv[idx + 1]

    if "--chapter" in sys.argv:
        idx = sys.argv.index("--chapter")
        if idx + 1 < len(sys.argv):
            build_single_chapter(sys.argv[idx + 1])
        else:
            print("사용법: python3 build_pdf_typst.py --chapter 01")
    elif "--all" in sys.argv:
        build_all_chapters()
    else:
        typst_builder.build(CONFIG)
        # 목차 depth 조정: 9챕터 × h3이 많아 목차가 넘침 → depth 2로 축소 후 재컴파일
        typ_path = CONFIG["output_typ"]
        text = typ_path.read_text(encoding="utf-8")
        if "depth: 3," in text:
            text = text.replace("depth: 3,", "depth: 2,")
            typ_path.write_text(text, encoding="utf-8")
            typst_builder.typst_compile(typ_path, CONFIG["output_pdf"], CONFIG.get("font_path"))
