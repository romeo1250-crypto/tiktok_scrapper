#  TikTok Interactive Offline Archiver 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https.opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![yt-dlp](https://img.shields.io/badge/downloader-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

> **Shower thought turned open-source reality!** 🚿💡  
> Extract TikTok videos along with their full context (metadata, comments, author profiles, stickers, and images) into a **self-contained, interactive offline HTML bundle** automatically saved straight to your system's `Downloads` folder.

---

##  Key Features

- ** Self-Contained Output Bundle**: Downloads a ready-to-use directory structure right into `~/Downloads/TikTok_Archive_[ID]/`.
- ** Local Video & Asset Storage**: Organizes video streams, author avatars, inline comment photos, and stickers into neat `videos/` and `images/` subfolders.
- ** TikTok-Inspired Dark Mode UI**: Interactively view the archived video alongside a responsive, scrollable comment sidebar designed to mirror the native app experience.
- ** Zero Local Server Required**: Uses pure client-side HTML/CSS/JS that fetches data from a local `data.json` file—simply double-click `index.html` to launch.
- ** Fast & Lightweight**: Avoids massive Base64 file bloating by serving standard media files locally.

---

##  Directory Structure Created

When you run the archiver on a TikTok URL, it builds the following bundle inside your **Downloads** directory:

```text
~/Downloads/TikTok_Archive_[ID]/
├── index.html          # Interactive TikTok viewer app
├── style.css           # TikTok dark mode styling
├── app.js              # Interactivity & media rendering engine
├── data.json           # Scraped metadata, comments, and file paths
├── videos/             # Downloaded .mp4 media file
│   └── video.mp4
└── images/             # Downloaded avatars, stickers & comment attachments
    ├── author_avatar.jpg
    └── comment_media_0.webp
```

---

##  Installation & Setup

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/tiktok-archiver.git
cd tiktok-archiver
```

### 2. Install Dependencies
Install [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) for media and metadata extraction:
```bash
pip install -r requirements.txt
```
> *Note: If `requirements.txt` is missing, run `pip install yt-dlp`.*

---

##  Quick Start

1. Run the archiver script:
   ```bash
   python tiktok_archiver.py
   ```
2. Paste any public TikTok URL when prompted:
   ```text
   Paste TikTok URL: https://www.tiktok.com/@user/video/1234567890123456789
   ```
3. Open your **Downloads** directory and open `TikTok_Archive_[ID]/index.html` in any modern browser!

---

##  Tech Stack & Architecture

- **Engine**: Python 3, `yt-dlp`
- **File System Automation**: Python `pathlib`, `urllib.request`
- **Frontend App**: Pure HTML5, CSS3 (Variables + Flexbox layout), Vanilla JS (ES6 Fetch API)

---

##  Contributing

Contributions are welcome! Here are a few features on the roadmap if you'd like to jump in:

- [ ] **Playwright Integration**: Deep-scroll comment threads to scrape sub-replies and high-res stickers.
- [ ] **Streamlit / FastAPI Web Interface**: Local GUI with a URL input field and download progress bar.
- [ ] **Zip Exporter**: Option to compress the generated folder into `.zip` automatically.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

##  License

Distributed under the MIT License. See `LICENSE` for more information.
