# app/routes/reddit.py
from fastapi import APIRouter
from app.routes.utils.fetch_data import fetch_from_api  # Correct import

router = APIRouter()

@router.get("/headlines/reddit")
async def get_reddit_headlines(limit: int = 5):
    headers = {
        'User-Agent': 'News-Quest/0.1 by YourUsername'
    }
    url = 'https://www.reddit.com/top.json'
    params = {'limit': limit}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        posts = response.json()['data']['children']
        headlines = []
        for post in posts:
            headline = {
                'title': post['data']['title'],
                'url': post['data']['url']
            }
            headlines.append(headline)
        return {"headlines": headlines}
    else:
        return {"error": "Failed to fetch posts", "status_code": response.status_code}