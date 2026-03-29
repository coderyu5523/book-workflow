const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8080';

export function getKakaoLoginUrl() {
  return `${API_BASE}/login/kakao`;
}

export async function requestPosts(token) {
  const response = await fetch(`${API_BASE}/posts`, {
    headers: {
      Authorization: token?.startsWith('Bearer ') ? token : `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || '게시글 요청이 실패했습니다.');
  }

  return response.json();
}
