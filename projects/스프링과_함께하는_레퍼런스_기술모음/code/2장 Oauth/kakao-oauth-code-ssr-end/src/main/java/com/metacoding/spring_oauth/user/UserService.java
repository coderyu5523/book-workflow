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
        String encodedRedirect = URLEncoder.encode(kakaoRedirectUri, StandardCharsets.UTF_8);
        return kakaoAuthorizeUri
                + "?response_type=code"
                + "&client_id=" + kakaoClientId
                + "&redirect_uri=" + encodedRedirect
                + "&scope=profile_nickname";
    }

    @Transactional
    public UserResponse.DTO 카카오로그인(String code) {
        KakaoResponse.TokenDTO token = kakaoApiClient.getKakaoToken(code);
        KakaoResponse.KakaoUserDTO kakaoUser = kakaoApiClient.getKakaoUser(token.accessToken());

        String username = kakaoUser.properties().nickname();

        User user = userRepository.findByUsername(username)
                .orElseGet(() -> userRepository.save(
                        User.builder()
                                .username(username)
                                .password(UUID.randomUUID().toString())
                                .email("kakao" + kakaoUser.id() + "@kakao.com")
                                .provider("kakao")
                                .build()));

        return new UserResponse.DTO(user);
    }
}
