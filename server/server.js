const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
const port = 5000;

// Enable CORS to allow communication from frontend
app.use(cors());

// Connect to the SQLite database
const db = new sqlite3.Database('./app/db/news.db', (err) => {
  if (err) {
    console.error('Database opening error:', err);
  } else {
    console.log('Connected to the SQLite database.');
  }
});

// Endpoint to get crossword clues
app.get('/clues', (req, res) => {
  const source = req.query.source; // Get source query parameter (Reddit, HackerNews, etc.)

  // Fetch clues based on the source
  db.all('SELECT * FROM clues WHERE source = ?', [source], (err, rows) => {
    if (err) {
      res.status(500).send('Error retrieving clues');
    } else {
      res.json(rows);
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
