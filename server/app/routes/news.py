from fastapi import APIRouter
import requests

router = APIRouter(prefix="/news", tags=["news"])

NEWS_API_URL = "https://hn.algolia.com/api/v1/search?tags=front_page"

@router.get("/")
def get_latest_news():
    response = requests.get(NEWS_API_URL)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch news"}
