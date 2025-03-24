# News-Quest

**News-Quest** is a project that converts the latest news into crossword puzzles. It sources news articles from platforms like Reddit and Hacker News, processes them into clues, and generates puzzles for users to solve. This project showcases a variety of skills learned during a one-year bootcamp, including API integration, puzzle generation, and deployment.

## Project Scope

1. **News Fetching**:
   - The application fetches the latest news articles from sources like Reddit and Hacker News.

2. **Crossword Puzzle Generation**:
   - The fetched news articles are processed into crossword clues and answers.
   - The crossword puzzles are generated using the `crossword-puzzle-maker` library.

3. **Frontend**:
   - The frontend is built with React, and it allows users to view headlines, solve crosswords, and interact with the generated puzzles.

4. **Backend**:
   - The backend uses FastAPI to serve the API for fetching news articles and serving crossword puzzles.

## Folder Structure

├── client/ # Frontend application built with React │ ├── README.md │ ├── package.json │ ├── public/ │ └── src/ ├── server/ # Backend API built with FastAPI │ ├── app/ │ ├── db/ │ ├── requirements.txt │ └── venv/ ├── db/ # SQLite database storing crossword data and user progress

shell
Kopieren
Bearbeiten

## How to Run

### Backend (FastAPI)
1. Install dependencies:
   ```bash
   pip install -r server/requirements.txt
Run the FastAPI server:
bash
Kopieren
Bearbeiten
uvicorn server/app.main:app --reload
Frontend (React)
Install dependencies:
bash
Kopieren
Bearbeiten
cd client
npm install
Run the React app:
bash
Kopieren
Bearbeiten
npm start
Technologies Used
Frontend: React, JavaScript, CSS
Backend: FastAPI, Python
Puzzle Generation: crossword-puzzle-maker library
Database: SQLite
