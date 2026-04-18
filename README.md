# AI Viral Shorts Creator ✂️

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://attentionx-hackathon-henfjhgvip5tl99x3eyvbi.streamlit.app/)

An automated system that transforms long-form videos (lectures, podcasts, workshops) into viral-ready short-form content for platforms like TikTok, Instagram Reels, and YouTube Shorts.

**🔗 Live Demo:** [attentionx-hackathon.streamlit.app](https://attentionx-hackathon-henfjhgvip5tl99x3eyvbi.streamlit.app/)

## 📺 Demo Video

[![Watch Demo Video](https://img.shields.io/badge/▶%20Watch%20Demo-Google%20Drive-blue?style=for-the-badge&logo=googledrive)](https://drive.google.com/file/d/1KUEHVqhlyFNqfq-nm8sq4CBXbVRDmYjt/view?usp=drive_link)

> Click the button above to watch the full demo of AI Viral Shorts Creator in action.

## ✨ Features

1. **AI Storyboarding (Summarization)**
   - Transcribes entire videos using **Gemini 2.5 Flash** (Multimodal API) for high accuracy without local heavy models.
   - Intelligently selects discrete segments that summarize the entire video into a <60s viral short.
   - Automatically detects audio energy peaks (loud/excited moments) using **Librosa** to guide the selection.

2. **Smart Face-Tracking (9:16 Crop)**
   - Converts standard 16:9 horizontal videos to 9:16 vertical format.
   - Automatically utilizes **OpenCV Haar-Cascades** to track the speaker's face and perfectly center them in every frame.

3. **Dynamic Karaoke Captions**
   - Precise word-level highlighter based on STT timestamps.
   - Features high-contrast hook headlines injected via **Pillow**.

## 🛠 Tech Stack

- **AI/ML**: Google Gemini 2.5 Flash (Transcription & Curation)
- **Video/Vision**: MoviePy (Editing), OpenCV (Face Tracking), Librosa (Audio), Pillow (Rendering)
- **Frontend**: Streamlit

## 🚀 Deployment

### Live link
The application is deployed at: [https://attentionx-hackathon-henfjhgvip5tl99x3eyvbi.streamlit.app/](https://attentionx-hackathon-henfjhgvip5tl99x3eyvbi.streamlit.app/)

### 📁 Directory Structure
```
.
├── app.py                  # Streamlit Dashboard
├── core/
│   ├── analyzer.py         # Gemini 2.5 Logic (Transcription & Summarization)
│   └── editor.py           # OpenCV Face tracking & Concatenation engine
├── requirements.txt        # Python dependencies (Optimized)
├── packages.txt            # System dependencies (FFmpeg)
└── README.md               # Documentation
```
