package com.metacoding.springv3.user;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.metacoding.springv3.core.util.Resp;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class UserController {

    private final UserService userService;

    // 회원가입
    @PostMapping("/join")
    public ResponseEntity<?> join(@Valid @RequestBody UserRequest.SaveDTO requestDTO) {
        userService.회원가입(requestDTO);
        return Resp.ok(null);
    }

    // 로그인 -> JWT 발급
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody UserRequest.LoginDTO requestDTO) {
        String accessToken = userService.로그인(requestDTO);
        return Resp.ok(accessToken);
    }
}
