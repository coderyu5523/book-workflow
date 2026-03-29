package com.metacoding.spring_oauth_oidc.user;

public class UserResponse {

    public record DTO(Integer id, String username, String email, String token) {

        // 토큰 없음
        public DTO(User user) {
            this(user.getId(), user.getUsername(), user.getEmail(), null);
        }

        // 토큰 있음
        public DTO(User user, String token) {
            this(user.getId(), user.getUsername(), user.getEmail(), token);
        }
    }
}
