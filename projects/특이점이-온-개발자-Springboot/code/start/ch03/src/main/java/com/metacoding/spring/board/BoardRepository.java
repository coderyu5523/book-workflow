package com.metacoding.spring.board;

import java.util.*;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;

// TODO : 실습 3 - JpaRepository 상속
@RequiredArgsConstructor
@Repository
public class BoardRepository {

    private final EntityManager em;

    public Board findById(int boardId) {
        return em.find(Board.class, boardId);
    }

    public List<Board> findAll() {
        return em.createQuery("select b from Board b", Board.class).getResultList();
    }

    public void save(Board board) {
        em.persist(board);
    }

    public void delete(Board board) {
        em.remove(board);
    }
}
