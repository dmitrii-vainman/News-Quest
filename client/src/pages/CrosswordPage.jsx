import React, { useState, useEffect } from 'react';
import './style.css';

const CrosswordPage = ({ source }) => {
  const [puzzleData, setPuzzleData] = useState(null);

  useEffect(() => {
    // Fetch puzzle data based on the source
    fetch(`/api/headline/${source}`)
      .then(response => response.json())
      .then(data => setPuzzleData(data))
      .catch(error => {
        console.error('Error fetching puzzle data:', error);
      });
  }, [source]);

  const renderCrosswordGrid = () => {
    if (!puzzleData || !puzzleData.clues) return null;

    return puzzleData.clues.map((clue, index) => (
      <div key={index} className={`crossword-cell ${clue.word ? 'filled' : 'empty'}`}>
        {clue.word || ''}
      </div>
    ));
  };

  return (
    <div className="crossword-page-container">
      <header className="crossword-page-header">
        <h1>{puzzleData ? puzzleData.headline.title : 'Loading crossword...'}</h1>
        <p>Let's solve the crossword puzzle based on {source} news!</p>
      </header>
      <main className="main-content">
        {/* Crossword Area */}
        <div className="crossword-area">
          {renderCrosswordGrid()}
        </div>
        {/* Clue Section */}
        <div className="clue-section">
          <h3>Clues</h3>
          <table className="clue-table">
            <thead>
              <tr>
                <th>Clue</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {puzzleData && puzzleData.clues.map((clue, index) => (
                <tr key={index}>
                  <td>{clue.clue}</td>
                  <td>
                    <button
                      className="url-button"
                      onClick={() => window.open(puzzleData.headline.url, '_blank')}
                    >
                      Reveal URL
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
};

export default CrosswordPage;
