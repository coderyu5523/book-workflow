package com.metacoding.spring.reply;

import java.sql.Timestamp;

import org.hibernate.annotations.CreationTimestamp;

import com.metacoding.spring.board.Board;
import com.metacoding.spring.user.User;

import jakarta.persistence.*;
import lombok.*;

@NoArgsConstructor
@Data
@Entity
@Table(name = "reply_tb")
public class Reply {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String comment;

    @ManyToOne(fetch = FetchType.LAZY) // 외래키 필드
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne(fetch = FetchType.LAZY) // 외래키 필드
    @JoinColumn(name = "board_id")
    private Board board;

    @CreationTimestamp
    private Timestamp createdAt;

    @Builder
    public Reply(Integer id, String comment, User user, Board board,
            Timestamp createdAt) {
        this.id = id;
        this.comment = comment;
        this.user = user;
        this.board = board;
        this.createdAt = createdAt;
    }

}