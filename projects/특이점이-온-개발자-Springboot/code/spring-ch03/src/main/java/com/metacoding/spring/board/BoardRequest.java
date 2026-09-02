package com.metacoding.spring.board;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        public Board toEntity() {
            return Board.builder()
                    .title(title)
                    .content(content)
                    .build();
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
