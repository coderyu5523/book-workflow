package com.metacoding.spring.user;

import java.sql.Timestamp;

import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.*;
import lombok.*;

@NoArgsConstructor
@Data
@Entity
@Table(name = "user_tb")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // 자동 증가
    private Integer id;
    @Column(unique = true)
    private String username;
    private String password;
    private String email;

    @CreationTimestamp // 자동으로 현재 시간 저장
    private Timestamp createdAt;

    // 객체 생성을 위한 생성자
    @Builder
    public User(Integer id, String username, String password,
            String email, Timestamp createdAt) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.email = email;
        this.createdAt = createdAt;
    }
}