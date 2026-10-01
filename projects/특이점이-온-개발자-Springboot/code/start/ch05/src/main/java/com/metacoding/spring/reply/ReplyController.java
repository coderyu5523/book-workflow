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
