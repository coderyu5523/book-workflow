package com.metacoding.spring.board;

import java.util.Optional;

import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;

public interface BoardRepository extends JpaRepository<Board, Integer> {

    // TODO : 실습 9 - 회원을 함께 가져오는 조회
}
