package com.metacoding.spring.user;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.metacoding.spring.core.handler.ex.*;
import com.metacoding.spring.core.util.*;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class UserService {

    private final UserRepository userRepository;

    @Transactional
    public void 회원가입(UserRequest.SaveDTO requestDTO) {
        // 유저네임 중복 체크
        if (userRepository.findByUsername(requestDTO.username()).isPresent()) {
            throw new Exception400("이미 존재하는 유저네임입니다");
        }
        userRepository.save(requestDTO.toEntity());
    }

    public String 로그인(UserRequest.LoginDTO requestDTO) {
        // 유저 조회
        User user = userRepository.findByUsername(requestDTO.username())
                .orElseThrow(() -> new Exception401("유저네임 또는 비밀번호가 일치하지 않습니다"));
        // 비밀번호 검증
        if (!user.getPassword().equals(requestDTO.password())) {
            throw new Exception401("유저네임 또는 비밀번호가 일치하지 않습니다");
        }
        // JWT 발급
        return JwtUtil.create(user);
    }
}
