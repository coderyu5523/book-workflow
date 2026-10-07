package com.metacoding.spring.board;

import com.metacoding.spring.user.User;

public class BoardResponse {

    public record DTO(Integer boardId, String title, String content) {

        public DTO(Board board) {
            this(board.getId(), board.getTitle(), board.getContent());
        }
    }

    public record DetailDTO(
            Integer boardId,
            String title,
            String content,
            Integer userId, // 작성자 아이디 추가
            String username, // 작성자 유저네임 추가
            Boolean isOwner) { // 본인 여부 추가

        public DetailDTO(Board board, User loginUser) { // 로그인 유저 매개변수 추가
            this(
                    board.getId(),
                    board.getTitle(),
                    board.getContent(),
                    board.getUser().getId(), // 작성자 아이디 추가
                    board.getUser().getUsername(), // 작성자 유저네임 추가
                    // 비로그인이면 false, 요청자와 작성자가 같으면 true
                    loginUser != null
                            && loginUser.getId().equals(board.getUser().getId()));
        }
    }
}
