package com.metacoding.spring.reply;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.handler.ex.Exception401;
import com.metacoding.spring.core.util.Resp;
import com.metacoding.spring.user.User;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/replies")
public class ReplyController {

    private final ReplyService replyService;

    // 댓글 쓰기 (로그인 필요)
    @PostMapping
    public ResponseEntity<?> save(HttpServletRequest request,
            @RequestBody ReplyRequest.SaveDTO requestDTO) {
        User loginUser = (User) request.getAttribute("loginUser");
        if (loginUser == null) {
            throw new Exception401("로그인이 필요합니다");
        }
        ReplyResponse.DTO respDTO = replyService.댓글쓰기(requestDTO, loginUser);
        return Resp.ok(respDTO);
    }

    // 댓글 삭제 (작성자만)
    @DeleteMapping("/{replyId}")
    public ResponseEntity<?> deleteById(HttpServletRequest request, @PathVariable("replyId") Integer replyId) {
        User loginUser = (User) request.getAttribute("loginUser");
        if (loginUser == null) {
            throw new Exception401("로그인이 필요합니다");
        }
        replyService.댓글삭제(replyId, loginUser.getId());
        return Resp.ok(null);
    }
}
