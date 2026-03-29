package com.metacoding.spring_oauth_oidc.user;

public class KakaoRequset {

    public record KakaoDTO(
            String code,
            String nonce) {
    }

}
