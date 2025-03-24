
News-Quest is a project that converts the latest news into crossword puzzles. It sources news articles from platforms like Reddit and Hacker News, processes them into clues, and generates puzzles for users to solve. This project demonstrates a variety of skills learned during a one-year bootcamp, including API integration, puzzle generation, and deployment.

Project Scope:
News Fetching:

The application fetches the latest news articles from sources like Reddit and Hacker News.
Crossword Puzzle Generation:

The fetched news articles are processed into crossword clues and answers.
The crossword puzzles are generated using the crossword-puzzle-maker library.
Frontend:

The frontend is built with React, and it allows users to view headlines, and crosswords, and interact with the generated puzzles.
Backend:

The backend uses FastAPI and serves the API for fetching news articles and serving crossword puzzles.
Folder Structure:
client/: Frontend application built with React.
server/: Backend API built with FastAPI.
db/: SQLite database storing crossword data and user progress.
How to Run:
Set up the backend:

Install dependencies: pip install -r requirements.txt
Run the FastAPI server: uvicorn app.main:app --reload
Set up the frontend:

Install dependencies: npm install
Run the React app: npm start
Technologies Used:
Frontend: React, JavaScript, CSS
Backend: FastAPI, Python
Puzzle Generation: crossword-puzzle-maker library
Database: SQLite
