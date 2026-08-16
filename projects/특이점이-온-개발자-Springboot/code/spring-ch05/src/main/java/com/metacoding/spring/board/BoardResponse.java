package com.metacoding.spring.board;

import java.util.*;
import com.metacoding.spring.reply.Reply;
import com.metacoding.spring.user.User;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        public DTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }

    public record DetailDTO(
            Integer boardId,
            String title,
            String content,
            Integer userId,
            String username,
            Boolean isOwner,
            List<ReplyDTO> replies) {

        public DetailDTO(Board board, User loginUser) {
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(),
                    board.getUser().getUsername(),
                    loginUser != null && loginUser.getId()
                            .equals(board.getUser().getId()),
                    board.getReplies().stream()
                            .map(reply -> new ReplyDTO(reply, loginUser))
                            .toList());
        }

        public record ReplyDTO(
                Integer replyId,
                String username,
                String comment,
                Boolean isOwner) {

            public ReplyDTO(Reply reply, User loginUser) {
                this(
                        reply.getId(),
                        reply.getUser().getUsername(),
                        reply.getComment(),
                        loginUser != null && loginUser.getId()
                                .equals(reply.getUser().getId()));
            }
        }
    }
}
