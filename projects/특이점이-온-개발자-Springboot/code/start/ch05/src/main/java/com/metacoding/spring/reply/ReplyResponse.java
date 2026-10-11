package com.metacoding.spring.reply;

public class ReplyResponse {

    public record DTO(Integer replyId, String comment, String username) {

        // TODO : 실습 6 - 댓글 응답 DTO
    }
}
