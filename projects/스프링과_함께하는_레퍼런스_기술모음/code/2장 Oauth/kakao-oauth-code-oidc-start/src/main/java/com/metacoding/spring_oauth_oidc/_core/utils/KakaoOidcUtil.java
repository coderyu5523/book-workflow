package com.metacoding.spring_oauth_oidc._core.utils;

import java.net.URI;
import java.text.ParseException;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.metacoding.spring_oauth_oidc.user.KakaoOidcResponse;
import com.nimbusds.jose.JOSEException;
import com.nimbusds.jose.crypto.RSASSAVerifier;
import com.nimbusds.jose.jwk.JWK;
import com.nimbusds.jose.jwk.JWKSet;
import com.nimbusds.jose.jwk.RSAKey;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.SignedJWT;

@Component
public class KakaoOidcUtil {

}
