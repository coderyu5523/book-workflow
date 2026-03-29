package com.metacoding.spring_oauth.user;

public class UserRequest {

    public record JoinDTO(String username, String password, String email) {

        public User toEntity() {
            return User.builder()
                    .username(username)
                    .password(password)
                    .email(email)
                    .provider("local")
                    .build();
        }
    }

    public record LoginDTO(String username, String password) {
    }
}

