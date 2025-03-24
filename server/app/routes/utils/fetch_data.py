# /app/routes/utils/fetch_data.py
import requests

def fetch_from_api(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}. Status code: {response.status_code}")
        return []
