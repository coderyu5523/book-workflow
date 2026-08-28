package com.metacoding.spring.board;

import java.util.*;

import org.springframework.stereotype.Service;

import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class BoardService {

    private final BoardRepository boardRepository;

    public List<Board> 게시글목록() {
        return boardRepository.findAll();
    }

    public Board 게시글상세(Integer boardId) {
        return boardRepository.findById(boardId);
    }

    @Transactional
    public Board 게시글추가(BoardRequest.SaveDTO requestDTO) {
        Board board = new Board();
        board.setTitle(requestDTO.title());
        board.setContent(requestDTO.content());
        boardRepository.save(board);
        return board; // 저장된 게시글 반환 (REST)
    }

    @Transactional
    public void 게시글삭제(Integer boardId) {
        Board board = boardRepository.findById(boardId);
        boardRepository.delete(board);
    }

    @Transactional
    public Board 게시글수정(Integer boardId, BoardRequest.UpdateDTO requestDTO) {
        Board board = boardRepository.findById(boardId);
        // 더티 체킹
        board.setTitle(requestDTO.title());
        board.setContent(requestDTO.content());
        return board; // 수정된 게시글 반환 (REST)
    } // 트랜잭션 종료시 flush()
}
