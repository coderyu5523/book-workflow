"""디자인 컴포넌트 어셈블러 — 유저 선택에 따라 book_base 내용을 조립

사용법:
  from design_assembler import parse_design_arg, assemble_book_base
  selection = parse_design_arg("1")           # 프리셋 1
  selection = parse_design_arg("body=2,heading=1")  # 믹스매치
  result = assemble_book_base(selection)       # 조립된 Typst 문자열
"""

import json
from pathlib import Path

COMPONENTS_DIR = (
    Path(__file__).resolve().parents[3]
    / "pub-typst-design"
    / "references"
    / "templates"
    / "components"
)

# 결합 순서 (Typst 스코프 순서 중요)
ASSEMBLY_ORDER = [
    ("_shared", "00-variables.typ"),
    ("_shared", "01-page.typ"),
    ("_variant", "body_{sel}.typ"),
    ("_variant", "heading_{sel}.typ"),
    ("_variant", "code_{sel}.typ"),
    ("_variant", "inline_code_{sel}.typ"),
    ("_variant", "quote_{sel}.typ"),
    ("_variant", "table_{sel}.typ"),
    ("_shared", "80-misc.typ"),
    ("_shared", "85-image.typ"),
    ("_shared", "90-cover.typ"),
    ("_variant", "toc_{sel}.typ"),
]

VARIANT_KEYS = ["body", "heading", "code", "inline_code", "quote", "table", "toc"]


def load_preset(preset_id: str) -> dict[str, str]:
    """프리셋 ID로 컴포넌트 선택 딕셔너리를 로드"""
    presets_path = COMPONENTS_DIR / "presets.json"
    with open(presets_path, encoding="utf-8") as f:
        presets = json.load(f)
    if preset_id not in presets:
        available = ", ".join(presets.keys())
        raise ValueError(f"프리셋 '{preset_id}' 없음. 사용 가능: {available}")
    return dict(presets[preset_id]["components"])


def parse_design_arg(arg: str) -> dict[str, str]:
    """디자인 인자를 파싱하여 컴포넌트 선택 딕셔너리로 변환

    '1' 또는 '2'       → 프리셋 로드
    'body=2,heading=1'  → 기본 프리셋 1 + 오버라이드
    """
    arg = arg.strip()
    if arg in ("1", "2"):
        return load_preset(arg)

    # 믹스매치: 기본값은 프리셋 1, 지정된 키만 오버라이드
    selection = load_preset("1")
    parts = [p.strip() for p in arg.split(",")]
    for part in parts:
        if "=" not in part:
            raise ValueError(f"잘못된 형식: '{part}'. 'key=value' 형태 필요")
        key, val = part.split("=", 1)
        key = key.strip()
        val = val.strip()
        if key not in VARIANT_KEYS:
            available = ", ".join(VARIANT_KEYS)
            raise ValueError(f"알 수 없는 컴포넌트: '{key}'. 사용 가능: {available}")
        selection[key] = f"d{val}" if not val.startswith("d") else val
    return selection


def assemble_book_base(selection: dict[str, str]) -> str:
    """선택된 컴포넌트를 결합하여 완성된 book_base Typst 문자열 반환"""
    parts = []
    for subdir, pattern in ASSEMBLY_ORDER:
        if "{sel}" in pattern:
            # body_{sel}.typ → body, inline_code_{sel}.typ → inline_code
            key = pattern.split("_{sel}")[0]
            filename = pattern.replace("{sel}", selection[key])
        else:
            filename = pattern
        filepath = COMPONENTS_DIR / subdir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"컴포넌트 파일 없음: {filepath}")
        parts.append(filepath.read_text(encoding="utf-8"))
    return "\n".join(parts)


if __name__ == "__main__":
    import sys

    arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    sel = parse_design_arg(arg)
    print(f"선택: {sel}")
    result = assemble_book_base(sel)
    print(f"결합 완료: {len(result)} chars, {result.count(chr(10))} lines")
