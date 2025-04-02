import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Crossword from './pages/Crossword';
import CrosswordPage from './pages/CrosswordPage';
import Reddit from './pages/newsp/Reddit';
import Hackernews from './pages/newsp/Hackernews';
import NewsAPI from './pages/newsp/Newsapi';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/crossword" element={<Crossword />} />
        <Route path="/crossword/reddit" element={<Reddit />} />
        <Route path="/crossword/hackernews" element={<Hackernews />} />
        <Route path="/crossword/newsapi" element={<NewsAPI />} />
      </Routes>
    </Router>
  );
}

export default App;
