package com.metacoding.spring.reply;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.util.Resp;
import com.metacoding.spring.user.User;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/replies")
public class ReplyController {

    private final ReplyService replyService;

    // 댓글 쓰기 (로그인 필요)
    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @Valid @RequestBody ReplyRequest.SaveDTO requestDTO) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        ReplyResponse.DTO respDTO = replyService.댓글쓰기(requestDTO, sessionUser);
        return Resp.ok(respDTO);
    }

    // 댓글 삭제 (작성자만)
    @DeleteMapping("/{replyId}")
    public ResponseEntity<?> deleteById(HttpServletRequest request, @PathVariable("replyId") Integer replyId) {
        User sessionUser = (User) request.getAttribute("sessionUser");
        replyService.댓글삭제(replyId, sessionUser.getId());
        return Resp.ok(null);
    }
}
