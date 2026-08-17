package com.metacoding.spring.board;

import java.util.*;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.util.Resp;
import com.metacoding.spring.user.User;
import jakarta.servlet.http.HttpServletRequest;
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
    public ResponseEntity<?> detail(HttpServletRequest request, @PathVariable("boardId") Integer boardId) {
        User loginUser = (User) request.getAttribute("loginUser"); // 비로그인 시 null
        BoardResponse.DetailDTO respDTO = boardService.게시글상세(boardId, loginUser);
        return Resp.ok(respDTO);
    }

    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @RequestBody BoardRequest.SaveDTO requestDTO) {
        User loginUser = (User) request.getAttribute("loginUser");
        BoardResponse.DTO respDTO = boardService.게시글추가(requestDTO, loginUser);
        return Resp.ok(respDTO);
    }

    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(HttpServletRequest request, @PathVariable("boardId") Integer boardId,
            @RequestBody BoardRequest.UpdateDTO requestDTO) {
        User loginUser = (User) request.getAttribute("loginUser");
        BoardResponse.DTO respDTO = boardService.게시글수정(boardId, requestDTO, loginUser);
        return Resp.ok(respDTO);
    }

    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(HttpServletRequest request, @PathVariable("boardId") Integer boardId) {
        User loginUser = (User) request.getAttribute("loginUser");
        boardService.게시글삭제(boardId, loginUser);
        return Resp.ok(null);
    }
}
