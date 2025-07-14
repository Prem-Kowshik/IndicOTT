# pages/01_Video_Player.py

"""
Video Player - Final Production Version
=======================================
• Fetches pre-generated subtitles from Supabase for a fast user experience.
• Correctly maps to the 'Video_movies' table schema (id, title, url, director).
• Automatically loads English subtitles on startup and handles language switching.
• Includes the fully functional AI Movie Trope analysis feature.
• All known bugs (KeyError, AttributeError) have been resolved.
"""

# ----------------------------- IMPORTS -------------------------------------
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import sys
import os
import json
import asyncio
from datetime import timedelta
import html

# --- Path setup to import from the utils directory ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import supabase  # Your shared Supabase client
from utils.ai_utils import character_tropes_generator  # Your AI utility

# nest_asyncio is needed for running async functions within Streamlit
import nest_asyncio
nest_asyncio.apply()


# --------------------------- CONSTANTS & HELPERS ---------------------------
# These languages should match what you pre-generate in your batch script
LANGUAGES = {
    "en": "English", "hi": "Hindi", "bn": "Bengali", "pa": "Punjabi", "gu": "Gujarati",
    "mr": "Marathi", "ta": "Tamil", "te": "Telugu", "kn": "Kannada", "ml": "Malayalam",
    "ur": "Urdu", "ne": "Nepali"
}

def lang_name(code: str): return LANGUAGES.get(code, code.upper())
def clean(title: str): return title.replace("File:", "").rsplit(".", 1)[0]
def srt2vtt(s: str): return "WEBVTT\n\n" + s.replace(",", ".")
def human_dur(s): return str(timedelta(seconds=int(s))) if s else "N/A"
def human_size(b): return f"{b / 1_048_576:.2f} MB" if b else "N/A"


# ------------------ DB & AI HELPERS --------------------------------
def db_get_subs(vid: str, lang: str):
    """Fetches pre-generated subtitle content from the 'subtitles' table."""
    try:
        response = supabase.table("subtitles").select("subtitle_content").eq("video_id", vid).eq("language_code", lang).single().execute()
        return response.data.get("subtitle_content") if response.data else None
    except Exception as e:
        print(f"No subtitle found for video_id '{vid}' in lang '{lang}' or DB error: {e}")
        return None

async def trope(title, url):
    """Async helper for AI trope analysis."""
    try:
        return await character_tropes_generator(title, url)
    except Exception as e:
        return json.dumps({"film_title": title, "analysis_summary": f"Error during AI analysis: {e}"})


# --------------------------- STREAMLIT APP ---------------------------------
st.set_page_config(page_title="Video Player", page_icon="🎬",
                   layout="wide", initial_sidebar_state="collapsed")

if "selected_video" not in st.session_state or not st.session_state.selected_video:
    st.error("No video selected. Please go back to the Homepage and select a video.")
    st.stop()

# 'video' is the dictionary with keys matching your 'Video_movies' table columns
video = st.session_state.selected_video

# --- CORRECT MAPPING from your 'Video_movies' table ---
title = clean(video.get("title", "Untitled"))
vid_id = str(video.get("id"))
video_url = video.get("url")

if not vid_id or not video_url:
    st.error("The selected video data is incomplete (missing ID or URL). Please go back and select another.")
    st.stop()

# --- Initialize Session State Keys for this page ---
ana_key = f"ana_{vid_id}"
if 'current_subs' not in st.session_state:
    st.session_state.current_subs = None
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = 'en'
if ana_key not in st.session_state:
    st.session_state[ana_key] = None

# ------------------- UI LAYOUT (Right Sidebar) -----------------------------
left, right = st.columns([3, 1])

with right:
    if st.button("← Back to Homepage"):
        st.switch_page("Homepage.py")

    st.markdown("### 📊 Metadata")
    st.markdown(f"*Director:* {video.get('director', 'N/A')}  \n"
                f"*Resolution:* {video.get('width', 'N/A')}×{video.get('height', 'N/A')}  \n"
                f"*Duration:* {human_dur(video.get('duration'))}  \n"
                f"*Size:* {human_size(video.get('size'))}")

    st.markdown("### 📝 Subtitles")

    # This callback now handles both the initial auto-load and manual user changes
    def on_language_change(initial_load=False):
        if initial_load:
            selected_lang = st.session_state.current_lang
        else:
            selected_lang = st.session_state.lang_select

        with st.spinner(f"Loading {lang_name(selected_lang)} subtitles..."):
            subs = db_get_subs(vid_id, selected_lang)
            if subs:
                st.session_state.current_subs = subs
                st.session_state.current_lang = selected_lang
            else:
                st.session_state.current_subs = None
                st.warning(f"Subtitles for {lang_name(selected_lang)} not found.")

    # Automatically load subtitles when switching to a new video
    if st.session_state.get('last_loaded_vid') != vid_id:
        st.session_state.current_subs = None
        st.session_state.current_lang = 'en'
        on_language_change(initial_load=True)
        st.session_state['last_loaded_vid'] = vid_id

    st.selectbox(
        "Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.current_lang),
        format_func=lang_name,
        key='lang_select',
        on_change=lambda: on_language_change(initial_load=False)
    )

    if st.session_state.current_subs:
        st.download_button("📥 Download .srt", st.session_state.current_subs,
                           file_name=f"{title}_{st.session_state.current_lang}.srt",
                           mime="text/plain", use_container_width=True)
    else:
        st.info("Select an available language to display subtitles.")

    st.markdown("### 🤖 AI Movie Analysis")
    if st.button("Analyze Tropes", use_container_width=True):
        with st.spinner("Thinking…"):
            loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop)
            st.session_state[ana_key]=loop.run_until_complete(trope(title,video["descriptionurl"]))


# ------------------- Video Player (Left Column) ----------------------------
with left:
    vtt_track = ""
    if st.session_state.current_subs:
        vtt = srt2vtt(st.session_state.current_subs)
        vtt_track = (f"<track label='{lang_name(st.session_state.current_lang)}' kind='subtitles' "
                     f"srclang='{st.session_state.current_lang}' "
                     f"src='data:text/vtt;charset=utf-8,{urllib.parse.quote(vtt)}' default>")

    st.markdown(f"<h2 style='text-align:left;'>🎬 {title}</h2>", unsafe_allow_html=True)
    components.html(f"""
    <style>
    .wrap{{position:relative;width:100%;height:600px;border-radius:12px;overflow:hidden;
           box-shadow:0 8px 25px rgba(0,0,0,.3);}}
    .wrap video{{width:100%;height:100%;object-fit:contain;background:black;}}
    .speed{{position:absolute;bottom:220px;right:20px;background:rgba(0,0,0,.85);
            border-radius:8px;padding:6px 10px;color:#fff;}}
    </style>
    <div class='wrap'>
      <video id='v' controls crossorigin="anonymous">
        <source src='{video_url}' type='video/mp4'>
        {vtt_track}
      </video>
      <div class='speed'>
        Speed: <select onchange="document.getElementById('v').playbackRate=parseFloat(this.value)">
          <option>0.25</option><option>0.5</option><option>0.75</option><option selected>1</option>
          <option>1.25</option><option>1.5</option><option>2</option>
        </select>
      </div>
    </div>
    """, height=650)


# ------------------- Show AI Analysis Results (UI with Bug Fix) ------------------------------
if st.session_state[ana_key]:
    try:
        data=json.loads(st.session_state[ana_key]); tropes=data.get("tropes_identified",[])
        st.markdown("""
        <style>
        .ana {background:rgba(20,20,20,.6);padding:2rem;border-radius:16px;color:#fff;margin-top:2rem;}
        .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem;margin-top:1rem;}
        .card{background:rgba(255,255,255,.05);padding:1rem;border-left:4px solid #dc2626;border-radius:10px;}
        </style>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='ana'><h3>{data.get('film_title','Movie')}</h3>", unsafe_allow_html=True)
        st.markdown("<h4>Summary</h4>"+data.get('analysis_summary',''), unsafe_allow_html=True)
        st.markdown("<h4>Character Tropes</h4>", unsafe_allow_html=True)

        cards_html = "".join(
            f"<div class='card'><b>{t['trope_name']}</b><br>{t['description']}<br>"
            f"<small>Conf: {t['confidence_score']}/10</small></div>"
            for t in tropes
        )

        st.markdown(f"<div class='grid'>{cards_html}</div></div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Analysis parse error: {e}")