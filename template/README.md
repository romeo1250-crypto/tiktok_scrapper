# CatTok — TikTok-style HTML video viewer

A lightweight, dependency-free TikTok-inspired short-video interface.

## Folder structure

```text
├── index.html
├── style.css
├── script.js
├── videos/
│   └── mycatstourinmybackyard.mp4
└── images/
    ├── author_avatar.jpg
    └── comment_media_0.webp
```

## Run it

Put your GoPro video at:

`videos/mycatstourinmybackyard.mp4`

Put your avatar at:

`images/author_avatar.jpg`

Then serve the folder from a local HTTP server. This is preferable to opening
`index.html` directly because some browsers restrict video/media behavior under
`file://`.

Example with Python:

```bash
python -m http.server 8000
```

Then open:

`http://localhost:8000`

## Interactions implemented

- Single tap/click video: play/pause
- Double tap: like + animated heart
- Like / unlike
- Follow / unfollow
- Save / unsave
- Comments bottom sheet with posting
- Comment likes
- Native share on supported devices
- Share fallback menu with copy link / WhatsApp / email
- Search overlay
- Mute/unmute
- Progress bar seeking
- Desktop keyboard controls: Space, M, L, Left/Right arrows, Escape
- Mobile safe-area support for notches and Android gesture bars
- Responsive desktop phone-style presentation
