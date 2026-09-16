# 🎵 ZipTok — TikTok Interactive Offline Archiver 📦

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![yt-dlp](https://img.shields.io/badge/downloader-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

> **Shower thought turned open-source web application!** 🚿💡  
> **ZipTok** is a lightweight, web-based tool that extracts TikTok videos along with their full context—comments, stickers, images, and metadata—and bundles them into a standalone, interactive HTML package inside a `.zip` file for 24/7 offline viewing.

---

## 🌟 Key Features

- **🌐 Cross-Platform Web Tool**: Access ZipTok from any desktop or mobile browser (iOS & Android).
- **📂 Template Canvas Architecture**: Uses a static canvas directory (`template/`) to inject scraped data into `data.json`, eliminating runtime unzipping overhead and saving CPU resources.
- **⚡ Fast & Lightweight**: Generates dynamic `.zip` archives on the fly without heavy Base64 bloat.
- **📱 Responsive UI + Theme Toggle**: Minimalist, dark-mode-first web interface with an instant Dark/Light theme switcher.
- **📦 Fully Self-Contained Output**: Downloaded archives include video files (`.mp4`), stickers/media (`.webp`), styling (`style.css`), and an interactive player (`app.js`).

---

## 📁 Repository Structure

```text
ziptok_server/
├── main.py                # FastAPI server & archiver pipeline
├── template/              # Static canvas for the downloadable package
│   ├── index.html         # Offline interactive TikTok player
│   ├── style.css          # Viewer styling
│   ├── app.js             # Client-side renderer (loads data.json)
│   ├── videos/            # Target folder for video streams
│   └── images/            # Target folder for stickers & avatars
└── website/               # Static assets for the public ZipTok site
    ├── index.html         # Minimalist UI & URL submission form
    ├── style.css          # Site layout & CSS theme variables
    ├── app.js             # Theme toggle & download handler
    └── logo.png           # ZipTok logo
```

---

## 🛠️ Installation & Setup

### Prerequisites

Ensure you have **Python 3.8+** installed on your server or home machine.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ZipTok.git
cd ZipTok
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn yt-dlp python-multipart
```

---

## 🚀 Running the Server

Start the ZipTok FastAPI web server using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to `http://localhost:8000` to access the ZipTok web app!

---

## 📱 How It Works

1. Paste a public TikTok video link into the input bar on the ZipTok website.
2. Click **Download ZIP**.
3. ZipTok copies the `template/` canvas, downloads the video and comment media into subfolders, updates `data.json`, and compresses the bundle.
4. Your browser automatically receives the `.zip` archive.
5. Extract the `.zip` file anywhere and open `index.html` to view the interactive video and comments offline.

---

## 🤝 Contributing

Contributions are welcome! Roadmap goals include:

- [ ] **Playwright Worker Integration**: Scrape deep nested comment replies and high-resolution webp stickers.
- [ ] **Cloudflare Tunnel Guide**: Setup instructions for hosting on a home server/mini PC.
- [ ] **Background Task Queue**: Redis/Celery queue for handling simultaneous high-volume extraction requests.

1. Fork the Repository
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
