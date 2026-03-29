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
import com.metacoding.spring_oauth_oidc._core.utils.KakaoOidcUtil;

import lombok.RequiredArgsConstructor;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final KakaoOidcUtil kakaoOidcUtil;
    private final RestTemplate restTemplate = new RestTemplate();
    private final KakaoApiClient kakaoApiClient;

    @Value("${kakao.authorize-uri}")
    private String kakaoAuthorizeUri;

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;

    /**
     * 카카오 로그인 URL 생성
     * 
     * 예시)
     * https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3F
     * response_type%3Dcode%26
     * client_id%3D200429b30f3909ea3fd28224cddc7b25%26
     * redirect_uri%3Dhttp%253A%252F%252Flocalhost%253A8080%252Foauth%252Fcallback%26
     * scope%3Dopenid%2520profile_nickname%26
     */
    public String 카카오로그인주소() {

        String encodedRedirect = URLEncoder.encode(kakaoRedirectUri, StandardCharsets.UTF_8);
        String scope = URLEncoder.encode("openid profile_nickname", StandardCharsets.UTF_8);
        return kakaoAuthorizeUri
                + "?response_type=code"
                + "&client_id=" + kakaoClientId
                + "&redirect_uri=" + encodedRedirect
                + "&scope=" + scope;
    }

    /**
     * 카카오 로그인 (인가코드 방식)
     */
    @Transactional
    public UserResponse.DTO 카카오로그인(String code) {
        // 인가 코드로 토큰 요청 (access_token + id_token 포함)
        KakaoResponse.TokenDTO tokenDTO = kakaoApiClient.getKakaoToken(code, restTemplate);

        // OIDC 검증
        KakaoOidcResponse resDTO = kakaoOidcUtil.verify(tokenDTO.idToken());

        User user = 카카오유저생성및갱신(resDTO.subject(), resDTO.nickname());

        String jwt = JwtUtil.create(user);
        return new UserResponse.DTO(user, jwt);
    }

    /**
     * 카카오 유저 생성/갱신
     */
    @Transactional
    public User 카카오유저생성및갱신(String providerId, String username) {
        String resolvedEmail = "kakao_" + providerId + "@kakao.com";
        String resolvedUsername = username;

        return userRepository.findByProviderAndProviderId("kakao", providerId)
                .map(user -> {
                    user.updateEmail(resolvedEmail);
                    user.updateUsername(resolvedUsername);
                    return user;
                })
                .orElseGet(() -> userRepository.save(User.builder()
                        .username(resolvedUsername)
                        .password(UUID.randomUUID().toString())
                        .email(resolvedEmail)
                        .provider("kakao")
                        .providerId(providerId)
                        .build()));
    }

}
