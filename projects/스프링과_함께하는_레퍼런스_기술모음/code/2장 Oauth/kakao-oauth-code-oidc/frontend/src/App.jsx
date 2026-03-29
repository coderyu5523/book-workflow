import { Route, Routes } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import ResultPage from './pages/ResultPage.jsx';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/result" element={<ResultPage />} />
    </Routes>
  );
}

export default App;
