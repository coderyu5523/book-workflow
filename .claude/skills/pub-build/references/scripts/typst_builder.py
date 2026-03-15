#!/usr/bin/env python3
"""범용 마크다운 → Typst → PDF 변환 엔진
   프로젝트별 설정(챕터 목록, 경로 등)은 호출 측에서 config로 전달.
   의존성: typst, pandoc, Pillow, PyMuPDF
   다이어그램: D2로 사전 렌더링된 PNG를 사용 (Mermaid 미사용)
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path


# ══════════════════════════════════════
# 이미지 공백 자동 제거
# ══════════════════════════════════════

def autocrop_image(img_path: Path, padding: int = 6, tolerance: int = 10) -> bool:
    """이미지 파일의 위아래/좌우 공백을 자동으로 잘라냄.
    tolerance: 배경색과의 허용 오차 (Gemini 이미지 등 연한 회색 배경 대응)"""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return False

    try:
        img = Image.open(img_path).convert("RGB")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        if tolerance > 0:
            diff = diff.point(lambda x: 0 if x <= tolerance else x)
        bbox = diff.getbbox()
        if bbox:
            bbox = (
                max(0, bbox[0] - padding),
                max(0, bbox[1] - padding),
                min(img.width, bbox[2] + padding),
                min(img.height, bbox[3] + padding),
            )
            trimmed = (bbox[1]) + (img.height - bbox[3])
            if trimmed > 20:
                cropped = img.crop(bbox)
                cropped.save(img_path)
                return True
    except Exception:
        pass
    return False


def _tolerance_for_image(img_path: Path) -> int:
    """이미지 경로에 따른 autocrop tolerance 결정.
    gemini/ → 15 (연한 배경), diagram/ → 5, terminal/ → 0"""
    parts = str(img_path)
    if '/gemini/' in parts:
        return 15
    elif '/diagram/' in parts:
        return 5
    elif '/terminal/' in parts:
        return 0
    return 10  # 기본값


def autocrop_all_assets(assets_dir: Path, mermaid_out: Path):
    """assets + mermaid 디렉토리의 모든 PNG 이미지 공백 제거"""
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("   [경고] Pillow 미설치 → 이미지 공백 자르기 건너뜀 (pip install Pillow)")
        return

    count = 0
    for png in assets_dir.rglob("*.png"):
        tol = _tolerance_for_image(png)
        if autocrop_image(png, tolerance=tol):
            count += 1
    if mermaid_out.exists():
        for png in mermaid_out.rglob("*.png"):
            tol = _tolerance_for_image(png)
            if autocrop_image(png, tolerance=tol):
                count += 1
    if count:
        print(f"   이미지 공백 제거: {count}개 파일")


# ══════════════════════════════════════
# 전처리 함수
# ══════════════════════════════════════

def fix_image_paths(text: str, source_file: Path) -> str:
    """마크다운 이미지 상대경로 → 절대경로로 변환 (file:// 없이)"""
    source_dir = source_file.parent

    def replace_img(m):
        alt = m.group(1)
        rel_path = m.group(2)
        if rel_path.startswith('file://'):
            return f'![{alt}]({rel_path[7:]})'
        abs_path = (source_dir / rel_path).resolve()
        if abs_path.exists():
            return f'![{alt}]({abs_path})'
        else:
            return f'*[이미지: {alt}]*'

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)


def clean_comments(text: str) -> str:
    """HTML 주석 제거 (GEMINI PROMPT, CAPTURE NEEDED, 기타).
    DUAL-IMAGE 마커는 보존하여 2열 이미지 배치에 사용."""
    text = re.sub(r'<!--\s*\[GEMINI PROMPT.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--\s*\[CAPTURE NEEDED.*?-->', '', text, flags=re.DOTALL)
    # DUAL-IMAGE 마커를 임시 플레이스홀더로 보존
    text = re.sub(r'<!--\s*\[DUAL-IMAGE\]\s*-->', '%%DUAL_IMAGE_START%%', text)
    text = re.sub(r'<!--\s*\[/DUAL-IMAGE\]\s*-->', '%%DUAL_IMAGE_END%%', text)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text


def fix_br_tags(text: str) -> str:
    """코드 블록 밖의 <br> → 마크다운 줄바꿈으로 변환.
    코드 블록(```) 내의 <br>는 보존."""
    parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if not part.startswith('```'):
            parts[i] = re.sub(r'<br\s*/?>', '  ', part)
    return ''.join(parts)


def remove_story_part_heading(text: str) -> str:
    """'## 이야기 파트' 및 '## 기술 파트' 제목을 제거."""
    text = re.sub(r'^##\s+이야기\s*파트\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+기술\s*파트\s*$', '', text, flags=re.MULTILINE)
    return text


# ══════════════════════════════════════
# 통합
# ══════════════════════════════════════

def build_integrated_md(front: list, chapters: list, back: list) -> str:
    """모든 파일을 하나의 마크다운으로 통합"""
    parts = []
    all_files = [("front", front), ("chapters", chapters), ("back", back)]

    for section_name, files in all_files:
        for f in files:
            if not f.exists():
                print(f"   [경고] 파일 없음: {f}")
                continue

            print(f"   처리 중: {f.name}")
            content = f.read_text(encoding="utf-8")
            content = clean_comments(content)
            content = fix_image_paths(content, f)
            content = remove_story_part_heading(content)
            content = fix_br_tags(content)
            parts.append(content)
            parts.append("\n\n---\n\n")

    return "\n".join(parts)


# ══════════════════════════════════════
# Pandoc 변환
# ══════════════════════════════════════

def md_to_typst(md_path: Path, typ_path: Path) -> bool:
    """Pandoc으로 마크다운 → Typst 변환"""
    cmd = [
        'pandoc',
        str(md_path),
        '-f', 'markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks-citations',
        '-t', 'typst',
        '-o', str(typ_path),
        '--wrap=none',
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   [오류] Pandoc 변환 실패: {result.stderr}")
        return False

    print(f"   Pandoc 변환 완료: {typ_path.name}")
    return True


# ══════════════════════════════════════
# Typst 후처리
# ══════════════════════════════════════

def _get_image_aspect_ratio(path: str) -> float | None:
    """이미지의 종횡비(width/height)를 반환. 실패 시 None."""
    try:
        from PIL import Image
        img = Image.open(path)
        w, h = img.size
        return w / h if h > 0 else None
    except Exception:
        return None


def _detect_image_max_width(path: str) -> str:
    """이미지 실제 크기 + 종횡비 기반으로 최대 너비(비율) 결정.
    경로 패턴 의존을 최소화하고 이미지 자체 특성으로 크기를 결정한다.

    예외 (경로 기반 고정값):
      - chapter-opening: 항상 0.4
      - exercise-flow: 항상 0.85

    일반 이미지 (종횡비 기반):
      - 초광폭 (AR > 2.5): 0.85
      - 가로형  (AR > 1.8): 0.75
      - 가로형  (AR > 1.3): 0.65
      - 정방형  (0.7~1.3):  0.55
      - 세로형  (AR < 0.7): 0.4
    """
    # 예외: 경로 기반 고정값
    if 'chapter-opening' in path:
        return '0.4'
    if 'exercise-flow' in path:
        return '0.85'

    # 이미지 종횡비 분석
    ar = _get_image_aspect_ratio(path)
    if ar is None:
        return '0.6'  # 분석 실패 시 기본값

    if ar > 2.5:
        return '0.7'
    elif ar > 1.8:
        return '0.65'
    elif ar > 1.3:
        return '0.6'
    elif ar > 0.7:
        return '0.45'
    else:
        return '0.4'


def fix_typst_content(text: str) -> str:
    """Pandoc 출력의 Typst 코드를 후처리"""

    # 1. 이미지 수정: !#link("path")[alt] → #auto-image (페이지 공간 자동 조절)
    def fix_image(m):
        path = m.group(1)
        alt = m.group(2).strip()
        max_w = _detect_image_max_width(path)
        if alt:
            return f'#auto-image("{path}", alt: [{alt}], max-width: {max_w})'
        else:
            return f'#auto-image("{path}", max-width: {max_w})'

    text = re.sub(r'!#link\("([^"]+)"\)\[([^\]]*)\]', fix_image, text)

    # 2. 이미지 수정: #box(image("path")) → #auto-image
    def fix_box_image(m):
        path = m.group(1)
        max_w = _detect_image_max_width(path)
        return f'#auto-image("{path}", max-width: {max_w})'

    text = re.sub(r'#box\(image\("([^"]+)"\)\)', fix_box_image, text)

    # 3. 이미지 수정: #figure(image("path"), caption: [...]) → #auto-image
    def fix_figure_image(m):
        path = m.group(1)
        alt = ' '.join(m.group(2).split()) if m.group(2) else ""
        max_w = _detect_image_max_width(path)
        if alt:
            return f'#auto-image("{path}", alt: [{alt}], max-width: {max_w})'
        else:
            return f'#auto-image("{path}", max-width: {max_w})'

    text = re.sub(
        r'#figure\(image\("([^"]+)"\)\s*,\s*caption:\s*\[([^\]]*)\]\s*\)',
        fix_figure_image, text
    )

    # 3.5 이미지 바로 뒤의 #emph[그림 N-M: ...] 캡션을 auto-image의 alt 파라미터로 병합
    #     이미지와 캡션이 같은 페이지에 있도록 보장 (캡션만 다음 페이지로 넘어가는 고아 방지)
    def _merge_caption_into_auto_image(m):
        img_call = m.group(1)  # #auto-image("path", max-width: 0.6)
        caption = m.group(2)    # 그림 2-4: 설명 텍스트
        # alt: 파라미터가 이미 있으면 건드리지 않음
        if 'alt:' in img_call:
            return m.group(0)
        # max-width: 앞에 alt: 삽입
        return img_call.replace('max-width:', f'alt: [{caption}], max-width:')

    text = re.sub(
        r'(#auto-image\([^)]*\))\s*\n?#emph\[((?:[^\]\\]|\\.)*)\]',
        _merge_caption_into_auto_image,
        text
    )

    # 4. 한국어 라벨 제거 (Pandoc이 생성하는 <한국어-라벨>)
    text = re.sub(r'<[가-힣a-zA-Z0-9.\-_]+>\n', '\n', text)

    # 5. 수평선 바로 뒤에 heading(= 또는 ==)이 오면 수평선 제거 (pagebreak 중복 방지)
    text = re.sub(r'#horizontalrule\n+(?==)', '', text)

    # 6. 남은 수평선을 Typst 방식으로
    text = text.replace('#horizontalrule', '#v(4pt)\n#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))\n#v(4pt)')

    # 7. 라벨이 있는 blockquote → callout-box 변환
    #    > **참고**: 텍스트 → #callout-box([참고], [텍스트])
    def _replace_labeled_quote(m):
        label = m.group(1)
        body = m.group(2).strip()
        return f'#callout-box([{label}], [{body}])'

    text = re.sub(
        r'#quote\(block: true\)\[\s*\n?#strong\[(참고|팁|Note|주의)\]:?\s*(.*?)\s*\]',
        _replace_labeled_quote, text, flags=re.DOTALL
    )

    # 7b. 기술 파트 blockquote → callout-box 변환
    #     이야기→기술 전환점(수평선) 이후의 일반 blockquote를 디자인 B로 변환
    #     대괄호 중첩을 고려하여 매칭 깊이를 추적
    divider = '#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))'
    divider_pos = text.find(divider)
    if divider_pos >= 0:
        story_part = text[:divider_pos]
        tech_part = text[divider_pos:]

        def _replace_tech_quote(text_in):
            """대괄호 깊이를 추적하여 #quote(block: true)[...] → #callout-box([], [...]) 변환"""
            marker = '#quote(block: true)['
            result = []
            i = 0
            while i < len(text_in):
                pos = text_in.find(marker, i)
                if pos < 0:
                    result.append(text_in[i:])
                    break
                result.append(text_in[i:pos])
                # marker 뒤부터 대괄호 깊이 추적
                start = pos + len(marker)
                depth = 1
                j = start
                while j < len(text_in) and depth > 0:
                    if text_in[j] == '[':
                        depth += 1
                    elif text_in[j] == ']':
                        depth -= 1
                    j += 1
                body = text_in[start:j - 1].strip()
                result.append(f'#callout-box([], [{body}])')
                i = j
            return ''.join(result)

        tech_part = _replace_tech_quote(tech_part)
        text = story_part + tech_part

    # 8. 표 정리: Pandoc이 생성하는 table.hline(), align: (auto,...) 제거
    #    + figure(align(center)[#table(...)]) → 그냥 #table(...)로 언래핑 (왼쪽 정렬)
    text = re.sub(r'\s*table\.hline\(\),?\n?', '\n', text)
    text = re.sub(r'\s*align:\s*\((?:auto,?\s*)+\),?\n', '\n', text)
    # figure + align(center) 래핑 제거: 표를 왼쪽 정렬로
    text = re.sub(
        r'#figure\(\s*align\(center\)\[#table\(',
        '#table(',
        text
    )
    text = re.sub(
        r'\)\]\s*,\s*kind:\s*table\s*\)',
        ')',
        text
    )

    # 9. 표 열 균등화: Pandoc이 생성한 퍼센트 기반 열(38.71%, 32.26%, ...)을 1fr로 변환
    #    짧은 열이 과도하게 넓고 긴 텍스트 열이 좁아지는 문제 해결
    def _equalize_table_columns(m):
        pct_list = m.group(1)
        col_count = len(re.findall(r'[\d.]+%', pct_list))
        if col_count >= 3:
            # 3열 이상: 마지막 열(보통 설명)을 넓게
            cols = ["1fr"] * (col_count - 1) + ["2fr"]
            return f'columns: ({", ".join(cols)})'
        elif col_count > 0:
            return f'columns: ({", ".join(["1fr"] * col_count)})'
        return m.group(0)

    text = re.sub(r'columns:\s*\(([\d.%,\s]+)\)', _equalize_table_columns, text)

    # 10. DUAL-IMAGE: 2열 이미지 그리드 변환
    #     %%DUAL_IMAGE_START%% 와 %%DUAL_IMAGE_END%% 사이의 auto-image 2개를 grid로 변환
    def _replace_dual_image(m):
        inner = m.group(1)
        images = re.findall(r'(#auto-image\([^)]+\))', inner)
        if len(images) == 2:
            return (
                '#grid(\n'
                '  columns: (1fr, 1fr),\n'
                '  column-gutter: 12pt,\n'
                f'  {images[0]},\n'
                f'  {images[1]},\n'
                ')'
            )
        return inner  # 2개가 아니면 그대로

    text = re.sub(
        r'%%DUAL_IMAGE_START%%\s*(.*?)\s*%%DUAL_IMAGE_END%%',
        _replace_dual_image, text, flags=re.DOTALL
    )
    # 남은 마커 제거
    text = text.replace('%%DUAL_IMAGE_START%%', '')
    text = text.replace('%%DUAL_IMAGE_END%%', '')

    return text


def merge_template_and_content(template_path: Path, content: str) -> str:
    """템플릿 + Pandoc 변환 내용을 하나의 .typ 파일로 합침

    template_path가 가리키는 디렉토리에 book_base.typ이 있으면
    프로젝트 설정(book.typ) + 범용 스타일(book_base.typ) + 본문 순서로 합침.
    없으면 기존처럼 단일 템플릿 + 본문.
    """
    template = template_path.read_text(encoding="utf-8")
    base_path = template_path.parent / "book_base.typ"
    if base_path.exists():
        base = base_path.read_text(encoding="utf-8")
        return template + "\n" + base + "\n" + content
    return template + "\n" + content


# ══════════════════════════════════════
# Typst 컴파일
# ══════════════════════════════════════

def typst_compile(typ_path: Path, pdf_path: Path,
                  font_path: Path | None = None) -> bool:
    """Typst로 PDF 컴파일"""
    cmd = [
        'typst', 'compile',
        str(typ_path),
        str(pdf_path),
        '--root', '/',
    ]
    if font_path:
        cmd.extend(['--font-path', str(font_path)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   [오류] Typst 컴파일 실패:\n{result.stderr}")
        return False

    print(f"   Typst 컴파일 완료: {pdf_path.name}")
    return True


# ══════════════════════════════════════
# 의존성 확인
# ══════════════════════════════════════

def check_dependencies() -> bool:
    """필수 도구 설치 확인"""
    missing = []
    for tool in ['typst', 'pandoc']:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print(f"[오류] 필수 도구 미설치: {', '.join(missing)}")
        print(f"  설치: brew install {' '.join(missing)}")
        return False

    for tool in ['typst', 'pandoc']:
        result = subprocess.run([tool, '--version'], capture_output=True, text=True)
        version = result.stdout.strip().split('\n')[0]
        print(f"   {tool}: {version}")

    return True


# ══════════════════════════════════════
# 메인 빌드 함수
# ══════════════════════════════════════

def build(config: dict):
    """PDF 빌드 실행.

    config 필수 키:
        title:       str       — 책 제목 (출력 메시지용)
        base:        Path      — 프로젝트 루트
        assets_dir:  Path      — 이미지 에셋 디렉토리
        template:    Path      — Typst 템플릿 (book.typ)
        font_path:   Path|None — 추가 폰트 디렉토리
        front:       list[Path]— 전문 마크다운 파일 목록
        chapters:    list[Path]— 챕터 마크다운 파일 목록
        back:        list[Path]— 후문 마크다운 파일 목록
        output_md:   Path      — 통합 마크다운 출력 경로
        output_typ:  Path      — 최종 Typst 출력 경로
        output_pdf:  Path      — PDF 출력 경로
    """
    title = config.get('title', 'Book')
    print(f"{title} 통합 PDF 생성 (Typst)")
    print("=" * 50)

    # 0. 의존성 확인
    if not check_dependencies():
        return

    # 1. 마크다운 통합 + 전처리 (이야기 파트 제목 제거 포함)
    print("\n[1/5] 마크다운 통합 + 전처리...")
    integrated_md = build_integrated_md(
        config['front'], config['chapters'], config['back']
    )
    output_md = config['output_md']
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(integrated_md, encoding="utf-8")
    print(f"\n   통합 마크다운: {output_md.name}")

    # 2. 이미지 공백 자동 제거
    print("\n[2/5] 이미지 공백 자동 제거...")
    assets_dir = config['assets_dir']
    autocrop_all_assets(assets_dir, assets_dir)

    # 3. Pandoc: MD → Typst (임시)
    print("\n[3/5] Pandoc 변환 (MD → Typst)...")
    output_typ = config['output_typ']
    temp_typ = output_typ.with_suffix('.raw.typ')
    if not md_to_typst(output_md, temp_typ):
        return

    # 4. 후처리 + 템플릿 병합
    print("\n[4/5] 후처리 + 템플릿 병합...")
    raw_content = temp_typ.read_text(encoding="utf-8")
    fixed_content = fix_typst_content(raw_content)
    final_typ = merge_template_and_content(config['template'], fixed_content)
    output_typ.write_text(final_typ, encoding="utf-8")
    temp_typ.unlink(missing_ok=True)
    print(f"   최종 Typst: {output_typ.name}")

    # 5. Typst 컴파일: TYP → PDF
    print("\n[5/5] Typst 컴파일 (TYP → PDF)...")
    output_pdf = config['output_pdf']
    if not typst_compile(output_typ, output_pdf, config.get('font_path')):
        return

    size_mb = output_pdf.stat().st_size / (1024 * 1024)
    print(f"\n   PDF 생성 완료: {output_pdf.name} ({size_mb:.1f} MB)")
    print(f"\n{'=' * 50}")
    print(f"완료: {output_pdf}")
    return output_pdf


def build_chapter(md_file: Path, config: dict) -> Path | None:
    """단일 챕터 마크다운 → PDF 빌드.
    config는 build()와 동일한 키를 가짐. output_dir 키가 있으면 해당 폴더에 저장."""
    base_output_dir = config.get('output_dir', md_file.parent.parent / 'book' / 'chapters')
    stem = md_file.stem
    # 챕터 번호 추출 (예: "01-환각과..." → "CH01")
    ch_num_match = re.match(r'^(\d{2})', stem)
    if ch_num_match:
        ch_folder = f"CH{ch_num_match.group(1)}"
        output_dir = base_output_dir / ch_folder
    else:
        output_dir = base_output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    ch_md = output_dir / f"{stem}.md"
    ch_typ = output_dir / f"{stem}.typ"
    ch_pdf = output_dir / f"{stem}.pdf"

    # 1. 전처리
    content = md_file.read_text(encoding="utf-8")
    content = clean_comments(content)
    content = fix_image_paths(content, md_file)
    content = remove_story_part_heading(content)
    content = fix_br_tags(content)
    ch_md.write_text(content, encoding="utf-8")

    # 2. 이미지 공백 제거
    assets_dir = config.get('assets_dir')
    if assets_dir and assets_dir.exists():
        autocrop_all_assets(assets_dir, assets_dir)

    # 3. Pandoc
    temp_typ = ch_typ.with_suffix('.raw.typ')
    if not md_to_typst(ch_md, temp_typ):
        return None

    # 4. 후처리 + 템플릿
    raw = temp_typ.read_text(encoding="utf-8")
    fixed = fix_typst_content(raw)
    final = merge_template_and_content(config['template'], fixed)
    ch_typ.write_text(final, encoding="utf-8")
    temp_typ.unlink(missing_ok=True)

    # 5. 컴파일
    if not typst_compile(ch_typ, ch_pdf, config.get('font_path')):
        return None

    size_mb = ch_pdf.stat().st_size / (1024 * 1024)
    print(f"   {stem}.pdf ({size_mb:.1f} MB)")

    # 6. 레이아웃 자동 검수 + 공백 해소 루프
    #    Round 1-2: 이미지 축소, Round 3: 이미지 위치 이동, Round 4: 최종
    try:
        checker_dir = str(Path(__file__).parent)
        if checker_dir not in sys.path:
            sys.path.insert(0, checker_dir)
        from pdf_layout_checker import analyze_layout, print_page_usage, print_report
        import fitz as _fitz

        for attempt in range(4):
            print(f"\n   레이아웃 검수 중...")
            print_page_usage(str(ch_pdf))
            issues = analyze_layout(str(ch_pdf))

            fixable = [i for i in issues if i["type"] in ("low_usage", "push_pattern", "orphan_content")]
            if not fixable:
                print_report(issues, str(ch_pdf))
                break

            typ_text = ch_typ.read_text(encoding="utf-8")
            _doc = _fitz.open(str(ch_pdf))
            _total_pages = len(_doc)
            _doc.close()

            if attempt < 2:
                # Round 1-2: 이미지 축소
                print(f"\n   이미지 축소 시도 {attempt + 1}/2...")
                changed = _shrink_images_for_issues(typ_text, fixable, total_pages=_total_pages)
            elif attempt == 2:
                # Round 3: 축소 실패 시 이미지 위치 이동
                print(f"\n   이미지 위치 이동 시도...")
                changed = _reorder_images_for_issues(typ_text, fixable, total_pages=_total_pages)
            else:
                # Round 4: 최종 보고
                print_report(issues, str(ch_pdf))
                break

            if changed == typ_text:
                if attempt < 2:
                    print("   축소 가능한 이미지 없음")
                else:
                    print("   이동 가능한 이미지 없음")
                print_report(issues, str(ch_pdf))
                break

            ch_typ.write_text(changed, encoding="utf-8")
            if not typst_compile(ch_typ, ch_pdf, config.get('font_path')):
                break
            size_mb = ch_pdf.stat().st_size / (1024 * 1024)
            print(f"   재빌드 완료 ({size_mb:.1f} MB)")

    except ImportError:
        print("   [layout-check 스킵] pdf_layout_checker.py import 실패")
    except Exception as e:
        print(f"   [layout-check 오류] {e}")

    return ch_pdf


def _shrink_images_for_issues(typ_text: str, issues: list, total_pages: int = 0) -> str:
    """이슈 페이지에 대응하는 이미지의 max-width를 축소.

    Typst 파일의 라인 위치 기반으로 이미지-페이지 매핑을 정밀하게 수행.
    이슈 페이지 근처 이미지를 찾아 max-width를 0.05씩 감소 (최소 0.25).
    """
    pattern = re.compile(r'(#auto-image\([^)]*max-width:\s*)([\d.]+)(\))')
    matches = list(pattern.finditer(typ_text))
    if not matches:
        return typ_text

    issue_pages = set()
    for issue in issues:
        p = issue.get("page", 0)
        if p > 2:
            issue_pages.add(p)
    if not issue_pages:
        return typ_text

    total_images = len(matches)
    total_lines = typ_text.count('\n') + 1

    # 각 이미지의 라인 번호 계산
    img_lines = []
    for m in matches:
        line_num = typ_text[:m.start()].count('\n') + 1
        img_lines.append(line_num)

    # 페이지당 평균 라인 수 추정 (표지 2페이지 제외)
    content_pages = max(1, (total_pages or total_images + 5) - 2)
    lines_per_page = total_lines / content_pages

    # 이슈 페이지 → 라인 범위 → 해당 범위의 이미지 인덱스 매핑
    target_indices = set()
    for p in sorted(issue_pages):
        page_start_line = int((p - 2.5) * lines_per_page)
        page_end_line = int((p - 0.5) * lines_per_page)

        # 해당 라인 범위에 있는 이미지 + 바로 앞 이미지
        for idx, line in enumerate(img_lines):
            if page_start_line <= line <= page_end_line:
                target_indices.add(idx)
                if idx > 0:
                    target_indices.add(idx - 1)

        # 범위에 이미지가 없으면 가장 가까운 이전 이미지
        if not any(page_start_line <= img_lines[i] <= page_end_line for i in range(total_images)):
            closest = max((i for i, l in enumerate(img_lines) if l < page_start_line), default=None)
            if closest is not None:
                target_indices.add(closest)

    # 대상 이미지의 max-width 축소 (0.05씩, 최소 0.25)
    result = typ_text
    offset = 0
    for idx, m in enumerate(matches):
        if idx not in target_indices:
            continue
        current_val = float(m.group(2))
        new_val = max(0.25, current_val - 0.05)
        if new_val >= current_val:
            continue
        start = m.start(2) + offset
        end = m.end(2) + offset
        new_str = f"{new_val:.2f}"
        result = result[:start] + new_str + result[end:]
        offset += len(new_str) - (end - start)
        print(f"   이미지 {idx + 1}/{total_images} (L{img_lines[idx]}): max-width {current_val:.2f} → {new_val:.2f}")

    return result


def _reorder_images_for_issues(typ_text: str, issues: list, total_pages: int = 0) -> str:
    """push_pattern/orphan_content 이슈 시 이미지를 1~2 문단 앞으로 이동.

    전략:
      - push_pattern: 다음 페이지로 밀린 이미지를 이전 문단 앞으로 이동
      - orphan_content: 이전 페이지 마지막 이미지를 현재 페이지로 이동
    제약: 이미지와 관련 텍스트 사이 거리 3문단 이내 유지.
    """
    pattern = re.compile(r'(#auto-image\([^)]+\))')
    matches = list(pattern.finditer(typ_text))
    if not matches:
        return typ_text

    issue_pages = set()
    for issue in issues:
        if issue.get("type") in ("push_pattern", "orphan_content"):
            p = issue.get("page", 0)
            if p > 2:
                issue_pages.add(p)
    if not issue_pages:
        return typ_text

    total_lines = typ_text.count('\n') + 1
    content_pages = max(1, (total_pages or len(matches) + 5) - 2)
    lines_per_page = total_lines / content_pages

    lines = typ_text.split('\n')
    moved = False

    for p in sorted(issue_pages):
        page_start_line = int((p - 2.5) * lines_per_page)
        page_end_line = int((p - 0.5) * lines_per_page)

        # 해당 페이지 범위에서 이미지 라인 찾기
        img_line_idx = None
        for m in matches:
            line_num = typ_text[:m.start()].count('\n')
            if page_start_line <= line_num <= page_end_line:
                img_line_idx = line_num
                break

        if img_line_idx is None:
            continue

        # 이미지를 1~2 문단(빈 줄) 앞으로 이동
        target_line = img_line_idx
        blank_count = 0
        for i in range(img_line_idx - 1, max(0, img_line_idx - 30), -1):
            if lines[i].strip() == '':
                blank_count += 1
                if blank_count == 2:
                    target_line = i + 1
                    break

        if target_line < img_line_idx and blank_count >= 2:
            # 이미지 라인을 제거하고 target_line에 삽입
            removed = lines.pop(img_line_idx)
            lines.insert(target_line, removed)
            moved = True
            print(f"   이미지 L{img_line_idx + 1} → L{target_line + 1}로 이동 (2문단 앞)")

    if not moved:
        return typ_text

    return '\n'.join(lines)
