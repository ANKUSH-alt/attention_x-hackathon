import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

def find_center_x(clip):
    """Find average face center X to use for smart cropping using OpenCV."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    center_xs = []
    # check 1 frame per second
    for t in range(0, int(clip.duration), max(1, int(clip.duration // 5))):
        frame = clip.get_frame(t)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        scale = 640.0 / gray.shape[1]
        small_gray = cv2.resize(gray, (0, 0), fx=scale, fy=scale)
        faces = face_cascade.detectMultiScale(small_gray, scaleFactor=1.1, minNeighbors=4)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            cx = (x + w / 2) / 640.0
            center_xs.append(cx)
            break
            
    if center_xs:
        return sum(center_xs) / len(center_xs)
    return 0.5 # default center

def generate_video(video_path, segments, transcript_result, hook_headline, output_path):
    main_clip = VideoFileClip(video_path)
    processed_clips = []
    first_segment = True
    
    for seg in segments:
        st = max(0, seg["start_time"])
        et = min(main_clip.duration, seg["end_time"])
        if st >= et: continue
            
        subclip = main_clip.subclip(st, et)
        w, h = subclip.size
        target_w = int(h * 9 / 16)
        
        if w > target_w:
            center_x_rel = find_center_x(subclip)
            center_x_abs = int(w * center_x_rel)
            x1 = max(0, center_x_abs - target_w // 2)
            x2 = x1 + target_w
            if x2 > w:
                x2 = w
                x1 = w - target_w
            subclip = subclip.crop(x1=x1, y1=0, x2=x2, y2=h)
            
        w, h = subclip.size
        words = []
        for transcript_segment in transcript_result.get("segments", []):
            for w_info in transcript_segment.get("words", []):
                if w_info["end"] >= st and w_info["start"] <= et:
                    words.append(w_info)
                    
        phrases = []
        current_phrase = []
        for w_info in words:
            current_phrase.append(w_info)
            word_text = w_info["word"].strip()
            if len(current_phrase) >= 5 or word_text.endswith(('.', ',', '?', '!')):
                phrases.append({
                    "words": current_phrase,
                    "start": current_phrase[0]["start"],
                    "end": current_phrase[-1]["end"]
                })
                current_phrase = []
        if current_phrase:
            phrases.append({
                "words": current_phrase,
                "start": current_phrase[0]["start"],
                "end": current_phrase[-1]["end"]
            })
            
        try:
            font_large = ImageFont.truetype("Arial.ttf", int(h * 0.05))
            font_headline = ImageFont.truetype("Arial-Bold.ttf", int(h * 0.06))
        except (IOError, OSError):
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", int(h * 0.05))
                font_headline = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", int(h * 0.06))
            except (IOError, OSError):
                font_large = ImageFont.load_default()
                font_headline = ImageFont.load_default()
                
        def make_render_func(st_offset, is_first):
            def render_captions(get_frame, t):
                frame = get_frame(t)
                global_t = t + st_offset
                img = Image.fromarray(frame)
                draw = ImageDraw.Draw(img)
                
                if is_first and t < 3.0 and hook_headline:
                    try:
                        head_bbox = draw.textbbox((0, 0), hook_headline, font=font_headline)
                        head_w = head_bbox[2] - head_bbox[0]
                        head_h = head_bbox[3] - head_bbox[1]
                    except AttributeError:
                        head_w, head_h = draw.textsize(hook_headline, font=font_headline)
                    bx = (w - head_w) // 2
                    by = int(h * 0.15)
                    padding = 15
                    draw.rectangle([bx-padding, by-padding, bx+head_w+padding, by+head_h+padding], fill=(255, 0, 0))
                    draw.text((bx, by), hook_headline, font=font_headline, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))
                
                active_phrase = None
                for p in phrases:
                    if p["start"] <= global_t <= p["end"] + 0.5:
                        active_phrase = p
                        break
                        
                if active_phrase:
                    parts = []
                    total_width = 0
                    for w_info in active_phrase["words"]:
                        word_text = w_info["word"].strip() + " "
                        is_active = w_info["start"] <= global_t <= w_info["end"]
                        try:
                            w_bbox = draw.textbbox((0, 0), word_text, font=font_large)
                            word_w = w_bbox[2] - w_bbox[0]
                            word_h = w_bbox[3] - w_bbox[1]
                        except AttributeError:
                            word_w, word_h = draw.textsize(word_text, font=font_large)
                            
                        parts.append({"text": word_text, "width": word_w, "height": word_h, "active": is_active})
                        total_width += word_w
                        
                    start_x = (w - total_width) // 2
                    y = int(h * 0.8)
                    
                    max_h = max([pt["height"] for pt in parts] + [0])
                    padding = 10
                    draw.rectangle([start_x - padding, y - padding, start_x + total_width + padding, y + max_h + padding], fill=(0, 0, 0, 150))
                    
                    current_x = start_x
                    for pt in parts:
                        color = (255, 255, 0) if pt["active"] else (255, 255, 255)
                        draw.text((current_x, y), pt["text"], font=font_large, fill=color, stroke_width=2, stroke_fill=(0, 0, 0))
                        current_x += pt["width"]
                        
                return np.array(img)
            return render_captions
            
        render_func = make_render_func(st, first_segment)
        processed_clips.append(subclip.fl(render_func))
        first_segment = False
        
    final_clip = concatenate_videoclips(processed_clips)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', threads=4)
    main_clip.close()
