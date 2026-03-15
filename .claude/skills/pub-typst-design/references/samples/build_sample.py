#!/usr/bin/env python3
"""샘플 PDF 생성 스크립트 — 새 디자인 확인용"""
import subprocess
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
SKILL_DIR = Path(__file__).resolve().parents[4] / ".claude" / "skills"
TEMPLATE = SKILL_DIR / "pub-typst-design" / "references" / "templates" / "book_base.typ"

# typst_builder의 후처리 함수를 임포트
sys.path.insert(0, str(SKILL_DIR / "pub-build" / "references" / "scripts"))
from typst_builder import fix_typst_content


def main():
    md_path = BASE / "sample_test.md"
    typ_raw = BASE / "sample_test.raw.typ"
    typ_final = BASE / "sample_test.typ"
    pdf_path = BASE / "sample_test.pdf"

    # 1. Pandoc: MD → Typst
    cmd = [
        "pandoc", str(md_path),
        "-f", "markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks-citations",
        "-t", "typst", "-o", str(typ_raw), "--wrap=none",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Pandoc 오류: {result.stderr}")
        return
    print("Pandoc 변환 완료")

    # 2. 후처리
    raw = typ_raw.read_text(encoding="utf-8")
    fixed = fix_typst_content(raw)

    # 3. 표 열 균등화 (이미 fix_typst_content에 포함)

    # 4. 템플릿 병합 (프로젝트 변수 + book_base.typ + 본문)
    project_vars = """
#let book-title = "사내 AI 비서"
#let book-subtitle = "RAG 기반 업무 자동화"
#let book-description = [사내 문서를 활용한 AI 비서 구축 가이드]
#let book-header-title = "사내 AI 비서"
"""
    template = TEMPLATE.read_text(encoding="utf-8")
    final = project_vars + "\n" + template + "\n" + fixed
    typ_final.write_text(final, encoding="utf-8")
    print("템플릿 병합 완료")

    # 5. Typst 컴파일
    cmd = [
        "typst", "compile", str(typ_final), str(pdf_path),
        "--font-path", str(Path.home() / "Library" / "Fonts"),
        "--root", "/",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Typst 오류:\n{result.stderr}")
        return

    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"PDF 생성 완료: {pdf_path} ({size_mb:.2f} MB)")
    typ_raw.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
