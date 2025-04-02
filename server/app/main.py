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

# News API fetch
newsapi_key = os.getenv('newsapi_key')

def reset_headlines_table():
    try:
        with sqlite3.connect("app/db/news.db") as conn:
            cursor = conn.cursor()
            logger.info("Dropping and recreating the headlines table.")

            # Drop and recreate the headlines table
            cursor.execute("DROP TABLE IF EXISTS headlines;")
            cursor.execute('''
            CREATE TABLE headlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                url TEXT NOT NULL
            )
            ''')

            conn.commit()
            logger.info("Headlines table reset successfully!")

    except Exception as e:
        logger.error(f"Error resetting headlines table: {e}")


import requests
import time

def fetch_newsapi_headlines(limit=8, fetch_limit=20):
    """
    Fetch headlines from NewsAPI and ensure we have exactly `limit` valid headlines.
    The `fetch_limit` determines how many articles to initially fetch (higher than the `limit`).
    """
    api_key = newsapi_key  # Your NewsAPI key
    url = "https://newsapi.org/v2/everything"
    
    while True:
        params = {
            "q": "global events",  # Search for global events
            "sortBy": "publishedAt",  # Sort by latest news
            "language": "en",  # English news
            "pageSize": fetch_limit,  # Fetch more articles initially
            "apiKey": api_key
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            headlines = []
            
            # Filter articles that have both title and URL
            for article in articles:
                title = article.get('title')
                url = article.get('url')
                
                if title and url:
                    headlines.append({"title": title, "url": url})
                else:
                    print(f"Skipping article due to missing title or URL: {article}")

            print(f"Fetched {len(headlines)} valid headlines.")
            
            if len(headlines) >= limit:
                return headlines[:limit]  # Return the first `limit` valid headlines
            
            # If we haven't got enough valid headlines, fetch more
            print(f"Not enough valid headlines. Fetching more articles...")
            time.sleep(2)  # Small delay before retrying to prevent API overuse
        else:
            print(f"Failed to fetch NewsAPI headlines. Status code: {response.status_code}")
            return []



# Function to fetch and save top 10 Hacker News headlines


# Fetches top 10 story IDs from Hacker News
def fetch_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[:8]  # Get top 10
    else:
        logger.error(f"Failed to fetch top stories. Status code: {response.status_code}")
        return []

# Fetches details of a single story from Hacker News
def fetch_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    response = requests.get(url)
    if response.status_code == 200:
        story = response.json()
        story_url = story.get("url")
        
        # If there's no URL in the story, use the post URL
        if not story_url:
            logger.warning(f"Story {story_id} has no direct URL. Using post URL.")
            story_url = f"https://news.ycombinator.com/item?id={story_id}"
        
        return {
            "title": story.get("title"),
            "url": story_url  # Return the fallback URL if needed
        }
    else:
        logger.error(f"Failed to fetch story details for {story_id}. Status code: {response.status_code}")
        return None



def fetch_and_save_hackernews_headlines():
    top_story_ids = fetch_top_stories()  # Get top 8 story IDs
    if not top_story_ids:
        logger.error("No top stories fetched from Hacker News.")
        return []

    headlines = []
    for story_id in top_story_ids:
        story = fetch_story_details(story_id)
        if story:
            # Ensure the headline has both title and url before adding to the list
            if 'title' in story and 'url' in story:
                headlines.append(story)
            else:
                logger.warning(f"Skipping story ID {story_id} due to missing title or url.")

    return headlines  # Don't save here, just return the headlines



# Fetch and save Reddit headlines from r/worldnews
def fetch_and_save_reddit_headlines(limit=8):
    url = "https://www.reddit.com/r/worldnews/top.json"
    params = {'limit': limit, 't': 'day'}
    headers = {'User-Agent': 'News-Quest/0.1 by Dmitrii'}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        posts = response.json().get('data', {}).get('children', [])
        headlines = []
        for post in posts:
            post_data = post['data']
            title = post_data.get('title')
            post_url = post_data.get('url')
            
            # If no URL is provided, use the permalink
            if not post_url:
                post_url = f"https://www.reddit.com{post_data.get('permalink', '')}"
            
            headlines.append({
                "title": title,
                "url": post_url  # Use the fallback URL if needed
            })
        return headlines
    else:
        logger.error(f"Failed to fetch Reddit posts. Status code: {response.status_code}")
        return []



# Combined fetch function for all three sources
def fetch_and_save_all_headlines():
    # Reset the headlines table ONCE at the beginning
    reset_headlines_table()

    # Fetch headlines from all sources
    hackernews_headlines = fetch_and_save_hackernews_headlines()
    reddit_headlines = fetch_and_save_reddit_headlines()
    newsapi_headlines = fetch_newsapi_headlines()

    # Combine all headlines into one list
    all_headlines = {
        "HackerNews": hackernews_headlines,
        "Reddit": reddit_headlines,
        "NewsAPI": newsapi_headlines
    }

    # Save each source's headlines to the database
    save_headlines_to_db(hackernews_headlines, "HackerNews")
    save_headlines_to_db(reddit_headlines, "Reddit")
    save_headlines_to_db(newsapi_headlines, "NewsAPI")

    return all_headlines



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
     
def save_headlines_to_db(headlines, source):
    try:
        with sqlite3.connect("app/db/news.db") as conn:
            cursor = conn.cursor()

            logger.info(f"Saving {len(headlines)} headlines from {source} to database.")

            # Insert new headlines for the given source
            cursor.executemany(''' 
            INSERT INTO headlines (title, url, source)
            VALUES (?, ?, ?)
            ''', [(headline['title'], headline['url'], source) for headline in headlines])

            conn.commit()
            logger.info("Commit successful!")
    except Exception as e:
        logger.error(f"Error during database insertion: {e}")



# API Route: Fetch and return all headlines from all sources
@app.get("/headlines")
def read_all_headlines():
    all_headlines = fetch_and_save_all_headlines()
    return {"headlines": all_headlines}  # Returns a dictionary of headlines by source


import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a model for the clues and headlines
class Clue(BaseModel):
    id: int
    word: str
    clue: str
    source: str
    headline_id: int
    url: str

class Headline(BaseModel):
    title: str
    source: str
    url: str

# Function to fetch clues based on source
def fetch_clues_and_headline(source: str):
    conn = sqlite3.connect('../db/news.db')
    cursor = conn.cursor()

    # Fetch the headline for the selected source (now including the URL)
    cursor.execute("SELECT title, source, url FROM headlines WHERE source = ? LIMIT 1", (source,))
    headline_data = cursor.fetchone()

    # Fetch clues associated with the headline
    cursor.execute("SELECT id, word, clue, source, headline_id FROM clues WHERE source = ?", (source,))
    clues_data = cursor.fetchall()

    conn.close()

    # Return the fetched data
    if headline_data:
        headline = Headline(title=headline_data[0], source=headline_data[1], url=headline_data[2])
    else:
        headline = None

    # Modify clues to include the URL from the associated headline
    clues = [
        Clue(id=row[0], word=row[1], clue=row[2], source=row[3], headline_id=row[4], url=headline_data[2])
        for row in clues_data
    ]

    return {"headline": headline, "clues": clues}


# Endpoint to fetch the clues and headline data
@app.get("/api/headline/{source}")
def get_headline_and_clues(source: str):
    return fetch_clues_and_headline(source)
