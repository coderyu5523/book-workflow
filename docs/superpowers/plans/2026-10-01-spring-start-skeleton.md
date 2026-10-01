# 스프링책 start 예제 골격 재작성 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 스프링책 `code/start`를 "클래스 골격·의존성·메서드 틀은 남기고 본문만 비운" 형태로 다시 만든다. 이 과정에서 할 일이 없어지는 챕터 실습 4개를 [참고]로 바꾸고, 뒤 실습 번호를 당긴다.

**Architecture:** 기준 코드는 `code/final/chNN`(완성본)이다. start는 final에서 실습 코드블록이 쓰는 부분만 비운다. 새로 만드는 클래스는 틀을 남기고, 이전 챕터 코드를 고치는 실습은 이전 챕터 완성 코드를 그대로 두고 TODO로 바꿀 곳만 표시한다. 챕터 마크다운은 코드블록 헤더 번호와 CH05 파일 트리 표시 한 곳만 고친다. 검증은 scratchpad의 점검 스크립트, start 사본 컴파일, 스프링 컨텍스트 로딩 테스트로 한다.

**Tech Stack:** Java 21, Spring Boot 4 (Gradle wrapper, `--offline`), Lombok, Python 3 (점검 스크립트), Git Bash

**Spec:** 이 문서의 "승인된 규칙" 절. 2026-10-01 대화에서 사용자가 제안 규칙 1~6과 "[참고]로 바꾸고 번호 당김"을 승인했다.

## 승인된 규칙

1. import, 클래스 어노테이션, 주입 필드는 남긴다. 주입 필드가 `final`이므로 `@RequiredArgsConstructor`도 남긴다.
2. 새 메서드는 어노테이션과 시그니처를 남기고 본문만 비운다. 본문에는 TODO 한 줄을 두고, 반환형이 있으면 `return null;`을 둔다.
3. 리포지토리 인터페이스는 `extends JpaRepository<...>`까지 남긴다. 추가 조회 메서드는 선언 자체가 정답이므로 TODO 한 줄만 둔다.
4. DTO record는 선언부(필드)를 남긴다. `toEntity()`는 2번처럼 틀을 두고, 엔티티를 받는 생성자는 TODO 한 줄만 둔다. record 보조 생성자는 첫 줄에 `this(...)`가 와야 해서 빈 본문으로는 컴파일되지 않는다.
5. 이전 챕터 코드를 고치는 실습은 이전 챕터 코드를 두고, 바꿀 곳 위에 TODO 한 줄을 둔다.
6. 단계 주석(`// 1.`)은 넣지 않는다. TODO에는 할 일만 적고, 예외 클래스나 호출 순서는 나열하지 않는다.
7. 예외를 두지 않는다. 실습이 설명하는 어노테이션(`@GetMapping`, `@Transactional`, `@Test`, `@RestControllerAdvice` 등)도 규칙 1·2에 따라 틀에 남긴다.
8. CH02 [실습 1]·[실습 6], CH04 [실습 6], CH05 [실습 4]는 [참고]로 바꾸고 뒤 번호를 당긴다. CH05 파일 트리의 `ReplyRepository.java` 표시는 [작성]에서 [참고]로 바꾼다.

## Global Constraints

- TODO 형식: `// TODO : 실습 N - 설명` (콜론 앞뒤 공백, 하이픈 앞뒤 공백). N은 번호를 당긴 뒤의 새 번호
- 코드 파일은 이 문서에 적힌 내용 그대로 쓴다. 들여쓰기는 공백 4칸, 파일 끝은 줄바꿈 하나
- `code/final/**`은 건드리지 않는다
- 챕터는 각 챕터의 최신 버전 파일만 그 자리에서 고친다. 새 `-vN` 파일을 만들지 않는다
- 챕터에서 고치는 것은 Task에 적힌 코드블록 헤더 줄과 CH05 파일 트리 한 줄뿐이다. 리드인 문장·본문·코드블록 내용은 고치지 않는다(리드인 문구는 사용자 승인 대기)
- 커밋하지 않는다(사용자가 요청할 때만)
- HTML 빌드는 `PYTHONUTF8=1`을 먼저 설정하고 `--open` 없이 실행한다. 브라우저를 열지 않는다

## Review Focus

1. 첫 실행 시점의 부팅: 주입 필드를 남겼는데 주입 대상이 빈이 아니면 앱이 뜨지 않는다. CH05는 실습 3 직후 앱을 실행하므로 `ReplyRepository`가 처음부터 `JpaRepository`를 상속해야 한다. `verify_build.sh`의 컨텍스트 로딩 테스트가 잡는다
2. 틀이 참조하는 타입: `UserService` 틀이 `UserRequest.LoginDTO`를, `ReplyService` 틀이 `ReplyRequest.SaveDTO`를 쓴다. 이 record가 start에 없으면 컴파일되지 않는다. `verify_build.sh`가 잡는다
3. 번호 정합: 번호를 당긴 뒤 챕터 [실습 N]과 start의 `TODO : 실습 N`이 같은 파일을 가리켜야 한다. `verify_start.py`의 (a)(c)(d)가 잡는다
4. 틀 시그니처 변형: 매개변수 어노테이션(`@PathVariable("boardId")` 등)이나 타입이 final과 달라지면 독자가 챕터 코드를 붙여 넣을 때 어긋난다. `verify_start.py`의 (e)가 final 골격 줄과 비교한다
5. 정답 유출: 틀 파일 본문에 final 코드가 남거나, 고치는 실습 파일이 이미 고쳐진 상태면 실습할 것이 없다. `verify_start.py`의 (e) 본문 검사와 (f) 금지 패턴이 잡는다

---

## File Structure

경로 기준: `projects/특이점이-온-개발자-Springboot/` (이하 `BOOK/`)

- `BOOK/code/start/ch01/src/main/java/com/reflection/` : ex01/App, ex01/BoardController, ex02/App, ex02/BoardController, ex02/RequestMapping, ex03/App, ex03/BoardController, ex03/Controller 수정 (ex03/RequestMapping은 그대로)
- `BOOK/code/start/ch02/src/main/java/com/metacoding/spring/board/` : BoardRepository, BoardService, BoardController 수정
- `BOOK/code/start/ch02/src/test/java/com/metacoding/spring/board/BoardRepositoryTest.java` 수정
- `BOOK/code/start/ch03/src/main/java/com/metacoding/spring/` : board/BoardRequest, board/BoardResponse, board/BoardRepository, board/BoardService, core/handler/GlobalExceptionHandler 수정 (board/BoardController는 그대로)
- `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/` : user/UserRepository, user/UserRequest, user/UserResponse, user/UserService, user/UserController, board/BoardRepository, board/BoardRequest, board/BoardResponse, board/BoardService, board/BoardController 수정
- `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/` : reply/ReplyRepository, reply/ReplyRequest, reply/ReplyResponse, reply/ReplyService, reply/ReplyController, board/BoardRepository, board/BoardResponse, board/BoardService 수정
- `BOOK/chapters/02-게시판CRUD-v6.md`, `04-인증과인가-v8.md`, `05-댓글과JPA심화-v7.md` : 코드블록 헤더(와 CH05 파일 트리 한 줄) 수정
- 검증 도구(프로젝트 밖): `C:/Users/BJ/AppData/Local/Temp/claude/C--work-----book-workflow/baf42c0f-4d8a-4236-889d-65f9ae26ef7f/scratchpad/verify/` 아래 `verify_start.py`, `verify_build.sh` (이하 `VERIFY/`)

---

### Task 1: 검증 도구 작성과 현재 상태 실패 확인

**Files:**
- Create: `VERIFY/verify_start.py`
- Create: `VERIFY/verify_build.sh`

**Interfaces:**
- Produces: `python VERIFY/verify_start.py [챕터번호 ...]` (생략 시 1~5) → 문제 없으면 `PASS chN` 출력 후 종료코드 0, 문제 있으면 `FAIL chN` + 항목 출력 후 종료코드 1
- Produces: `bash VERIFY/verify_build.sh [ch01 ch02 ...]` (생략 시 전부) → start를 `VERIFY/work`에 복사해 ch01은 javac, ch02~05는 `@SpringBootTest` 컨텍스트 로딩 테스트까지 실행. 전부 통과하면 종료코드 0

- [ ] **Step 1: `VERIFY/verify_start.py` 작성**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""start 예제 코드가 승인 규칙과 챕터 [실습] 헤더에 맞는지 점검한다.

사용: python verify_start.py [챕터번호 ...]   (생략하면 1~5 전부)
"""
import re
import sys
from pathlib import Path

BOOK = Path("C:/work_삭제용/book-workflow/projects/특이점이-온-개발자-Springboot")
START = BOOK / "code" / "start"
FINAL = BOOK / "code" / "final"
CHAPTER_FILES = {
    1: "01-리플렉션-v5.md",
    2: "02-게시판CRUD-v6.md",
    3: "03-예외처리DTO-v5.md",
    4: "04-인증과인가-v8.md",
    5: "05-댓글과JPA심화-v7.md",
}

# 번호를 당긴 뒤 기대하는 [실습 N] -> 파일
EXPECTED = {
    1: {1: "ex01/BoardController.java", 2: "ex01/App.java", 3: "ex02/RequestMapping.java",
        4: "ex02/BoardController.java", 5: "ex02/App.java", 6: "ex03/Controller.java",
        7: "ex03/BoardController.java", 8: "ex03/App.java"},
    2: {1: "board/BoardRepository.java", 2: "board/BoardRepository.java",
        3: "board/BoardRepository.java", 4: "board/BoardRepository.java",
        5: "BoardRepositoryTest.java", 6: "BoardRepositoryTest.java",
        7: "BoardRepositoryTest.java", 8: "BoardRepositoryTest.java",
        9: "BoardRepositoryTest.java",
        10: "board/BoardService.java", 11: "board/BoardController.java",
        12: "board/BoardService.java", 13: "board/BoardController.java",
        14: "board/BoardService.java", 15: "board/BoardController.java",
        16: "board/BoardService.java", 17: "board/BoardController.java",
        18: "board/BoardService.java", 19: "board/BoardController.java"},
    3: {1: "board/BoardRequest.java", 2: "board/BoardResponse.java",
        3: "board/BoardRepository.java", 4: "core/handler/GlobalExceptionHandler.java",
        5: "board/BoardService.java", 6: "board/BoardController.java"},
    4: {1: "user/UserRepository.java", 2: "user/UserRequest.java", 3: "user/UserResponse.java",
        4: "user/UserService.java", 5: "user/UserController.java", 6: "user/UserService.java",
        7: "user/UserController.java", 8: "board/BoardRepository.java",
        9: "board/BoardResponse.java", 10: "board/BoardService.java",
        11: "board/BoardController.java", 12: "board/BoardRequest.java",
        13: "board/BoardService.java", 14: "board/BoardController.java",
        15: "board/BoardService.java", 16: "board/BoardController.java",
        17: "board/BoardService.java", 18: "board/BoardController.java"},
    5: {1: "board/BoardRepository.java", 2: "board/BoardResponse.java",
        3: "board/BoardService.java", 4: "reply/ReplyRequest.java",
        5: "reply/ReplyResponse.java", 6: "reply/ReplyService.java",
        7: "reply/ReplyController.java", 8: "reply/ReplyService.java",
        9: "reply/ReplyController.java"},
}

# [실습]에서 [참고]로 바꾼 블록 ("경로. 제목")
EXPECTED_REF = {
    2: ["board/BoardRepository.java. 리포지토리 골격",
        "BoardRepositoryTest.java. 테스트 클래스 골격"],
    4: ["user/UserRequest.java. 로그인 요청 DTO"],
    5: ["reply/ReplyRepository.java. JpaRepository 상속"],
}

# 메서드 틀을 남기는 파일: final의 골격 줄이 start에 있어야 하고, 본문 코드는 없어야 한다
FRAME_FILES = {
    1: ["ex01/BoardController.java", "ex01/App.java", "ex02/App.java", "ex03/App.java"],
    2: ["board/BoardRepository.java", "board/BoardService.java",
        "board/BoardController.java", "BoardRepositoryTest.java"],
    3: ["board/BoardRequest.java", "board/BoardResponse.java",
        "core/handler/GlobalExceptionHandler.java"],
    4: ["user/UserRepository.java", "user/UserRequest.java", "user/UserResponse.java",
        "user/UserService.java", "user/UserController.java"],
    5: ["reply/ReplyRepository.java", "reply/ReplyRequest.java", "reply/ReplyResponse.java",
        "reply/ReplyService.java", "reply/ReplyController.java"],
}

# 고치는 실습 파일과 어노테이션 실습 파일: 코드 줄(주석 제외)에 있으면 안 되는 패턴(정답 유출)
MUST_NOT = {
    1: {"ex02/BoardController.java": [r"@RequestMapping\("],
        "ex03/BoardController.java": [r"^\s*@Controller\s*$"],
        "ex02/RequestMapping.java": [r"@Retention", r"@Target", r"uri\(\)"],
        "ex03/Controller.java": [r"@Retention", r"@Target"]},
    3: {"board/BoardRepository.java": [r"interface BoardRepository"],
        "board/BoardService.java": [r"orElseThrow", r"BoardResponse\."],
        "board/BoardController.java": [r"BoardResponse\.", r"BoardRequest\."]},
    4: {"board/BoardRepository.java": [r"@Query", r"findByIdJoinUser"],
        "board/BoardResponse.java": [r"isOwner", r"User loginUser"],
        "board/BoardRequest.java": [r"toEntity\(User"],
        "board/BoardService.java": [r"findByIdJoinUser", r"loginUser"],
        "board/BoardController.java": [r"HttpServletRequest request", r"loginUser"]},
    5: {"board/BoardRepository.java": [r"findByIdJoinUserAndReplies"],
        "board/BoardResponse.java": [r"ReplyDTO", r"getReplies"],
        "board/BoardService.java": [r"findByIdJoinUserAndReplies"]},
}

HEADER = re.compile(r"^```\w+ \[(?:실습 (\d+)|참고)\] (\S+?\.java)\. (.+)$")
TODO = re.compile(r"// TODO : 실습 (\d+)")
STEP = re.compile(r"^\s*// \d+\. ")
BARE = re.compile(r"// TODO : 실습 \d+\s*$")
SKELETON = re.compile(r"^(@|public |private |import )")
RECORD_CTOR = re.compile(r"^public (DTO|DetailDTO|ReplyDTO)\(")
RECORD_HEADER = re.compile(r"public record \w+\([^)]*\)", re.S)
ALLOWED_IN_FRAME = re.compile(
    r"^(|//.*|package .*|import .*|@.*|public .*|private .*|\}|\{|return null;"
    r"|[\w<>.,\s]+[,)]\s*\{?"
    r"|String uri = \"/\w+\";|BoardController boardController = new BoardController\(\);)$"
)


def java_file(root, ch, rel):
    base = root / f"ch{ch:02d}"
    if ch == 1:
        return base / "src/main/java/com/reflection" / rel
    if rel == "BoardRepositoryTest.java":
        return base / "src/test/java/com/metacoding/spring/board" / rel
    return base / "src/main/java/com/metacoding/spring" / rel


def norm(s):
    return re.sub(r"\s+", "", s)


def code_only(line):
    return line.split("//")[0]


def check(ch):
    errors = []
    md = (BOOK / "chapters" / CHAPTER_FILES[ch]).read_text(encoding="utf-8")
    practices, refs = {}, []
    for line in md.splitlines():
        m = HEADER.match(line)
        if not m:
            continue
        num, path, title = m.groups()
        if num:
            if int(num) in practices:
                errors.append(f"[실습 {num}] 헤더 중복")
            practices[int(num)] = path
        else:
            refs.append(f"{path}. {title}")

    # (a) 챕터 [실습 N] -> 파일 매핑
    if practices != EXPECTED[ch]:
        errors.append(f"챕터 [실습] 매핑 불일치\n    기대: {EXPECTED[ch]}\n    실제: {practices}")
    # (b) [참고]로 바꾼 블록
    for r in EXPECTED_REF.get(ch, []):
        if r not in refs:
            errors.append(f"[참고] 헤더 없음: {r}")

    start_root = START / f"ch{ch:02d}"
    todo_map = {}
    for f in sorted(start_root.rglob("*.java")):
        rel = f.relative_to(start_root).as_posix()
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if STEP.match(line):
                errors.append(f"단계 주석: {rel}:{i}: {line.strip()}")
            if BARE.search(line):
                errors.append(f"설명 없는 TODO: {rel}:{i}")
            for n in TODO.findall(line):
                todo_map.setdefault(int(n), set()).add(f)

    # (c) 모든 [실습 N] 파일에 TODO 실습 N이 있다
    for n, path in EXPECTED[ch].items():
        if java_file(START, ch, path) not in todo_map.get(n, set()):
            errors.append(f"TODO 없음: 실습 {n} -> {path}")
    # (d) start의 TODO 실습 N은 기대 파일에만 있다
    for n, files in sorted(todo_map.items()):
        exp = EXPECTED[ch].get(n)
        for f in files:
            if exp is None or f != java_file(START, ch, exp):
                errors.append(f"잘못된 TODO 번호: 실습 {n} in {f.relative_to(start_root).as_posix()}")

    # (e) 틀 파일: final 골격 줄과 record 선언이 start에 있고, 본문 코드는 없다
    for path in FRAME_FILES[ch]:
        fin = java_file(FINAL, ch, path).read_text(encoding="utf-8")
        st = java_file(START, ch, path).read_text(encoding="utf-8")
        st_norm = {norm(code_only(x)) for x in st.splitlines()}
        for line in fin.splitlines():
            s = line.strip()
            if SKELETON.match(s) and not RECORD_CTOR.match(s):
                core = norm(code_only(s))
                if core and core not in st_norm:
                    errors.append(f"틀 누락: {path}: {s}")
        for h in RECORD_HEADER.findall(fin):
            if norm(h) not in norm(st):
                errors.append(f"record 선언 누락: {path}: {norm(h)}")
        for i, line in enumerate(st.splitlines(), 1):
            if not ALLOWED_IN_FRAME.match(line.strip()):
                errors.append(f"본문 코드 유출: {path}:{i}: {line.strip()}")

    # (f) 고치는 실습 파일·어노테이션 실습 파일에 정답이 없다
    for path, patterns in MUST_NOT.get(ch, {}).items():
        lines = java_file(START, ch, path).read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, 1):
            code = code_only(line)
            for p in patterns:
                if re.search(p, code):
                    errors.append(f"정답 유출: {path}:{i}: {line.strip()}")
    return errors


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    chapters = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5]
    failed = False
    for ch in chapters:
        errors = check(ch)
        if errors:
            failed = True
            print(f"FAIL ch{ch} ({len(errors)}건)")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"PASS ch{ch}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: `VERIFY/verify_build.sh` 작성**

```bash
#!/usr/bin/env bash
# start 사본을 만들어 컴파일하고, 스프링 챕터는 컨텍스트 로딩(@SpringBootTest)까지 확인한다
# 사용: bash verify_build.sh [ch01 ch02 ...]   (생략하면 전부)
set -u
SRC="/c/work_삭제용/book-workflow/projects/특이점이-온-개발자-Springboot/code/start"
WORK="/c/Users/BJ/AppData/Local/Temp/claude/C--work-----book-workflow/baf42c0f-4d8a-4236-889d-65f9ae26ef7f/scratchpad/verify/work"
CHS=("$@")
[ ${#CHS[@]} -eq 0 ] && CHS=(ch01 ch02 ch03 ch04 ch05)
rm -rf "$WORK" && mkdir -p "$WORK" && cp -r "$SRC/." "$WORK/"
fail=0
for c in "${CHS[@]}"; do
  if [ "$c" = "ch01" ]; then
    mkdir -p "$WORK/ch01/out"
    if javac -encoding UTF-8 -d "$WORK/ch01/out" $(find "$WORK/ch01/src" -name "*.java") > "$WORK/ch01-javac.log" 2>&1; then
      echo "ch01 compile OK"
    else
      echo "ch01 compile FAIL"; cat "$WORK/ch01-javac.log"; fail=1
    fi
    continue
  fi
  dir="$WORK/$c/src/test/java/com/metacoding/spring"
  mkdir -p "$dir"
  cat > "$dir/ContextLoadsCheckTest.java" <<'EOF'
package com.metacoding.spring;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ContextLoadsCheckTest {

    @Test
    void contextLoads() {
    }
}
EOF
  if (cd "$WORK/$c" && chmod +x gradlew && ./gradlew test --offline -q --tests "com.metacoding.spring.ContextLoadsCheckTest" > "$WORK/$c-test.log" 2>&1); then
    echo "$c compile + context OK"
  else
    echo "$c FAIL (log: $WORK/$c-test.log)"; grep -E "error:|FAILED|required a bean|Caused by" "$WORK/$c-test.log" | head -20; fail=1
  fi
done
exit $fail
```

- [ ] **Step 3: 현재 start에 실행해 실패를 확인**

Run: `python "VERIFY/verify_start.py"`
Expected: 다섯 챕터 모두 `FAIL`. ch01은 단계 주석·설명 없는 TODO, ch02·04·05는 챕터 [실습] 매핑 불일치(번호를 아직 당기지 않음), ch02~05는 틀 누락 항목이 나온다.

Run: `bash "VERIFY/verify_build.sh"`
Expected: 현재 start는 컴파일·컨텍스트 로딩 모두 `OK` (기준선 확인). 종료코드 0

---

### Task 2: CH01 start 재작성

**Files:**
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex01/App.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex01/BoardController.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex02/RequestMapping.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex02/BoardController.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex02/App.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex03/Controller.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex03/BoardController.java`
- Modify: `BOOK/code/start/ch01/src/main/java/com/reflection/ex03/App.java`
- Test: `VERIFY/verify_start.py 1`, `VERIFY/verify_build.sh ch01`

**Interfaces:**
- Consumes: Task 1의 검증 도구
- Produces: 챕터 1 [실습 1~8]과 1:1로 맞는 start/ch01 (챕터 1은 번호 변경 없음)

- [ ] **Step 1: 실패 확인**

Run: `python "VERIFY/verify_start.py" 1`
Expected: `FAIL ch1` (단계 주석, 설명 없는 TODO, 틀 누락)

- [ ] **Step 2: 8개 파일을 아래 내용으로 덮어쓴다**

`ex01/App.java`
```java
package com.reflection.ex01;

public class App {
    public static void main(String[] args) {

        String uri = "/insert";
        BoardController boardController = new BoardController();

        // TODO : 실습 2 - 주소에 따라 메서드 호출
    }
}
```

`ex01/BoardController.java`
```java
package com.reflection.ex01;

public class BoardController {

    public void insert(){
        // TODO : 실습 1 - 메서드 이름 출력
    }

    public void delete(){
        // TODO : 실습 1 - 메서드 이름 출력
    }

    public void update(){
        // TODO : 실습 1 - 메서드 이름 출력
    }
}
```

`ex02/RequestMapping.java`
```java
package com.reflection.ex02;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

// TODO : 실습 3 - 주소를 담는 커스텀 어노테이션
public @interface RequestMapping {
}
```

`ex02/BoardController.java`
```java
package com.reflection.ex02;

public class BoardController {

    // TODO : 실습 4 - /insert를 담당하도록 @RequestMapping 추가
    public void insert(){
        System.out.println("insert 호출됨");
    }

    // TODO : 실습 4 - /delete를 담당하도록 @RequestMapping 추가
    public void delete(){
        System.out.println("delete 호출됨");
    }

    // TODO : 실습 4 - /update를 담당하도록 @RequestMapping 추가
    public void update(){
        System.out.println("update 호출됨");
    }

    // TODO : 실습 4 - /select를 담당하도록 @RequestMapping 추가
    public void select(){
        System.out.println("select 호출됨");
    }
}
```

`ex02/App.java`
```java
package com.reflection.ex02;

import java.lang.reflect.Method;

public class App {
    public static void main(String[] args) {

        String uri = "/update";
        BoardController boardController = new BoardController();

        // TODO : 실습 5 - 어노테이션을 읽어 맞는 메서드를 호출
    }
}
```

`ex03/Controller.java`
```java
package com.reflection.ex03;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

// TODO : 실습 6 - 컨트롤러임을 나타내는 어노테이션
public @interface Controller {
}
```

`ex03/BoardController.java`
```java
package com.reflection.ex03;

// TODO : 실습 7 - 클래스 위에 @Controller 어노테이션
public class BoardController {

    @RequestMapping(uri = "/insert")
    public void insert(){
        System.out.println("insert 호출됨");
    }
    @RequestMapping(uri = "/delete")
    public void delete(){
        System.out.println("delete 호출됨");
    }
    @RequestMapping(uri = "/update")
    public void update(){
        System.out.println("update 호출됨");
    }
    @RequestMapping(uri = "/select")
    public void select(){
        System.out.println("select 호출됨");
    }
    @RequestMapping(uri = "/create")
    public void create(){
        System.out.println("create 호출됨");
    }
}
```

`ex03/App.java`
```java
package com.reflection.ex03;

import java.io.File;
import java.lang.reflect.Method;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.*;

public class App {

    public static void main(String[] args) throws URISyntaxException, ReflectiveOperationException {
        // TODO : 실습 8 - 폴더를 뒤져 @Controller 클래스를 등록하고 주소로 호출
    }

    public static void findUri(List<Object> instances, String uri) {
        // TODO : 실습 8 - 주소가 일치하는 메서드 호출
    }
}
```

- [ ] **Step 3: 통과 확인**

Run: `python "VERIFY/verify_start.py" 1` → Expected: `PASS ch1`
Run: `bash "VERIFY/verify_build.sh" ch01` → Expected: `ch01 compile OK`

---

### Task 3: CH02 start 재작성과 챕터 2 헤더 번호 변경

**Files:**
- Modify: `BOOK/code/start/ch02/src/main/java/com/metacoding/spring/board/BoardRepository.java`
- Modify: `BOOK/code/start/ch02/src/main/java/com/metacoding/spring/board/BoardService.java`
- Modify: `BOOK/code/start/ch02/src/main/java/com/metacoding/spring/board/BoardController.java`
- Modify: `BOOK/code/start/ch02/src/test/java/com/metacoding/spring/board/BoardRepositoryTest.java`
- Modify: `BOOK/chapters/02-게시판CRUD-v6.md` (코드블록 헤더 21줄)
- Test: `VERIFY/verify_start.py 2`, `VERIFY/verify_build.sh ch02`

**Interfaces:**
- Produces: 챕터 2 [실습 1~19] (기존 1·6은 [참고]). 새 번호 → 파일은 Task 1의 `EXPECTED[2]`

- [ ] **Step 1: 실패 확인**

Run: `python "VERIFY/verify_start.py" 2`
Expected: `FAIL ch2` (매핑 불일치, [참고] 헤더 없음, 틀 누락)

- [ ] **Step 2: 챕터 2 헤더를 아래 표대로 바꾼다 (헤더 줄만, 나머지 그대로)**

| 지금 헤더 | 바꿀 헤더 |
|---|---|
| ```` ```java [실습 1] board/BoardRepository.java. 리포지토리 골격 ```` | ```` ```java [참고] board/BoardRepository.java. 리포지토리 골격 ```` |
| `[실습 2] board/BoardRepository.java. 기본 키로 한 건 조회` | `[실습 1] ...` |
| `[실습 3] board/BoardRepository.java. JPQL로 전체 조회` | `[실습 2] ...` |
| `[실습 4] board/BoardRepository.java. 새 게시글 저장` | `[실습 3] ...` |
| `[실습 5] board/BoardRepository.java. 게시글 삭제` | `[실습 4] ...` |
| ```` ```java [실습 6] BoardRepositoryTest.java. 테스트 클래스 골격 ```` | ```` ```java [참고] BoardRepositoryTest.java. 테스트 클래스 골격 ```` |
| `[실습 7] BoardRepositoryTest.java. 한 건 조회` | `[실습 5] ...` |
| `[실습 8] BoardRepositoryTest.java. 전체 조회` | `[실습 6] ...` |
| `[실습 9] BoardRepositoryTest.java. 저장` | `[실습 7] ...` |
| `[실습 10] BoardRepositoryTest.java. 수정과 더티체킹` | `[실습 8] ...` |
| `[실습 11] BoardRepositoryTest.java. 삭제` | `[실습 9] ...` |
| `[실습 12] board/BoardService.java. 게시글 목록` | `[실습 10] ...` |
| `[실습 13] board/BoardController.java. 게시글 목록` | `[실습 11] ...` |
| `[실습 14] board/BoardService.java. 게시글 상세` | `[실습 12] ...` |
| `[실습 15] board/BoardController.java. 게시글 상세` | `[실습 13] ...` |
| `[실습 16] board/BoardService.java. 게시글 추가` | `[실습 14] ...` |
| `[실습 17] board/BoardController.java. 게시글 추가` | `[실습 15] ...` |
| `[실습 18] board/BoardService.java. 더티체킹으로 수정` | `[실습 16] ...` |
| `[실습 19] board/BoardController.java. 게시글 수정` | `[실습 17] ...` |
| `[실습 20] board/BoardService.java. 게시글 삭제` | `[실습 18] ...` |
| `[실습 21] board/BoardController.java. 게시글 삭제` | `[실습 19] ...` |

(`...`는 경로·제목을 그대로 둔다는 뜻. 숫자만 바꾼다. 번호가 겹치지 않도록 앞에서부터 차례로 바꾼다)

- [ ] **Step 3: start 4개 파일을 아래 내용으로 덮어쓴다**

`board/BoardRepository.java`
```java
package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Repository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class BoardRepository {

    private final EntityManager em;

    public Board findById(int boardId) {
        // TODO : 실습 1 - 기본 키로 한 건 조회
        return null;
    }

    public List<Board> findAll() {
        // TODO : 실습 2 - JPQL로 전체 조회
        return null;
    }

    public void save(Board board) {
        // TODO : 실습 3 - 새 게시글 저장
    }

    public void delete(Board board) {
        // TODO : 실습 4 - 게시글 삭제
    }
}
```

`board/BoardService.java`
```java
package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Service;

import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class BoardService {

    private final BoardRepository boardRepository;

    public List<Board> 게시글목록() {
        // TODO : 실습 10 - 게시글 목록
        return null;
    }

    public Board 게시글상세(Integer boardId) {
        // TODO : 실습 12 - 게시글 상세
        return null;
    }

    @Transactional
    public Board 게시글추가(Board requestBoard) {
        // TODO : 실습 14 - 게시글 추가
        return null;
    }

    @Transactional
    public void 게시글삭제(Integer boardId) {
        // TODO : 실습 18 - 게시글 삭제
    }

    @Transactional
    public Board 게시글수정(Integer boardId, Board requestBoard) {
        // TODO : 실습 16 - 더티체킹으로 수정
        return null;
    }
}
```

`board/BoardController.java`
```java
package com.metacoding.spring.board;

import java.util.*;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.util.Resp;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/boards")
public class BoardController {

    private final BoardService boardService;

    @GetMapping
    public ResponseEntity<?> findAll() {
        // TODO : 실습 11 - 게시글 목록
        return null;
    }

    @GetMapping("/{boardId}")
    public ResponseEntity<?> findById(@PathVariable("boardId") Integer boardId) {
        // TODO : 실습 13 - 게시글 상세
        return null;
    }

    @PostMapping
    public ResponseEntity<?> save(@RequestBody Board requestBoard) {
        // TODO : 실습 15 - 게시글 추가
        return null;
    }

    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(@PathVariable("boardId") Integer boardId, @RequestBody Board requestBoard) {
        // TODO : 실습 17 - 게시글 수정
        return null;
    }

    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(@PathVariable("boardId") Integer boardId) {
        // TODO : 실습 19 - 게시글 삭제
        return null;
    }
}
```

`BoardRepositoryTest.java` (src/test 쪽)
```java
package com.metacoding.spring.board;

import java.util.*;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;
import jakarta.persistence.EntityManager;

@Import(BoardRepository.class)
@DataJpaTest
public class BoardRepositoryTest {

    @Autowired
    private BoardRepository boardRepository;

    @Autowired
    private EntityManager em;

    @Test
    public void findById_test() {
        // TODO : 실습 5 - 한 건 조회
    }

    @Test
    public void findAll_test() {
        // TODO : 실습 6 - 전체 조회
    }

    @Test
    public void save_test() {
        // TODO : 실습 7 - 저장
    }

    @Test
    public void update_test() {
        // TODO : 실습 8 - 수정과 더티체킹
    }

    @Test
    public void delete_test() {
        // TODO : 실습 9 - 삭제
    }
}
```

- [ ] **Step 4: 통과 확인**

Run: `python "VERIFY/verify_start.py" 2` → Expected: `PASS ch2`
Run: `bash "VERIFY/verify_build.sh" ch02` → Expected: `ch02 compile + context OK`

---

### Task 4: CH03 start 재작성

**Files:**
- Modify: `BOOK/code/start/ch03/src/main/java/com/metacoding/spring/board/BoardRequest.java`
- Modify: `BOOK/code/start/ch03/src/main/java/com/metacoding/spring/board/BoardResponse.java`
- Modify: `BOOK/code/start/ch03/src/main/java/com/metacoding/spring/core/handler/GlobalExceptionHandler.java`
- Modify: `BOOK/code/start/ch03/src/main/java/com/metacoding/spring/board/BoardRepository.java` (TODO 한 줄만)
- Modify: `BOOK/code/start/ch03/src/main/java/com/metacoding/spring/board/BoardService.java` (TODO 다섯 줄만)
- Test: `VERIFY/verify_start.py 3`, `VERIFY/verify_build.sh ch03`

**Interfaces:**
- Produces: 챕터 3 [실습 1~6]과 1:1 (챕터 3은 번호 변경 없음, 챕터 파일 수정 없음)

- [ ] **Step 1: 실패 확인**

Run: `python "VERIFY/verify_start.py" 3`
Expected: `FAIL ch3` (단계 주석, 설명 없는 TODO, 틀 누락, record 선언 누락)

- [ ] **Step 2: 새 파일 3개를 아래 내용으로 덮어쓴다**

`board/BoardRequest.java`
```java
package com.metacoding.spring.board;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        public Board toEntity() {
            // TODO : 실습 1 - 엔티티로 변환
            return null;
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
```

`board/BoardResponse.java`
```java
package com.metacoding.spring.board;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        // TODO : 실습 2 - 엔티티를 받는 생성자
    }

    public record DetailDTO(Integer boardId, String title, String content) {

        // TODO : 실습 2 - 엔티티를 받는 생성자
    }
}
```

`core/handler/GlobalExceptionHandler.java`
```java
package com.metacoding.spring.core.handler;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.core.util.Resp;

// 예외를 JSON 응답으로 변환하는 전역 핸들러
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception400.class)
    public ResponseEntity<?> exApi400(Exception400 e) {
        // TODO : 실습 4 - 400 실패 응답
        return null;
    }

    @ExceptionHandler(Exception401.class)
    public ResponseEntity<?> exApi401(Exception401 e) {
        // TODO : 실습 4 - 401 실패 응답
        return null;
    }

    @ExceptionHandler(Exception403.class)
    public ResponseEntity<?> exApi403(Exception403 e) {
        // TODO : 실습 4 - 403 실패 응답
        return null;
    }

    @ExceptionHandler(Exception404.class)
    public ResponseEntity<?> exApi404(Exception404 e) {
        // TODO : 실습 4 - 404 실패 응답
        return null;
    }

    @ExceptionHandler(Exception500.class)
    public ResponseEntity<?> exApi500(Exception500 e) {
        // TODO : 실습 4 - 500 실패 응답
        return null;
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> exUnKnown(Exception e) {
        // TODO : 실습 4 - 나머지 예외는 500 실패 응답
        return null;
    }
}
```

- [ ] **Step 3: 고치는 실습 파일 2개는 TODO 줄만 바꾼다 (코드는 그대로)**

`board/BoardRepository.java`
- 지금: `// TODO : 실습 3 - JpaRepository<Board, Integer>를 상속하는 인터페이스로 변경한다 (아래 메서드는 모두 삭제)`
- 바꿈: `// TODO : 실습 3 - JpaRepository<Board, Integer>를 상속하는 인터페이스로 변경 (아래 메서드는 모두 삭제)`

`board/BoardService.java`
- `// TODO : 실습 5 - 반환 타입을 List<BoardResponse.DTO>로 변경 (엔티티를 DTO로 변환)` → `// TODO : 실습 5 - 반환 타입을 List<BoardResponse.DTO>로 변경`
- `// TODO : 실습 5 - 반환 타입을 BoardResponse.DetailDTO로 변경, 게시글이 없으면 Exception404` → `// TODO : 실습 5 - 반환 타입을 BoardResponse.DetailDTO로 변경, 게시글이 없으면 예외`
- `// TODO : 실습 5 - BoardRequest.SaveDTO를 받아 엔티티로 변환해 저장하고 BoardResponse.DTO 반환` → `// TODO : 실습 5 - BoardRequest.SaveDTO를 받아 저장하고 BoardResponse.DTO 반환`
- `// TODO : 실습 5 - 게시글이 없으면 Exception404` → `// TODO : 실습 5 - 게시글이 없으면 예외`
- `// TODO : 실습 5 - BoardRequest.UpdateDTO를 받아 수정하고 BoardResponse.DTO 반환, 게시글이 없으면 Exception404` → `// TODO : 실습 5 - BoardRequest.UpdateDTO를 받아 수정하고 BoardResponse.DTO 반환, 게시글이 없으면 예외`

`board/BoardController.java`는 그대로 둔다.

- [ ] **Step 4: 통과 확인**

Run: `python "VERIFY/verify_start.py" 3` → Expected: `PASS ch3`
Run: `bash "VERIFY/verify_build.sh" ch03` → Expected: `ch03 compile + context OK`

---

### Task 5: CH04 start 재작성과 챕터 4 헤더 번호 변경

**Files:**
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/user/UserRepository.java`
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/user/UserRequest.java`
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/user/UserResponse.java`
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/user/UserService.java`
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/user/UserController.java`
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/board/BoardRepository.java` (TODO 한 줄만)
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/board/BoardResponse.java` (TODO 한 줄만)
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/board/BoardRequest.java` (TODO 한 줄만)
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/board/BoardService.java` (TODO 네 줄만)
- Modify: `BOOK/code/start/ch04/src/main/java/com/metacoding/spring/board/BoardController.java` (TODO 네 줄만)
- Modify: `BOOK/chapters/04-인증과인가-v8.md` (코드블록 헤더 14줄)
- Test: `VERIFY/verify_start.py 4`, `VERIFY/verify_build.sh ch04`

**Interfaces:**
- Produces: 챕터 4 [실습 1~18] (기존 6은 [참고]). 새 번호 → 파일은 Task 1의 `EXPECTED[4]`

- [ ] **Step 1: 실패 확인**

Run: `python "VERIFY/verify_start.py" 4`
Expected: `FAIL ch4`

- [ ] **Step 2: 챕터 4 헤더를 바꾼다 (헤더 줄의 숫자만)**

| 지금 | 바꿈 |
|---|---|
| ```` ```java [실습 6] user/UserRequest.java. 로그인 요청 DTO ```` | ```` ```java [참고] user/UserRequest.java. 로그인 요청 DTO ```` |
| `[실습 7] user/UserService.java. 로그인` | `[실습 6]` |
| `[실습 8] user/UserController.java. 로그인 엔드포인트` | `[실습 7]` |
| `[실습 9] board/BoardRepository.java. 작성자를 함께 가져오는 조회` | `[실습 8]` |
| `[실습 10] board/BoardResponse.java. 상세 응답에 작성자와 본인 여부 추가` | `[실습 9]` |
| `[실습 11] board/BoardService.java. 상세 조회에 fetch 조인과 본인 여부` | `[실습 10]` |
| `[실습 12] board/BoardController.java. 상세 요청에서 로그인 유저 꺼내기` | `[실습 11]` |
| `[실습 13] board/BoardRequest.java. toEntity에 작성자 추가` | `[실습 12]` |
| `[실습 14] board/BoardService.java. 로그인 확인 후 작성자와 함께 저장` | `[실습 13]` |
| `[실습 15] board/BoardController.java. 추가 요청에서 로그인 유저 꺼내기` | `[실습 14]` |
| `[실습 16] board/BoardService.java. 로그인 확인과 소유자 검증` | `[실습 15]` |
| `[실습 17] board/BoardController.java. 수정 요청에서 로그인 유저 꺼내기` | `[실습 16]` |
| `[실습 18] board/BoardService.java. 삭제의 로그인 확인과 소유자 검증` | `[실습 17]` |
| `[실습 19] board/BoardController.java. 삭제 요청에서 로그인 유저 꺼내기` | `[실습 18]` |

[실습 1]~[실습 5]는 그대로 둔다.

- [ ] **Step 3: user 패키지 5개 파일을 아래 내용으로 덮어쓴다**

`user/UserRepository.java`
```java
package com.metacoding.spring.user;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Integer> {

    // TODO : 실습 1 - 유저네임으로 조회
}
```

`user/UserRequest.java`
```java
package com.metacoding.spring.user;

public class UserRequest {

    public record SaveDTO(String username, String password, String email) {

        public User toEntity() {
            // TODO : 실습 2 - 엔티티로 변환
            return null;
        }
    }

    public record LoginDTO(String username, String password) {
    }
}
```

`user/UserResponse.java`
```java
package com.metacoding.spring.user;

import java.time.LocalDateTime;

public class UserResponse {

    public record DTO(
            Integer userId,
            String username,
            String email,
            LocalDateTime createdAt) {

        // TODO : 실습 3 - 엔티티를 받는 생성자
    }
}
```

`user/UserService.java`
```java
package com.metacoding.spring.user;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.core.util.*;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class UserService {

    private final UserRepository userRepository;

    @Transactional
    public UserResponse.DTO 회원가입(UserRequest.SaveDTO requestDTO) {
        // TODO : 실습 4 - 회원가입
        return null;
    }

    public String 로그인(UserRequest.LoginDTO requestDTO) {
        // TODO : 실습 6 - 로그인
        return null;
    }
}
```

`user/UserController.java`
```java
package com.metacoding.spring.user;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.util.Resp;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class UserController {

    private final UserService userService;

    @PostMapping("/join")
    public ResponseEntity<?> join(@RequestBody UserRequest.SaveDTO requestDTO) {
        // TODO : 실습 5 - 회원가입 엔드포인트
        return null;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody UserRequest.LoginDTO requestDTO) {
        // TODO : 실습 7 - 로그인 엔드포인트
        return null;
    }
}
```

- [ ] **Step 4: board 패키지(고치는 실습)는 TODO 줄만 바꾼다 (코드는 그대로)**

`board/BoardRepository.java`
- `// TODO : 실습 9 - 작성자를 join fetch로 함께 가져오는 findByIdJoinUser()` → `// TODO : 실습 8 - 작성자를 join fetch로 함께 가져오는 findByIdJoinUser()`

`board/BoardResponse.java`
- `// TODO : 실습 10 - 작성자 아이디(userId)·유저네임(username)·본인 여부(isOwner)를 추가하고, 생성자가 로그인 유저(User)도 받도록 변경한다` → `// TODO : 실습 9 - 상세 응답에 작성자와 본인 여부 추가`

`board/BoardRequest.java`
- `// TODO : 실습 13 - toEntity()가 작성자(User)를 받아 함께 담도록 변경한다` → `// TODO : 실습 12 - toEntity에 작성자 추가`

`board/BoardService.java`
- `// TODO : 실습 11 - 로그인 유저(User)를 받고, findByIdJoinUser()로 조회해 본인 여부를 담은 DetailDTO 반환` → `// TODO : 실습 10 - 상세 조회에 fetch 조인과 본인 여부`
- `// TODO : 실습 14 - 로그인 유저(User)를 받아 로그인 확인(Exception401) 후 작성자와 함께 저장` → `// TODO : 실습 13 - 로그인 확인 후 작성자와 함께 저장`
- `// TODO : 실습 16 - 로그인 유저(User)를 받아 로그인 확인(Exception401), findByIdJoinUser()로 조회, 작성자 본인 확인(Exception403)` → `// TODO : 실습 15 - 로그인 확인과 소유자 검증`
- `// TODO : 실습 18 - 로그인 유저(User)를 받아 로그인 확인(Exception401), findByIdJoinUser()로 조회, 작성자 본인 확인(Exception403)` → `// TODO : 실습 17 - 삭제의 로그인 확인과 소유자 검증`

`board/BoardController.java`
- `// TODO : 실습 12 - HttpServletRequest에서 필터가 담아 둔 로그인 유저(loginUser)를 꺼내 서비스로 전달` → `// TODO : 실습 11 - 상세 요청에서 로그인 유저 꺼내기`
- `// TODO : 실습 15 - HttpServletRequest에서 로그인 유저(loginUser)를 꺼내 서비스로 전달` → `// TODO : 실습 14 - 추가 요청에서 로그인 유저 꺼내기`
- `// TODO : 실습 17 - HttpServletRequest에서 로그인 유저(loginUser)를 꺼내 서비스로 전달` → `// TODO : 실습 16 - 수정 요청에서 로그인 유저 꺼내기`
- `// TODO : 실습 19 - HttpServletRequest에서 로그인 유저(loginUser)를 꺼내 서비스로 전달` → `// TODO : 실습 18 - 삭제 요청에서 로그인 유저 꺼내기`

- [ ] **Step 5: 통과 확인**

Run: `python "VERIFY/verify_start.py" 4` → Expected: `PASS ch4`
Run: `bash "VERIFY/verify_build.sh" ch04` → Expected: `ch04 compile + context OK`

---

### Task 6: CH05 start 재작성과 챕터 5 헤더·파일 트리 변경

**Files:**
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/reply/ReplyRepository.java`
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/reply/ReplyRequest.java`
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/reply/ReplyResponse.java`
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/reply/ReplyService.java`
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/reply/ReplyController.java`
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/board/BoardRepository.java` (TODO 한 줄만)
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/board/BoardResponse.java` (TODO 두 줄만)
- Modify: `BOOK/code/start/ch05/src/main/java/com/metacoding/spring/board/BoardService.java` (TODO 한 줄만)
- Modify: `BOOK/chapters/05-댓글과JPA심화-v7.md` (코드블록 헤더 7줄 + 파일 트리 1줄)
- Test: `VERIFY/verify_start.py 5`, `VERIFY/verify_build.sh ch05`

**Interfaces:**
- Produces: 챕터 5 [실습 1~9] (기존 4는 [참고]). 새 번호 → 파일은 Task 1의 `EXPECTED[5]`

- [ ] **Step 1: 실패 확인**

Run: `python "VERIFY/verify_start.py" 5`
Expected: `FAIL ch5`

- [ ] **Step 2: 챕터 5 헤더와 파일 트리를 바꾼다**

| 지금 | 바꿈 |
|---|---|
| ```` ```java [실습 4] reply/ReplyRepository.java. JpaRepository 상속 ```` | ```` ```java [참고] reply/ReplyRepository.java. JpaRepository 상속 ```` |
| `[실습 5] reply/ReplyRequest.java. 댓글 요청 DTO` | `[실습 4]` |
| `[실습 6] reply/ReplyResponse.java. 댓글 응답 DTO` | `[실습 5]` |
| `[실습 7] reply/ReplyService.java. 댓글 저장` | `[실습 6]` |
| `[실습 8] reply/ReplyController.java. 댓글 작성 엔드포인트` | `[실습 7]` |
| `[실습 9] reply/ReplyService.java. 댓글 삭제` | `[실습 8]` |
| `[실습 10] reply/ReplyController.java. 댓글 삭제 엔드포인트` | `[실습 9]` |

파일 트리(`::::prep` 안): `ReplyRepository.java              # [작성] 댓글 리포지토리` → `ReplyRepository.java              # [참고] 댓글 리포지토리` (공백 정렬 유지)

- [ ] **Step 3: reply 패키지 5개 파일을 아래 내용으로 덮어쓴다**

`reply/ReplyRepository.java`
```java
package com.metacoding.spring.reply;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ReplyRepository extends JpaRepository<Reply, Integer> {
}
```

`reply/ReplyRequest.java`
```java
package com.metacoding.spring.reply;

import com.metacoding.spring.board.Board;
import com.metacoding.spring.user.User;

public class ReplyRequest {

    public record SaveDTO(String comment, Integer boardId) {

        public Reply toEntity(User user, Board board) {
            // TODO : 실습 4 - 엔티티로 변환
            return null;
        }
    }
}
```

`reply/ReplyResponse.java`
```java
package com.metacoding.spring.reply;

public class ReplyResponse {

    public record DTO(Integer replyId, String comment, String username) {

        // TODO : 실습 5 - 엔티티를 받는 생성자
    }
}
```

`reply/ReplyService.java`
```java
package com.metacoding.spring.reply;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.board.*;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.user.User;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;

    @Transactional
    public ReplyResponse.DTO 댓글추가(ReplyRequest.SaveDTO requestDTO, User loginUser) {
        // TODO : 실습 6 - 댓글 저장
        return null;
    }

    @Transactional
    public void 댓글삭제(Integer replyId, User loginUser) {
        // TODO : 실습 8 - 댓글 삭제
    }
}
```

`reply/ReplyController.java`
```java
package com.metacoding.spring.reply;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.util.Resp;
import com.metacoding.spring.user.User;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/replies")
public class ReplyController {

    private final ReplyService replyService;

    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @RequestBody ReplyRequest.SaveDTO requestDTO) {
        // TODO : 실습 7 - 댓글 작성 엔드포인트
        return null;
    }

    @DeleteMapping("/{replyId}")
    public ResponseEntity<?> deleteById(HttpServletRequest request, @PathVariable("replyId") Integer replyId) {
        // TODO : 실습 9 - 댓글 삭제 엔드포인트
        return null;
    }
}
```

- [ ] **Step 4: board 패키지(고치는 실습)는 TODO 줄만 바꾼다 (코드는 그대로)**

`board/BoardRepository.java`
- `// TODO : 실습 1 - 작성자와 댓글(댓글 작성자 포함)을 함께 가져오는 findByIdJoinUserAndReplies()` → `// TODO : 실습 1 - 작성자와 댓글을 함께 가져오는 findByIdJoinUserAndReplies()`

`board/BoardResponse.java`
- `// TODO : 실습 2 - 댓글 목록(List<ReplyDTO> replies) 필드를 추가하고, 생성자에서 댓글 엔티티를 ReplyDTO로 변환해 담는다` → `// TODO : 실습 2 - 상세에 댓글 목록 추가`
- `// TODO : 실습 2 - 댓글 하나를 담는 ReplyDTO(replyId, username, comment, isOwner)` → `// TODO : 실습 2 - 댓글 하나를 담는 ReplyDTO`

`board/BoardService.java`
- `// TODO : 실습 3 - findByIdJoinUser() 대신 findByIdJoinUserAndReplies()를 호출하도록 변경한다` → `// TODO : 실습 3 - findByIdJoinUser() 대신 findByIdJoinUserAndReplies() 호출`

- [ ] **Step 5: 통과 확인**

Run: `python "VERIFY/verify_start.py" 5` → Expected: `PASS ch5`
Run: `bash "VERIFY/verify_build.sh" ch05` → Expected: `ch05 compile + context OK` (이 테스트가 실습 3 직후 실행 시점의 부팅을 대신 확인한다)

---

### Task 7: 전체 검증과 HTML 빌드

**Files:**
- Build output: `BOOK/.build/02-*.html`, `BOOK/.build/04-*.html`, `BOOK/.build/05-*.html`

- [ ] **Step 1: 전체 점검**

Run: `python "VERIFY/verify_start.py"` → Expected: `PASS ch1` ~ `PASS ch5`, 종료코드 0
Run: `bash "VERIFY/verify_build.sh"` → Expected: ch01~ch05 전부 OK, 종료코드 0

- [ ] **Step 2: final과 start 차이 육안 확인**

Run: `cd BOOK/code && diff -r --strip-trailing-cr final start -x bin -x build -x .gradle -x test | head -400`
Expected: 차이는 메서드 본문·TODO 줄·고치는 실습 파일(이전 챕터 코드)뿐. 패키지·import·필드·시그니처 차이는 없다 (ch01 ex03/App의 `findUri` 시그니처 공백, 설명 주석 차이는 허용)

- [ ] **Step 3: 챕터 2·4·5 HTML 빌드**

```bash
cd "C:/work_삭제용/book-workflow"
export PYTHONUTF8=1; export PYTHONIOENCODING=utf-8
python .claude/skills/pub-html-build/build_html.py --project-root "projects/특이점이-온-개발자-Springboot" --chapter 2
python .claude/skills/pub-html-build/build_html.py --project-root "projects/특이점이-온-개발자-Springboot" --chapter 4
python .claude/skills/pub-html-build/build_html.py --project-root "projects/특이점이-온-개발자-Springboot" --chapter 5
```
Expected: 각 명령이 최신 버전(02-…-v6.html, 04-…-v8.html, 05-…-v7.html) 빌드 성공 메시지 출력. 브라우저는 열지 않는다

- [ ] **Step 4: 커밋하지 않는다** (사용자가 요청할 때만)

---

## 범위 밖 (사용자 승인 대기, 구현자는 건드리지 않음)

[참고]로 바꾼 블록 위 리드인 문장 4곳은 아직 "열어 아래와 같이 작성합니다/추가합니다"로 남는다. 문구는 사용자가 정한 뒤 반영한다.

- CH02 2.7: `` `board/BoardRepository.java`를 열어 아래와 같이 작성합니다. ``
- CH02 2.10.2: `` `board` 패키지의 `BoardRepositoryTest.java`를 열어 아래와 같이 작성합니다. ``
- CH04 4.7.1: `` 로그인 요청을 담을 DTO를 `user/UserRequest.java`에 아래와 같이 추가합니다. ``
- CH05 5.4.1: `댓글을 저장할 리포지토리를 작성합니다.` + `` `reply/ReplyRepository.java`를 열어 아래와 같이 작성합니다. ``
