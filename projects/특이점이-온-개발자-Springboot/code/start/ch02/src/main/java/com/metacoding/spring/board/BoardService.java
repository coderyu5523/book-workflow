package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Service;

import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class BoardService {

    private final BoardRepository boardRepository;

    public List<Board> 게시글목록() {
        // TODO : 실습 10 - 게시글 목록
        return null;
    }

    public Board 게시글상세(Integer boardId) {
        // TODO : 실습 12 - 게시글 상세
        return null;
    }

    @Transactional
    public Board 게시글추가(Board requestBoard) {
        // TODO : 실습 14 - 게시글 추가
        return null;
    }

    @Transactional
    public void 게시글삭제(Integer boardId) {
        // TODO : 실습 18 - 게시글 삭제
    }

    @Transactional
    public Board 게시글수정(Integer boardId, Board requestBoard) {
        // TODO : 실습 16 - 더티체킹으로 수정
        return null;
    }
}
