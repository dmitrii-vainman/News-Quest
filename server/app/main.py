import sqlite3
import requests
from fastapi import FastAPI
from app.routes.hackernews import router as hackernews_router
from app.routes.reddit import router as reddit_router




app = FastAPI()

# Include routes for both HackerNews and Reddit
app.include_router(hackernews_router, prefix="/hackernews", tags=["HackerNews"])
app.include_router(reddit_router, prefix="/reddit", tags=["Reddit"])


# Function to fetch top story IDs from Hacker News
def fetch_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch top stories. Status code: {response.status_code}")
        return []

# Function to fetch the story details (headlines)
def fetch_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch story details for {story_id}. Status code: {response.status_code}")
        return None

# Function to fetch and save headlines to the database (only first 10 headlines)
def fetch_and_save_headlines():
    top_story_ids = fetch_top_stories()[:10]  # Limit to top 10 stories
    headlines = []
    for story_id in top_story_ids:
        story = fetch_story_details(story_id)
        if story:
            headlines.append({
                "title": story.get("title")
            })

    return headlines


# Function to create the database
def create_db():
    conn = sqlite3.connect("app/db/news.db")  # Relative path
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS headlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        source TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Make sure the database and table are created when the app starts
create_db()

def save_headlines_to_db(headlines, source):
    conn = sqlite3.connect("app/db/news.db")  # Relative path
    cursor = conn.cursor()

    try:
        print(f"Saving {len(headlines)} headlines to the database...")  # Add a print statement here
        for headline in headlines:
            print(f"Inserting headline: {headline['title']}")  # Check individual headline
            cursor.execute("INSERT INTO headlines (title, source) VALUES (?, ?)", 
               (headline['title'], source))
        
        conn.commit()  # Commit changes
        print("Commit successful!")  # Print confirmation after commit
    except Exception as e:
        print(f"Error during database insertion: {e}")  # Catch any exceptions during insertion
    finally:
        conn.close()  # Ensure the connection is always closed

@app.get("/headlines/hackernews")
def read_hackernews_headlines():
    headlines = fetch_and_save_headlines()  # Fetches headlines
    print(f"Fetched {len(headlines)} headlines from HackerNews.")  # Add a print statement here
    save_headlines_to_db(headlines, "HackerNews")  # Save to DB
    
    # Modify output to show only titles
    headlines_output = [{"title": headline["title"]} for headline in headlines]
    return {"headlines": headlines_output}

