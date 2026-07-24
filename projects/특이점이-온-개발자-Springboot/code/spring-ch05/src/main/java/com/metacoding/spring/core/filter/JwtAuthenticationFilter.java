package com.metacoding.spring.core.filter;

import com.metacoding.spring.core.util.JwtProvider;
import com.metacoding.spring.user.User;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import lombok.RequiredArgsConstructor;
import java.io.IOException;

// Spring Security 제거 후 인증 필터
// 토큰이 유효하면 로그인 유저를 request attribute("sessionUser")에 담아둔다. (차단하지 않음 - 인가는 인터셉터 담당)
@RequiredArgsConstructor
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    public static final String SESSION_USER = "sessionUser";

    private final JwtProvider jwtProvider;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        String token = jwtProvider.resolveToken(request);

        if (token != null) {
            User sessionUser = jwtProvider.getUser(token); // 유효하지 않으면 null
            if (sessionUser != null) {
                request.setAttribute(SESSION_USER, sessionUser);
            }
        }

        filterChain.doFilter(request, response);
    }
}
