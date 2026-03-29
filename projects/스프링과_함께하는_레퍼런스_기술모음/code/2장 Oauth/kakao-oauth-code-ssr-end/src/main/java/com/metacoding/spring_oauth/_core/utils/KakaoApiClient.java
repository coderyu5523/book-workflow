package com.metacoding.spring_oauth._core.utils;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import com.metacoding.spring_oauth.user.KakaoResponse;

@Component
public class KakaoApiClient {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.client-secret:}")
    private String kakaoClientSecret;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;

    @Value("${kakao.token-uri}")
    private String kakaoTokenUri;

    @Value("${kakao.user-info-uri}")
    private String kakaoUserInfoUri;

    public KakaoResponse.TokenDTO getKakaoToken(String code) {
        HttpEntity<MultiValueMap<String, String>> request = createTokenRequest(code);
        ResponseEntity<KakaoResponse.TokenDTO> response = restTemplate.exchange(
                kakaoTokenUri,
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
        body.add("client_secret", kakaoClientSecret);

        return new HttpEntity<>(body, headers);
    }

    public KakaoResponse.KakaoUserDTO getKakaoUser(String accessToken) {
        HttpEntity<MultiValueMap<String, String>> request = createUserRequest(accessToken);

        ResponseEntity<KakaoResponse.KakaoUserDTO> response = restTemplate.exchange(
                kakaoUserInfoUri,
                HttpMethod.GET,
                request,
                KakaoResponse.KakaoUserDTO.class);
        return response.getBody();
    }

    private HttpEntity<MultiValueMap<String, String>> createUserRequest(String accessToken) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");
        headers.add("Authorization", "Bearer " + accessToken);

        return new HttpEntity<>(headers);
    }
}