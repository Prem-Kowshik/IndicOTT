#!/usr/bin/env python3
"""
Translation Generator Script
============================
This script generates translations for all UI strings in all supported languages
and saves them to a JSON file for faster loading.
"""

from utils.translation_utils import preload_all_translations, UI_STRINGS, LANGUAGES

if __name__ == "__main__":
    print("🌐 Generating translations for all supported languages...")
    print(f"Supported languages: {list(LANGUAGES.keys())}")
    print(f"UI strings to translate: {len(UI_STRINGS)}")
    print("\nStarting translation process...")
    
    try:
        all_translations = preload_all_translations()
        print(f"\n✅ Successfully generated translations for {len(all_translations)} languages!")
        print("📁 Translations saved to 'translations_cache.json'")
        
        # Show some stats
        for lang_code, translations in all_translations.items():
            print(f"  {LANGUAGES[lang_code]}: {len(translations)} strings translated")
            
    except Exception as e:
        print(f"❌ Error generating translations: {e}")
        print("Some translations may have failed, but the process will continue with available translations.") 