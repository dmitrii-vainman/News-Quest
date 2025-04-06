import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CrosswordPage.css'; // Import the CSS file for this component

const CrosswordG = () => {
  const [clues, setClues] = useState([]);
  const [gridData, setGridData] = useState(null); // State to store crossword grid data
  const [loading, setLoading] = useState(true);
  const [clueWithHint, setClueWithHint] = useState(null);

  useEffect(() => {
    // Fetch crossword data and clues from the backend when the component mounts
    axios
      .get('http://localhost:5000/crossword/NewsAPI') // Adjust URL to get crossword grid
      .then((response) => {
        setGridData(response.data); // Set the crossword grid data
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching crossword:', error);
        setLoading(false);
      });

    axios
      .get('http://localhost:5000/clues?source=NewsAPI') // Fetch clues
      .then((response) => {
        setClues(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching clues:', error);
        setLoading(false);
      });
  }, []);

  const handleShowHint = (clueId) => {
    // Fetch the URL for the clue based on its id
    axios
      .get(`http://localhost:5000/clue/${clueId}`)
      .then((response) => {
        setClueWithHint(response.data.url); // Set the URL to be displayed
      })
      .catch((error) => {
        console.error('Error fetching clue hint:', error);
      });
  };

  const renderGrid = (grid) => {
    return grid.map((row, rowIndex) => (
      <div key={rowIndex} className="crossword-row">
        {row.map((cell, colIndex) => (
          <input
            key={colIndex}
            className="crossword-cell"
            type="text"
            maxLength="1" // Limit input to one character
            style={{ width: '30px', height: '30px', textAlign: 'center' }}
            value={cell !== '.' ? cell : ''}
            onChange={(e) => handleInputChange(e, rowIndex, colIndex)} // Handle input change
          />
        ))}
      </div>
    ));
  };

  const handleInputChange = (e, rowIndex, colIndex) => {
    const updatedGrid = [...gridData.grid]; // Make a copy of the grid
    updatedGrid[rowIndex][colIndex] = e.target.value.toUpperCase(); // Update the cell with the new input (uppercase)
    setGridData({ ...gridData, grid: updatedGrid }); // Update the grid state
  };

  if (loading) {
    return <div className="loading-message">Loading clues...</div>;
  }

  return (
    <div className="newsapi-container">
      <div className="blank-field">
        {/* Render crossword grid here with text fields */}
        {gridData && renderGrid(gridData.grid)}
      </div>

      <div className="clues-container">
        <h1>NewsAPI Crossword Clues</h1>
        <ul>
          {clues.map((clue) => (
            <li key={clue.id} className="clue-item">
              <strong>{clue.clue}</strong> {clue.answer}
              {/* Button to fetch and show URL */}
              <button
                onClick={() => handleShowHint(clue.id)}
                style={{
                  marginLeft: '10px',
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
              {clueWithHint && clue.id === clue.id && (
                <div
                  style={{
                    marginTop: '10px',
                    fontSize: '14px',
                    color: '#0073e6',
                  }}
                >
                  Hint: <a href={clueWithHint} target="_blank" rel="noopener noreferrer">View Hint</a>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default CrosswordG;
