import os
import json
import re
import urllib.request
from pathlib import Path
import yt_dlp

def get_downloads_path() -> Path:
    """Finds the default Downloads path for Windows, macOS, or Linux."""
    return Path.home() / "Downloads"

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_asset(url: str, dest_path: Path) -> str:
    """Downloads a remote image/media file and saves it locally."""
    if not url:
        return ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest_path, 'wb') as out:
            out.write(resp.read())
        return str(dest_path.name)
    except Exception as e:
        print(f"[!] Warning: Failed to download asset {url}: {e}")
        return ""

def create_css() -> str:
    return """
:root {
  --bg: #121212;
  --card-bg: #1e1e1e;
  --text: #ffffff;
  --subtext: #8a8a8a;
  --accent: #fe2c55;
  --border: #2f2f2f;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background-color: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  display: flex;
  height: 100vh;
  overflow: hidden;
}
.app-container {
  display: flex;
  width: 100%;
  height: 100%;
}
.video-section {
  flex: 1.5;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
video {
  max-height: 100vh;
  max-width: 100%;
}
.sidebar {
  flex: 1;
  max-width: 480px;
  background: var(--card-bg);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
}
.author-header {
  padding: 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 12px;
}
.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  background: #333;
}
.author-meta h3 { font-size: 1rem; color: #fff; }
.author-meta p { font-size: 0.85rem; color: var(--subtext); }
.caption-box {
  padding: 16px;
  border-bottom: 1px solid var(--border);
  font-size: 0.95rem;
  line-height: 1.4;
}
.stats-bar {
  display: flex;
  gap: 16px;
  margin-top: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--accent);
}
.comments-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
.comment-card {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
}
.comment-body { flex: 1; }
.comment-user { font-weight: 600; font-size: 0.85rem; margin-bottom: 2px; }
.comment-text { font-size: 0.9rem; line-height: 1.35; color: #ececec; }
.comment-media {
  max-width: 140px;
  border-radius: 8px;
  margin-top: 6px;
  display: block;
}
"""

def create_js() -> str:
    return """
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('./data.json');
    const data = await response.json();

    // Set Video Source
    if (data.video_path) {
      document.getElementById('main-video').src = data.video_path;
    }

    // Populate Author Info
    document.getElementById('author-name').textContent = '@' + data.author;
    document.getElementById('caption').textContent = data.caption;
    document.getElementById('like-count').textContent = `❤️ ${data.like_count.toLocaleString()}`;
    document.getElementById('comment-count').textContent = `💬 ${data.comment_count.toLocaleString()}`;
    
    if (data.author_avatar) {
      document.getElementById('author-avatar').src = data.author_avatar;
    }

    // Populate Comments
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';

    data.comments.forEach(c => {
      const card = document.createElement('div');
      card.className = 'comment-card';

      const avatarSrc = c.avatar || data.author_avatar || '';
      const mediaHTML = c.media ? `<img class="comment-media" src="${c.media}" />` : '';

      card.innerHTML = `
        <img class="avatar" src="${avatarSrc}" onerror="this.style.opacity='0.2'" />
        <div class="comment-body">
          <div class="comment-user">@${c.author}</div>
          <div class="comment-text">${c.text}</div>
          ${mediaHTML}
        </div>
      `;
      commentsList.appendChild(card);
    });
  } catch (err) {
    console.error('Error loading data payload:', err);
  }
});
"""

def create_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TikTok Interactive Archive</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="app-container">
    <div class="video-section">
      <video id="main-video" controls loop autoplay></video>
    </div>
    <div class="sidebar">
      <div class="author-header">
        <img id="author-avatar" class="avatar" src="" alt="Avatar" />
        <div class="author-meta">
          <h3 id="author-name">@user</h3>
          <p>TikTok Archiver</p>
        </div>
      </div>
      <div class="caption-box">
        <div id="caption">Loading video caption...</div>
        <div class="stats-bar">
          <span id="like-count">❤️ 0</span>
          <span id="comment-count">💬 0</span>
        </div>
      </div>
      <div class="comments-container" id="comments-list">
        <!-- Comments will render dynamically via app.js -->
      </div>
    </div>
  </div>
  <script src="app.js"></script>
</body>
</html>
"""

def archive_tiktok(tiktok_url: str):
    print(f"[*] Starting scraper for: {tiktok_url}")
    
    # 1. Setup Base Output Folder in Downloads
    downloads_dir = get_downloads_path()
    
    # Temporary YTDL extraction to get ID
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(tiktok_url, download=False)
        video_id = info.get('id', 'archive')

    folder_name = f"TikTok_Archive_{video_id}"
    base_folder = downloads_dir / folder_name
    videos_folder = base_folder / "videos"
    images_folder = base_folder / "images"

    # Create directory tree
    for folder in [base_folder, videos_folder, images_folder]:
        folder.mkdir(parents=True, exist_ok=True)

    print(f"[+] Output directory created: {base_folder}")

    # 2. Download Video using yt-dlp directly into videos/
    video_filename = "video.mp4"
    video_target_path = videos_folder / video_filename
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(video_target_path),
        'getcomments': True,
        'quiet': False
    }

    print("[*] Extracting video & raw comments via yt-dlp...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(tiktok_url, download=True)

    # 3. Process Author Avatar
    avatar_url = info_dict.get('avatar', '')
    local_avatar = ""
    if avatar_url:
        avatar_path = images_folder / "author_avatar.jpg"
        rel_avatar = download_asset(avatar_url, avatar_path)
        if rel_avatar:
            local_avatar = f"images/{rel_avatar}"

    # 4. Parse Comments and Download Comment Media (Stickers/Images)
    parsed_comments = []
    raw_comments = info_dict.get('comments', [])
    print(f"[*] Processing {len(raw_comments)} extracted comments...")

    for idx, c in enumerate(raw_comments[:100]): # Cap at top 100 comments
        comment_obj = {
            "author": c.get('author', 'anonymous'),
            "text": c.get('text', ''),
            "likes": c.get('like_count', 0),
            "avatar": "",
            "media": ""
        }
        
        # If comment contains a sticker or image attachment URL
        sticker_url = c.get('sticker_url') or c.get('image_url')
        if sticker_url:
            media_path = images_folder / f"comment_media_{idx}.webp"
            rel_media = download_asset(sticker_url, media_path)
            if rel_media:
                comment_obj["media"] = f"images/{rel_media}"

        parsed_comments.append(comment_obj)

    # 5. Build JSON Payload
    payload = {
        "title": info_dict.get('title', ''),
        "caption": info_dict.get('description') or info_dict.get('title', ''),
        "author": info_dict.get('uploader', 'unknown'),
        "author_avatar": local_avatar,
        "like_count": info_dict.get('like_count', 0),
        "comment_count": info_dict.get('comment_count', len(parsed_comments)),
        "video_path": f"videos/{video_filename}",
        "comments": parsed_comments
    }

    # Save data.json
    with open(base_folder / "data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # 6. Write HTML, CSS, and JS static files
    with open(base_folder / "index.html", "w", encoding="utf-8") as f:
        f.write(create_html())

    with open(base_folder / "style.css", "w", encoding="utf-8") as f:
        f.write(create_css())

    with open(base_folder / "app.js", "w", encoding="utf-8") as f:
        f.write(create_js())

    print("\n==================================================")
    print(f"SUCCESS! Archive downloaded to your Downloads folder:")
    print(f"Folder: {base_folder}")
    print(f"Open this file in your browser to test: {base_folder / 'index.html'}")
    print("==================================================\n")

if __name__ == "__main__":
    url_input = input("Paste TikTok URL: ").strip()
    if url_input:
        archive_tiktok(url_input)