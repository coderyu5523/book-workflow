package com.metacoding.spring_oauth.user;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final HttpSession session;

    @GetMapping("/")
    public String loginPage() {
        return "login";
    }

    @PostMapping("/login")
    public String login(@ModelAttribute UserRequest.LoginDTO loginDTO) {
        
        System.out.println("로그인: " +loginDTO);
        
        UserResponse.DTO sessionUser = userService.로그인(loginDTO);
        session.setAttribute("sessionUser", sessionUser);
        return "redirect:/post/list";
    }

    @PostMapping("/join")
    public String join(@ModelAttribute UserRequest.JoinDTO joinDTO) {
        UserResponse.DTO sessionUser = userService.회원가입(joinDTO);
        session.setAttribute("sessionUser", sessionUser);
        return "redirect:/post/list";
    }

    @GetMapping("/logout")
    public String logout() {
        session.removeAttribute("sessionUser");
        session.invalidate();
        return "redirect:/";
    }

    @GetMapping("/login/kakao")
    public String redirectToKakao() {
        return "redirect:" + userService.카카오로그인주소();
    }

    @GetMapping("/oauth/callback")
    public String kakaoCallback(
            @RequestParam(value = "code", required = false) String code) {
        if (code == null || code.isBlank()) {
            return "redirect:/login";
        }

        UserResponse.DTO sessionUser = userService.카카오로그인(code);
        session.setAttribute("sessionUser", sessionUser);
        return "redirect:/post/list";
    }
}
