package com.metacoding.spring.board;

import java.util.*;
import com.metacoding.spring.reply.Reply;

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

        public DetailDTO(Board board, Integer loginUserId) {
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(),
                    board.getUser().getUsername(),
                    loginUserId != null
                            && loginUserId.equals(board.getUser().getId()),
                    board.getReplies().stream()
                            .map(reply -> new ReplyDTO(reply, loginUserId))
                            .toList());
        }

        public record ReplyDTO(
                Integer replyId,
                String username,
                String comment,
                Boolean isOwner) {

            public ReplyDTO(Reply reply, Integer loginUserId) {
                this(
                        reply.getId(),
                        reply.getUser().getUsername(),
                        reply.getComment(),
                        loginUserId != null && loginUserId.equals(
                                reply.getUser().getId()));
            }
        }
    }
}
