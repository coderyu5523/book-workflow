package com.metacoding.spring.board;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        public Board toEntity() {
            // TODO : 실습 1 - 엔티티로 변환
            return null;
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
