import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from the .env file
newsapi_key = os.getenv('newsapi_key')

# Function to fetch top stories from Hacker News
def fetch_hackernews_top_stories(limit=10):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        story_ids = response.json()[:limit]
        headlines = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            if story_response.status_code == 200:
                story = story_response.json()
                headlines.append({"title": story.get("title"), "url": story.get("url")})
        return headlines
    else:
        print(f"Error fetching Hacker News stories. Status code: {response.status_code}")
        return []

# Function to fetch top posts from r/worldnews (Reddit)
def fetch_reddit_top_posts(limit=10):
    headers = {
        'User-Agent': 'News-Quest/0.1 by Dmitrii'
    }

    url = "https://www.reddit.com/r/worldnews/top.json"
    params = {'limit': limit, 't': 'day'}  # Fetches top posts of the day

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
        return headlines
    else:
        print(f"Error fetching Reddit posts. Status code: {response.status_code}")
        return []

# Function to fetch top headlines from NewsAPI
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
