package com.metacoding.spring.board;

import com.metacoding.spring.user.User;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        // TODO : 실습 12 - toEntity에 작성자 추가
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
