# -*- coding: utf-8 -*-
"""chapters/*.md · book/*.md 수정 시 금지 패턴과 인라인 서식을 강제하는 PreToolUse 훅.

stdin: {"tool_input": {"file_path": ..., "new_string"|"content": ...}}
위반이 있으면 permissionDecision=deny JSON을 출력한다.
"""
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="")

try:
    payload = json.loads(sys.stdin.read() or "{}")
except ValueError:
    sys.exit(0)

ti = payload.get("tool_input") or {}
path = ti.get("file_path") or ""
if "/chapters/" not in path.replace("\\", "/") and "/book/" not in path.replace("\\", "/"):
    sys.exit(0)

text = ti.get("new_string") or ti.get("content") or ""
if not text.strip():
    sys.exit(0)

# 코드 펜스 안은 검사하지 않는다 (본문 서식 규칙은 산문에만 적용)
prose = re.sub(r"```.*?```", "", text, flags=re.S)

CHECKS = [
    # (정규식, 위반 메시지)
    (r"이것이야말로", "설교 패턴: '이것이야말로' 사용 금지 (style.md)"),
    (r"이것이 바로", "반복 강조: '이것이 바로...이유' 패턴 금지 (style.md)"),
    (r"[\U0001F300-\U0001FAFF☀-➿]", "이모지 사용 금지 (style.md)"),
    (r"^## (이야기 파트|기술 파트)", "라벨형 H2 금지: 자연스러운 제목 사용 (style.md)"),
    (r"^---$", "수평선(---) 사용 금지: 파트 전환은 문장으로 (style.md)"),
    (r"비로소|드디어|마침내|진정한", "AI 선호어: '비로소/드디어/마침내/진정한' 지양 (writing-chapters.md)"),
    # 인라인 서식 (code.md "인라인 서식")
    (r"`[A-Z][A-Za-z0-9]*[a-z][A-Za-z0-9]*`",
     "클래스는 볼드: `User` -> **User** (code.md)"),
    (r"`@[A-Za-z][A-Za-z0-9]*`",
     "어노테이션은 볼드: `@ManyToOne` -> **@ManyToOne** (code.md)"),
    (r"`[a-z][a-z_]*_tb`",
     "테이블은 볼드: `board_tb` -> **board_tb** (code.md)"),
    (r"`(?:null|true|false)`",
     "값은 평문: null·true·false에 백틱 금지 (code.md)"),
    (r"\*\*[^*\n]*(?:/|\.java|\.sql|\.gradle)[^*\n]*\*\*",
     "파일은 백틱: **board/Board.java** -> `board/Board.java` (code.md)"),
    (r"^#{1,4} .*\*\*",
     "제목에 볼드 금지: 제목 자체가 강조다 (code.md)"),
]

violations = []
for pattern, message in CHECKS:
    if re.search(pattern, prose, flags=re.M):
        violations.append(message)

if violations:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "스타일 위반: " + " / ".join(violations),
        }
    }, ensure_ascii=False))
