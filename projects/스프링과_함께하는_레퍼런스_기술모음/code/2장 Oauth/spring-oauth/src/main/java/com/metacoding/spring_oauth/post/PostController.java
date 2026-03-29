package com.metacoding.spring_oauth.post;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.metacoding.spring_oauth.user.UserResponse;

import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class PostController {

    private final PostService postService;
    private final HttpSession session;

    @GetMapping("/post/list")
    public String list(Model model) {
        UserResponse.DTO sessionUser = (UserResponse.DTO) session.getAttribute("sessionUser");
        model.addAttribute("user", sessionUser);
        model.addAttribute("posts", postService.게시글목록());
        return "list";
    }
}
