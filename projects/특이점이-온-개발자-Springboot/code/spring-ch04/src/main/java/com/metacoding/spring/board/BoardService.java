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

    public BoardResponse.DetailDTO 게시글상세(Integer boardId, User loginUser) {
        Board board = boardRepository.findByIdJoinUser(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        return new BoardResponse.DetailDTO(board, loginUser);
    }

    @Transactional
    public BoardResponse.DTO 게시글추가(BoardRequest.SaveDTO requestDTO, User loginUser) {
        Board board = requestDTO.toEntity(loginUser); // DTO -> 엔티티 (작성자 연결)
        boardRepository.save(board);
        return new BoardResponse.DTO(board);
    }

    @Transactional
    public BoardResponse.DTO 게시글수정(Integer boardId, BoardRequest.UpdateDTO requestDTO, Integer loginUserId) {
        Board board = boardRepository.findByIdJoinUser(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        // 작성자 본인 확인 (Integer 는 equals 로 비교)
        if (!board.getUser().getId().equals(loginUserId)) {
            throw new Exception403("게시글을 수정할 권한이 없습니다");
        }
        board.setTitle(requestDTO.title()); // 더티 체킹
        board.setContent(requestDTO.content());
        return new BoardResponse.DTO(board);
    }

    @Transactional
    public void 게시글삭제(Integer boardId, Integer loginUserId) {
        Board board = boardRepository.findByIdJoinUser(boardId)
                .orElseThrow(() -> new Exception404("게시글을 찾을 수 없습니다"));
        if (!board.getUser().getId().equals(loginUserId)) {
            throw new Exception403("게시글을 삭제할 권한이 없습니다");
        }
        boardRepository.delete(board);
    }
}
