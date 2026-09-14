import base64
import json
import yt_dlp
from jinja2 import Template

def get_base64_file(file_path: str) -> str:
    """Reads a local file and encodes it to Base64 data URI."""
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return f"data:video/mp4;base64,{encoded}"

def scrape_tiktok(tiktok_url: str) -> dict:
    """Extracts video, author details, and comments payload."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'temp_video.mp4',
        'getcomments': True, # Pulls basic comment metadata from yt-dlp
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(tiktok_url, download=True)
        
    video_base64 = get_base64_file('temp_video.mp4')
    
    # Process structured metadata
    payload = {
        "title": info.get('title', 'TikTok Video'),
        "author": info.get('uploader', 'Unknown'),
        "author_avatar": info.get('avatar', ''),
        "like_count": info.get('like_count', 0),
        "comment_count": info.get('comment_count', 0),
        "video_data_uri": video_base64,
        "comments": []
    }
    
    # Parse comments (yt-dlp extracts basic comments; extend with Playwright for stickers)
    raw_comments = info.get('comments', [])
    for c in raw_comments:
        payload["comments"].append({
            "author": c.get('author', 'Anonymous'),
            "text": c.get('text', ''),
            "likes": c.get('like_count', 0),
            "timestamp": c.get('timestamp', ''),
            "sticker": c.get('sticker_url', None) # Custom Playwright logic can populate this
        })
        
    return payload