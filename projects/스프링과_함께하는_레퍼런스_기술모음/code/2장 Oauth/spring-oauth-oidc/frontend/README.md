# React OIDC 학습용 프론트

카카오 OIDC 로그인을 테스트하기 위한 최소한의 React(Vite) 프로젝트입니다.  
`/` → 로그인, `/callback` → ID Token 처리, `/result` → 서버에서 받은 JWT/이메일을 보여줍니다.

## 1. 환경 변수

루트에 `.env.local` (또는 `.env`) 파일을 만들고 아래 값을 채워주세요.

```bash
VITE_API_BASE=http://localhost:8080
VITE_KAKAO_CLIENT_ID=카카오_REST_API_KEY
VITE_KAKAO_REDIRECT_URI=http://localhost:5173/callback
```

> `VITE_KAKAO_REDIRECT_URI`는 카카오 개발자 콘솔에도 동일하게 등록되어 있어야 합니다.

## 2. 실행

```bash
cd frontend
npm install
npm run dev
```

`http://localhost:5173`에서 화면을 확인할 수 있습니다.  
카카오 로그인을 마치면 `/callback` → `/result` 순으로 이동하며 서버(`/oidc`)로부터 받은 JWT를 테이블로 보여줍니다.

## 3. 흐름 요약

1. **LoginPage**  
   - 로그인 버튼 클릭 → `nonce/state` 생성 후 `sessionStorage` 저장  
   - 카카오 로그인 URL로 이동
2. **CallbackPage**  
   - URL Hash에서 `id_token` 추출  
   - 저장한 `nonce/state`와 비교 후 백엔드(`/oidc`)에 전달  
   - 응답을 `sessionStorage`에 저장하고 `/result`로 이동
3. **ResultPage**  
   - Access Token과 이메일을 테이블로 표시  
   - 필요하면 토큰 복사 및 다시 로그인 가능

학습용으로 예외 처리가 최소화되어 있으니 실제 서비스에서는 보안/UX를 보강해 주세요.
