package com.metacoding.springv3.core.interceptor;

import com.metacoding.springv3.core.handler.ex.Exception401;
import com.metacoding.springv3.user.User;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.HandlerInterceptor;

// 인증 인터셉터
// 읽기(GET)와 CORS preflight(OPTIONS)는 공개, 쓰기(POST/PUT/DELETE)는 로그인 필요
public class AuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String method = request.getMethod();
        if ("GET".equalsIgnoreCase(method) || "OPTIONS".equalsIgnoreCase(method)) {
            return true;
        }

        User sessionUser = (User) request.getAttribute("sessionUser");
        if (sessionUser == null) {
            // 던지면 GlobalExceptionHandler가 JSON 응답으로 변환
            throw new Exception401("로그인이 필요합니다");
        }
        return true;
    }
}
