import streamlit as st
from utils.translation_utils import get_all_translations_for_language

def render_multilanguage_keyboard():
    """
    Renders a multi-language on-screen keyboard component in Streamlit.

    This function relies on the following st.session_state variables, which
    should be initialized in the main part of your app:
    - 'show_keyboard': (bool) Toggles the visibility of the keyboard.
    - 'keyboard_query': (str) The string that the keyboard will modify.
    - 'selected_language': (str) The name of the currently selected language
                         (e.g., "English", "Hindi").

    The output of the keyboard is stored back into st.session_state.keyboard_query.
    """

    # Initialize session state variables if they don't exist
    if 'keyboard_query' not in st.session_state:
        st.session_state.keyboard_query = ""
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "Hindi"

    # Get current translations for the UI language
    current_translations = get_all_translations_for_language(st.session_state.get('language', 'en'))

    # --- Data for the Keyboard ---
    language_options = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "Bengali": "bn"
    }
    
    # Note: English (en) doesn't have a defined keyboard, it's assumed the user
    # has a physical keyboard. This component is for non-Latin scripts.
    keyboards = {
        "hi": [
            ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ'],
            ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ट', 'ठ'],
            ['ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ'],
            ['ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स'],
            ['ह', 'ळ', 'क्ष', 'त्र', 'ज्ञ', 'ं', 'ः', '़', ' ', '⌫']
        ],
        "te": [
            ['అ', 'ఆ', 'ఇ', 'ఈ', 'ఉ', 'ఊ', 'ఎ', 'ఐ', 'ఒ', 'ఓ'],
            ['క', 'ఖ', 'గ', 'ఘ', 'చ', 'ఛ', 'జ', 'ఝ', 'ట', 'ఠ'],
            ['డ', 'ఢ', 'ణ', 'త', 'థ', 'ద', 'ధ', 'న', 'ప', 'ఫ'],
            ['బ', 'భ', 'మ', 'య', 'ర', 'ల', 'వ', 'శ', 'ష', 'స'],
            ['హ', 'ళ', 'క్ష', 'త్ర', 'జ్ఞ', 'ం', 'ః', '', ' ', '⌫']
        ],
        "ta": [
            ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஒ', 'ஓ'],
            ['க', 'ங', 'ச', 'ஜ', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ன'],
            ['ப', 'ம', 'ய', 'ர', 'ல', 'ள', 'வ', 'ழ', 'ஶ', 'ஷ'],
            ['ஸ', 'ஹ', 'ஃ', '', '', '', '', '', '', '⌫']
        ],
        "bn": [
            ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'এ', 'ঐ', 'ও', 'ঔ'],
            ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ঝ', 'ট', 'ঠ'],
            ['ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ'],
            ['ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ'],
            ['ঁ', 'ঃ', '়', '', '', '', '', '', ' ', '⌫']
        ]
    }

    # --- Keyboard Styling (optional but recommended) ---
    st.markdown("""
    <style>
        .keyboard-container {
            border: 2px solid #dc2626;
            border-radius: 15px;
            padding: 1rem;
            margin-top: 1rem;
            background: #181818;
            box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
        }
        .keyboard-container .stButton > button {
            background: #2F2F2F;
            border: 1px solid #333333;
            color: #dc2626;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .keyboard-container .stButton > button:hover {
            border-color: #dc2626;
            background-color: #383838;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(220, 38, 38, 0.4);
        }
        .keyboard-language-select {
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Render Keyboard if it should be shown ---
    if st.session_state.get('show_keyboard', False):
        with st.container():
            st.markdown('<div class="keyboard-container">', unsafe_allow_html=True)

            # Language Selection Dropdown
            lang_name = st.selectbox(
                current_translations.get("Language", "Language"),
                options=language_options.keys(),
                key="keyboard_language_select",
                index=list(language_options.keys()).index(st.session_state.selected_language)
            )

            # Update session state if language changes
            if lang_name != st.session_state.get('selected_language'):
                st.session_state.selected_language = lang_name

            lang_code = language_options.get(st.session_state.selected_language)

            # Display the keyboard for the selected language
            if lang_code in keyboards:
                for row_index, row in enumerate(keyboards[lang_code]):
                    key_cols = st.columns(len(row))
                    for col_index, key in enumerate(row):
                        if key and key_cols[col_index].button(key, key=f"key_{lang_code}{row_index}{col_index}"):
                            if key == '⌫': # Backspace
                                st.session_state.keyboard_query = st.session_state.keyboard_query[:-1]
                            else: # Any other character
                                st.session_state.keyboard_query += key

            # Keyboard control buttons
            btn_col1, btn_col2 = st.columns([1, 1])
            
            with btn_col1:
                if st.button(current_translations.get('Clear', 'Clear'), key="clear_keyboard_btn"):
                    st.session_state.keyboard_query = ""
                    if 'current_search_term' in st.session_state:
                        st.session_state.current_search_term = ""
            
            with btn_col2:
                if st.button(current_translations.get('Close Keyboard', 'Close Keyboard'), key="close_keyboard_btn"):
                    st.session_state.show_keyboard = False

            st.markdown('</div>', unsafe_allow_html=True)

def initialize_keyboard_state():
    """Initialize keyboard-related session state variables"""
    if 'show_keyboard' not in st.session_state:
        st.session_state.show_keyboard = False
    if 'keyboard_query' not in st.session_state:
        st.session_state.keyboard_query = ""
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "Hindi"