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
