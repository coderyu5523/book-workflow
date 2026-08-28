package com.metacoding.spring.core.util;

import java.time.Duration;
import java.time.Instant;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.metacoding.spring.user.User;

// JWT 토큰 생성/검증 (roles 없음 - v1 User는 권한 개념이 없다)
public class JwtUtil {
    public static final String HEADER = "Authorization";
    public static final String TOKEN_PREFIX = "Bearer ";
    // 실제 서비스에서는 외부 설정으로 분리한다
    public static final String SECRET = "메타코딩시크릿키";
    public static final Duration EXPIRATION_TIME = Duration.ofDays(7);

    // 토큰 생성
    public static String create(User user) {
        String jwt = JWT.create()
                .withSubject(user.getUsername())
                .withExpiresAt(Instant.now().plus(EXPIRATION_TIME))
                .withClaim("id", user.getId())
                .sign(Algorithm.HMAC512(SECRET));
        return TOKEN_PREFIX + jwt;
    }

    // 토큰 검증 후 User 복원
    public static User verify(String jwt) {
        DecodedJWT decodedJWT = JWT.require(Algorithm.HMAC512(SECRET))
                .build()
                .verify(jwt);
        Integer userId = decodedJWT.getClaim("id").asInt();
        String username = decodedJWT.getSubject();
        return User.builder()
                .id(userId)
                .username(username)
                .build();
    }
}
