package com.metacoding.spring.reply;

public class ReplyResponse {

    public record DTO(Integer replyId, String comment, String username) {

        // TODO : 실습 5 - 엔티티를 받는 생성자
    }
}
