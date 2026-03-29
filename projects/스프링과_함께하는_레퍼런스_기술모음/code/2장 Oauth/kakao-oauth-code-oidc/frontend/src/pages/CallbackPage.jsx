import { useNavigate } from 'react-router-dom';

function CallbackPage() {
  const navigate = useNavigate();

  return (
    <main>
      <h1>콜백 처리 안내</h1>
      <p className="notice">카카오 콜백은 백엔드에서 처리합니다.</p>
      <button type="button" onClick={() => navigate('/', { replace: true })}>
        로그인 페이지로 이동
      </button>
    </main>
  );
}

export default CallbackPage;
