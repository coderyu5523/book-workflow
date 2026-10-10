package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Repository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class BoardRepository {

    private final EntityManager em;

    public Board findById(int boardId) {
        // TODO : 실습 1 - 게시글 상세
        return null;
    }

    public List<Board> findAll() {
        // TODO : 실습 2 - JPQL로 게시글 목록 조회
        return null;
    }

    public void save(Board board) {
        // TODO : 실습 3 - 게시글 추가
    }

    public void delete(Board board) {
        // TODO : 실습 4 - 게시글 삭제
    }
}
