// client/src/pages/Reddit.jsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Hackernews = () => {
  const [clues, setClues] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch clues from the backend when the component mounts
    axios
      .get('http://localhost:5000/clues?source=HackerNews')
      .then((response) => {
        setClues(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching clues:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading clues...</div>;
  }

  return (
    <div>
      <h1>Hackernews Crossword Clues</h1>
      <ul>
        {clues.map((clue) => (
          <li key={clue.id}>{clue.id} - 
            <strong>{clue.clue}</strong> - Answer: {clue.answer}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Hackernews;
