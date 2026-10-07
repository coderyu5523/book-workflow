package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.core.handler.ex.*;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class BoardService {

    private final BoardRepository boardRepository;

    // TODO : 실습 5 - 주고받는 타입을 DTO로, 없으면 예외
    public List<Board> 게시글목록() {
        return boardRepository.findAll();
    }

    // TODO : 실습 5 - 주고받는 타입을 DTO로, 없으면 예외
    public Board 게시글상세(Integer boardId) {
        return boardRepository.findById(boardId);
    }

    // TODO : 실습 5 - 주고받는 타입을 DTO로, 없으면 예외
    @Transactional
    public Board 게시글추가(Board requestBoard) {
        boardRepository.save(requestBoard);
        return requestBoard; // 저장된 게시글 반환 (REST)
    }

    // TODO : 실습 5 - 주고받는 타입을 DTO로, 없으면 예외
    @Transactional
    public void 게시글삭제(Integer boardId) {
        Board board = boardRepository.findById(boardId);
        boardRepository.delete(board);
    }

    // TODO : 실습 5 - 주고받는 타입을 DTO로, 없으면 예외
    @Transactional
    public Board 게시글수정(Integer boardId, Board requestBoard) {
        Board board = boardRepository.findById(boardId);
        // 더티체킹
        board.setTitle(requestBoard.getTitle());
        board.setContent(requestBoard.getContent());
        return board; // 수정된 게시글 반환 (REST)
    } // 트랜잭션 종료시 flush()
}
