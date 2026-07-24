package com.metacoding.spring.board;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.core.handler.ex.*;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class BoardService {

    private final BoardRepository boardRepository;

    public List<BoardResponse.DTO> 게시글목록() {
        return boardRepository.findAll().stream()
                .map(BoardResponse.DTO::new)
                .toList();
    }

    public BoardResponse.DetailDTO 게시글상세(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board);
    }

    @Transactional
    public BoardResponse.DTO 게시글추가(BoardRequest.SaveDTO requestDTO) {
        Board board = requestDTO.toEntity(); // DTO -> 엔티티
        boardRepository.save(board);
        return new BoardResponse.DTO(board); // 저장된 게시글 반환
    }

    @Transactional
    public BoardResponse.DTO 게시글수정(Integer boardId, BoardRequest.UpdateDTO requestDTO) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        // 더티 체킹
        board.setTitle(requestDTO.title());
        board.setContent(requestDTO.content());
        return new BoardResponse.DTO(board); // 수정된 게시글 반환
    }

    @Transactional
    public void 게시글삭제(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        boardRepository.delete(board);
    }
}
