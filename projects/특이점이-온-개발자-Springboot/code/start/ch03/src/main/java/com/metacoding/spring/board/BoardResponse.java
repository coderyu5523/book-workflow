package com.metacoding.spring.board;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        // TODO : 실습 2 - 응답 DTO
    }

    public record DetailDTO(Integer boardId, String title, String content) {

        // TODO : 실습 2 - 응답 DTO
    }
}
