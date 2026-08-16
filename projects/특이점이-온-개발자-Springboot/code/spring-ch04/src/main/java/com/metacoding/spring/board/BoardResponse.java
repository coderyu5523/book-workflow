package com.metacoding.spring.board;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        public DTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }

    public record DetailDTO(Integer boardId, String title, String content,
            Integer userId, String username, Boolean isOwner) {

        public DetailDTO(Board board, Integer loginUserId) {
            this(board.getId(), board.getTitle(), board.getContent(),
                    board.getUser().getId(), board.getUser().getUsername(),
                    checkOwner(loginUserId, board.getUser().getId()));
        }

        // 로그인한 사용자가 작성자인지 (비로그인 시 false)
        private static boolean checkOwner(Integer loginUserId, Integer writerId) {
            return loginUserId != null && loginUserId.equals(writerId);
        }
    }
}
