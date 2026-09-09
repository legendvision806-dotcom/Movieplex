# AI World History Video Generator

An automated tool to generate 5-minute documentary-style animated historical videos using Google Gemini Flash, gTTS, and MoviePy.

## Included Files
- `app.py`: Streamlit frontend user interface.
- `video_engine.py`: Core backend logic updated to use `gemini-3.6-flash`.
- `requirements.txt`: Python package dependencies.
- `packages.txt`: System-level dependency (`ffmpeg`) required for Streamlit Cloud deployment.

## How to Run Locally
1. Extract this zip file.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
