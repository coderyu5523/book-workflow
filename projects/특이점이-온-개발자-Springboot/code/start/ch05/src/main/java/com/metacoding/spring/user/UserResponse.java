package com.metacoding.spring.user;

import java.time.LocalDateTime;

public class UserResponse {

    public record DTO(
            Integer userId,
            String username,
            String email,
            LocalDateTime createdAt) {

        public DTO(User user) {
            this(
                    user.getId(),
                    user.getUsername(),
                    user.getEmail(),
                    user.getCreatedAt());
        }
    }
}
