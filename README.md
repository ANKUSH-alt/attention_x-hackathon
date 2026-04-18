# AI Viral Shorts Creator ✂️

An automated system that transforms long-form videos (lectures, podcasts, workshops) into viral-ready short-form content for platforms like TikTok, Instagram Reels, and YouTube Shorts.

## ✨ Features

1. **Emotional Peak Detection**
   - Transcribes audio and maps it precisely using **OpenAI Whisper**
   - Analyzes audio volume and energy spikes using **Librosa** to identify the most hype/energetic moments.
   - Leverages **Gemini 1.5 Flash** to analyze transcript chunks and energy peaks to find the single most "shareable" 30-60s segment, with a punchy viral hook headline.

2. **Smart Vertical Cropping**
   - Converts standard 16:9 horizontal videos to 9:16 vertical format.
   - Automatically utilizes **MediaPipe Face Detection (Computer Vision)** to track the speaker's face and perfectly center them.

3. **Dynamic Caption Generation**
   - Generates karaoke-style animated captions.
   - Features precise timing based on Whisper's word-level timestamps.
   - Highlights the currently spoken word, ensuring excellent retention rates.
   - Injects heavy, high-contrast headline hooks over the video for maximum engagement.

## 🛠 Tech Stack

- **AI/ML Layer**: Google Gemini 1.5 Flash (Analysis/Curation), OpenAI Whisper (STT)
- **Video & Audio Processing**: MoviePy (Editing), Librosa (Audio analysis), MediaPipe (CV Face Tracking), Pillow/OpenCV (Drawing frames)
- **Frontend App**: Streamlit

## 🚀 Quick Start

1. Create a Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure system dependencies like `ffmpeg` are installed: `brew install ffmpeg` on macOS or `sudo apt install ffmpeg` on Linux)*

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Usage:
   - Provide your **Google Gemini API Key**
   - Upload any long-form video (.mp4, .mov, etc.)
   - Wait for the processing to finish, then download your viral short!

## 📁 Directory Structure
```
.
├── app.py                  # Main Streamlit dashboard
├── core/
│   ├── analyzer.py         # AI extraction, librosa energy mapping, and Gemini curation
│   └── editor.py           # MoviePy automated editing, face tracking, and custom captions
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

## ⚖️ Evaluation Criteria Addressed
- **Impact & Innovation**: Solves a major pain point by truly integrating multi-modal AI (audio analysis + LLM transcript analysis + CV for video).
- **Technical Execution**: Modularized code, automated frame-by-frame caption generation bypassing buggy libraries, dynamic layout handling.
- **User Experience**: One-click UI via Streamlit with a clean minimal design showing active progress steps.
