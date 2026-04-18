# AI Viral Shorts Creator ✂️

An automated system that transforms long-form videos (lectures, podcasts, workshops) into viral-ready short-form content for platforms like TikTok, Instagram Reels, and YouTube Shorts.

## ✨ Features

1. **AI Storyboarding (Summarization)**
   - Transcribes entire videos and maps them precisely using **OpenAI Whisper**.
   - Leverages **Gemini 2.5 Flash** to read the full context and intelligently select discrete segments that summarize the entire video into a <60s viral short.
   - Automatically detects audio energy peaks (loud/excited moments) using **Librosa** to guide the selection.

2. **Smart Face-Tracking (9:16 Crop)**
   - Converts standard 16:9 horizontal videos to 9:16 vertical format.
   - Automatically utilizes **OpenCV Haar-Cascades** to track the speaker's face and perfectly center them in every frame.

3. **Dynamic Karaoke Captions**
   - Precise word-level highlighter based on STT timestamps.
   - Features high-contrast hook headlines injected via **Pillow**.

## 🛠 Tech Stack

- **AI/ML**: Google Gemini 2.5 Flash (Curation), OpenAI Whisper (Transcription)
- **Video/Vision**: MoviePy (Editing), OpenCV (Face Tracking), Librosa (Audio), Pillow (Rendering)
- **Frontend**: Streamlit

## 🚀 Deployment

### Recommended: Streamlit Community Cloud (Free & Easy)
1. Push this code to your GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your repo and set main file to `app.py`.
4. **Important**: Go to `Settings > Secrets` and add your API key:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```

### Why not Vercel?
Streamlit is a stateful Python server and processing videos requires persistent memory/disk and long timeouts. Vercel's serverless functions are limited to 10-60s timeouts and small payloads, which will crash during video processing.

## 📁 Directory Structure
```
.
├── app.py                  # Modernized Dashboard
├── core/
│   ├── analyzer.py         # Gemini 2.5 Logic & Whisper bypass
│   └── editor.py           # OpenCV Face tracking & Concatenation engine
├── .streamlit/             # (Ignored) Secret local config
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```
