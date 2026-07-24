package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Repository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class BoardRepository {

    private final EntityManager em;

    public Optional<Board> findById(int boardId) {
        return Optional.ofNullable(em.find(Board.class, boardId));
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
