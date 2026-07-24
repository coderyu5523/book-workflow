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

    // 게시글 목록
    @GetMapping
    public ResponseEntity<?> findAll() {
        List<Board> boardList = boardService.게시글목록();
        return Resp.ok(boardList);
    }

    // 게시글 상세
    @GetMapping("/{boardId}")
    public ResponseEntity<?> detail(@PathVariable("boardId") Integer boardId) {
        Board board = boardService.게시글상세(boardId);
        return Resp.ok(board);
    }

    // 게시글 쓰기
    @PostMapping
    public ResponseEntity<?> save(@RequestBody BoardRequest.SaveDTO requestDTO) {
        Board board = boardService.게시글추가(requestDTO);
        return Resp.ok(board);
    }

    // 게시글 수정
    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(@PathVariable("boardId") Integer boardId, @RequestBody BoardRequest.UpdateDTO requestDTO) {
        Board board = boardService.게시글수정(boardId, requestDTO);
        return Resp.ok(board);
    }

    // 게시글 삭제
    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(@PathVariable("boardId") Integer boardId) {
        boardService.게시글삭제(boardId);
        return Resp.ok(null);
    }
}
