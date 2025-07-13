# utils/translation_utils.py

import json
import os
from typing import Dict, Any

# Supported languages and their codes
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "ur": "Urdu",
    "ne": "Nepali"
}

# UI string keys
UI_STRINGS = [
    "StreamFlix",
    "Search movies...",
    "Search",
    "Watch",
    "Load More Videos",
    "Videos Displayed",
    "Total Available",
    "Total Runtime",
    "Total Size",
    "No Results Found",
    "Try adjusting your search terms or wait for videos to load.",
    "Browse by Genre",
    "Duration:",
    "Resolution:",
    "Size:",
    "Collection Statistics",
    "Genre",
    "Back",
    "Language",
    "Hindi",
    "Bengali",
    "Tamil",
    "Telugu",
    "Marathi",
    "Gujarati",
    "Punjabi",
    "Kannada",
    "Malayalam",
    "Urdu",
    "Nepali",
    "Drag",
    "Type here...",
    "Close Keyboard",
    "Open on-screen keyboard",
    "Search videos",
    "Watch this video",
    "Previous video",
    "Next video",
    "Clear",
    "Apply",
    "MB",
    "Fetching videos from Wikimedia Commons...",
    "Error fetching video data:",
    "Fallback data used:",
    "videos",
    "Data from",
    "Wikimedia Commons",
    "Built with",
    "Streamlit",
    "Open Source Films",
]

# Global variable to store all translations
_TRANSLATIONS_DATA: Dict[str, Dict[str, str]] = {}

def load_translations_from_json() -> Dict[str, Dict[str, str]]:
    """Load all translations directly from the JSON file for instant access"""
    global _TRANSLATIONS_DATA
    
    try:
        if os.path.exists('translations_cache.json'):
            with open('translations_cache.json', 'r', encoding='utf-8') as f:
                _TRANSLATIONS_DATA = json.load(f)
            print(f"✅ Loaded translations for {len(_TRANSLATIONS_DATA)} languages from JSON cache")
            return _TRANSLATIONS_DATA
        else:
            print("❌ translations_cache.json not found")
            return {}
    except Exception as e:
        print(f"❌ Error loading translations from JSON: {e}")
        return {}

def get_translation(text: str, lang: str) -> str:
    """Instant translation using JSON cache - no API calls, no fallbacks"""
    global _TRANSLATIONS_DATA
    
    # Load translations if not already loaded
    if not _TRANSLATIONS_DATA:
        load_translations_from_json()
    
    # Get translation from loaded data
    if lang in _TRANSLATIONS_DATA and text in _TRANSLATIONS_DATA[lang]:
        return _TRANSLATIONS_DATA[lang][text]
    
    # Fallback to English if translation not found
    if lang != "en" and "en" in _TRANSLATIONS_DATA and text in _TRANSLATIONS_DATA["en"]:
        return _TRANSLATIONS_DATA["en"][text]
    
    # Last resort: return original text
    return text

def get_all_translations_for_language(lang: str) -> Dict[str, str]:
    """Get all translations for a specific language"""
    global _TRANSLATIONS_DATA
    
    # Load translations if not already loaded
    if not _TRANSLATIONS_DATA:
        load_translations_from_json()
    
    return _TRANSLATIONS_DATA.get(lang, {})

def is_translation_available(text: str, lang: str) -> bool:
    """Check if a translation is available for the given text and language"""
    global _TRANSLATIONS_DATA
    
    # Load translations if not already loaded
    if not _TRANSLATIONS_DATA:
        load_translations_from_json()
    
    return lang in _TRANSLATIONS_DATA and text in _TRANSLATIONS_DATA[lang]

def get_available_languages() -> list:
    """Get list of available languages from the JSON cache"""
    global _TRANSLATIONS_DATA
    
    # Load translations if not already loaded
    if not _TRANSLATIONS_DATA:
        load_translations_from_json()
    
    return list(_TRANSLATIONS_DATA.keys())

# Load translations on module import
load_translations_from_json()