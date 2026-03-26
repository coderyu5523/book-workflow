#!/usr/bin/env python3
"""집필에이전트 v2 — PDF 디자인 프리뷰 서버

실행:
    python3 preview.py                    # 프로젝트 자동 감지
    python3 preview.py 사내AI비서_v2       # 프로젝트 지정
    python3 preview.py --port 8080        # 포트 지정
"""

import argparse
import http.server
import json
import mimetypes
import os
import re
import shutil
import socket
import sys
import time
import urllib.parse
import webbrowser
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
PROJECTS_DIR = ROOT / "projects"
HTML_FILE = ROOT / "preview_editor.html"
DEFAULT_PORT = 3333

# ══════════════════════════════════════
# 프로젝트 감지
# ══════════════════════════════════════

def find_projects():
    if not PROJECTS_DIR.exists():
        return []
    dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return [{"name": d.name, "path": str(d)} for d in dirs]


def select_project(name=None):
    projects = find_projects()
    if not projects:
        print("projects/ 폴더에 프로젝트가 없습니다.")
        sys.exit(1)

    if name:
        for p in projects:
            if p["name"] == name:
                return Path(p["path"])
        print(f"프로젝트 '{name}'을 찾을 수 없습니다.")
        print(f"사용 가능: {', '.join(p['name'] for p in projects)}")
        sys.exit(1)

    if len(projects) == 1:
        print(f"프로젝트: {projects[0]['name']}")
        return Path(projects[0]["path"])

    print("\n프로젝트를 선택하세요:\n")
    for i, p in enumerate(projects, 1):
        print(f"  {i}. {p['name']}")
    print()

    while True:
        try:
            choice = int(input("번호: ").strip())
            if 1 <= choice <= len(projects):
                return Path(projects[choice - 1]["path"])
        except (ValueError, EOFError):
            pass
        print(f"1~{len(projects)} 사이 번호를 입력하세요.")


def scan_project(project_path):
    result = {
        "name": project_path.name,
        "path": str(project_path),
        "chapters": [],
        "front": [],
        "back": [],
        "assets": {},
    }

    # chapters
    chapters_dir = project_path / "chapters"
    if chapters_dir.exists():
        for f in sorted(chapters_dir.glob("*.md")):
            result["chapters"].append({
                "name": f.name,
                "path": f"chapters/{f.name}",
                "size": f.stat().st_size,
            })

    # front
    front_dir = project_path / "book" / "front"
    if front_dir.exists():
        for f in sorted(front_dir.glob("*.md")):
            result["front"].append({"name": f.name, "path": f"book/front/{f.name}"})

    # back
    back_dir = project_path / "book" / "back"
    if back_dir.exists():
        for f in sorted(back_dir.glob("*.md")):
            result["back"].append({"name": f.name, "path": f"book/back/{f.name}"})

    # assets
    assets_dir = project_path / "assets"
    if assets_dir.exists():
        for ch_dir in sorted(assets_dir.iterdir()):
            if not ch_dir.is_dir() or ch_dir.name.startswith("."):
                continue
            ch_assets = {}
            for sub in sorted(ch_dir.iterdir()):
                if sub.is_dir():
                    images = [f.name for f in sorted(sub.iterdir())
                              if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")]
                    if images:
                        ch_assets[sub.name] = images
                elif sub.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
                    ch_assets.setdefault("_root", []).append(sub.name)
            if ch_assets:
                result["assets"][ch_dir.name] = ch_assets

    # progress.json
    progress_file = project_path / "progress.json"
    if progress_file.exists():
        try:
            result["progress"] = json.loads(progress_file.read_text(encoding="utf-8"))
        except Exception:
            result["progress"] = {}

    return result


# ══════════════════════════════════════
# MD 블록 파서
# ══════════════════════════════════════

def parse_md_to_blocks(text):
    lines = text.split("\n")
    blocks = []
    i = 0
    counter = 0

    def make_block(btype, content, meta, start, end):
        nonlocal counter
        counter += 1
        return {
            "id": f"blk_{counter:03d}",
            "type": btype,
            "content": content,
            "meta": meta,
            "start_line": start + 1,
            "end_line": end + 1,
        }

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # empty line — skip
        if not stripped:
            i += 1
            continue

        # HTML comment (multi-line)
        if stripped.startswith("<!--"):
            start = i
            comment_lines = [line]
            if "-->" not in stripped[4:]:
                i += 1
                while i < len(lines) and "-->" not in lines[i]:
                    comment_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    comment_lines.append(lines[i])
            content = "\n".join(comment_lines)
            meta = {}
            if "GEMINI PROMPT" in content:
                meta["prompt_type"] = "GEMINI PROMPT"
            elif "CAPTURE NEEDED" in content:
                meta["prompt_type"] = "CAPTURE NEEDED"
            blocks.append(make_block("comment", content, meta, start, i))
            i += 1
            continue

        # code block
        if stripped.startswith("```"):
            start = i
            lang = stripped[3:].strip()
            code_lines = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                code_lines.append(lines[i])
            blocks.append(make_block("code", "\n".join(code_lines), {"lang": lang}, start, i))
            i += 1
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.+)", line)
        if m:
            blocks.append(make_block("heading", line, {"level": len(m.group(1))}, i, i))
            i += 1
            continue

        # hr
        if re.match(r"^---+\s*$", stripped):
            blocks.append(make_block("hr", line, {}, i, i))
            i += 1
            continue

        # image (standalone line)
        img_m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if img_m:
            blocks.append(make_block("image", line, {
                "alt": img_m.group(1),
                "src": img_m.group(2),
            }, i, i))
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            start = i
            quote_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i])
                i += 1
            blocks.append(make_block("quote", "\n".join(quote_lines), {}, start, i - 1))
            continue

        # table
        if stripped.startswith("|"):
            start = i
            table_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append(make_block("table", "\n".join(table_lines), {}, start, i - 1))
            continue

        # paragraph (consecutive non-empty lines)
        start = i
        para_lines = [line]
        i += 1
        while i < len(lines):
            nl = lines[i]
            ns = nl.strip()
            if (not ns or ns.startswith("#") or ns.startswith("```") or
                ns.startswith("---") or ns.startswith(">") or ns.startswith("|") or
                ns.startswith("<!--") or re.match(r"^!\[", ns)):
                break
            para_lines.append(nl)
            i += 1
        blocks.append(make_block("paragraph", "\n".join(para_lines), {}, start, i - 1))

    return blocks


def blocks_to_md(blocks):
    parts = []
    for i, block in enumerate(blocks):
        if i > 0:
            prev = blocks[i - 1]
            # comment → image: no blank line (preserve GEMINI PROMPT pattern)
            if prev["type"] == "comment" and block["type"] == "image":
                parts.append("\n")
            else:
                parts.append("\n\n")
        parts.append(block["content"])
    return "".join(parts) + "\n"


def rewrite_image_paths(md_text, chapter_rel_path):
    chapter_dir = Path(chapter_rel_path).parent
    def replace(m):
        alt, rel = m.group(1), m.group(2)
        if rel.startswith("http://") or rel.startswith("https://") or rel.startswith("/"):
            return m.group(0)
        resolved = (chapter_dir / rel).as_posix()
        parts = []
        for p in resolved.split("/"):
            if p == ".." and parts:
                parts.pop()
            elif p != ".":
                parts.append(p)
        return f'![{alt}](/{"/".join(parts)})'
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace, md_text)


def add_preview_src(blocks, chapter_rel_path):
    chapter_dir = Path(chapter_rel_path).parent
    for block in blocks:
        if block["type"] == "image" and "src" in block["meta"]:
            src = block["meta"]["src"]
            if not (src.startswith("http") or src.startswith("/")):
                resolved = (chapter_dir / src).as_posix()
                parts = []
                for p in resolved.split("/"):
                    if p == ".." and parts:
                        parts.pop()
                    elif p != ".":
                        parts.append(p)
                block["meta"]["preview_src"] = "/" + "/".join(parts)
    return blocks


# ══════════════════════════════════════
# 파일 I/O
# ══════════════════════════════════════

def backup_file(file_path):
    today = datetime.now().strftime("%Y-%m-%d")
    backup_path = file_path.with_suffix(f".md.{today}.bak")
    if not backup_path.exists():
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    return None


# ══════════════════════════════════════
# Typst 빌드 헬퍼
# ══════════════════════════════════════

_typst_builder = None

def _get_typst_builder():
    """typst_builder 모듈을 lazy import (스킬 스크립트 경로 추가)"""
    global _typst_builder
    if _typst_builder is None:
        skill_scripts = ROOT / ".claude" / "skills" / "pub-build" / "references" / "scripts"
        if str(skill_scripts) not in sys.path:
            sys.path.insert(0, str(skill_scripts))
        import typst_builder
        _typst_builder = typst_builder
    return _typst_builder


def _make_build_config(project_path, design_state=None):
    """프로젝트 경로에서 빌드 CONFIG 생성 (build_pdf_typst.py의 CONFIG와 동일 구조)"""
    build_script = project_path / "book" / "build_pdf_typst.py"
    if not build_script.exists():
        raise FileNotFoundError("build_pdf_typst.py not found")

    # build_pdf_typst.py를 import하여 CONFIG 가져오기
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_pdf_typst", build_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    config = dict(mod.CONFIG)

    # design_state 주입
    if design_state:
        config["design_state"] = design_state
        components = design_state.get("components", {})
        if components:
            config["design"] = ",".join(f"{k}={v}" for k, v in components.items())

    return config


# ══════════════════════════════════════
# SVG 프리뷰 캐시
# ══════════════════════════════════════

import hashlib

_cache = {
    "file_hash": None,      # 선택 파일 경로 + mtime 해시
    "raw_typ": None,         # Stage 1 결과 (raw .typ 문자열)
    "design_hash": None,     # design_state JSON 해시
    "svg_dir": None,         # SVG 출력 디렉토리
    "page_count": 0,
    "typ_path": None,        # 최종 .typ 파일 경로
}


def _compute_file_hash(project_path, files_dict):
    """선택된 파일 경로 + mtime → 해시"""
    parts = []
    for section in ("front", "chapters", "back"):
        for rel in sorted(files_dict.get(section, [])):
            fp = project_path / rel
            if fp.exists():
                parts.append(f"{rel}:{fp.stat().st_mtime}")
    return hashlib.md5("|".join(parts).encode()).hexdigest()


def _compute_design_hash(design_state):
    """design_state dict → 해시"""
    raw = json.dumps(design_state or {}, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(raw.encode()).hexdigest()


def _resolve_file_lists(project_path, files_dict):
    """파일 상대경로 dict → Path 리스트 (front, chapters, back)"""
    front = [project_path / f for f in files_dict.get("front", []) if (project_path / f).exists()]
    chapters = [project_path / f for f in files_dict.get("chapters", []) if (project_path / f).exists()]
    back = [project_path / f for f in files_dict.get("back", []) if (project_path / f).exists()]
    return front, chapters, back


# ══════════════════════════════════════
# HTTP 핸들러
# ══════════════════════════════════════

def make_handler(project_path):
    project_info = scan_project(project_path)

    class PreviewHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # quiet logging
            pass

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            path = urllib.parse.unquote(parsed.path)
            query = dict(urllib.parse.parse_qsl(parsed.query))

            if path == "/":
                self.serve_file(HTML_FILE, "text/html; charset=utf-8")
            elif path == "/api/project":
                self.serve_json(project_info)
            elif path == "/api/files":
                self.serve_json({
                    "chapters": project_info["chapters"],
                    "front": project_info["front"],
                    "back": project_info["back"],
                })
            elif path == "/api/blocks":
                rel_path = query.get("path", "")
                file_path = project_path / rel_path
                if not file_path.exists() or not file_path.suffix == ".md":
                    self.serve_json({"error": "File not found"}, 404)
                    return
                text = file_path.read_text(encoding="utf-8")
                blocks = parse_md_to_blocks(text)
                blocks = add_preview_src(blocks, rel_path)
                mtime = file_path.stat().st_mtime
                self.serve_json({"path": rel_path, "blocks": blocks, "last_modified": mtime})
            elif path == "/api/file-content":
                rel_path = query.get("path", "")
                file_path = project_path / rel_path
                if not file_path.exists() or not file_path.suffix == ".md":
                    self.serve_json({"error": "File not found"}, 404)
                    return
                text = file_path.read_text(encoding="utf-8")
                mtime = file_path.stat().st_mtime
                self.serve_json({"path": rel_path, "content": text, "last_modified": mtime})
            elif path.startswith("/api/svg/"):
                # SVG 페이지 서빙: /api/svg/3 → page_3.svg
                page_num = path.split("/")[-1].split("?")[0]
                if _cache["svg_dir"]:
                    svg_file = Path(_cache["svg_dir"]) / f"page_{page_num}.svg"
                    if svg_file.exists():
                        self.serve_file(svg_file, "image/svg+xml")
                        return
                self.send_error(404, "SVG page not found")
            elif path == "/api/svg-meta":
                self.serve_json({
                    "page_count": _cache["page_count"],
                    "has_cache": _cache["raw_typ"] is not None,
                })
            elif path.startswith("/assets/") or path.startswith("/chapters/") or path.startswith("/book/"):
                file_path = project_path / path.lstrip("/")
                if file_path.exists() and file_path.is_file():
                    ctype, _ = mimetypes.guess_type(str(file_path))
                    self.serve_file(file_path, ctype or "application/octet-stream")
                else:
                    self.send_error(404)
            else:
                self.send_error(404)

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            path = urllib.parse.unquote(parsed.path)

            body = self.read_body()
            if body is None:
                return

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.serve_json({"error": "Invalid JSON"}, 400)
                return

            if path == "/api/save":
                rel_path = data.get("path", "")
                blocks = data.get("blocks", [])
                client_mtime = data.get("last_modified", 0)

                file_path = project_path / rel_path
                if not file_path.exists():
                    self.serve_json({"error": "File not found"}, 404)
                    return

                # conflict check
                current_mtime = file_path.stat().st_mtime
                if client_mtime and abs(current_mtime - client_mtime) > 1:
                    self.serve_json({"error": "File modified externally", "server_mtime": current_mtime}, 409)
                    return

                backup = backup_file(file_path)
                md_text = blocks_to_md(blocks)
                file_path.write_text(md_text, encoding="utf-8")
                new_mtime = file_path.stat().st_mtime
                self.serve_json({"ok": True, "backup": backup, "last_modified": new_mtime})

            elif path == "/api/save-raw":
                rel_path = data.get("path", "")
                content = data.get("content", "")

                file_path = project_path / rel_path
                if not file_path.exists():
                    self.serve_json({"error": "File not found"}, 404)
                    return

                backup = backup_file(file_path)
                file_path.write_text(content, encoding="utf-8")
                new_mtime = file_path.stat().st_mtime
                self.serve_json({"ok": True, "backup": backup, "last_modified": new_mtime})

            elif path == "/api/build-svg":
                files_dict = data.get("files", {})
                design_state = data.get("design_state")
                force_stage1 = data.get("force_stage1", False)

                if not any(files_dict.get(s) for s in ("front", "chapters", "back")):
                    self.serve_json({"error": "No files selected"}, 400)
                    return

                start = time.time()
                stage_run = 0
                try:
                    tb = _get_typst_builder()
                    config = _make_build_config(project_path, design_state)

                    # Stage 1: 파일 해시 비교 → 캐시 미스 시 실행
                    file_hash = _compute_file_hash(project_path, files_dict)
                    if file_hash != _cache["file_hash"] or force_stage1 or _cache["raw_typ"] is None:
                        front, chapters, back = _resolve_file_lists(project_path, files_dict)
                        _cache["raw_typ"] = tb.build_raw_typ(
                            front, chapters, back,
                            config['mermaid_out'], config['assets_dir'],
                            config['output_md'],
                            image_border_preset=config.get('image_border_preset', 'plain'),
                            use_image_variables=True
                        )
                        _cache["file_hash"] = file_hash
                        _cache["design_hash"] = None  # Stage 1 변경 → Stage 2 강제 재실행
                        stage_run = 1

                    # Stage 2: 디자인 해시 비교 → 캐시 미스 시 실행
                    design_hash = _compute_design_hash(design_state)
                    if design_hash != _cache["design_hash"] or stage_run == 1:
                        design_arg = None
                        if design_state:
                            components = design_state.get("components", {})
                            if components:
                                design_arg = ",".join(f"{k}={v}" for k, v in components.items())

                        final_typ = tb.merge_template_and_content(
                            config['template'], _cache["raw_typ"],
                            design=design_arg, design_state=design_state,
                            skip_cover=not data.get("include_cover", True),
                            skip_toc=not data.get("include_toc", True)
                        )

                        # SVG 출력 디렉토리
                        svg_dir = project_path / "book" / "_preview_svg"
                        typ_path = project_path / "book" / "_preview.typ"
                        typ_path.write_text(final_typ, encoding="utf-8")

                        page_count = tb.typst_compile_svg(
                            typ_path, svg_dir, config.get('font_path')
                        )

                        _cache["design_hash"] = design_hash
                        _cache["svg_dir"] = str(svg_dir)
                        _cache["page_count"] = page_count
                        _cache["typ_path"] = str(typ_path)
                        stage_run = max(stage_run, 2)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self.serve_json({"ok": False, "error": str(e)[-2000:]})
                    return

                duration = round(time.time() - start, 2)
                self.serve_json({
                    "ok": True,
                    "page_count": _cache["page_count"],
                    "svg_base": "/api/svg/",
                    "duration": duration,
                    "stage": stage_run if stage_run else "cached",
                })

            elif path == "/api/export-pdf":
                design_state = data.get("design_state")
                start = time.time()
                try:
                    if _cache["typ_path"] and Path(_cache["typ_path"]).exists():
                        tb = _get_typst_builder()
                        config = _make_build_config(project_path, design_state)
                        pdf_path = config['output_pdf']
                        typ_path = Path(_cache["typ_path"])
                        if not tb.typst_compile(typ_path, pdf_path, config.get('font_path')):
                            self.serve_json({"ok": False, "error": "Typst PDF 컴파일 실패"})
                            return
                    else:
                        self.serve_json({"ok": False, "error": "프리뷰를 먼저 빌드하세요"})
                        return
                except Exception as e:
                    self.serve_json({"ok": False, "error": str(e)[-2000:]})
                    return

                duration = round(time.time() - start, 1)
                rel_pdf = str(pdf_path.relative_to(project_path))
                self.serve_json({"ok": True, "pdf": "/" + rel_pdf, "duration": duration})

            elif path == "/api/combine-md":
                files_dict = data.get("files", {})
                if not any(files_dict.get(s) for s in ("front", "chapters", "back")):
                    self.serve_json({"error": "No files selected"}, 400)
                    return

                try:
                    tb = _get_typst_builder()
                    config = _make_build_config(project_path)
                    front, chapters, back = _resolve_file_lists(project_path, files_dict)
                    integrated = tb.build_integrated_md(front, chapters, back, config['mermaid_out'])
                    output_md = project_path / "book" / f"{project_path.name}_통합본.md"
                    output_md.parent.mkdir(parents=True, exist_ok=True)
                    output_md.write_text(integrated, encoding="utf-8")
                    self.serve_json({
                        "ok": True,
                        "path": str(output_md.relative_to(project_path)),
                        "size": len(integrated),
                    })
                except Exception as e:
                    self.serve_json({"ok": False, "error": str(e)[-2000:]})

            elif path == "/api/build-pdf":
                design_state = data.get("design_state")
                start = time.time()
                try:
                    build_config = _make_build_config(project_path, design_state)
                    _get_typst_builder().build(build_config)
                except Exception as e:
                    self.serve_json({"ok": False, "error": str(e)[-2000:], "log": ""})
                    return

                duration = round(time.time() - start, 1)
                book_dir = project_path / "book"
                pdf_path = None
                if book_dir.exists():
                    pdfs = sorted(book_dir.rglob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
                    if pdfs:
                        pdf_path = pdfs[0]

                if pdf_path and pdf_path.stat().st_mtime >= start:
                    rel_pdf = str(pdf_path.relative_to(project_path))
                    self.serve_json({"ok": True, "pdf": "/" + rel_pdf, "duration": duration, "log": ""})
                else:
                    self.serve_json({"ok": False, "error": "PDF not generated", "log": ""})
            else:
                self.send_error(404)

        def serve_file(self, file_path, content_type):
            try:
                data = file_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", len(data))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_error(500)

        def serve_json(self, data, status=200):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        def read_body(self):
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                self.serve_json({"error": "Empty body"}, 400)
                return None
            return self.rfile.read(length)

    return PreviewHandler


# ══════════════════════════════════════
# 서버 실행
# ══════════════════════════════════════

def find_free_port(start=DEFAULT_PORT, tries=10):
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"포트 {start}~{start + tries - 1} 모두 사용 중")


def run_server(project_path, port):
    handler = make_handler(project_path)
    with http.server.HTTPServer(("", port), handler) as server:
        url = f"http://localhost:{port}"
        print(f"\n  프로젝트: {project_path.name}")
        print(f"  서버:     {url}")
        print(f"  종료:     Ctrl+C\n")
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n서버 종료.")


def main():
    parser = argparse.ArgumentParser(description="PDF 디자인 프리뷰 서버")
    parser.add_argument("project", nargs="?", help="프로젝트 이름 (생략 시 선택)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"포트 (기본: {DEFAULT_PORT})")
    args = parser.parse_args()

    if not HTML_FILE.exists():
        print(f"오류: {HTML_FILE} 파일이 없습니다.")
        sys.exit(1)

    project_path = select_project(args.project)
    port = find_free_port(args.port)
    run_server(project_path, port)


if __name__ == "__main__":
    main()
