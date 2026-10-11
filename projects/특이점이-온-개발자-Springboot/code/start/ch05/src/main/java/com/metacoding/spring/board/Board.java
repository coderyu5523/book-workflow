package com.metacoding.spring.board;

import java.time.LocalDateTime;
import java.util.*;

import org.hibernate.annotations.CreationTimestamp;

import com.metacoding.spring.reply.Reply;
import com.metacoding.spring.user.User;

import jakarta.persistence.*;
import lombok.*;

@NoArgsConstructor
@Data
@Entity
@Table(name = "board_tb")
public class Board {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String title;
    private String content;

    @CreationTimestamp
    private LocalDateTime createdAt;

    // TODO : 실습 1 - 댓글 목록 추가와 회원 필드 수정
    @ManyToOne
    private User user;

    @Builder
    public Board(Integer id, String title, String content,
            LocalDateTime createdAt, User user) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.createdAt = createdAt;
        this.user = user;
    }

}