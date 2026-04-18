import streamlit as st
import os
import shutil
import tempfile
from core.analyzer import extract_audio, analyze_audio_energy, transcribe_audio, summarize_video_into_short
from core.editor import generate_video

st.set_page_config(page_title="Viral Shorts Creator", layout="wide", page_icon="✂️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

/* Animated gradient background spanning the whole app */
.stApp {
    background: linear-gradient(-45deg, #050511, #130a1e, #0a0514, #12050f) !important;
    background-size: 400% 400% !important;
    animation: gradientBG 15s ease infinite !important;
    color: white !important;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glowing Gradient Headers */
h1, h2, h3 {
    font-weight: 900 !important;
}

h1 {
    background: -webkit-linear-gradient(45deg, #ff007f, #7928ca);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glowpulse 3s infinite alternate;
}

@keyframes glowpulse {
    from { filter: drop-shadow(0 0 5px rgba(255, 0, 127, 0.2)); }
    to { filter: drop-shadow(0 0 15px rgba(121, 40, 202, 0.6)); }
}

/* Glassmorphism sidebar */
[data-testid="stSidebar"] {
    background: rgba(20, 20, 30, 0.3) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}

/* Premium Primary Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff007f, #7928ca) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    transform: scale(1);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

.stButton>button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 25px rgba(255, 0, 127, 0.5) !important;
}

.stButton>button:active {
    transform: translateY(1px) scale(0.98) !important;
}

/* Glassmorphism File Uploader Area */
[data-testid="stFileUploadDropzone"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border-radius: 20px !important;
    border: 2px dashed rgba(255,255,255,0.15) !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.4s ease !important;
    padding: 40px !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: #ff007f !important;
    background: rgba(255, 255, 255, 0.08) !important;
    box-shadow: inset 0 0 20px rgba(255,0,127,0.1) !important;
}

/* Styling the Status boxes */
[data-testid="stStatusWidget"] {
    background: rgba(20, 20, 25, 0.6) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(5px) !important;
}

/* Make Video Player display massive like a phone screen */
[data-testid="stVideo"] {
    display: flex;
    justify-content: center;
    background: rgba(0,0,0,0.5);
    border-radius: 24px;
    padding: 10px;
}
[data-testid="stVideo"] video {
    height: 50vh !important;
    width: 50% !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8) !important;
    object-fit: contain !important;
}
</style>
""", unsafe_allow_html=True)

st.title("✂️ AI Viral Shorts Creator")
st.markdown("Transform long-form videos into viral-ready vertical shorts with **smart cropping**, **karaoke captions**, and **emotional peak detection**.")

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

uploaded_file = st.file_uploader("Upload Long-Form Video", type=["mp4", "mov", "mkv"])

if uploaded_file is not None and api_key:
    if st.button("Generate Short", use_container_width=True, type="primary"):
        with st.spinner("Processing your video... This might take a few minutes."):
            try:
                # 1. Save uploaded file to temp
                temp_dir = tempfile.mkdtemp()
                video_path = os.path.join(temp_dir, "input_video.mp4")
                audio_path = os.path.join(temp_dir, "extracted_audio.wav")
                output_path = os.path.join(temp_dir, "output_short.mp4")
                
                with open(video_path, "wb") as f:
                    f.write(uploaded_file.read())
                    
                st.status("Extracting Audio...")
                extract_audio(video_path, audio_path)
                
                st.status("Detecting Emotional Peaks...")
                peaks = analyze_audio_energy(audio_path)
                
                st.status("Transcribing with Whisper...")
                transcript = transcribe_audio(audio_path)
                
                st.status("Gemini extracting the best summary chunks...")
                viral_segment = summarize_video_into_short(transcript, peaks, api_key)
                
                segments = viral_segment.get("segments", [{"start_time": 0.0, "end_time": 30.0}])
                hook = viral_segment.get("hook_headline", "Check this out!")
                justification = viral_segment.get("justification", "Automatic pick.")
                
                st.markdown("### 📊 AI Curation Report")
                rpt_col1, rpt_col2 = st.columns([2, 1])
                with rpt_col1:
                    st.info(f"**Main Hook Headline:** {hook}")
                    st.markdown(f"**AI Justification:** {justification}")
                with rpt_col2:
                    st.markdown("**✂️ Tracked Segments:**")
                    for i, s in enumerate(segments):
                        st.markdown(f"- **Clip {i+1}:** `{s['start_time']:.1f}s` ➔ `{s['end_time']:.1f}s`")
                
                st.status("Cutting, Cropping, and concatenating your video summary...")
                generate_video(
                    video_path=video_path,
                    segments=segments,
                    transcript_result=transcript,
                    hook_headline=hook,
                    output_path=output_path
                )
                
                st.balloons()
                st.subheader("Your Viral Short is Ready!")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Video",
                        data=file,
                        file_name="viral_short.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                if 'temp_dir' in locals():
                    shutil.rmtree(temp_dir, ignore_errors=True)
elif uploaded_file and not api_key:
    st.warning("Please set the \`GEMINI_API_KEY\` environment variable before running the app. Example: `export GEMINI_API_KEY='your-key'`")

st.markdown("---")
st.markdown("### 🚀 Technical Engine Under the Hood:")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**1. Emotional Intelligence**\nAnalyzes audio volume, frequency spikes, and energy using `librosa` to find where the action is.")
with col2:
    st.markdown("**2. AI Script & Storyboarding**\n`Gemini 2.5 Flash` reads the entire transcript and reconstructs a cohesive summary while `Whisper` handles word-level timing.")
with col3:
    st.markdown("**3. Computer Vision Crop**\nUses `OpenCV` Haar Cascades to track faces in real-time, centering them perfectly for the 9:16 vertical format.")
