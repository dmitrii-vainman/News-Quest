# app/routes/reddit.py
from fastapi import APIRouter
from app.routes.utils.fetch_data import fetch_reddit_top_posts  # Import the correct function

router = APIRouter()

@router.get("/headlines")
async def get_reddit_headlines(limit: int = 10):
    # Fetch the headlines using the function from fetch_data.py
    headlines = fetch_reddit_top_posts(limit)
    
    if isinstance(headlines, list):  # Check if the response is a list (successful fetch)
        return {"headlines": headlines}
    else:
        return {"error": "Failed to fetch posts", "status_code": headlines.get('status_code', 'Unknown')}
