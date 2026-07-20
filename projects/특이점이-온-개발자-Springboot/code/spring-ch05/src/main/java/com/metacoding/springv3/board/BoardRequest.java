package com.metacoding.springv3.board;

import com.metacoding.springv3.user.User;
import jakarta.validation.constraints.*;

public class BoardRequest {

    public record SaveDTO(
            @NotEmpty(message = "제목을 입력해주세요")
            @Size(max = 30, message = "제목은 30자 이내로 입력해주세요")
            String title,

            @NotEmpty(message = "내용을 입력해주세요")
            String content) {

        // 빌더 패턴으로 엔티티 생성 (작성자 연결)
        public Board toEntity(User user) {
            return Board.builder()
                    .title(title)
                    .content(content)
                    .user(user)
                    .build();
        }
    }

    public record UpdateDTO(
            @NotEmpty(message = "제목을 입력해주세요")
            @Size(max = 30, message = "제목은 30자 이내로 입력해주세요")
            String title,

            @NotEmpty(message = "내용을 입력해주세요")
            String content) {
    }
}
