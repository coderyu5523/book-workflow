package com.metacoding.spring.board;

import java.util.*;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;
import jakarta.persistence.EntityManager;

@Import(BoardRepository.class)
@DataJpaTest
public class BoardRepositoryTest {

    @Autowired
    private BoardRepository boardRepository;

    @Autowired
    private EntityManager em;

    @Test
    public void findById_test() {
        // TODO : 실습 5 - 한 건 조회
    }

    @Test
    public void findAll_test() {
        // TODO : 실습 6 - 전체 조회
    }

    @Test
    public void save_test() {
        // TODO : 실습 7 - 저장
    }

    @Test
    public void update_test() {
        // TODO : 실습 8 - 수정과 더티체킹
    }

    @Test
    public void delete_test() {
        // TODO : 실습 9 - 삭제
    }
}
