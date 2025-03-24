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
        <h1>Welcome to News-Quest Crossword</h1>
        <p>Your daily news made into a fun crossword puzzle!</p>
      </header>
      <main>
        <p>Ready to challenge yourself with the latest news? Click below to start solving today's puzzle!</p>
        <button className="start-button" onClick={handleStartGame}>Start Game</button>
      </main>
    </div>
  );
};

export default Home;
