package com.metacoding.springv3.core.util;

import at.favre.lib.crypto.bcrypt.BCrypt;
import org.springframework.stereotype.Component;

// Spring Security 제거 후 BCrypt 대체 (at.favre.lib:bcrypt)
// verifyer().verify() 는 non-strict 라 기존 $2y$ 해시도 검증 가능
@Component
public class PasswordEncoder {

    private static final int COST = 10; // 기존 BCryptPasswordEncoder 기본 strength 와 동일

    public String encode(String rawPassword) {
        return BCrypt.withDefaults().hashToString(COST, rawPassword.toCharArray());
    }

    public boolean matches(String rawPassword, String encodedPassword) {
        return BCrypt.verifyer().verify(rawPassword.toCharArray(), encodedPassword).verified;
    }
}
