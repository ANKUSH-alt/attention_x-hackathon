# ✂️ AI Viral Shorts Creator - Hackathon Submission

This project transforms long-form horizontal content into engaging 9:16 vertical shorts using a multi-modal AI pipeline.

## 🏗 System Architecture

1. **Transcription**: **Gemini 2.5 Flash** (Multimodal) for lightning-fast transcription without heavy local models.
2. **Audio Intelligence**: **Librosa** energy mapping to detect hype peaks.
3. **AI Editor**: **Gemini 2.5 Flash** acts as a lead editor, selecting snippets that summarize the video narrative.
4. **Computer Vision**: **OpenCV** face tracking to ensure the subject is always centered in the vertical crop.
5. **Captioning**: Frame-by-frame rendering with **Pillow** to create high-retention karaoke captions.

### Optimization Notes
- **Removed Whisper/Torch**: Significantly reduced deployment time and server startup by switching to Gemini API for transcription.
- **FFmpeg Inclusion**: Added `packages.txt` for seamless cloud execution.

## 🚀 Deployment Guide

### Deploying to GitHub
I have already initialized the git repo. Run this in your terminal to finish:
```bash
git push -u origin main
```

### Deploying to Streamlit Cloud (Recommended)
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Connect this repo.
3. In **Advanced Settings**, add your Secret: `GEMINI_API_KEY = "your-key"`.

### Tech Stack
- **AI**: Gemini 2.5 Flash (Transcription & Summarization)
- **Video**: MoviePy, OpenCV, Librosa
- **UI**: Streamlit (with Custom CSS)
