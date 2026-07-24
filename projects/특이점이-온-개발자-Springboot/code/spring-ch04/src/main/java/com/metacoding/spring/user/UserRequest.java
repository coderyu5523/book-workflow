package com.metacoding.spring.user;

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

        // 요청 값으로 엔티티 생성
        public User toEntity() {
            return User.builder()
                    .username(username)
                    .password(password)
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
