package com.metacoding.spring.board;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        // TODO : 실습 2 - 엔티티를 받는 생성자
    }

    public record DetailDTO(Integer boardId, String title, String content) {

        // TODO : 실습 2 - 엔티티를 받는 생성자
    }
}
