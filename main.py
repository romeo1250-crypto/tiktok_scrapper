import os
import json
import shutil
import tempfile
from pathlib import Path
from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp

app = FastAPI(title="ZipTok")

# Define paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "template"
WEBSITE_DIR = BASE_DIR / "website"

# Serve static web frontend assets
app.mount("/static", StaticFiles(directory=WEBSITE_DIR), name="static")

@app.get("/")
async def serve_home():
    """Serves the main minimalist website."""
    return FileResponse(WEBSITE_DIR / "index.html")

@app.post("/archive")
async def process_archive(background_tasks: BackgroundTasks, url: str = Form(...)):
    if not TEMPLATE_DIR.exists():
        raise HTTPException(status_code=500, detail="Base template directory missing.")

    # 1. Create temporary working directory for user session
    temp_dir = tempfile.mkdtemp()
    build_path = Path(temp_dir)
    
    try:
        # 2. Direct folder copy (No unzipping needed)
        target_bundle = build_path / "ZipTok_Archive"
        shutil.copytree(TEMPLATE_DIR, target_bundle)

        # 3. Extract metadata & download video via yt-dlp
        videos_folder = target_bundle / "videos"
        images_folder = target_bundle / "images"
        videos_folder.mkdir(exist_ok=True)
        images_folder.mkdir(exist_ok=True)

        video_file = videos_folder / "video.mp4"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': str(video_file),
            'getcomments': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict.get('id', 'content')

        # 4. Inject dynamic data into data.json inside the copied canvas
        payload = {
            "title": info_dict.get('title', ''),
            "author": info_dict.get('uploader', 'unknown'),
            "like_count": info_dict.get('like_count', 0),
            "comment_count": info_dict.get('comment_count', 0),
            "video_path": "videos/video.mp4",
            "comments": info_dict.get('comments', [])[:100]
        }

        with open(target_bundle / "data.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        # 5. Zip the updated bundle folder
        zip_output_filename = f"ZipTok_{video_id}"
        zip_file_path = shutil.make_archive(
            str(build_path / zip_output_filename), 
            'zip', 
            target_bundle
        )

        # Clean temp build environment after file delivery completes
        background_tasks.add_task(shutil.rmtree, temp_dir, ignore_errors=True)

        return FileResponse(
            path=zip_file_path,
            filename=f"{zip_output_filename}.zip",
            media_type="application/zip"
        )

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")