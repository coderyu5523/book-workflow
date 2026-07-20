package com.metacoding.springv3.core.util;

import java.util.Date;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.metacoding.springv3.user.User;

// JWT 토큰 생성/검증 (roles 없음 - v1 User는 권한 개념이 없다)
public class JwtUtil {
    public static final String HEADER = "Authorization";
    public static final String TOKEN_PREFIX = "Bearer ";
    public static final String SECRET = "메타코딩시크릿키"; // 실제 서비스에선 외부 설정으로 분리
    public static final Long EXPIRATION_TIME = 1000L * 60 * 60 * 24 * 7; // 7일

    // 토큰 생성
    public static String create(User user) {
        String jwt = JWT.create()
                .withSubject(user.getUsername())
                .withExpiresAt(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
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
