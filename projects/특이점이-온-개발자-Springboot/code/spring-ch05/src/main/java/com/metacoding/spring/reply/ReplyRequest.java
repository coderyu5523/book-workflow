package com.metacoding.spring.reply;

import com.metacoding.spring.board.Board;
import com.metacoding.spring.user.User;
import jakarta.validation.constraints.*;

public class ReplyRequest {

    public record SaveDTO(
            @NotEmpty(message = "댓글 내용을 입력해주세요")
            String comment,

            @NotNull(message = "게시글 번호가 필요합니다")
            Integer boardId) {

        public Reply toEntity(User user, Board board) {
            return Reply.builder()
                    .comment(comment)
                    .user(user)
                    .board(board)
                    .build();
        }
    }
}
