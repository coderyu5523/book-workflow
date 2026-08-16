#!/bin/bash
# chapters/*.md 또는 book/*.md 수정 시 금지 패턴과 인라인 서식을 강제 차단하는 PreToolUse 훅
# 실제 검사는 check_chapter_style.py 가 수행한다 (jq 의존 제거)

exec python "$(dirname "$0")/check_chapter_style.py"
