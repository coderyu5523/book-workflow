package com.metacoding.spring_oauth_oidc.user;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.metacoding.spring_oauth_oidc._core.utils.Resp;

import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @Value("${front.redirect-uri}")
    private String frontRedirectUri;

    @GetMapping("/login/kakao")
    public String redirectToKakao() {
        return "redirect:" + userService.카카오로그인주소();
    }

    // 카카오 로그인 콜백 (JWT 발급)
    // @GetMapping("/oauth/callback")
    // @ResponseBody
    // public ResponseEntity<?> kakaoCallback(@RequestParam("code") String code) {
    // UserResponse.DTO resDTO = userService.카카오로그인(code);
    // return Resp.ok("카카오 로그인 성공", resDTO);
    // }

    // 카카오 로그인 콜백 (프론트로 리다이렉트)
    @GetMapping("/oauth/callback")
    public String kakaoCallbackRedirect(@RequestParam("code") String code, HttpServletResponse response) {

        // 1) code로 카카오 처리 + 우리 JWT 발급(네가 이미 구현한 로직)
        UserResponse.DTO resDTO = userService.카카오로그인(code);
        String accessJwt = resDTO.token(); // "Bearer " 없는 순수 토큰 권장

        // 2) HttpOnly 쿠키로 심기 (브라우저 JS에서 접근 불가)
        ResponseCookie cookie = ResponseCookie.from("access_token", accessJwt)
                .httpOnly(true)
                .secure(true) // https 운영에서 true (로컬 http면 false로 테스트)
                .sameSite("Lax") // 크로스사이트면 "None" + secure(true) 필요
                .path("/")
                .maxAge(Duration.ofMinutes(30))
                .build();

        response.addHeader(HttpHeaders.SET_COOKIE, cookie.toString());

        // 3) 프론트로는 "로그인 완료" 화면만 이동(토큰 전달 X)
        return "redirect:" + frontRedirectUri + "/auth/success";
    }
}
