package com.metacoding.springv3.user;

import jakarta.validation.constraints.*;

public class UserRequest {

    public record SaveDTO(
            @NotEmpty(message = "유저네임을 입력해주세요")
            @Size(min = 2, max = 20, message = "유저네임은 2자 이상 20자 이하로 입력해주세요")
            String username,

            @NotEmpty(message = "비밀번호를 입력해주세요")
            String password,

            @Email(message = "이메일 형식이 올바르지 않습니다")
            String email) {

        // 암호화된 비밀번호로 엔티티 생성
        public User toEntity(String encPassword) {
            return User.builder()
                    .username(username)
                    .password(encPassword)
                    .email(email)
                    .build();
        }
    }

    public record LoginDTO(
            @NotEmpty(message = "유저네임을 입력해주세요")
            String username,

            @NotEmpty(message = "비밀번호를 입력해주세요")
            String password) {
    }
}
