package com.metacoding.spring_oauth_oidc.post;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.metacoding.spring_oauth_oidc._core.utils.Resp;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class PostController {

    private final PostService postService;

    @GetMapping("/posts")
    public ResponseEntity<?> 목록조회() {
        return Resp.ok("게시글 목록 조회", postService.게시글목록());
    }
}
