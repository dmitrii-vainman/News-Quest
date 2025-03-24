# /app/routes/utils/fetch_data.py
import requests

def fetch_from_api(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}. Status code: {response.status_code}")
        return []

def fetch_reddit_top_posts(limit=5):
    headers = {
        'User-Agent': 'News-Quest/0.1 by YourUsername'  # Reddit requires a user-agent header
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
        return headlines
    else:
        return {"error": "Failed to fetch posts", "status_code": response.status_code}