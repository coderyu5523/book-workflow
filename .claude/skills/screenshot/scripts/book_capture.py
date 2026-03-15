#!/usr/bin/env python3
"""서적용 터미널 캡처 — Rich SVG → 2단계 Playwright PNG.

흰 배경 + 검정 텍스트(볼드만 유지). D2Coding 고정폭 폰트로 한글 표 정렬 보장.
Rich SVG 내장 프레임을 제거하고, 커스텀 macOS 터미널 HTML 프레임으로 감싸서
인쇄 품질 PNG를 생성한다.

파이프라인:
    1. 명령 실행 → ANSI 출력 수집
    2. Rich SVG 렌더링 (프레임 요소 제거 + D2Coding 폰트 + textLength 수정)
    3. 1차 캡처: SVG 콘텐츠만 → 투명 배경 PNG
    4. 2차 캡처: macOS HTML 프레임에 내부 PNG 삽입 → 최종 PNG

사용법 (CLI):
    # 명령 실행
    python book_capture.py \\
        --cmd ".venv/bin/python -m tuning.step1_chunk_experiment --step 1-1" \\
        --cwd projects/사내AI비서_v2/code/ex08 \\
        --output assets/CH08/08_chunk-size.png \\
        --title "step 1-1: 청크 크기 실험"

    # 텍스트 직접 입력
    python book_capture.py --text "Hello World" --output out.png

    # 파일 읽기
    python book_capture.py --file output.txt --output out.png

    # stdin 파이프
    cat output.txt | python book_capture.py --output out.png

사용법 (Python):
    from book_capture import book_capture_png
    # 명령 실행
    book_capture_png(
        cmd=".venv/bin/python -m tuning.step1_chunk_experiment --step 1-1",
        output="assets/CH08/08_chunk-size.png",
        cwd="projects/사내AI비서_v2/code/ex08",
        title="step 1-1: 청크 크기 실험",
    )
    # 텍스트 직접 입력
    book_capture_png(text="Hello World", output="out.png", title="예시")
"""

import argparse
import html as html_mod
import os
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from rich.cells import cell_len
from rich.console import Console
from rich.terminal_theme import TerminalTheme
from rich.text import Text


# ---------------------------------------------------------------------------
# 1. 명령 실행 → ANSI 텍스트 획득
# ---------------------------------------------------------------------------

def run_command(cmd: str, cwd: str, columns: int = 200) -> str:
    """셸 명령을 실행하고 ANSI 컬러가 포함된 stdout을 반환한다."""
    env = os.environ.copy()
    env["COLUMNS"] = str(columns)
    env["FORCE_COLOR"] = "1"
    env["TERM"] = "xterm-256color"

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        env=env,
    )
    if result.returncode != 0 and not result.stdout.strip():
        raise RuntimeError(
            f"명령 실패 (rc={result.returncode}): {result.stderr[:300]}"
        )
    return result.stdout


# ---------------------------------------------------------------------------
# 2. ANSI 텍스트 전처리
# ---------------------------------------------------------------------------

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """ANSI 이스케이프 시퀀스를 제거한다."""
    return _ANSI_RE.sub("", text)


def filter_lines(
    ansi_text: str,
    patterns: list[dict] | None = None,
) -> str:
    """장식선이 포함된 행을 필터링한다.

    각 패턴은 {"keywords": [...], "replace": "..."} 형태.
    - replace가 None이면 해당 패턴 스킵
    - replace가 ""이면 행 삭제
    - replace가 문자열이면 볼드 텍스트로 교체

    Args:
        ansi_text: 원본 ANSI 텍스트
        patterns: 필터 패턴 리스트
    """
    if not patterns:
        return ansi_text

    lines = ansi_text.split("\n")
    result = []
    for line in lines:
        plain = strip_ansi(line)
        matched = False
        for pat in patterns:
            keywords = pat.get("keywords", [])
            replace = pat.get("replace")
            pad = pat.get("pad", 28)
            if not keywords or replace is None:
                continue
            if all(kw in plain for kw in keywords):
                matched = True
                if replace:
                    result.append(
                        " " * pad + f"\x1b[1m{replace}\x1b[0m"
                    )
                # replace == "" → 행 삭제
                break
        if not matched:
            result.append(line)
    return "\n".join(result)


# ---------------------------------------------------------------------------
# 3. Rich SVG 생성 (프레임 제거 + D2Coding 폰트)
# ---------------------------------------------------------------------------

# 서적용 테마: 모든 색상 → 검정, 배경 흰색
BOOK_THEME = TerminalTheme(
    background=(255, 255, 255),
    foreground=(0, 0, 0),
    normal=[(0, 0, 0)] * 8,
    bright=[(0, 0, 0)] * 8,
)

# D2Coding: 영문 1 : 한글 2 폭 비율이 정확한 고정폭 폰트
_FONT_IMPORT = (
    "@import url('//cdn.jsdelivr.net/gh/joungkyun/font-d2coding/d2coding.css');"
)
_FONT_FAMILY = "font-family: 'D2Coding', monospace;"


def make_svg(ansi_text: str, max_lines: int = 0, columns: int = 0) -> str:
    """ANSI 텍스트를 서적용 SVG 문자열로 변환한다.

    Rich SVG 내장 프레임(배경 rect, 신호등 circle)을 제거하여
    순수 콘텐츠만 남긴다. macOS 프레임은 HTML 래퍼에서 별도 생성.

    Args:
        ansi_text: 전처리된 ANSI 텍스트
        max_lines: 최대 줄 수 (0이면 제한 없음)
        columns: 콘솔 너비 상한 (0이면 콘텐츠에 맞춤, Rich Table은 0 권장)
    """
    text = ansi_text.strip()

    # 줄 수 제한
    if max_lines > 0:
        lines = text.split("\n")
        if len(lines) > max_lines:
            text = "\n".join(lines[:max_lines]) + "\n... (이하 생략)"

    # trailing 공백 제거 (COLUMNS 패딩)
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    # 콘텐츠 너비 계산 (타이트하게, 상한 적용)
    plain_lines = strip_ansi(text).split("\n")
    max_len = max([cell_len(line) for line in plain_lines] + [80])
    calc_width = max_len + 4
    if columns > 0:
        calc_width = min(calc_width, columns)

    # Rich Console → SVG
    console = Console(record=True, width=calc_width)
    text_obj = Text.from_ansi(text)
    console.print(text_obj)

    svg = console.export_svg(theme=BOOK_THEME)

    # D2Coding 폰트 주입 (영문:한글 = 1:2 폭 비율 보장)
    svg = svg.replace("<style>", f"<style>\n    {_FONT_IMPORT}")
    svg = svg.replace("font-family: Fira Code, monospace;", _FONT_FAMILY)

    # Rich 브랜딩 제거
    svg = svg.replace("Rich", "")
    svg = svg.replace("https://www.textualize.io", "")

    # Rich SVG 내장 프레임 제거 (macOS 프레임은 HTML에서 별도 생성)
    svg = re.sub(
        r'<rect fill="#ffffff" stroke="[^"]+" stroke-width="1" [^>]+/>', "", svg
    )
    svg = re.sub(r'<circle[^>]+fill="#ff5f57"(\s*/)?>', "", svg)
    svg = re.sub(r'<circle[^>]+fill="#febc2e"(\s*/)?>', "", svg)
    svg = re.sub(r'<circle[^>]+fill="#28c840"(\s*/)?>', "", svg)

    # 한글(더블 위드스) textLength 겹침 방지
    def _fix_text_length(match):
        full = match.group(0)
        text_content = match.group(2)
        raw_text = html_mod.unescape(text_content)
        if cell_len(raw_text) != len(raw_text):
            return re.sub(r'\s*textLength="[^"]+"', "", full)
        return full

    svg = re.sub(
        r'(<text[^>]*>)(.*?)</text>', _fix_text_length, svg, flags=re.DOTALL
    )

    # SVG 0x0 수축 버그 방지
    vb_match = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if vb_match:
        svg_w, svg_h = vb_match.group(1), vb_match.group(2)
        svg = svg.replace(
            "<svg ", f'<svg width="{svg_w}px" height="{svg_h}px" ', 1
        )

    return svg


# ---------------------------------------------------------------------------
# 4. 2단계 Playwright 캡처 (내부 PNG → macOS 프레임 래핑)
# ---------------------------------------------------------------------------

_INNER_HTML = """\
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; padding: 0; background: transparent; display: inline-block; }}
    #capture {{ display: inline-block; }}
    svg {{ display: block; }}
</style>
</head>
<body>
    <div id="capture">
        {svg}
    </div>
</body>
</html>
"""

_MACBOOK_HTML = """\
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 40px;
        background-color: transparent;
        display: inline-block;
    }}
    .macbook-terminal {{
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        border: 1px solid #d1d1d1;
        background: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                     Helvetica, Arial, sans-serif;
        display: inline-block;
    }}
    .title-bar {{
        background: linear-gradient(to bottom, #f5f5f5, #e8e8e8);
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        border-bottom: 1px solid #d1d1d1;
    }}
    .dots {{
        display: flex;
        gap: 8px;
        position: absolute;
        left: 12px;
    }}
    .dot {{
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }}
    .dot-red {{ background-color: #ff5f56; border: 1px solid #e0443e; }}
    .dot-yellow {{ background-color: #ffbd2e; border: 1px solid #dea123; }}
    .dot-green {{ background-color: #27c93f; border: 1px solid #1aab29; }}
    .title-text {{
        font-size: 13px;
        color: #555555;
        font-weight: 600;
        letter-spacing: 0.3px;
        user-select: none;
    }}
    .content-area {{
        padding: 0px 8px 8px 8px;
        display: flex;
    }}
    img {{
        display: block;
        max-width: 100%;
        margin-top: -35px;
        margin-bottom: -10px;
    }}
</style>
</head>
<body>
    <div id="macbook-capture" class="macbook-terminal">
        <div class="title-bar">
            <div class="dots">
                <div class="dot dot-red"></div>
                <div class="dot dot-yellow"></div>
                <div class="dot dot-green"></div>
            </div>
            <div class="title-text">{title}</div>
        </div>
        <div class="content-area">
            <img src="file://{inner_png}" />
        </div>
    </div>
</body>
</html>
"""


def svg_to_png(
    svg: str,
    output_path: str,
    title: str = "",
    font_wait_ms: int = 1000,
) -> None:
    """2단계 Playwright 캡처: SVG → 내부 PNG → macOS 프레임 래핑 → 최종 PNG.

    1차: SVG를 투명 배경으로 캡처 (콘텐츠만)
    2차: 내부 PNG를 macOS HTML 프레임에 삽입하여 최종 캡처
    """
    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    tmp_inner_html = output.with_name(output.stem + "_inner.tmp.html")
    tmp_inner_png = output.with_name(output.stem + "_inner.tmp.png")
    tmp_frame_html = output.with_name(output.stem + "_frame.tmp.html")

    # 1차: SVG 콘텐츠를 투명 배경 PNG로 캡처
    tmp_inner_html.write_text(
        _INNER_HTML.format(svg=svg), encoding="utf-8"
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 1000})

            # 1차 캡처 (투명 배경)
            page.goto(f"file://{tmp_inner_html}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(font_wait_ms)

            target = page.locator("#capture")
            target.screenshot(
                path=str(tmp_inner_png),
                omit_background=True,
                type="png",
            )

            # 2차: macOS 프레임 HTML 생성 및 캡처
            frame_html = _MACBOOK_HTML.format(
                title=title,
                inner_png=str(tmp_inner_png),
            )
            tmp_frame_html.write_text(frame_html, encoding="utf-8")

            page.goto(f"file://{tmp_frame_html}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)

            macbook = page.locator("#macbook-capture")
            macbook.screenshot(
                path=str(output),
                omit_background=True,
                type="png",
            )

            browser.close()
    finally:
        for tmp in (tmp_inner_html, tmp_inner_png, tmp_frame_html):
            if tmp.exists():
                tmp.unlink()

    size_kb = output.stat().st_size / 1024
    print(f"[book_capture] {output} ({size_kb:.1f} KB)")


# ---------------------------------------------------------------------------
# 5. 통합 함수 (스킬에서 호출)
# ---------------------------------------------------------------------------

def book_capture_png(
    cmd: str | None = None,
    output: str = "",
    cwd: str | None = None,
    columns: int = 200,
    max_lines: int = 0,
    title: str = "",
    filters: list[dict] | None = None,
    font_wait_ms: int = 1000,
    text: str | None = None,
    file: str | None = None,
) -> str:
    """서적용 PNG 캡처 원스텝 함수.

    입력 소스: cmd(셸 명령 실행), text(직접 텍스트), file(파일 읽기) 중 하나.

    Args:
        filters: 장식선 필터 패턴 리스트.
            [{"keywords": ["step 1-1:", "청크"], "replace": ""},
             {"keywords": ["실험 완료"], "replace": ""}]

    Returns:
        생성된 PNG 파일의 절대 경로
    """
    work_dir = cwd or os.getcwd()

    # 1. 텍스트 획득
    if cmd:
        ansi_text = run_command(cmd, work_dir, columns)
    elif text:
        ansi_text = text
    elif file:
        ansi_text = Path(file).read_text(encoding="utf-8")
    else:
        raise ValueError("cmd, text, file 중 하나를 지정해야 합니다.")

    # 2. 장식선 필터링
    ansi_text = filter_lines(ansi_text, filters)

    # 3. SVG 생성 (프레임 제거된 순수 콘텐츠)
    svg = make_svg(ansi_text, max_lines)

    # 4. 2단계 PNG 변환 (내부 PNG → macOS 프레임)
    svg_to_png(svg, output, title, font_wait_ms)

    return str(Path(output).resolve())


# ---------------------------------------------------------------------------
# 6. CLI
# ---------------------------------------------------------------------------

def resolve_input(args) -> str:
    """입력 소스(--cmd, --text, --file, stdin)에서 텍스트를 반환한다."""
    if args.cmd:
        return run_command(args.cmd, args.cwd or os.getcwd(), args.columns)
    elif args.text:
        return args.text.replace("\\n", "\n")
    elif args.file:
        return Path(args.file).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        raise SystemExit(
            "에러: --cmd, --text, --file 중 하나를 지정하거나 stdin으로 입력하세요."
        )


def main():
    parser = argparse.ArgumentParser(
        description="서적용 터미널 캡처 (Rich SVG → macOS 프레임 PNG)"
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--cmd", help="실행할 셸 명령")
    source.add_argument("--text", help="직접 입력할 텍스트")
    source.add_argument("--file", help="텍스트를 읽을 파일 경로")
    parser.add_argument("--output", required=True, help="출력 PNG 경로")
    parser.add_argument("--cwd", default=None, help="작업 디렉토리 (기본: 현재)")
    parser.add_argument(
        "--columns", type=int, default=200, help="COLUMNS 환경변수 (기본: 200)"
    )
    parser.add_argument(
        "--max-lines", type=int, default=0, help="최대 줄 수 (기본: 무제한)"
    )
    parser.add_argument(
        "--title", default="", help="macOS 타이틀바 제목 (기본: 빈칸)"
    )
    parser.add_argument(
        "--strip",
        action="append",
        default=None,
        help=(
            "장식선 필터. 여러 번 사용 가능. "
            "'키워드1,키워드2' → 행 삭제. "
            "'키워드1,키워드2=교체텍스트' → 깨끗한 제목으로 교체. "
            "예: --strip 'step 1-1:,청크=step 1-1: 청크 크기 실험'"
        ),
    )
    parser.add_argument(
        "--font-wait", type=int, default=1000,
        help="폰트 로딩 대기 ms (기본: 1000)",
    )

    args = parser.parse_args()

    filters = None
    if args.strip:
        filters = []
        for pat in args.strip:
            if "=" in pat:
                kw_part, replace = pat.split("=", 1)
            else:
                kw_part, replace = pat, ""
            keywords = [kw.strip() for kw in kw_part.split(",")]
            filters.append({"keywords": keywords, "replace": replace})

    ansi_text = resolve_input(args)

    book_capture_png(
        text=ansi_text,
        output=args.output,
        max_lines=args.max_lines,
        title=args.title,
        filters=filters,
        font_wait_ms=args.font_wait,
    )


if __name__ == "__main__":
    main()
