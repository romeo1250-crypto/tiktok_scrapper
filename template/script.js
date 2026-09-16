(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  const video = $("#video");
  const videoPage = $("#videoPage");
  const likeButton = $("#likeButton");
  const likeCount = $("#likeCount");
  const commentButton = $("#commentButton");
  const commentCount = $("#commentCount");
  const bookmarkButton = $("#bookmarkButton");
  const bookmarkCount = $("#bookmarkCount");
  const shareButton = $("#shareButton");
  const shareCount = $("#shareCount");
  const profileButton = $("#profileButton");
  const followBadge = $("#followBadge");
  const progressTrack = $("#progressTrack");
  const progressBar = $("#progressBar");
  const playIndicator = $("#playIndicator");
  const playIndicatorIcon = $("#playIndicatorIcon");
  const burstHeart = $("#burstHeart");
  const loadingIndicator = $("#loadingIndicator");
  const toast = $("#toast");

  const commentsSheet = $("#commentsSheet");
  const shareSheet = $("#shareSheet");
  const searchOverlay = $("#searchOverlay");

  const commentForm = $("#commentForm");
  const commentInput = $("#commentInput");
  const commentsList = $("#commentsList");
  const searchForm = $("#searchForm");
  const searchInput = $("#searchInput");

  const state = {
    likes: 5090,
    comments: 66,
    saves: 505,
    shares: 958,
    liked: false,
    saved: false,
    following: false,
    muted: false,
    draggingProgress: false,
    lastTap: 0,
    tapTimer: null,
    toastTimer: null
  };

  function formatCount(value) {
    if (value >= 1000000) return `${(value / 1000000).toFixed(value % 1000000 ? 1 : 0)}M`;
    if (value >= 1000) return `${(value / 1000).toFixed(value % 1000 ? 1 : 0)}K`;
    return String(value);
  }

  function renderState() {
    likeCount.textContent = formatCount(state.likes);
    commentCount.textContent = formatCount(state.comments);
    bookmarkCount.textContent = formatCount(state.saves);
    shareCount.textContent = formatCount(state.shares);

    likeButton.classList.toggle("liked", state.liked);
    likeButton.setAttribute("aria-pressed", String(state.liked));

    bookmarkButton.classList.toggle("saved", state.saved);
    bookmarkButton.setAttribute("aria-pressed", String(state.saved));

    profileButton.classList.toggle("following", state.following);
    profileButton.setAttribute("aria-pressed", String(state.following));

    followBadge.textContent = state.following ? "✓" : "+";
    followBadge.setAttribute("aria-label", state.following ? "Following" : "Follow");
  }

  function showToast(message) {
    clearTimeout(state.toastTimer);
    toast.textContent = message;
    toast.classList.add("show");
    state.toastTimer = setTimeout(() => toast.classList.remove("show"), 1800);
  }

  function pulse(element, text = null) {
    if (text !== null) element.textContent = text;
    element.classList.remove("show");
    void element.offsetWidth;
    element.classList.add("show");
  }

  function togglePlay() {
    if (video.paused) {
      const p = video.play();
      if (p?.catch) p.catch(() => showToast("Tap again to play the video"));
      playIndicatorIcon.textContent = "▶";
    } else {
      video.pause();
      playIndicatorIcon.textContent = "Ⅱ";
    }
    pulse(playIndicator);
  }

  function toggleLike(force = null) {
    const next = force === null ? !state.liked : force;
    if (next === state.liked) return;
    state.liked = next;
    state.likes += next ? 1 : -1;
    renderState();
  }

  function bigLike() {
    toggleLike(true);
    pulse(burstHeart);
    if (navigator.vibrate) navigator.vibrate(18);
  }

  function toggleSave() {
    state.saved = !state.saved;
    state.saves += state.saved ? 1 : -1;
    renderState();
    showToast(state.saved ? "Saved to Favorites" : "Removed from Favorites");
  }

  function toggleFollow() {
    state.following = !state.following;
    renderState();
    showToast(state.following ? "Following @catventures" : "Unfollowed @catventures");
  }

  function toggleMute() {
    state.muted = !state.muted;
    video.muted = state.muted;
    showToast(state.muted ? "Sound off" : "Sound on");
  }

  function openSheet(sheet) {
    sheet.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  function closeSheet(sheet) {
    sheet.classList.add("hidden");
    document.body.style.overflow = "";
  }

  async function shareCurrent() {
    const shareData = {
      title: "CatTok",
      text: "Check out this GoPro cat adventure!",
      url: location.href
    };

    try {
      if (navigator.share) {
        await navigator.share(shareData);
        state.shares += 1;
        renderState();
        showToast("Shared");
      } else {
        openSheet(shareSheet);
      }
    } catch (error) {
      // User cancelled the native share sheet; no UI error required.
      if (error?.name !== "AbortError") openSheet(shareSheet);
    }
  }

  function seekFromPointer(event) {
    if (!video.duration || !Number.isFinite(video.duration)) return;

    const rect = progressTrack.getBoundingClientRect();
    const x = Math.min(Math.max(event.clientX - rect.left, 0), rect.width);
    video.currentTime = (x / rect.width) * video.duration;
  }

  function updateProgress() {
    const pct = video.duration ? (video.currentTime / video.duration) * 100 : 0;
    progressBar.style.width = `${pct}%`;
  }

  function addComment(text) {
    const article = document.createElement("article");
    article.className = "comment";
    article.innerHTML = `
      <div class="comment-avatar">😺</div>
      <div class="comment-body">
        <strong>@you</strong>
        <p></p>
        <button class="reply-button" type="button">Reply</button>
      </div>
      <button class="comment-like" type="button" aria-label="Like comment">♡</button>
    `;
    $(".comment-body p", article).textContent = text;
    commentsList.prepend(article);

    state.comments += 1;
    renderState();
    commentsList.scrollTop = 0;
  }

  // Video autoplay. Browsers allow muted autoplay more reliably.
  async function tryAutoplay() {
    loadingIndicator.classList.add("visible");
    video.muted = true;
    try {
      await video.play();
    } catch {
      video.pause();
      showToast("Tap the video to start");
    } finally {
      setTimeout(() => loadingIndicator.classList.remove("visible"), 400);
    }
  }

  // Clicking the video: single tap toggles pause; double tap likes.
  videoPage.addEventListener("click", (event) => {
    // Ignore clicks on UI controls.
    if (event.target.closest("button, nav, .caption-area, .progress-wrap, .sheet")) return;

    const now = Date.now();
    const delta = now - state.lastTap;

    if (delta > 0 && delta < 320) {
      clearTimeout(state.tapTimer);
      state.lastTap = 0;
      bigLike();
      return;
    }

    state.lastTap = now;
    clearTimeout(state.tapTimer);
    state.tapTimer = setTimeout(() => {
      togglePlay();
      state.lastTap = 0;
    }, 320);
  });

  // Mouse/touch-friendly seek bar.
  progressTrack.addEventListener("pointerdown", (event) => {
    state.draggingProgress = true;
    progressTrack.setPointerCapture?.(event.pointerId);
    seekFromPointer(event);
  });

  progressTrack.addEventListener("pointermove", (event) => {
    if (state.draggingProgress) seekFromPointer(event);
  });

  progressTrack.addEventListener("pointerup", () => {
    state.draggingProgress = false;
  });

  progressTrack.addEventListener("pointercancel", () => {
    state.draggingProgress = false;
  });

  // Playback state.
  video.addEventListener("timeupdate", updateProgress);
  video.addEventListener("loadedmetadata", updateProgress);
  video.addEventListener("waiting", () => loadingIndicator.classList.add("visible"));
  video.addEventListener("playing", () => loadingIndicator.classList.remove("visible"));
  video.addEventListener("volumechange", () => {
    state.muted = video.muted;
  });

  // Like.
  likeButton.addEventListener("click", () => {
    toggleLike();
    showToast(state.liked ? "Liked" : "Like removed");
  });

  // Comments.
  commentButton.addEventListener("click", () => {
    openSheet(commentsSheet);
    setTimeout(() => commentInput.focus({ preventScroll: true }), 180);
  });

  commentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = commentInput.value.trim();
    if (!text) return;
    addComment(text);
    commentInput.value = "";
    showToast("Comment posted");
  });

  // Comment likes, including dynamically added comments.
  commentsList.addEventListener("click", (event) => {
    const button = event.target.closest(".comment-like");
    if (!button) return;
    button.classList.toggle("liked");
    button.textContent = button.classList.contains("liked") ? "♥" : "♡";
  });

  // Save / bookmark.
  bookmarkButton.addEventListener("click", toggleSave);

  // Follow.
  profileButton.addEventListener("click", toggleFollow);

  // Sound.
  $("#musicButton").addEventListener("click", toggleMute);
  $("#musicLine").addEventListener("click", toggleMute);

  // Share.
  shareButton.addEventListener("click", shareCurrent);

  $$(".share-option").forEach(button => {
    button.addEventListener("click", async () => {
      const type = button.dataset.share;

      if (type === "copy") {
        try {
          await navigator.clipboard.writeText(location.href);
          showToast("Link copied");
        } catch {
          showToast("Copy is not available in this browser");
        }
      } else if (type === "whatsapp") {
        window.open(
          `https://wa.me/?text=${encodeURIComponent("Check out this GoPro cat adventure! " + location.href)}`,
          "_blank",
          "noopener,noreferrer"
        );
      } else if (type === "email") {
        window.location.href =
          `mailto:?subject=${encodeURIComponent("Funny cat GoPro video")}&body=${encodeURIComponent(location.href)}`;
      } else {
        showToast(type === "x" ? "X sharing opened" : "More sharing options");
      }

      state.shares += 1;
      renderState();
      closeSheet(shareSheet);
    });
  });

  // Close sheets.
  $$("[data-close-sheet]").forEach(element => {
    element.addEventListener("click", () => {
      closeSheet(commentsSheet);
      closeSheet(shareSheet);
    });
  });

  // Search.
  $("#searchButton").addEventListener("click", () => {
    searchOverlay.classList.remove("hidden");
    setTimeout(() => searchInput.focus(), 50);
  });

  $("#searchClose").addEventListener("click", () => {
    searchOverlay.classList.add("hidden");
  });

  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;
    showToast(`Searching for “${query}”`);
    searchOverlay.classList.add("hidden");
    searchInput.value = "";
  });

  // Bottom nav demo.
  $$(".bottom-item").forEach(item => {
    item.addEventListener("click", () => {
      $$(".bottom-item").forEach(x => x.classList.remove("active"));
      item.classList.add("active");
      showToast(`${item.dataset.nav.charAt(0).toUpperCase() + item.dataset.nav.slice(1)} selected`);
    });
  });

  $("#createButton").addEventListener("click", () => showToast("Create button pressed"));

  $("#liveButton").addEventListener("click", () => showToast("LIVE section"));

  // Keyboard shortcuts for laptop / desktop testing.
  document.addEventListener("keydown", (event) => {
    if (event.target.matches("input, textarea")) return;

    if (event.code === "Space") {
      event.preventDefault();
      togglePlay();
    } else if (event.key.toLowerCase() === "m") {
      toggleMute();
    } else if (event.key.toLowerCase() === "l") {
      toggleLike();
      showToast(state.liked ? "Liked" : "Like removed");
    } else if (event.key === "ArrowRight" && video.duration) {
      video.currentTime = Math.min(video.duration, video.currentTime + 5);
    } else if (event.key === "ArrowLeft" && video.duration) {
      video.currentTime = Math.max(0, video.currentTime - 5);
    } else if (event.key === "Escape") {
      closeSheet(commentsSheet);
      closeSheet(shareSheet);
      searchOverlay.classList.add("hidden");
    }
  });

  // Swipe up/down demo: prevents accidental page scroll and gives feedback.
  let touchStartY = 0;
  let touchStartX = 0;

  videoPage.addEventListener("touchstart", (event) => {
    if (event.touches.length !== 1) return;
    touchStartY = event.touches[0].clientY;
    touchStartX = event.touches[0].clientX;
  }, { passive: true });

  videoPage.addEventListener("touchend", (event) => {
    if (!touchStartY || event.changedTouches.length !== 1) return;
    const endY = event.changedTouches[0].clientY;
    const endX = event.changedTouches[0].clientX;
    const dy = endY - touchStartY;
    const dx = endX - touchStartX;

    if (Math.abs(dy) > 100 && Math.abs(dy) > Math.abs(dx) * 1.3) {
      showToast(dy < 0 ? "Next video" : "Previous video");
    }

    touchStartY = 0;
    touchStartX = 0;
  }, { passive: true });

  // Protect against accidental drag-and-drop navigation.
  window.addEventListener("dragover", e => e.preventDefault());
  window.addEventListener("drop", e => e.preventDefault());

  renderState();
  tryAutoplay();
})();
