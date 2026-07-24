package com.metacoding.spring.reply;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;

import com.metacoding.spring.board.*;

@Import({ ReplyRepository.class, BoardRepository.class })
@DataJpaTest
public class ReplyRepositoryTest {

    @Autowired
    private ReplyRepository replyRepository;
    @Autowired
    private BoardRepository boardRepository;

    @Test
    public void save_test() {
        // given
        Integer boardId = 1;
        Board board = boardRepository.findByIdJoinUser(boardId).get();
        Reply reply = Reply.builder()
                .comment("test")
                .user(board.getUser())
                .board(board)
                .build();
        // when
        replyRepository.save(reply);
        // eye
        System.out.println("boardId : " + reply.getBoard().getId());
        System.out.println("username : " + reply.getBoard().getUser().getUsername());
        System.out.println("comment : " + reply.getComment());
    }

    @Test
    public void delete_test() {
        // given
        Integer replyId = 1;
        Integer boardId = 1;
        Reply reply = replyRepository.findById(replyId).get();

        // when
        replyRepository.delete(reply);

        // eye
        Board board = boardRepository.findById(boardId).get();
        System.out.println("Reply Count : " + board.getReplies().size());
    }
}