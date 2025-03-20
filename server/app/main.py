from fastapi import FastAPI
from app.routes import news
from server.app.routes import crossword

app = FastAPI()

app.include_router(news.router)
app.include_router(crossword.router)

@app.get("/")
def root():
    return {"message": "Welcome to NewsQuest!"}