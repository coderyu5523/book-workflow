package com.metacoding.spring_oauth.user;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.metacoding.spring_oauth._core.utils.KakaoApiClient;

import lombok.RequiredArgsConstructor;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {

    private final KakaoApiClient kakaoApiClient;
    private final UserRepository userRepository;

    @Value("${kakao.authorize-uri}")
    private String kakaoAuthorizeUri;

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;

    /**
     * 
     * 예시)
     * https://kauth.kakao.com/oauth/authorize
     * ?response_type=code
     * &client_id=${REST_API_KEY}
     * &redirect_uri=${REDIRECT_URI}
     */
    public String 카카오로그인주소() {
        return "";
    }
    
    @Transactional
    public void 카카오로그인(String code) {
        return;
    }
}
