import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const STORAGE_KEYS = {
  result: 'oidc_result'
};

const SAMPLE_POSTS = [
  { id: 1, title: '첫 번째 글', content: 'OIDC 학습 예제입니다.' },
  { id: 2, title: '두 번째 글', content: '카카오 ID 토큰을 검증하고 JWT를 발급했습니다.' },
  { id: 3, title: '세 번째 글', content: 'React 결과 페이지에서 글 목록을 간단히 보여줍니다.' }
];

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(() => location.state ?? null);
  const [posts] = useState(SAMPLE_POSTS);

  useEffect(() => {
    if (!result) {
      const stored = sessionStorage.getItem(STORAGE_KEYS.result);
      if (stored) {
        try {
          setResult(JSON.parse(stored));
        } catch (error) {
          console.error('결과 파싱 실패', error);
        }
      }
    } else {
      sessionStorage.setItem(STORAGE_KEYS.result, JSON.stringify(result));
    }
  }, [result]);

  if (!result) {
    return (
      <main>
        <h1>결과 없음</h1>
        <p className="notice">표시할 로그인 결과가 없습니다. 다시 로그인해주세요.</p>
        <button type="button" onClick={() => navigate('/', { replace: true })}>
          로그인 페이지로 이동
        </button>
      </main>
    );
  }

  const handleLogout = () => {
    sessionStorage.removeItem(STORAGE_KEYS.result);
    navigate('/', { replace: true });
  };

  return (
    <main>
      <h1>환영합니다, {result.nickname}님!</h1>
      <p className="notice">이메일: {result.email}</p>

      <section style={{ width: '100%', maxWidth: 520 }}>
        <h2>글 목록</h2>
        <ul style={{ listStyle: 'none', padding: 0, width: '100%' }}>
          {posts.map((post) => (
            <li
              key={post.id}
              style={{
                border: '1px solid #ccc',
                backgroundColor: '#fff',
                padding: '1rem',
                marginBottom: '0.75rem',
                textAlign: 'left'
              }}
            >
              <strong>{post.title}</strong>
              <p style={{ margin: '0.5rem 0 0' }}>{post.content}</p>
            </li>
          ))}
        </ul>
      </section>

      <button type="button" onClick={handleLogout}>
        로그아웃
      </button>
    </main>
  );
}

export default ResultPage;
