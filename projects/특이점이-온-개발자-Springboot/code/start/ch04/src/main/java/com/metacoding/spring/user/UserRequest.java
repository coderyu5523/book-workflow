package com.metacoding.spring.user;

public class UserRequest {

    public record SaveDTO(String username, String password, String email) {

        public User toEntity() {
            // TODO : 실습 2 - 엔티티로 변환
            return null;
        }
    }

    // TODO : 실습 6 - 로그인 요청 DTO
}
