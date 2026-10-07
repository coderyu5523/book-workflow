package com.metacoding.spring.user;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.spring.core.util.Resp;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class UserController {

    private final UserService userService;

    @PostMapping("/join")
    public ResponseEntity<?> join(@RequestBody UserRequest.SaveDTO requestDTO) {
        // TODO : 실습 5 - 회원가입 엔드포인트
        return null;
    }

    // TODO : 실습 8 - 로그인 엔드포인트
}
