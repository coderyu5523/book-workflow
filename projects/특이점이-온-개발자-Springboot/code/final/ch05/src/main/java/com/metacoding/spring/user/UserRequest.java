package com.metacoding.spring.user;

public class UserRequest {

    public record SaveDTO(String username, String password, String email) {

        public User toEntity() {
            return User.builder()
                    .username(username)
                    .password(password)
                    .email(email)
                    .build();
        }
    }

    public record LoginDTO(String username, String password) {
    }
}
