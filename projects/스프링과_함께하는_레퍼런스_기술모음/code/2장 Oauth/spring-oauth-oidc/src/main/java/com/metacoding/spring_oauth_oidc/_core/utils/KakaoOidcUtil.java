package com.metacoding.spring_oauth_oidc._core.utils;

import java.net.URI;
import java.text.ParseException;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.metacoding.spring_oauth_oidc.user.KakaoOidcResponse;
import com.nimbusds.jose.JOSEException;
import com.nimbusds.jose.crypto.RSASSAVerifier;
import com.nimbusds.jose.jwk.JWK;
import com.nimbusds.jose.jwk.JWKSet;
import com.nimbusds.jose.jwk.RSAKey;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.SignedJWT;

@Component
public class KakaoOidcUtil {

    @Value("${kakao.issuer}")
    private String kakaoIssuer;

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.oidc-jwks-uri}")
    private String kakaoOidcJwksUri;

    /**
     * 🔒 카카오 OIDC 토큰 검증 전체 처리
     */
    public KakaoOidcResponse verify(String idToken) {
        if (idToken == null || idToken.isBlank()) {
            throw new RuntimeException("id_token 값이 비어 있습니다.");
        }

        try {
            // 토큰 파싱
            SignedJWT signedJWT = SignedJWT.parse(idToken);

            // JWKS에서 공개키 가져오기
            RSAKey rsaKey = getKeyFromJwks(signedJWT.getHeader().getKeyID());

            // 서명 검증
            if (!signedJWT.verify(new RSASSAVerifier(rsaKey))) {
                throw new RuntimeException("카카오 id_token 서명 검증 실패");
            }

            // 클레임 추출
            JWTClaimsSet claims = signedJWT.getJWTClaimsSet();

            // 검증 완료 후 응답 생성
            return new KakaoOidcResponse(
                    claims.getSubject(),
                    claims.getStringClaim("nickname"),
                    claims.getExpirationTime().toInstant());

        } catch (ParseException | JOSEException e) {
            throw new RuntimeException("카카오 id_token 검증 중 오류 발생", e);
        }
    }

    /**
     * 🔑 JWKS에서 RSA 공개키 조회
     */
    private RSAKey getKeyFromJwks(String keyId) {
        if (keyId == null || keyId.isBlank()) {
            throw new RuntimeException("id_token 헤더에 kid 값이 없습니다.");
        }

        try {
            // JWKS JSON 가져오기
            JWKSet jwkSet = JWKSet.load(URI.create(kakaoOidcJwksUri).toURL());
            JWK jwk = jwkSet.getKeyByKeyId(keyId);

            if (jwk == null) {
                throw new RuntimeException("kid에 해당하는 공개키를 찾을 수 없습니다: " + keyId);
            }

            if (!(jwk instanceof RSAKey rsaKey)) {
                throw new RuntimeException("kid에 대한 키 타입이 RSA가 아닙니다: " + keyId);
            }

            return rsaKey;

        } catch (Exception e) {
            throw new RuntimeException("JWKS 불러오기 또는 파싱 실패", e);
        }
    }

}
