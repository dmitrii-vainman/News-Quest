import React from 'react';
import './style.css';
import { useNavigate } from 'react-router-dom';

const Crossword = () => {
  const navigate = useNavigate();

  const handlePuzzleSelection = (source) => {
    // Navigate to the crossword puzzle based on the selected source
    navigate(`/crossword/${source}`);
  };

  return (
    <div className="crossword-page-container">
      <header className="crossword-page-header">
        <h1>Choose Your Crossword Challenge!</h1>
        <p>Select a source to solve a crossword based on the latest news.</p>
      </header>

      <main className="crossword-options">
        <div className="option-card" onClick={() => handlePuzzleSelection('reddit')}>
          <h3>Reddit</h3>
          <p>Get your crossword puzzle based on the most upvoted Reddit stories.</p>
        </div>

        <div className="option-card" onClick={() => handlePuzzleSelection('hackernews')}>
          <h3>Hacker News</h3>
          <p>Challenge yourself with a puzzle based on the latest tech news from Hacker News.</p>
        </div>

        <div className="option-card" onClick={() => handlePuzzleSelection('newsapi')}>
          <h3>Newsapi</h3>
          <p>Solve a crossword based on the latest headlines from trusted newspapers.</p>
        </div>
      </main>

      <footer className="footer-section">
        <button className="back-button" onClick={() => navigate('/')}>Back to Home</button>
      </footer>
    </div>
  );
};

export default Crossword;
