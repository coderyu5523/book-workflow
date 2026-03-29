# OIDC 학습용 흐름 정리

학습을 위해 최소한의 로직만 남기고, 카카오 OIDC → 사용자 저장 → 자체 JWT 발급까지의 과정을 정리했습니다.

## 파일별 역할
- `src/main/java/com/metacoding/spring_oauth_oidc/_core/oidc/KakaoOidcJwkProvider.java`  
  카카오 `.well-known/jwks.json`을 받아와 kid에 맞는 공개키를 캐싱합니다. (주석 [1])
- `src/main/java/com/metacoding/spring_oauth_oidc/_core/oidc/KakaoOidcVerifier.java`  
  ID 토큰 서명과 iss/aud/exp/nonce 클레임을 확인합니다. (주석 [2], [3])
- `src/main/java/com/metacoding/spring_oauth_oidc/auth/OidcService.java`  
  검증된 토큰으로 사용자 정보를 저장/갱신하고 우리 JWT를 만듭니다. (주석 [4]~[6])
- `src/main/java/com/metacoding/spring_oauth_oidc/auth/OidcController.java`  
  프론트에서 들어온 `/oidc` 요청을 받아 JSON 응답을 돌려줍니다. (주석 [7])
- `src/main/java/com/metacoding/spring_oauth_oidc/user/SocialUserProcessor.java`  
  카카오 providerId 기준으로 사용자를 찾아 재사용하거나, 없으면 간단히 생성합니다.
- `src/main/java/com/metacoding/spring_oauth_oidc/_core/jwt/JwtProvider.java`  
  Nimbus 라이브러리로 HS256 서명 토큰을 발급하고 검증 도구를 제공합니다.
- `src/main/java/com/metacoding/spring_oauth_oidc/_core/jwt/JwtProperties.java`  
  `jwt.*` 설정(secret, issuer, 만료 시간)을 바인딩합니다.

## 실행 순서 (번호 = 주석)
1. (`KakaoOidcJwkProvider`) 카카오 kid에 맞는 공개키를 캐싱 후 조회
2. (`KakaoOidcVerifier`) 서명을 확인하면서 ID 토큰을 파싱
3. (`KakaoOidcVerifier`) iss/aud/exp/nonce 등 필수 클레임 검증
4. (`OidcService`) 검증이 끝난 사용자 정보를 확보
5. (`OidcService`) DB에서 사용자 생성/갱신
6. (`OidcService`) JwtProvider로 자체 Access Token 발급
7. (`OidcController`) JSON 응답으로 토큰과 이메일 전달

## 최소 구현 철학
- Spring Security, 복잡한 예외 처리, Refresh Token, 프론트 인터셉터는 모두 생략
- RestTemplate, H2 인메모리 DB 등 기본 도구만 활용
- 모든 예외는 `RuntimeException`으로 단순하게 던져 흐름을 명확히 확인
- 주석의 숫자를 따라가며 OIDC → 사용자 저장 → JWT 발급 순서를 직관적으로 확인

이 문서를 기준으로 추가 기능(Refresh Token, 보안 강화 등)을 붙이기 전에 전체 흐름을 먼저 익히는 것을 목표로 합니다.
