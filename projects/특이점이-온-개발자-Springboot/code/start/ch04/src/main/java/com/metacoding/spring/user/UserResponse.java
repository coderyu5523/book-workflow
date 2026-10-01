package com.metacoding.spring.user;

import java.time.LocalDateTime;

public class UserResponse {

    public record DTO(
            Integer userId,
            String username,
            String email,
            LocalDateTime createdAt) {

        // TODO : 실습 3 - 엔티티를 받는 생성자
    }
}
