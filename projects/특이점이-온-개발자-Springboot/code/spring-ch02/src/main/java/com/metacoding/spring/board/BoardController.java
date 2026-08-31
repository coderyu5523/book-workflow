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
        List<Board> responseBoardList = boardService.게시글목록();
        return Resp.ok(responseBoardList);
    }

    @GetMapping("/{boardId}")
    public ResponseEntity<?> findById(@PathVariable("boardId") Integer boardId) {
        Board responseBoard = boardService.게시글상세(boardId);
        return Resp.ok(responseBoard);
    }

    @PostMapping
    public ResponseEntity<?> save(@RequestBody Board requestBoard) {
        Board responseBoard = boardService.게시글쓰기(requestBoard);
        return Resp.ok(responseBoard);
    }

    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(@PathVariable("boardId") Integer boardId, @RequestBody Board requestBoard) {
        Board responseBoard = boardService.게시글수정(boardId, requestBoard);
        return Resp.ok(responseBoard);
    }

    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(@PathVariable("boardId") Integer boardId) {
        boardService.게시글삭제(boardId);
        return Resp.ok(null);
    }
}
