package com.metacoding.spring.board;

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
            Boolean isOwner) {

        public DetailDTO(Board board, User loginUser) {
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(),
                    board.getUser().getUsername(),
                    loginUser != null && loginUser.getId()
                            .equals(board.getUser().getId()));
        }
    }
}
