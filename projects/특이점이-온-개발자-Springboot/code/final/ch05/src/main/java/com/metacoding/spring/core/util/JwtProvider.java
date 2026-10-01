package com.metacoding.spring.core.util;

import org.springframework.stereotype.Component;
import com.metacoding.spring.user.User;
import jakarta.servlet.http.HttpServletRequest;

@Component
public class JwtProvider {

    // 요청 헤더에서 토큰 추출
    public String resolveToken(HttpServletRequest request) {
        String bearerToken = request.getHeader(JwtUtil.HEADER);
        if (bearerToken != null && bearerToken.startsWith(JwtUtil.TOKEN_PREFIX)) {
            return bearerToken.replace(JwtUtil.TOKEN_PREFIX, "");
        }
        return null;
    }

    // 토큰을 검증하고 User 반환 (유효하지 않으면 null)
    public User getUser(String token) {
        try {
            return JwtUtil.verify(token);
        } catch (Exception e) {
            return null;
        }
    }
}
