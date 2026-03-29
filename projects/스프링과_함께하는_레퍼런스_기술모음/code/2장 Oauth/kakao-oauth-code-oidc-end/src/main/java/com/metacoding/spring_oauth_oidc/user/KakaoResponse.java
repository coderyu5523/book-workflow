package com.metacoding.spring_oauth_oidc.user;

import com.fasterxml.jackson.annotation.JsonProperty;

public class KakaoResponse {

        // 토큰 응답 DTO (/oauth/token)
        public record TokenDTO(
                        @JsonProperty("token_type") String tokenType,
                        @JsonProperty("access_token") String accessToken,
                        @JsonProperty("expires_in") Long expiresIn,
                        @JsonProperty("refresh_token") String refreshToken,
                        @JsonProperty("refresh_token_expires_in") Long refreshTokenExpiresIn,

                        @JsonProperty("id_token") String idToken, // OIDC용 ID 토큰
                        String scope) {
        }

}