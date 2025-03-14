from fastapi import FastAPI
from app.routes import news, puzzle

app = FastAPI()

app.include_router(news.router)
app.include_router(puzzle.router)

@app.get("/")
def root():
    return {"message": "Welcome to NewsQuest!"}