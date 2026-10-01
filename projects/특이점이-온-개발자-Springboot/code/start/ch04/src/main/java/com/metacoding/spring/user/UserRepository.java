package com.metacoding.spring.user;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Integer> {

    // TODO : 실습 1 - 유저네임으로 조회
}
