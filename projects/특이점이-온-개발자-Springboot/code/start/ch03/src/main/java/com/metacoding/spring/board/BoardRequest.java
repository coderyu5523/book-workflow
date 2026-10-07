package com.metacoding.spring.board;

public class BoardRequest {

    public record SaveDTO(String title, String content) {

        public Board toEntity() {
            // TODO : 실습 1 - 요청 DTO와 엔티티 변환
            return null;
        }
    }

    public record UpdateDTO(String title, String content) {
    }
}
