# /app/routes/hackernews/__init__.py
from fastapi import APIRouter
from app.routes.utils.fetch_data import fetch_hackernews_top_stories

router = APIRouter()

@router.get("/headlines")
async def get_hackernews_headlines():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    top_story_ids = fetch_hackernews_top_stories(url)[:10]  # Limit to top 10 stories

    headlines = []
    for story_id in top_story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
        story_data = fetch_hackernews_top_stories(story_url)
        headlines.append(story_data.get("title", "Untitled"))
    
    return {"headlines": headlines}
