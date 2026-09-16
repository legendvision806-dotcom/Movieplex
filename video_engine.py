import os
import json
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import moviepy as mp
from google import genai

def generate_history_script(api_key: str, topic: str) -> dict:
    """Generates a structured multi-scene historical script with Gemini."""
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert history documentary producer. Create a detailed 5-minute documentary script on the topic: '{topic}'.
    Format your response EXACTLY as a JSON object with a key 'scenes' containing a list of 10 to 12 distinct scenes.
    Each scene must have:
    - 'scene_num': integer
    - 'narration': Detailed narrative text for voiceover.
    - 'visual_description': Brief text summarizing key visuals/title for the screen frame.
    
    Ensure coverage includes historical context, key figures, critical battles/events, and lasting impacts.
    Return ONLY valid JSON.
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_text)

def create_scene_frame(title: str, text: str, output_path: str, resolution=(1280, 720)):
    """Generates a stylish, fast, animated-style frame with text fallback graphics."""
    img = Image.new('RGB', resolution, color=(18, 18, 24))
    draw = ImageDraw.Draw(img)
    
    # Decorative historical border
    draw.rectangle([20, 20, resolution[0]-20, resolution[1]-20], outline=(212, 175, 55), width=4)
    draw.rectangle([30, 30, resolution[0]-30, resolution[1]-30], outline=(100, 100, 120), width=1)
    
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except IOError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Title & Text overlays
    draw.text((60, 60), title.upper(), fill=(212, 175, 55), font=title_font)
    
    # Simple word wrap
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line + " " + word) < 55:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
        
    y_text = 160
    for line in lines[:10]:
        draw.text((60, y_text), line, fill=(240, 240, 240), font=body_font)
        y_text += 40

    img.save(output_path)

def render_history_video(script_data: dict, progress_bar) -> str:
    """Assembles audio clips and frames into a cohesive MP4 video."""
    scenes = script_data.get('scenes', [])
    clips = []
    
    os.makedirs("temp_render", exist_ok=True)
    total_scenes = len(scenes)

    for idx, scene in enumerate(scenes):
        narration = scene['narration']
        visual = scene['visual_description']
        
        # 1. Generate Voiceover
        audio_path = f"temp_render/audio_{idx}.mp3"
        tts = gTTS(text=narration, lang='en', slow=False)
        tts.save(audio_path)
        
        audio_clip = mp.AudioFileClip(audio_path)
        duration = audio_clip.duration + 0.5  # Slight buffer
        
        # 2. Generate Frame Image
        image_path = f"temp_render/frame_{idx}.png"
        create_scene_frame(f"Scene {idx+1}: {visual[:30]}...", narration, image_path)
        
        # 3. Create Video Clip
        img_clip = mp.ImageClip(image_path).set_duration(duration)
        img_clip = img_clip.set_audio(audio_clip)
        
        clips.append(img_clip)
        progress_bar.progress((idx + 1) / total_scenes)

    # 4. Concatenate scenes into final video
    final_clip = mp.concatenate_videoclips(clips, method="compose")
    output_filename = "history_documentary.mp4"
    
    final_clip.write_videofile(
        output_filename, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        preset="ultrafast"  # Maximum rendering speed
    )
    
    # Cleanup individual files
    final_clip.close()
    for c in clips:
        c.close()
        
    return output_filename
