package com.metacoding.spring_oauth_oidc.user;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import com.metacoding.spring_oauth_oidc._core.utils.JwtUtil;
import com.metacoding.spring_oauth_oidc._core.utils.KakaoApiClient;

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
     * &scope=openid profile_nickname
     */
    public String 카카오로그인주소() {
        return "";
    }

    /**
     * 카카오 로그인 (인가코드 방식)
     */
    @Transactional
    public UserResponse.DTO 카카오로그인(String code) {
        // 인가 코드로 토큰 요청 (access_token + id_token 포함)
        KakaoResponse.TokenDTO tokenDTO = kakaoApiClient.getKakaoToken(code);
        System.out.println("tokenDTO = " + tokenDTO);
        return null;
    }

    /**
     * 카카오 유저 생성/갱신
     */
    @Transactional
    public User 카카오생성및갱신() {
        return null;
    }

}
