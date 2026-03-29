package com.metacoding.spring_oauth_oidc._core.filter;

import java.io.IOException;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.metacoding.spring_oauth_oidc._core.utils.JwtProvider;
import com.metacoding.spring_oauth_oidc._core.utils.Resp;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {

    // 요청에서 JWT를 꺼내고 검증하는 역할을 하는 클래스
    private final JwtProvider jwtProvider;

    // 에러 응답(JSON)을 만들기 위한 ObjectMapper
    private final ObjectMapper objectMapper;

    /**
     * JWT 검증을 하지 않아도 되는 요청 경로를 지정
     * - OPTIONS: CORS preflight 요청
     * - /login/kakao: 카카오 로그인 시작
     * - /oauth/callback: 카카오 로그인 콜백
     */
    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        String path = request.getRequestURI();
        return "OPTIONS".equalsIgnoreCase(request.getMethod())
                || "/login/kakao".equals(path)
                || "/oauth/callback".equals(path);
    }

    /**
     * 모든 요청에 대해 한 번만 실행되는 JWT 인증 필터
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain)
            throws ServletException, IOException {
        try {
            // Authorization 헤더에서 JWT 추출 (없거나 잘못되면 예외 발생)
            jwtProvider.verifyFromHeader(request);

            // JWT가 정상이라면 다음 필터 또는 컨트롤러로 요청 전달
            filterChain.doFilter(request, response);

        } catch (Exception e) {
            // JWT가 없거나 유효하지 않은 경우 → 인증 실패
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.setContentType("application/json;charset=UTF-8");

            // 공통 응답 포맷으로 401 에러 반환
            response.getWriter().write(
                    objectMapper.writeValueAsString(
                            new Resp<>(401, e.getMessage(), null)));
        }
    }
}