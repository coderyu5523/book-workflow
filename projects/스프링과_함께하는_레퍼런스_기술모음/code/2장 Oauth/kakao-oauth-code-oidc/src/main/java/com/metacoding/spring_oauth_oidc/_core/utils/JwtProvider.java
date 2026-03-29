package com.metacoding.spring_oauth_oidc._core.utils;

import org.springframework.stereotype.Component;

import com.metacoding.spring_oauth_oidc.user.User;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
public class JwtProvider {

    /**
     * 요청 헤더에서 JWT를 꺼내 바로 검증하고 User 복원
     */
    public User verifyFromHeader(HttpServletRequest request) {
        String token = resolveToken(request);
        if (token == null || token.isBlank()) {
            throw new RuntimeException("Authorization 헤더에 Bearer 토큰이 없습니다.");
        }
        return JwtUtil.verify(token);
    }

    /**
     * 요청 헤더에서 JWT 토큰 추출
     */
    public String resolveToken(HttpServletRequest request) {
        String bearerToken = request.getHeader(JwtUtil.HEADER);
        if (bearerToken != null && bearerToken.startsWith(JwtUtil.TOKEN_PREFIX)) {
            return bearerToken.substring(JwtUtil.TOKEN_PREFIX.length());
        }
        return null;
    }

}