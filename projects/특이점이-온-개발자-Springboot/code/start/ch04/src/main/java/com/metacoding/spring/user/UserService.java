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
    public UserResponse.DTO 회원가입(UserRequest.SaveDTO requestDTO) {
        // TODO : 실습 5 - 회원가입
        return null;
    }

    // TODO : 실습 8 - 로그인
}
