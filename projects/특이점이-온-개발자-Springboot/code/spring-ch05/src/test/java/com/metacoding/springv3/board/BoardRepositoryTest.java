package com.metacoding.springv3.board;

import java.util.List;
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
        // given
        int id = 2;
        // when
        Board board = boardRepository.findById(id).get();
        // eye
        System.out.println("=======================");
        System.out.println("Board Title : " + board.getTitle());
        System.out.println("Board Content : " + board.getContent());
    }

    @Test
    public void findAll_test() {
        // given

        // when
        List<Board> boards = boardRepository.findAll();
        // eye
        System.out.println("=======================");
        System.out.println("Board Count : " + boards.size());
        System.out.println("Board 1 title :" + boards.get(0).getTitle());
        System.out.println("Board 2 content :" + boards.get(1).getContent());
    }

    @Test
    public void save_test() {
        // given
        Board board = Board.builder()
                .title("title3")
                .content("content3")
                .build();
        // when
        boardRepository.save(board);
        // eye
        List<Board> boards = boardRepository.findAll();
        System.out.println("=======================");
        System.out.println("Board Count : " + boards.size());
        System.out.println("Board ID: " + boards.get(2).getId());
        System.out.println("Board Title: " + boards.get(2).getTitle());
        System.out.println("Board Content: " + boards.get(2).getContent());
    }

    @Test
    public void update_test() {
        // given
        int id = 2;
        // when
        Board board = boardRepository.findById(id).get();
        board.setTitle("title-update");
        board.setContent("Update-test");
        em.flush();
        // eye
        Board result = boardRepository.findById(id).get();
        System.out.println("=======================");
        System.out.println("Board title : " + result.getTitle());
        System.out.println("Board content : " + result.getContent());
    }

    @Test
    public void delete_test() {
        // given
        int id = 2;
        Board board = boardRepository.findById(id).get();
        // when
        boardRepository.delete(board);
        em.flush();
        // eye
        List<Board> boards = boardRepository.findAll();
        System.out.println("=======================");
        System.out.println("Board count : " + boards.size());
    }

    @Test
    public void findByIdEager_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findById(id).get();
        // eye
        System.out.println("=======================");
        System.out.println("Board ID : " + board.getId());
    }

    @Test
    public void findByIdLazy_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findById(id).get();
        // eye
        System.out.println("=======================");
        System.out.println("Board ID : " + board.getId());
    }

    @Test
    public void findByIdLazyLoading_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findById(id).get();
        // eye
        System.out.println("=======================");
        System.out.println("Board ID : " + board.getId());
        System.out.println("=======================");
        System.out.println("username : " + board.getUser().getUsername());
    }

    @Test
    public void findByIdJoinUser_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findByIdJoinUser(id).get();
        // eye
        System.out.println("=======================");
        System.out.println("Board ID : " + board.getId());
        System.out.println("username : " + board.getUser().getUsername());
    }

    @Test
    public void findByIdJoinUserAndReply_test() {
        // given
        int id = 1;
        // when
        Board board = boardRepository.findByIdJoinUserAndReply(id).get();
        // eye
        System.out.println("=======================");
        System.out.println("Board ID : " + board.getId());
        System.out.println("username : " + board.getUser().getUsername());
        System.out.println("Reply : " + board.getReplies().get(1).getComment());
    }
}
