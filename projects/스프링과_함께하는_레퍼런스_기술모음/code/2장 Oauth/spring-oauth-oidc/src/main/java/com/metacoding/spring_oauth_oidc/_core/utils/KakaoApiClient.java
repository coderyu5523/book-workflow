package com.metacoding.spring_oauth_oidc._core.utils;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import com.metacoding.spring_oauth_oidc.user.KakaoResponse;

@Component
public class KakaoApiClient {

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;

    @Value("${kakao.client-secret:}")
    private String kakaoClientSecret;

    public KakaoResponse.TokenDTO getKakaoToken(String code, RestTemplate restTemplate) {
        HttpEntity<MultiValueMap<String, String>> request = createTokenRequest(code);

        ResponseEntity<KakaoResponse.TokenDTO> response = restTemplate.exchange(
                "https://kauth.kakao.com/oauth/token",
                HttpMethod.POST,
                request,
                KakaoResponse.TokenDTO.class);
        return response.getBody();
    }

    private HttpEntity<MultiValueMap<String, String>> createTokenRequest(String code) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");

        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("grant_type", "authorization_code");
        body.add("client_id", kakaoClientId);
        body.add("redirect_uri", kakaoRedirectUri);
        body.add("code", code);
        if (kakaoClientSecret != null && !kakaoClientSecret.isBlank()) {
            body.add("client_secret", kakaoClientSecret);
        }

        return new HttpEntity<>(body, headers);
    }

}
