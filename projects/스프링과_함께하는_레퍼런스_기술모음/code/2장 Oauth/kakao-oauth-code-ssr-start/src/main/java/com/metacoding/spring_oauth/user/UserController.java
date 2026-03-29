package com.metacoding.spring_oauth.user;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final HttpSession session;

    @GetMapping("/")
    public String loginPage() {
        return "login";
    }

    @GetMapping("/logout")
    public String logout() {
        session.removeAttribute("sessionUser");
        session.invalidate();
        return "redirect:/";
    }

    @GetMapping("/login/kakao")
    public String redirectToKakao() {
        return "redirect:/";
    }

    @GetMapping("/oauth/callback")
    public String kakaoCallback() {
        return "redirect:/";
    }
}
