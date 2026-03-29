const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8080';

export async function requestOidcToken(idToken, nonce) {
  const response = await fetch(`${API_BASE}/oidc`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ idToken, nonce })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'OIDC 요청이 실패했습니다.');
  }

  return response.json();
}

export function buildKakaoAuthorizeUrl({ clientId, redirectUri, nonce, state }) {
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: 'openid profile_nickname',
    nonce,
    state
  });
  return `https://kauth.kakao.com/oauth/authorize?${params.toString()}`;
}
