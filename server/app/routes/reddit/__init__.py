# app/routes/reddit.py
from fastapi import APIRouter
from app.routes.utils.fetch_data import fetch_from_api  # Correct import

router = APIRouter()

@router.get("/headlines")
def get_reddit_headlines():
    headlines = fetch_from_api("reddit")
    return {"headlines": headlines}
