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

    public Optional<Board> findByIdJoinUser(int boardId) {
        return em.createQuery("select b from Board b join fetch b.user where b.id = :id", Board.class)
                .setParameter("id", boardId)
                .getResultStream()
                .findFirst();
    }

    public Optional<Board> findByIdJoinUserAndReply(int boardId) {
        return em.createQuery("select b from Board b join fetch b.user left join fetch b.replies where b.id = :id", Board.class)
                .setParameter("id", boardId)
                .getResultStream()
                .findFirst();
    }
}
