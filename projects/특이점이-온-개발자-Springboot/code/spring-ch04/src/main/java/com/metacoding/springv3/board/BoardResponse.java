package com.metacoding.springv3.board;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        public DTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }

    public record DetailDTO(Integer boardId, String title, String content, Integer userId, String username) {

        public DetailDTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent(),
                    board.getUser().getId(), board.getUser().getUsername());
        }
    }
}
