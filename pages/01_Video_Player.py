# pages/01_Video_Player.py

"""
Video Player - Enhanced Multilingual UI with 22 Indian Languages Support
=======================================================================
• Complete support for all 22 Indian scheduled languages
• Single-button translation for entire interface
• Metadata and heading translation support
• Streamlit-based video player with subtitle fetching
• AI trope analysis with translation
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
from deep_translator import GoogleTranslator

# --- Set up import path to utils ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(_file_))))
from utils.supabase_client import supabase
from utils.ai_utils import character_tropes_generator

# Required for running async in Streamlit
import nest_asyncio
nest_asyncio.apply()

# --------------------------- LANGUAGES -------------------------------------

# All 22 Indian scheduled languages from 8th Schedule of Indian Constitution
LANGUAGES = {
    "en": "English",
    "as": "Assamese",      # অসমীয়া
    "bn": "Bengali",       # বাংলা
    "brx": "Bodo",         # बर'
    "doi": "Dogri",        # डोगरी
    "gu": "Gujarati",      # ગુજરાતી
    "hi": "Hindi",         # हिंदी
    "kn": "Kannada",       # ಕನ್ನಡ
    "ks": "Kashmiri",      # کٲشُر
    "gom": "Konkani",      # कोंकणी
    "mai": "Maithili",     # मैथिली
    "ml": "Malayalam",     # മലയാളം
    "mni": "Manipuri",     # মনিপুরী
    "mr": "Marathi",       # मराठी
    "ne": "Nepali",        # नेपाली
    "or": "Odia",          # ଓଡ଼ିଆ
    "pa": "Punjabi",       # ਪੰਜਾਬੀ
    "sa": "Sanskrit",      # संस्कृत
    "sat": "Santali",      # ᱥᱟᱱᱛᱟᱲᱤ
    "sd": "Sindhi",        # سنڌي
    "ta": "Tamil",         # தமிழ்
    "te": "Telugu",        # తెలుగు
    "ur": "Urdu",          # اردو
}

# Enhanced translations dictionary with all interface elements
TRANSLATIONS = {
    "en": {
        "back_to_home": "← Back to Homepage",
        "metadata": "📊 Metadata",
        "director": "Director",
        "resolution": "Resolution", 
        "duration": "Duration",
        "size": "Size",
        "subtitles": "📝 Subtitles",
        "loading_subs": "Loading {lang} subtitles...",
        "subs_not_found": "Subtitles for {lang} not found.",
        "select_lang": "Language",
        "download_srt": "📥 Download .srt",
        "select_to_display_subs": "Select an available language to display subtitles.",
        "ai_analysis": "🤖 AI Movie Analysis",
        "analyze_tropes": "Analyze Tropes",
        "thinking": "Thinking…",
        "summary": "Summary",
        "character_tropes": "Character Tropes",
        "analysis_parse_error": "Analysis parse error:",
        "incomplete_video_data": "The selected video data is incomplete (missing ID or URL). Please go back and select another.",
        "no_video_selected": "No video selected. Please go back to the Homepage and select a video.",
        "translate_interface": "🌐 Translate Interface",
        "ui_language": "UI Language / भाषा",
        "video_title": "Video Title",
        "confidence_score": "Confidence"
    },
    "hi": {
        "back_to_home": "← होमपेज पर जाएँ",
        "metadata": "📊 मेटाडेटा",
        "director": "निर्देशक",
        "resolution": "रिज़ॉल्यूशन",
        "duration": "अवधि",
        "size": "आकार",
        "subtitles": "📝 सबटाइटल्स",
        "loading_subs": "{lang} के सबटाइटल्स लोड हो रहे हैं...",
        "subs_not_found": "{lang} के सबटाइटल्स उपलब्ध नहीं हैं।",
        "select_lang": "भाषा",
        "download_srt": "📥 .srt डाउनलोड करें",
        "select_to_display_subs": "दिखाने के लिए कोई भाषा चुनें।",
        "ai_analysis": "🤖 एआई मूवी विश्लेषण",
        "analyze_tropes": "ट्रोप्स विश्लेषण करें",
        "thinking": "सोच रहे हैं…",
        "summary": "सारांश",
        "character_tropes": "पात्रों के ट्रोप्स",
        "analysis_parse_error": "विश्लेषण त्रुटि:",
        "incomplete_video_data": "चयनित वीडियो अधूरा है (ID या URL नहीं)। कृपया अन्य चुनें।",
        "no_video_selected": "कोई वीडियो चयनित नहीं है। कृपया होमपेज पर जाएं और वीडियो चुनें।",
        "translate_interface": "🌐 इंटरफ़ेस का अनुवाद करें",
        "ui_language": "UI भाषा / भाषा",
        "video_title": "वीडियो शीर्षक",
        "confidence_score": "आत्मविश्वास"
    }
}

# --------------------------- HELPERS ---------------------------------------

def lang_name(code: str): 
    return LANGUAGES.get(code, code.upper())

def _(key, **kwargs):
    lang = st.session_state.get("ui_lang", "en")
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    return text.format(**kwargs)

def clean(title: str): 
    return title.replace("File:", "").rsplit(".", 1)[0]

def srt2vtt(s: str): 
    return "WEBVTT\n\n" + s.replace(",", ".")

def human_dur(s): 
    return str(timedelta(seconds=int(s))) if s else "N/A"

def human_size(b): 
    return f"{b / 1_048_576:.2f} MB" if b else "N/A"

# Enhanced translation function with better error handling
def translate_text(text, target_lang):
    if target_lang == "en" or not text:
        return text
    
    try:
        # Handle special cases for languages that might need alternative codes
        translation_code = target_lang
        if target_lang == "brx":  # Bodo might need special handling
            translation_code = "bo"  # Fallback code
        elif target_lang == "sat":  # Santali might need special handling
            translation_code = "sat"  # Use sat as Google now supports it
            
        translator = GoogleTranslator(source='en', target=translation_code)
        return translator.translate(text)
    except Exception as e:
        print(f"Translation failed for {target_lang}: {e}")
        return text  # Fallback to original English on failure

# Enhanced function to translate metadata
def translate_metadata(video_data, target_lang):
    if target_lang == "en":
        return video_data
    
    translated_data = video_data.copy()
    
    # Translate specific metadata fields
    translatable_fields = {
        "director": "Director",
        "genre": "Genre", 
        "description": "Description",
        "title": "Title"
    }
    
    for field, english_text in translatable_fields.items():
        if field in translated_data and translated_data[field]:
            translated_data[field] = translate_text(translated_data[field], target_lang)
    
    return translated_data

# Enhanced AI result translation
def translate_ai_result(data, target_lang):
    if target_lang == "en" or not data:
        return data
    
    try:
        translated_data = data.copy()
        
        # Translate main fields
        if "analysis_summary" in translated_data:
            translated_data["analysis_summary"] = translate_text(
                translated_data["analysis_summary"], target_lang
            )
        
        if "film_title" in translated_data:
            translated_data["film_title"] = translate_text(
                translated_data["film_title"], target_lang
            )
        
        # Translate tropes
        if "tropes_identified" in translated_data:
            for trope in translated_data["tropes_identified"]:
                trope["trope_name"] = translate_text(trope["trope_name"], target_lang)
                trope["description"] = translate_text(trope["description"], target_lang)
        
        return translated_data
    except Exception as e:
        print(f"AI result translation error: {e}")
        return data

# ---------------------- PAGE SETUP ----------------------------------------

st.set_page_config(page_title="Video Player", page_icon="🎬", layout="wide")

# Enhanced Language selector with all 22 Indian languages
if "ui_lang" not in st.session_state:
    st.session_state.ui_lang = "en"

# Single translation button in sidebar
st.sidebar.markdown("### " + _("translate_interface"))

# Language selector
selected_lang = st.sidebar.selectbox(
    _("ui_language"),
    options=list(LANGUAGES.keys()),
    format_func=lang_name,
    key="ui_lang_selector"
)

# Single translate button
if st.sidebar.button("🔄 Translate All", type="primary"):
    st.session_state.ui_lang = selected_lang
    st.rerun()

# ------------------- VIDEO SELECTION CHECK -------------------

if "selected_video" not in st.session_state or not st.session_state.selected_video:
    st.error(_("no_video_selected"))
    st.stop()

video = st.session_state.selected_video
title = clean(video.get("title", "Untitled"))
vid_id = str(video.get("id"))
video_url = video.get("url")

if not vid_id or not video_url:
    st.error(_("incomplete_video_data"))
    st.stop()

# Translate video metadata
translated_video = translate_metadata(video, st.session_state.ui_lang)

ana_key = f"ana_{vid_id}"
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = 'en'
if 'current_subs' not in st.session_state:
    st.session_state.current_subs = None
if ana_key not in st.session_state:
    st.session_state[ana_key] = None

# ------------------- DATABASE / AI -------------------

def db_get_subs(video_id, lang):
    try:
        res = supabase.table("subtitles").select("subtitle_content") \
            .eq("video_id", video_id).eq("language_code", lang).single().execute()
        return res.data.get("subtitle_content") if res.data else None
    except Exception as e:
        print("Sub fetch error:", e)
        return None

async def trope(title, url):
    try:
        return await character_tropes_generator(title, url)
    except Exception as e:
        return json.dumps({
            "film_title": title, 
            "analysis_summary": f"Error during AI analysis: {e}"
        })

# --------------------- UI LAYOUT -----------------------

left, right = st.columns([3, 1])

with right:
    if st.button(_("back_to_home")):
        st.switch_page("Homepage.py")

    # Translated metadata section
    st.markdown(f"### {_('metadata')}")
    
    # Use translated video data
    director_text = translated_video.get('director', 'N/A')
    if st.session_state.ui_lang != "en" and director_text != 'N/A':
        director_text = translate_text(video.get('director', 'N/A'), st.session_state.ui_lang)
    
    st.markdown(f"{_('director')}:** {director_text} \n"
                f"{_('resolution')}:** {translated_video.get('width', 'N/A')}×{translated_video.get('height', 'N/A')} \n"
                f"{_('duration')}:** {human_dur(translated_video.get('duration'))} \n"
                f"{_('size')}:** {human_size(translated_video.get('size'))}")

    # ---------- Subtitles ----------
    st.markdown(f"### {_('subtitles')}")

    def on_language_change(initial_load=False):
        selected_lang = st.session_state.current_lang if initial_load else st.session_state.lang_select
        with st.spinner(_('loading_subs', lang=lang_name(selected_lang))):
            subs = db_get_subs(vid_id, selected_lang)
            if subs:
                st.session_state.current_subs = subs
                st.session_state.current_lang = selected_lang
            else:
                st.session_state.current_subs = None
                st.warning(_('subs_not_found', lang=lang_name(selected_lang)))

    if st.session_state.get('last_loaded_vid') != vid_id:
        st.session_state.current_subs = None
        st.session_state.current_lang = 'en'
        on_language_change(initial_load=True)
        st.session_state['last_loaded_vid'] = vid_id

    st.selectbox(
        _('select_lang'),
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.current_lang),
        format_func=lang_name,
        key='lang_select',
        on_change=lambda: on_language_change(initial_load=False)
    )

    if st.session_state.current_subs:
        st.download_button(
            label=_("download_srt"),
            data=st.session_state.current_subs,
            file_name=f"{title}_{st.session_state.current_lang}.srt",
            mime="text/plain"
        )
    else:
        st.info(_("select_to_display_subs"))

    # ---------- AI Analysis --------------
    st.markdown(f"### {_('ai_analysis')}")
    
    if st.button(_("analyze_tropes"), use_container_width=True):
        with st.spinner(_("thinking")):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            st.session_state[ana_key] = loop.run_until_complete(trope(title, video["descriptionurl"]))

# Left column - Video player
with left:
    vtt_track = ""
    if st.session_state.current_subs:
        vtt_data = srt2vtt(st.session_state.current_subs)
        vtt_track = f"""
        <track kind="subtitles" src="data:text/vtt;base64,{vtt_data}" 
               srclang="{st.session_state.current_lang}" label="{lang_name(st.session_state.current_lang)}" default>
        """

    # Translate video title
    translated_title = translate_text(title, st.session_state.ui_lang) if st.session_state.ui_lang != "en" else title
    
    st.markdown(f"# 🎬 {translated_title}")

    # Video player HTML
    components.html(f"""
    <video controls width="100%" height="400">
        <source src="{video_url}" type="video/mp4">
        {vtt_track}
        Your browser does not support the video tag.
    </video>
    <div style="margin-top: 10px;">
        <label for="speed">Speed:</label>
        <select id="speed" onchange="document.querySelector('video').playbackRate = this.value">
            <option value="0.25">0.25x</option>
            <option value="0.5">0.5x</option>
            <option value="0.75">0.75x</option>
            <option value="1" selected>1x</option>
            <option value="1.25">1.25x</option>
            <option value="1.5">1.5x</option>
            <option value="2">2x</option>
        </select>
    </div>
    """, height=500)

    # -------------------- AI ANALYSIS RESULTS --------------------
    if st.session_state[ana_key]:
        try:
            data = json.loads(st.session_state[ana_key])
            
            # Translate AI result to selected UI language
            data = translate_ai_result(data, st.session_state.ui_lang)
            
            tropes = data.get("tropes_identified", [])
            
            # Enhanced CSS styling
            st.markdown("""
            <style>
            .movie-analysis {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                color: white;
            }
            .trope-card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                transition: transform 0.2s;
            }
            .trope-card:hover {
                transform: translateY(-2px);
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="movie-analysis">', unsafe_allow_html=True)
            st.markdown(f"<h2>🎭 {data.get('film_title', 'Movie')}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3>📝 {_('summary')}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>{data.get('analysis_summary', '')}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<h3>🎪 {_('character_tropes')}</h3>", unsafe_allow_html=True)
            
            for trope in tropes:
                st.markdown(f'''
                <div class="trope-card">
                    <h4>{trope['trope_name']}</h4>
                    <p>{trope['description']}</p>
                    <small>{_('confidence_score')}: {trope['confidence_score']}/10</small>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"{_('analysis_parse_error')} {e}")
