import { useMemo, useState } from 'react';
import { buildKakaoAuthorizeUrl } from '../api/oidcClient.js';

const KAKAO_CLIENT_ID = import.meta.env.VITE_KAKAO_CLIENT_ID ?? '';
const KAKAO_REDIRECT_URI =
  import.meta.env.VITE_KAKAO_REDIRECT_URI ?? `${window.location.origin}/callback`;

const STORAGE_KEYS = {
  nonce: 'oidc_nonce',
  state: 'oidc_state',
  result: 'oidc_result'
};

function randomString(size = 32) {
  if (window.crypto?.getRandomValues) {
    const bytes = new Uint8Array(size);
    window.crypto.getRandomValues(bytes);
    return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
  }
  return [...Array(size)].map(() => Math.random().toString(16).slice(2)).join('').slice(0, size);
}

function LoginPage() {
  const [error, setError] = useState('');
  const [localMessage, setLocalMessage] = useState('');

  const kakaoInfo = useMemo(
    () => ({
      clientId: KAKAO_CLIENT_ID,
      redirectUri: KAKAO_REDIRECT_URI
    }),
    []
  );

  const handleKakaoLogin = () => {
    if (!kakaoInfo.clientId) {
      setError('KAKAO REST API 키(VITE_KAKAO_CLIENT_ID)가 설정되어 있지 않습니다.');
      return;
    }

    const nonce = randomString(24);
    const state = randomString(24);

    sessionStorage.setItem(STORAGE_KEYS.nonce, nonce);
    sessionStorage.setItem(STORAGE_KEYS.state, state);
    sessionStorage.removeItem(STORAGE_KEYS.result);

    const authorizeUrl = buildKakaoAuthorizeUrl({
      clientId: kakaoInfo.clientId,
      redirectUri: kakaoInfo.redirectUri,
      nonce,
      state
    });

    window.location.href = authorizeUrl;
  };

  const handleLocalSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const username = formData.get('username');
    const password = formData.get('password');

    if (!username || !password) {
      setLocalMessage('아이디와 비밀번호를 모두 입력해주세요.');
      return;
    }

    setLocalMessage(
      `입력한 값은 전송되지 않습니다. (username=${username}, password=${'*'.repeat(
        password.length
      )})`
    );
    event.currentTarget.reset();
  };

  return (
    <main>
      <h1>로그인 페이지</h1>
      <p className="notice">OIDC 학습용 화면입니다. 카카오 로그인을 진행하세요.</p>

      <section style={{ maxWidth: 360, width: '100%' }}>
        <h2>일반 로그인 (학습용)</h2>
        <form onSubmit={handleLocalSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <input type="text" name="username" placeholder="유저네임" />
          <input type="password" name="password" placeholder="비밀번호" />
          <button type="submit">로그인</button>
        </form>
        {localMessage ? <p className="notice">{localMessage}</p> : null}
      </section>

      <hr style={{ width: '100%', maxWidth: 400 }} />

      {error ? <p style={{ color: 'red', marginTop: 0 }}>{error}</p> : null}

      <section style={{ textAlign: 'center', maxWidth: 360 }}>
        <h2>카카오 로그인</h2>
        <button type="button" onClick={handleKakaoLogin}>
          카카오로 로그인하기
        </button>
        <p className="notice">
          {`redirect_uri: ${kakaoInfo.redirectUri}`}
          <br />
          로그인 요청 시 nonce/state는 sessionStorage에 저장됩니다.
        </p>
      </section>
    </main>
  );
}

export default LoginPage;
