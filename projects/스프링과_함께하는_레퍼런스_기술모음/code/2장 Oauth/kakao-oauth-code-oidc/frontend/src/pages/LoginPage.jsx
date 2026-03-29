import { getKakaoLoginUrl } from '../api/oidcClient.js';

const STORAGE_KEYS = {
  result: 'oidc_result'
};

function LoginPage() {
  const loginUrl = getKakaoLoginUrl();

  const handleKakaoLogin = () => {
    localStorage.removeItem(STORAGE_KEYS.result);
    window.location.href = loginUrl;
  };

  return (
    <main>
      <h1>카카오 로그인</h1>
      <p className="notice">카카오 계정으로만 로그인합니다.</p>

      <section style={{ textAlign: 'center', maxWidth: 360 }}>
        <button type="button" onClick={handleKakaoLogin}>
          카카오로 로그인하기
        </button>
        <p className="notice">
          {`backend: ${loginUrl}`}
        </p>
      </section>
    </main>
  );
}

export default LoginPage;
