import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './NewsAPI.css'; // Import the CSS file for this component

const NewsAPI = () => {
  const [clues, setClues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [clueWithHint, setClueWithHint] = useState(null);
  const [gridData, setGridData] = useState(Array(15).fill().map(() => Array(15).fill(''))); // Initialize grid as 15x15 empty

  useEffect(() => {
    // Fetch clues from the backend when the component mounts
    axios
      .get('http://localhost:5000/clues?source=NewsAPI')
      .then((response) => {
        console.log("Fetched clues:", response.data);
        setClues(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching clues:', error);
        setLoading(false);
      });
  
    // Fetch the crossword puzzle (grid and placed words) from the backend
    axios
      .get('http://127.0.0.1:8000/crossword/NewsAPI')
      .then((response) => {
        console.log("Crossword Data:", response.data);
        const crosswordGrid = response.data.grid;
        const placedWords = response.data.words; // Get the placed words
  
        // Create a cleared grid: keep '.' for blocked cells; for others, start with empty strings
        let clearedGrid = crosswordGrid.map(row =>
          row.map(cell => (cell === '.' ? '.' : ''))
        );
  
        // For each placed word, fill in the first letter of the word at its starting cell
        placedWords.forEach((wordObj, idx) => {
          const { x, y, word } = wordObj;
          if (clearedGrid[x] && clearedGrid[x][y] !== undefined) {
            clearedGrid[x][y] = word[0]; // Keep only the first letter
          }
        });
  
        setGridData(clearedGrid);
      })
      .catch((error) => {
        console.error('Error fetching crossword puzzle:', error);
      });
  }, []);

  const handleShowHint = (clueId) => {
    axios
      .get(`http://127.0.0.1:8000/api/clue_with_headline/${clueId}`)
      .then((response) => {
        const { id, word, clue, source, headline, headlineUrl } = response.data;
        setClueWithHint({
          id,
          word,
          clue,
          source,
          headline,
          headlineUrl,
        });
      })
      .catch((error) => {
        console.error('Error fetching clue with headline:', error);
      });
  };
  
  

  const handleInputChange = (e, rowIndex, colIndex) => {
    // Handle text field input changes
    const value = e.target.value.toUpperCase(); // Ensure input is always capitalized
    const newGridData = [...gridData];
    newGridData[rowIndex][colIndex] = value; // Update the grid
    setGridData(newGridData);
  };

  const renderGrid = () => {
    return gridData.map((row, rowIndex) => (
      <div key={rowIndex} className="crossword-row">
        {row.map((cell, colIndex) => {
          const isEmptyCell = cell === "."; // Check if the cell is blocked
          const startingClues = clues.filter(
            (clue) => clue.x === colIndex && clue.y === rowIndex
          );
  
          const clueIdsPlaceholder = startingClues.map(clue => clue.id).join(',');
          const isStartOfWord = startingClues.length > 0;
  
          return (
            <div key={colIndex} className="crossword-cell-wrapper">
              <div className="crossword-cell-container">
                {isStartOfWord && (
                  <span className="clue-id-overlay">
                    {clueIdsPlaceholder}
                  </span>
                )}
                <input
                  className={`crossword-cell ${isEmptyCell ? 'locked' : ''}`}
                  type="text"
                  maxLength="1"
                  value={isEmptyCell ? '' : gridData[rowIndex][colIndex]}
                  onChange={(e) => handleInputChange(e, rowIndex, colIndex)}
                  disabled={isEmptyCell}
                />
              </div>
            </div>
          );
        })}
      </div>
    ));
  };

  if (loading) {
    return <div className="loading-message">Loading clues...</div>;
  }

  return (
    <div className="newsapi-container">
      <div className="blank-field">
        {renderGrid()}
      </div>
      <div className="clues-container">
        <h1>NewsAPI Crossword Clues</h1>
        <ul>
          {clues.map((clue) => (
            <li key={clue.id} className="clue-item">
              <span className="clue-number">{clue.id}</span>
              <strong>{clue.clue}</strong> {clue.answer}
              <button
                onClick={() => handleShowHint(clue.id)}
                style={{
                  marginLeft: '15px',
                  padding: '5px 10px',
                  backgroundColor: '#4CAF50',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                }}
              >
                Show Hint
              </button>
              {clueWithHint && clue.id === clueWithHint.id && (
                <div
                  style={{
                    marginTop: '10px',
                    fontSize: '14px',
                    color: '#0073e6',
                  }}
                >
                  Hint: <a href={clueWithHint.headlineUrl} target="_blank" rel="noopener noreferrer">
                    {clueWithHint.headline}
                  </a>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default NewsAPI;
