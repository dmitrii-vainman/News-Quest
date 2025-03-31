import sqlite3
import requests
import logging
import os
from fastapi import FastAPI
from app.routes.hackernews import router as hackernews_router
from app.routes.reddit import router as reddit_router
from dotenv import load_dotenv


# Initialize FastAPI app
app = FastAPI()
load_dotenv()

# Include routes for both HackerNews and Reddit
app.include_router(hackernews_router, prefix="/hackernews", tags=["HackerNews"])
app.include_router(reddit_router, prefix="/reddit", tags=["Reddit"])

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch and save top 10 Hacker News headlines
def fetch_and_save_hackernews_headlines():
    top_story_ids = fetch_top_stories()  # Get top 10 story IDs
    headlines = []

    for story_id in top_story_ids:
        story = fetch_story_details(story_id)
        if story:
            headlines.append(story)

    if headlines:
        save_headlines_to_db(headlines, "HackerNews")
    return headlines

# Fetches top 10 story IDs from Hacker News
def fetch_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[:10]  # Get top 10
    else:
        logger.error(f"Failed to fetch top stories. Status code: {response.status_code}")
        return []

# Fetches details of a single story from Hacker News
def fetch_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    response = requests.get(url)
    if response.status_code == 200:
        story = response.json()
        return {
            "title": story.get("title"),
            "url": story.get("url")  # Include the article URL
        }
    else:
        logger.error(f"Failed to fetch story details for {story_id}. Status code: {response.status_code}")
        return None


# news api fetch
newsapi_key = os.getenv('newsapi_key')
def fetch_newsapi_headlines(limit=10):
    api_key = newsapi_key 
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "global events",  # Search for global events
        "sortBy": "publishedAt",  # Sort by latest news
        "language": "en",  # English news
        "pageSize": limit,  # Limit to top headlines
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [
            {
                "title": article["title"],
                "url": article["url"]
            } 
            for article in articles
        ]
        return headlines
    else:
        print(f"Failed to fetch NewsAPI headlines. Status code: {response.status_code}")
        return []

# Fetch and save Reddit headlines from r/worldnews
def fetch_and_save_reddit_headlines(limit=10):
    url = "https://www.reddit.com/r/worldnews/top.json"
    params = {'limit': limit, 't': 'day'}
    headers = {'User-Agent': 'News-Quest/0.1 by Dmitrii'}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        posts = response.json().get('data', {}).get('children', [])
        headlines = [
            {
                "title": post['data']['title'],
                "url": post['data']['url']  # Include article URL
            } 
            for post in posts
        ]

        if headlines:
            save_headlines_to_db(headlines, "Reddit")
        return headlines
    else:
        logger.error(f"Failed to fetch Reddit posts. Status code: {response.status_code}")
        return []


# Ensure database is created on startup
def create_db():
    with sqlite3.connect("app/db/news.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            url TEXT NOT NULL
        )
        ''')
        conn.commit()

create_db()

def create_db2():
    with sqlite3.connect("app/db/news.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clues (
            id INTEGER PRIMARY KEY,
            word TEXT,
            clue TEXT,
            source TEXT,
            headline_id INTEGER,
            FOREIGN KEY (headline_id) REFERENCES headlines(id)
        )
        ''')
        conn.commit()

create_db2()
     
# Save headlines to SQLite (only title, URLs are fetched dynamically)
def save_headlines_to_db(headlines, source):
    try:
        with sqlite3.connect("app/db/news.db") as conn:
            cursor = conn.cursor()
            logger.info(f"Saving {len(headlines)} headlines from {source} to database.")
            
            # Delete existing entries for the given source
            cursor.execute("DELETE FROM headlines WHERE source = ?", (source,))
            logger.info(f"Deleted old headlines from {source}.")
            
            # Insert new headlines for the given source
            cursor.executemany('''
            INSERT INTO headlines (title, url, source)
            VALUES (?, ?, ?)
            ''', [(headline['title'], headline['url'], source) for headline in headlines])
            
            conn.commit()
            logger.info("Commit successful!")
    except Exception as e:
        logger.error(f"Error during database insertion: {e}")


# API Route: Fetch and return top 10 Hacker News headlines
@app.get("/headlines/hackernews")
def read_hackernews_headlines():
    headlines = fetch_and_save_hackernews_headlines()
    if not headlines:
        return {"error": "Failed to fetch HackerNews headlines"}
    return {"headlines": headlines}  # Now includes title & URL

# API Route: Fetch and return top 10 Reddit r/worldnews headlines
@app.get("/headlines/reddit")
def read_reddit_headlines():
    headlines = fetch_and_save_reddit_headlines()
    if not headlines:
        return {"error": "Failed to fetch Reddit headlines"}
    return {"headlines": headlines}  # Now includes title & URL

# API Route: Fetch and return top 10 NewsAPI headlines
@app.get("/headlines/newsapi")
def read_newsapi_headlines():
    headlines = fetch_newsapi_headlines()
    print(f"Fetched {len(headlines)} headlines from NewsAPI.")  
    save_headlines_to_db(headlines, "NewsAPI")  

    return {"headlines": headlines}  # Already includes title & URL
