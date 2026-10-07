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

    // TODO : 실습 6 - 요청·응답 타입을 DTO로
    @GetMapping
    public ResponseEntity<?> findAll() {
        List<Board> responseBoardList = boardService.게시글목록();
        return Resp.ok(responseBoardList);
    }

    // TODO : 실습 6 - 요청·응답 타입을 DTO로
    @GetMapping("/{boardId}")
    public ResponseEntity<?> findById(@PathVariable("boardId") Integer boardId) {
        Board responseBoard = boardService.게시글상세(boardId);
        return Resp.ok(responseBoard);
    }

    // TODO : 실습 6 - 요청·응답 타입을 DTO로
    @PostMapping
    public ResponseEntity<?> save(@RequestBody Board requestBoard) {
        Board responseBoard = boardService.게시글추가(requestBoard);
        return Resp.ok(responseBoard);
    }

    // TODO : 실습 6 - 요청·응답 타입을 DTO로
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
