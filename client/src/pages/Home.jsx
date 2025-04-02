import React from 'react';
import './Home.css';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();  // Hook to navigate between pages

  const handleStartGame = () => {
    // Navigate to the /crossword page when the button is clicked
    navigate('/crossword');
  };

  return (
    <div className="home-page-container">
      <header className="home-page-header">
        <h1 className="main-title">Welcome to News-Quest!</h1>
        <p className="sub-title">Your daily news made into a fun crossword puzzle.</p>
      </header>

      <section className="intro-section">
        <div className="description-box">
          <h2>How it Works</h2>
          <p>Stay updated and engaged by solving crosswords based on the latest news from various sources.</p>
        </div>

        <div className="sources-section">
          <h2>Crossword Sources</h2>
          <ul className="source-list">
            <li>Reddit</li>
            <li>Hacker News</li>
            <li>Newspapers</li>
          </ul>
        </div>
      </section>

      <footer className="footer-section">
        <p>Ready to challenge yourself with today’s news? Click below to start solving!</p>
        <button className="start-button" onClick={handleStartGame}>Start Game</button>
      </footer>
    </div>
  );
};

export default Home;
