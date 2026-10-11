package com.metacoding.spring.board;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.user.User;
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

    // TODO : 실습 12 - 상세 조회에 fetch 조인과 본인 여부
    public BoardResponse.DetailDTO 게시글상세(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board);
    }

    // TODO : 실습 15 - 로그인 확인 후 회원과 함께 저장
    @Transactional
    public BoardResponse.DTO 게시글추가(BoardRequest.SaveDTO requestDTO) {
        Board savedBoard = boardRepository.save(requestDTO.toEntity()); // DTO -> 엔티티
        return new BoardResponse.DTO(savedBoard); // 저장된 게시글 반환
    }

    // TODO : 실습 17 - 로그인 확인과 소유자 검증
    @Transactional
    public BoardResponse.DTO 게시글수정(Integer boardId, BoardRequest.UpdateDTO requestDTO) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        // 더티체킹
        board.setTitle(requestDTO.title());
        board.setContent(requestDTO.content());
        return new BoardResponse.DTO(board); // 수정된 게시글 반환
    }

    // TODO : 실습 19 - 삭제의 로그인 확인과 소유자 검증
    @Transactional
    public void 게시글삭제(Integer boardId) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        boardRepository.delete(board);
    }
}
