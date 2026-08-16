package com.metacoding.spring.user;

import java.sql.Timestamp;

public class UserResponse {

    public record DTO(
            Integer userId,
            String username,
            String email,
            Timestamp createdAt) {

        public DTO(User user) {
            this(
                    user.getId(),
                    user.getUsername(),
                    user.getEmail(),
                    user.getCreatedAt());
        }
    }
}
