package com.metacoding.spring_oauth.user;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Optional;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import com.metacoding.spring_oauth._core.utils.KakaoApiClient;

import lombok.RequiredArgsConstructor;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final KakaoApiClient kakaoApiClient;
    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${kakao.authorize-uri}")
    private String kakaoAuthorizeUri;

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;


    @Transactional
    public UserResponse.DTO 카카오로그인(String code) {
        KakaoResponse.TokenDTO tokenDTO = kakaoApiClient.getKakaoToken(code, restTemplate);
        if (tokenDTO == null || tokenDTO.accessToken() == null) {
            throw new RuntimeException("카카오 Access Token 발급에 실패했습니다.");
        }
        return 로그인토큰(tokenDTO.accessToken());
    }

    public String 카카오로그인주소() {
        String encodedRedirect = URLEncoder.encode(kakaoRedirectUri, StandardCharsets.UTF_8);
        return kakaoAuthorizeUri
                + "?response_type=code"
                + "&client_id=" + kakaoClientId
                + "&redirect_uri=" + encodedRedirect
                + "&scope=profile_nickname";
    }

    private UserResponse.DTO 로그인토큰(String kakaoAccessToken) {
        KakaoResponse.KakaoUserDTO kakaoUser = kakaoApiClient.getKakaoUser(kakaoAccessToken, restTemplate);
        if (kakaoUser == null) {
            throw new RuntimeException("카카오 사용자 정보를 불러올 수 없습니다.");
        }

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
