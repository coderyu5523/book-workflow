package com.metacoding.spring.reply;

import com.metacoding.spring.board.Board;
import com.metacoding.spring.user.User;

public class ReplyRequest {

    public record SaveDTO(String comment, Integer boardId) {

        public Reply toEntity(User user, Board board) {
            return Reply.builder()
                    .comment(comment)
                    .user(user)
                    .board(board)
                    .build();
        }
    }
}
