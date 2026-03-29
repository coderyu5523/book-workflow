# React OIDC 학습용 프론트

카카오 OIDC 로그인을 테스트하기 위한 최소한의 React(Vite) 프로젝트입니다.  
`/` → 로그인, `/result` → 서버에서 받은 토큰으로 글 목록을 보여줍니다.

## 1. 환경 변수

루트에 `.env.local` (또는 `.env`) 파일을 만들고 아래 값을 채워주세요.

```bash
VITE_API_BASE=http://localhost:8080
```

## 2. 실행

```bash
cd frontend
npm install
npm run dev
```

`http://localhost:5173`에서 화면을 확인할 수 있습니다.  
카카오 로그인을 마치면 서버가 `/result`로 리다이렉트하며 토큰/유저 정보를 쿼리로 전달합니다.

## 3. 흐름 요약

1. **LoginPage**  
   - 로그인 버튼 클릭 → 백엔드 `/login/kakao`로 이동
2. **백엔드 콜백**  
   - 카카오 로그인 완료 → 백엔드 `/oauth/callback`  
   - 백엔드가 `/result?token=...&username=...`로 리다이렉트
3. **ResultPage**  
   - 쿼리로 받은 토큰을 `localStorage`에 저장  
   - 토큰을 Authorization 헤더에 담아 `/posts` 요청

학습용으로 예외 처리가 최소화되어 있으니 실제 서비스에서는 보안/UX를 보강해 주세요.
