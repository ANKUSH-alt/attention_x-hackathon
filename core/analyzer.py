import os
import whisper
import librosa
import numpy as np
import google.generativeai as genai
import json
import subprocess

def extract_audio(video_path, audio_path):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()

def analyze_audio_energy(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    # calculate rms energy
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    
    # get top 10% peaks
    threshold = np.percentile(rms, 90)
    peaks = []
    for t, r in zip(times, rms):
        if r > threshold:
            peaks.append({"time": float(t), "energy": float(r)})
            
    # aggregate close peaks
    aggregated_peaks = []
    for p in peaks:
        if not aggregated_peaks or p["time"] - aggregated_peaks[-1]["time"] > 5.0:
            aggregated_peaks.append(p)
            
    return aggregated_peaks

def transcribe_audio(audio_path):
    # Load model (using 'tiny' for lightning fast speeds since 'base' took too long)
    model = whisper.load_model("tiny")
    
    # Load audio explicitly into a NumPy array at 16kHz
    # This fully bypasses Whisper's internal FFmpeg call which crashes when FFmpeg binary is missing
    audio_data, _ = librosa.load(audio_path, sr=16000)
    
    result = model.transcribe(audio_data, word_timestamps=True)
    return result

def summarize_video_into_short(transcript_result, top_peaks, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Format the transcript with timestamps
    formatted_transcript = ""
    for seg in transcript_result["segments"]:
        formatted_transcript += f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}\n"
        
    peaks_str = ", ".join([f"{p['time']:.2f}s" for p in top_peaks[:10]])
    
    prompt = f"""
You are an expert short-form video producer (TikTok, Reels, Shorts).
Analyze the following transcript from a video.
I have also detected audio energy peaks (loud/excited moments) at these timestamps: {peaks_str}

Summarize the ENTIRE video into a viral short by selecting the most impactful, sequential segments from the transcript that tell the core story or deliver the main value.
The final compiled short MUST:
1. Be under 60 seconds long in total when combined.
2. Have a strong hook (starts with an interesting statement).
3. Connect logically even though parts are cut.

Output ONLY a JSON object (no markdown formatting, no comments) with the following structure:
{{
    "hook_headline": "A catchy, short 3-5 word headline overlay text for the first few seconds",
    "segments": [
        {{"start_time": <float start>, "end_time": <float end>}},
        {{"start_time": <float start>, "end_time": <float end>}}
    ],
    "justification": "Brief reason why this summary is viral-worthy"
}}

Transcript:
{formatted_transcript}
"""
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    try:
        text = response.text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        # fallback
        return {
            "hook_headline": "Viral Summary",
            "segments": [
                {"start_time": 0.0, "end_time": min(15.0, transcript_result["segments"][-1]["end"])},
                {"start_time": max(0.0, transcript_result["segments"][-1]["end"] - 15.0), "end_time": transcript_result["segments"][-1]["end"]}
            ],
            "justification": "Fallback summary"
        }
