import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_video_metadata(video_id):
    """
    Fetch basic metadata like title, description, and tags for a given video_id.
    """
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if items:
            snippet = items[0].get("snippet", {})
            return {
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "tags": snippet.get("tags", [])
            }
    return None