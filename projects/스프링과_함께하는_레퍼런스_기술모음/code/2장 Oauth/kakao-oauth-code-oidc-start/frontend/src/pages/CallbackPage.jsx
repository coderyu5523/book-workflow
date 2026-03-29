import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { requestOidcToken } from '../api/oidcClient.js';

const STORAGE_KEYS = {
  nonce: 'oidc_nonce',
  state: 'oidc_state',
  result: 'oidc_result'
};

function parseHashParams(hash) {
  if (!hash) return new URLSearchParams();
  const cleaned = hash.startsWith('#') ? hash.substring(1) : hash;
  return new URLSearchParams(cleaned);
}

function CallbackPage() {
  const [message, setMessage] = useState('카카오 응답을 확인하는 중입니다...');
  const navigate = useNavigate();

  useEffect(() => {
    const params = parseHashParams(window.location.hash);
    const error = params.get('error');
    if (error) {
      setMessage(`카카오 인증 오류: ${error}`);
      return;
    }

    const idToken = params.get('id_token');
    const state = params.get('state');
    if (!idToken) {
      setMessage('id_token 정보가 없습니다.');
      return;
    }

    const storedState = sessionStorage.getItem(STORAGE_KEYS.state);
    if (!storedState || storedState !== state) {
      setMessage('state 값이 일치하지 않습니다. 다시 로그인해주세요.');
      sessionStorage.removeItem(STORAGE_KEYS.state);
      sessionStorage.removeItem(STORAGE_KEYS.nonce);
      return;
    }

    const nonce = sessionStorage.getItem(STORAGE_KEYS.nonce);
    if (!nonce) {
      setMessage('nonce 정보가 없습니다. 로그인 과정을 다시 시도해주세요.');
      return;
    }

    window.history.replaceState(null, '', `${window.location.pathname}${window.location.search}`);

    requestOidcToken(idToken, nonce)
      .then((result) => {
        sessionStorage.removeItem(STORAGE_KEYS.state);
        sessionStorage.removeItem(STORAGE_KEYS.nonce);
        sessionStorage.setItem(STORAGE_KEYS.result, JSON.stringify(result));
        navigate('/result', { replace: true, state: result });
      })
      .catch((err) => {
        console.error(err);
        setMessage('서버와 통신 중 오류가 발생했습니다. 다시 로그인해주세요.');
      });
  }, [navigate]);

  return (
    <main>
      <h1>로그인 처리 중...</h1>
      <p className="notice">{message}</p>
    </main>
  );
}

export default CallbackPage;
