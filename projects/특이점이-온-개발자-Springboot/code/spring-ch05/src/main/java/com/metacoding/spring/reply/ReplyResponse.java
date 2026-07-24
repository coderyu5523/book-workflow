package com.metacoding.spring.reply;

public class ReplyResponse {

    public record DTO(Integer replyId, String comment, String username) {

        public DTO(Reply reply) {
            this(reply.getId(), reply.getComment(), reply.getUser().getUsername());
        }
    }
}
