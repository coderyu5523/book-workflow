package com.metacoding.spring.board;

public class BoardRequest {
    public record SaveDTO(String title, String content) {
    }

    public record UpdateDTO(String title, String content) {
    }
}
