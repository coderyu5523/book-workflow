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
        // TODO : 실습 1 - 기본 키로 한 건 조회
        return null;
    }

    public List<Board> findAll() {
        // TODO : 실습 2 - JPQL로 전체 조회
        return null;
    }

    public void save(Board board) {
        // TODO : 실습 3 - 새 게시글 저장
    }

    public void delete(Board board) {
        // TODO : 실습 4 - 게시글 삭제
    }
}
