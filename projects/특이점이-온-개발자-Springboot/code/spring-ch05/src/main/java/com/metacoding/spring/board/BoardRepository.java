package com.metacoding.spring.board;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface BoardRepository extends JpaRepository<Board, Integer> {

    @Query("select b from Board b join fetch b.user where b.id = :boardId")
    Optional<Board> findByIdJoinUser(@Param("boardId") Integer boardId);

    @Query("select b from Board b join fetch b.user "
            + "left join fetch b.replies where b.id = :boardId")
    Optional<Board> findByIdJoinUserAndReply(@Param("boardId") Integer boardId);
}
