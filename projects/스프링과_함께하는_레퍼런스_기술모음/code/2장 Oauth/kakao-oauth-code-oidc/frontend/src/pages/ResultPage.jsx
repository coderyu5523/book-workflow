import { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { requestPosts } from '../api/oidcClient.js';

const STORAGE_KEYS = {
  result: 'oidc_result'
};

function parseQueryResult(search) {
  if (!search) return null;
  const params = new URLSearchParams(search);
  const token = params.get('token');
  const username = params.get('username');
  const email = params.get('email');
  if (!token && !username && !email) return null;
  return { token, username, email };
}

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const queryResult = useMemo(() => parseQueryResult(location.search), [location.search]);
  const [result, setResult] = useState(() => location.state ?? queryResult ?? null);
  const [posts, setPosts] = useState([]);
  const [postsMessage, setPostsMessage] = useState('');
  const [postsError, setPostsError] = useState('');

  useEffect(() => {
    if (queryResult) {
      setResult(queryResult);
      localStorage.setItem(STORAGE_KEYS.result, JSON.stringify(queryResult));
      navigate('/result', { replace: true });
      return;
    }

    if (!result) {
      const stored = localStorage.getItem(STORAGE_KEYS.result);
      if (stored) {
        try {
          setResult(JSON.parse(stored));
        } catch (error) {
          console.error('결과 파싱 실패', error);
        }
      }
    } else {
      localStorage.setItem(STORAGE_KEYS.result, JSON.stringify(result));
    }
  }, [navigate, queryResult, result]);

  const token = result?.body?.token ?? result?.token;
  const user = result?.body ?? result;

  useEffect(() => {
    if (!token) {
      setPostsError('토큰이 없습니다. 다시 로그인해주세요.');
      return;
    }
    let isCancelled = false;

    requestPosts(token)
      .then((response) => {
        if (isCancelled) return;
        setPosts(response.body ?? []);
        setPostsMessage(response.msg ?? '');
        setPostsError('');
      })
      .catch((error) => {
        if (isCancelled) return;
        setPostsError(error.message || '게시글 요청에 실패했습니다.');
      });

    return () => {
      isCancelled = true;
    };
  }, [token]);

  if (!user) {
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
    localStorage.removeItem(STORAGE_KEYS.result);
    navigate('/', { replace: true });
  };

  return (
    <main>
      <h1>환영합니다, {user.username ?? '사용자'}님!</h1>
      <p className="notice">이메일: {user.email ?? '없음'}</p>

      <section style={{ width: '100%', maxWidth: 520 }}>
        <h2>글 목록</h2>
        {postsMessage ? <p className="notice">{postsMessage}</p> : null}
        {postsError ? <p style={{ color: 'red' }}>{postsError}</p> : null}
        {posts.length ? (
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
                <p style={{ margin: '0.5rem 0 0' }}>작성자: {post.author}</p>
                <p style={{ margin: '0.25rem 0 0', fontSize: '0.875rem' }}>
                  작성일: {post.createdAt}
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="notice">표시할 글이 없습니다.</p>
        )}
      </section>

      <button type="button" onClick={handleLogout}>
        로그아웃
      </button>
    </main>
  );
}

export default ResultPage;
