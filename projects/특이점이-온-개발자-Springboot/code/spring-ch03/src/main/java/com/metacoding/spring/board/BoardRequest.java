package com.metacoding.spring.board;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        // 빌더 패턴으로 엔티티 생성
        public Board toEntity() {
            return Board.builder()
                .title(title())
                .content(content())
                .build();
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
