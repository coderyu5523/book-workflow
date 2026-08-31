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
        List<BoardResponse.DTO> respDTOList = boardService.게시글목록();
        return Resp.ok(respDTOList);
    }

    @GetMapping("/{boardId}")
    public ResponseEntity<?> findById(@PathVariable("boardId") Integer boardId) {
        BoardResponse.DetailDTO respDTO = boardService.게시글상세(boardId);
        return Resp.ok(respDTO);
    }

    @PostMapping
    public ResponseEntity<?> save(@RequestBody BoardRequest.SaveDTO requestDTO) {
        BoardResponse.DTO respDTO = boardService.게시글쓰기(requestDTO);
        return Resp.ok(respDTO);
    }

    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(@PathVariable("boardId") Integer boardId, @RequestBody BoardRequest.UpdateDTO requestDTO) {
        BoardResponse.DTO respDTO = boardService.게시글수정(boardId, requestDTO);
        return Resp.ok(respDTO);
    }

    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(@PathVariable("boardId") Integer boardId) {
        boardService.게시글삭제(boardId);
        return Resp.ok(null);
    }
}
