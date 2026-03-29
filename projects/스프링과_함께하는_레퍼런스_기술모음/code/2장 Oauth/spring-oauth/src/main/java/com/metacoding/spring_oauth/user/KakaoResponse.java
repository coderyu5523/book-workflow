package com.metacoding.spring_oauth.user;

import java.sql.Timestamp;

import com.fasterxml.jackson.annotation.JsonProperty;

public class KakaoResponse {

        public static record KakaoUserDTO(
                        Long id,
                        @JsonProperty("connected_at") Timestamp connectedAt,
                        Properties properties) {
        }

        public static record Properties(
                        String nickname) {
        }

        public static record TokenDTO(
                        @JsonProperty("token_type") String tokenType,
                        @JsonProperty("access_token") String accessToken,
                        @JsonProperty("expires_in") Long expiresIn,
                        @JsonProperty("refresh_token") String refreshToken,
                        @JsonProperty("refresh_token_expires_in") Long refreshTokenExpiresIn,
                        String scope) {
        }
}
