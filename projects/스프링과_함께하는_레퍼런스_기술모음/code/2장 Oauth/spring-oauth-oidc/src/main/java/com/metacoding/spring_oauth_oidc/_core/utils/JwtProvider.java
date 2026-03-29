package com.metacoding.spring_oauth_oidc._core.utils;

import org.springframework.stereotype.Component;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
public class JwtProvider {

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

    /**
     * 단순 유효성 체크 (true / false)
     */
    public boolean validateToken(String token) {
        if (token == null || token.isBlank()) {
            return false;
        }
        try {
            JwtUtil.verify(token);
            return true;
        } catch (Exception e) {
            log.warn("유효하지 않은 토큰: {}", e.getMessage());
            return false;
        }
    }
}
