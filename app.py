import streamlit as st
import os
from video_engine import generate_history_script, render_history_video

st.set_page_config(page_title="AI World History Video Generator", layout="wide", page_icon="📜")

st.title("📜 AI Historical Video Generator")
st.markdown("Generate full-length animated documentary videos on world history, ancient empires, and historic wars.")

# Sidebar for configuration
st.sidebar.header("🔑 Credentials & Settings")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

st.sidebar.info("""
**Supported Topics:**
- Subcontinent Wars (e.g., Battle of Plassey, Mughal Empire)
- Roman Empire & Punic Wars
- World Wars & Ancient Civilizations
""")

# Pre-set topic selector or custom input
topic_option = st.selectbox(
    "Select or Type a Historical Topic:",
    [
        "The Punic Wars and the Rise of Rome",
        "The Mughal Empire and the Battle of Panipat",
        "The Alexander the Great Conquests",
        "World War I: The Western Front",
        "The Maurya Empire under Ashoka the Great",
        "Custom Topic..."
    ]
)

if topic_option == "Custom Topic...":
    topic = st.text_input("Enter your custom historical topic:")
else:
    topic = topic_option

if st.button("🚀 Generate 5-Minute Documentary Video", type="primary"):
    if not api_key:
        st.error("Please enter a valid Google API Key in the sidebar.")
    elif not topic:
        st.error("Please provide a valid historical topic.")
    else:
        try:
            st.info("Step 1/2: Synthesizing script using Gemini 3.6 Flash...")
            script = generate_history_script(api_key, topic)
            
            st.success(f"Script generated with {len(script.get('scenes', []))} detailed scenes!")
            
            st.info("Step 2/2: Rendering voiceovers and visual scenes...")
            progress_bar = st.progress(0.0)
            
            video_file = render_history_video(script, progress_bar)
            
            st.success("Video rendering complete!")
            
            # Display and download options
            st.video(video_file)
            
            with open(video_file, "rb") as file:
                st.download_button(
                    label="💾 Download Documentary MP4",
                    data=file,
                    file_name=f"{topic.replace(' ', '_')}.mp4",
                    mime="video/mp4"
                )
        except Exception as e:
            st.error(f"An error occurred during generation: {str(e)}")
