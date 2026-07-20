package com.metacoding.springv3.board;

import java.util.*;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.springv3.core.util.Resp;
import com.metacoding.springv3.user.User;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/boards")
public class BoardController {

    private final BoardService boardService;

    // 게시글 목록 (공개)
    @GetMapping
    public ResponseEntity<?> findAll() {
        List<BoardResponse.DTO> respDTOList = boardService.게시글목록();
        return Resp.ok(respDTOList);
    }

    // 게시글 상세 (공개)
    @GetMapping("/{boardId}")
    public ResponseEntity<?> detail(@PathVariable("boardId") Integer boardId) {
        BoardResponse.DetailDTO respDTO = boardService.게시글상세(boardId);
        return Resp.ok(respDTO);
    }

    // 게시글 쓰기 (로그인 필요 - 인터셉터가 보장)
    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @Valid @RequestBody BoardRequest.SaveDTO requestDTO) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        BoardResponse.DTO respDTO = boardService.게시글추가(requestDTO, sessionUser);
        return Resp.ok(respDTO);
    }

    // 게시글 수정 (작성자만)
    @PutMapping("/{boardId}")
    public ResponseEntity<?> update(HttpServletRequest request, @PathVariable("boardId") Integer boardId,
            @Valid @RequestBody BoardRequest.UpdateDTO requestDTO) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        BoardResponse.DTO respDTO = boardService.게시글수정(boardId, requestDTO, sessionUser.getId());
        return Resp.ok(respDTO);
    }

    // 게시글 삭제 (작성자만)
    @DeleteMapping("/{boardId}")
    public ResponseEntity<?> deleteById(HttpServletRequest request, @PathVariable("boardId") Integer boardId) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        boardService.게시글삭제(boardId, sessionUser.getId());
        return Resp.ok(null);
    }
}
