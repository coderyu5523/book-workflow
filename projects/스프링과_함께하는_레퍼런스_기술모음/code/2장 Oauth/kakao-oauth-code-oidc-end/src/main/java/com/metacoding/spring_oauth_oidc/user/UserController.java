package com.metacoding.spring_oauth_oidc.user;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.metacoding.spring_oauth_oidc._core.utils.Resp;

import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/login/kakao")
    public String redirectToKakao() {
        return "redirect:" + userService.카카오로그인주소();
    }

    // 카카오 로그인 콜백 (JWT 발급)
    @GetMapping("/oauth/callback")
    @ResponseBody
    public ResponseEntity<?> kakaoCallback(@RequestParam("code") String code) {
        UserResponse.DTO resDTO = userService.카카오로그인(code);
        return Resp.ok("카카오 로그인 성공", resDTO);
    }
}
