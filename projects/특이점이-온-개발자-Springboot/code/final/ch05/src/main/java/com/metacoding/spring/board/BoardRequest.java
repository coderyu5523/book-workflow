package com.metacoding.spring.board;

import com.metacoding.spring.user.User;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        public Board toEntity(User user) {
            return Board.builder()
                    .title(title)
                    .content(content)
                    .user(user)
                    .build();
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
