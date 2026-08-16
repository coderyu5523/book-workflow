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
            Boolean isOwner, // 게시글 작성자 여부
            List<ReplyDTO> replies) {

        public DetailDTO(Board board, Integer loginUserId) {
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(),
                    board.getUser().getUsername(),
                    checkOwner(loginUserId, board.getUser().getId()),
                    board.getReplies().stream()
                            .map(reply -> new ReplyDTO(reply, loginUserId))
                            .toList());
        }

        // 댓글 DTO
        public record ReplyDTO(
                Integer replyId,
                String username,
                String comment,
                Boolean isOwner) { // 댓글 작성자 여부

            public ReplyDTO(Reply reply, Integer loginUserId) {
                this(
                        reply.getId(),
                        reply.getUser().getUsername(),
                        reply.getComment(),
                        checkOwner(loginUserId, reply.getUser().getId()));
            }
        }

        // 로그인한 사용자가 작성자인지 (비로그인 시 false)
        private static boolean checkOwner(Integer loginUserId, Integer writerId) {
            return loginUserId != null && loginUserId.equals(writerId);
        }
    }
}
