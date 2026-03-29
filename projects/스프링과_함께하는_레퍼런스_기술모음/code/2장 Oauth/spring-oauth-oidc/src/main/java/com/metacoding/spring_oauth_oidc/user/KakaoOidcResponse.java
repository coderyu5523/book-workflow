package com.metacoding.spring_oauth_oidc.user;

import java.time.Instant;

public record KakaoOidcResponse(
                String subject,
                String nickname,
                Instant expiresAt) {

}
