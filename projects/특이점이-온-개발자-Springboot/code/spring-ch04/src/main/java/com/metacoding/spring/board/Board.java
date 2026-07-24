package com.metacoding.spring.board;

import java.sql.Timestamp;

import org.hibernate.annotations.CreationTimestamp;

import com.metacoding.spring.user.User; // 추가
import jakarta.persistence.*;
import lombok.*;

@NoArgsConstructor
@Data
@Entity
@Table(name = "board_tb")
public class Board {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // 자동 증가
    private Integer id;
    private String title;
    private String content;

    @CreationTimestamp // 자동으로 현재 시간 저장
    private Timestamp createdAt;

    @ManyToOne(fetch = FetchType.EAGER) // 다대일 관계 설정
    @JoinColumn(name = "user_id") // 외래 키지정
    private User user; // 객체를 직접 참조

    @Builder
    public Board(Integer id, String title, String content, Timestamp createdAt, User user) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.createdAt = createdAt;
        this.user = user;
    }

}