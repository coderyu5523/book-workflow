package com.metacoding.spring.user;

import java.time.LocalDateTime;

public class UserResponse {

    public record DTO(
            Integer userId,
            String username,
            String email,
            LocalDateTime createdAt) {

        // TODO : 실습 4 - 회원가입 응답 DTO
    }
}
