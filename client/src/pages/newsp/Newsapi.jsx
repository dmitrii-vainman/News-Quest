import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './NewsAPI.css'; // Import the CSS file for this component

const NewsAPI = () => {
  const [clues, setClues] = useState([]);
  const [loading, setLoading] = useState(true);

  const [clueWithHint, setClueWithHint] = useState(null);
  
  useEffect(() => {
    // Fetch clues from the backend when the component mounts
    axios
      .get('http://localhost:5000/clues?source=NewsAPI')
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

  if (loading) {
    return <div className="loading-message">Loading clues...</div>;
  }

  return (
    <div className="newsapi-container">
      <div className="blank-field"></div> {/* This is the large blank field */}
      <div className="clues-container">
        <h1>NewsAPI Crossword Clues</h1>
        <ul>
          {clues.map((clue) => (
            <li key={clue.id} className="clue-item">
              <strong>{clue.clue}</strong> - Answer: {clue.answer}
              {/* Button to fetch and show URL */}
              <button 
                onClick={() => handleShowHint(clue.id)}
                style={{ marginLeft: '10px', padding: '5px 10px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                Show Hint
              </button>
              {clueWithHint && clue.id === clue.id && (
                <div style={{ marginTop: '10px', fontSize: '14px', color: '#0073e6' }}>
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

export default NewsAPI;
