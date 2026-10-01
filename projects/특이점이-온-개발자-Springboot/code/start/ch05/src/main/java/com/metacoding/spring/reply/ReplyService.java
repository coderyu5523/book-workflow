package com.metacoding.spring.reply;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.board.*;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.user.User;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class ReplyService {

    private final ReplyRepository replyRepository;
    private final BoardRepository boardRepository;

    @Transactional
    public ReplyResponse.DTO 댓글추가(ReplyRequest.SaveDTO requestDTO, User loginUser) {
        // TODO : 실습 6 - 댓글 저장
        return null;
    }

    @Transactional
    public void 댓글삭제(Integer replyId, User loginUser) {
        // TODO : 실습 8 - 댓글 삭제
    }
}
