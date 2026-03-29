package com.metacoding.spring_oauth_oidc._core.utils;

import java.text.ParseException;
import java.util.Date;

import com.metacoding.spring_oauth_oidc.user.User;
import com.nimbusds.jose.JOSEException;
import com.nimbusds.jose.JWSAlgorithm;
import com.nimbusds.jose.JWSHeader;
import com.nimbusds.jose.crypto.MACSigner;
import com.nimbusds.jose.crypto.MACVerifier;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.SignedJWT;

/**
 * JwtUtil
 * - OAuth/OIDC 로그인 성공 "이후" 우리 서비스에서 사용할 JWT를 만든다.
 * - 이후 요청에서 넘어온 JWT를 검증해서 "누가 요청했는지" 복원한다.
 */
public class JwtUtil {

    // HTTP 헤더 이름 (Authorization: Bearer {JWT})
    public static final String HEADER = "Authorization";

    // Authorization 헤더에서 JWT 앞에 붙는 접두어
    public static final String TOKEN_PREFIX = "Bearer ";

    // HS256 서명용 대칭키(최소 32바이트 이상 권장)
    // 운영에서는 .env / 환경변수로 빼서 관리해야 한다.
    private static final String SECRET = "metacoding-secret-key-should-be-long";

    // 만료 시간(7일) = 밀리초 단위
    private static final long EXPIRATION_TIME = 1000L * 60 * 60 * 24 * 7;

    /**
     * JWT 생성
     * - 로그인 성공 후 user 정보를 기반으로 "우리 서비스용 토큰"을 만든다.
     * - 토큰에는 username(sub), 발급시간(iat), 만료시간(exp), 사용자 id(claim)를 담는다.
     */
    public static String create(User user) {
        try {
            // 1) Payload(Claims) 구성: 토큰에 넣을 사용자 정보와 시간 정보
            JWTClaimsSet claims = new JWTClaimsSet.Builder()
                    .subject(user.getUsername()) // sub: 이 토큰의 주인(대표 식별자)
                    .issueTime(new Date()) // iat: 발급 시간
                    .expirationTime(new Date(System.currentTimeMillis() + EXPIRATION_TIME)) // exp: 만료 시간
                    .claim("id", user.getId()) // 우리 서비스에서 쓰는 사용자 PK
                    .build();

            // 2) Header + Claims 결합 (HS256 = 대칭키 서명)
            SignedJWT signedJWT = new SignedJWT(
                    new JWSHeader(JWSAlgorithm.HS256),
                    claims);

            // 3) SECRET으로 서명 → 위조 방지
            signedJWT.sign(new MACSigner(SECRET));

            // 4) Authorization 헤더에 바로 넣을 수 있게 "Bearer "를 붙여 반환
            return TOKEN_PREFIX + signedJWT.serialize();

        } catch (JOSEException e) {
            throw new RuntimeException("JWT 생성 실패", e);
        }
    }

    /**
     * JWT 검증
     * - 클라이언트가 보낸 JWT가 위조되지 않았는지(서명) 확인한다.
     * - 검증에 성공하면 토큰 안의 정보로 User(인증 주체)를 복원한다.
     */
    public static User verify(String jwt) {
        try {
            // 1) 문자열 JWT → SignedJWT 파싱
            SignedJWT signedJWT = SignedJWT.parse(jwt);

            // 2) 서명 검증: SECRET으로 검증 실패하면 위조/변조 토큰
            if (!signedJWT.verify(new MACVerifier(SECRET))) {
                throw new RuntimeException("JWT 서명 검증 실패");
            }

            // 3) Claims(Payload) 추출
            JWTClaimsSet claims = signedJWT.getJWTClaimsSet();

            // 4) 우리가 create()에서 넣어둔 값들 꺼내기
            Integer id = claims.getIntegerClaim("id");
            String username = claims.getSubject();

            // 5) 토큰 정보로 User 복원 (필요하면 여기서 DB 조회를 추가할 수도 있다)
            return User.builder()
                    .id(id)
                    .username(username)
                    .build();

        } catch (ParseException | JOSEException e) {
            throw new RuntimeException("JWT 검증 실패", e);
        }
    }
}