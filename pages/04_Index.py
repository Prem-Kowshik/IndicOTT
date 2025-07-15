import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Load Supabase credentials from .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page config
st.set_page_config(page_title="🎬 Movie Index", layout="wide")

# Inject custom CSS for Netflix theme
st.markdown("""
    <style>
    :root {
        --primary-red: #e50914;
        --shadow-red: #e50914;
    }
    </style>
""", unsafe_allow_html=True)

# Top Navigation Bar
top_col1, top_col2 = st.columns([1, 2])
with top_col1:
    st.markdown("""
    <h1 style='margin-top: 0; color: var(--primary-red); text-shadow: 0 0 10px var(--shadow-red);'>
        🎬 StreamFlix
    </h1>
    """, unsafe_allow_html=True)

# Netflix-style CSS for AgGrid Table
st.markdown("""
    <style>
    :root {
        --primary-red: #e50914;
        --shadow-red: #e50914;
    }

    .ag-theme-streamlit {
        background-color: #141414 !important;
        --ag-background-color: #141414 !important;
        --ag-foreground-color: #ffffff !important;
        --ag-header-background-color: #1f1f1f !important;
        --ag-header-foreground-color: var(--primary-red) !important;
        --ag-border-color: #e50914 !important;
        --ag-row-hover-color: #e5091420 !important;
        --ag-selected-row-background-color: #e5091430 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    .ag-theme-streamlit .ag-header-cell-label {
        justify-content: center;
    }

    .ag-theme-streamlit .ag-row {
        transition: background 0.2s ease-in-out;
    }

    .ag-theme-streamlit .ag-row-hover {
        background-color: #e5091420 !important;
    }

    .ag-theme-streamlit .ag-cell {
        border-right: 1px solid #e50914 !important;
    }

    .ag-theme-streamlit .ag-header-cell {
        border-right: 1px solid #e50914 !important;
    }

    .ag-theme-streamlit .ag-root-wrapper {
        border: 2px solid #e50914 !important;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# Predefined options
STANDARD_GENRES = [
    "Action", "Romance", "Drama", "Comedy", "Thriller", "Horror", "Sci-Fi", "Melodrama",
    "Adventure", "Historical Romance", "Musical", "Mythological", "Social", "War",
    "Social Guidance", "Crime", "Documentary", "Short", "Animation", "Fantasy", "History",
    "Family", "Historical", "Social"
]
STANDARD_LANGUAGE = ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Marathi", "Bengali"]

# Fetch all movies
@st.cache_data(ttl=300)
def fetch_all_movies():
    all_data = []
    batch_size = 1000
    offset = 0

    while True:
        try:
            response = (
                supabase.table("Video_movies")
                .select("*")
                .range(offset, offset + batch_size - 1)
                .execute()
            )
            batch = response.data
            if not batch:
                break
            all_data.extend(batch)
            offset += batch_size
        except Exception as e:
            st.error(f"❌ Error fetching batch starting at {offset}: {e}")
            break

    return all_data

movies = fetch_all_movies()

# Get unique values from a field
def get_unique_values(field):
    return sorted(set([item[field] for item in movies if item.get(field)]))

# Sidebar Filters
st.sidebar.header("🔎 Filter Movies")

selected_genre = st.sidebar.selectbox("Genre", ["All"] + STANDARD_GENRES)
selected_director = st.sidebar.selectbox("Director", ["All"] + get_unique_values("director"))
selected_language = st.sidebar.selectbox("Language", ["All"] + STANDARD_LANGUAGE)
selected_cast = st.sidebar.selectbox("Cast", ["All"] + get_unique_values("cast"))

# Apply filtering
filtered_movies = movies

if selected_genre != "All":
    filtered_movies = [m for m in filtered_movies if selected_genre.lower() in (m.get("genre") or "").lower()]

if selected_director != "All":
    filtered_movies = [m for m in filtered_movies if m.get("director") == selected_director]

if selected_language != "All":
    filtered_movies = [m for m in filtered_movies if m.get("language") == selected_language]

if selected_cast != "All":
    filtered_movies = [m for m in filtered_movies if m.get("cast") == selected_cast]

# Show AgGrid if there are results
if filtered_movies:
    st.success(f"🎞 Found {len(filtered_movies)} movie(s).")

    # Prepare AgGrid
    gb = GridOptionsBuilder.from_dataframe(pd.DataFrame(filtered_movies))
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(filterable=True, sortable=True, resizable=True)
    grid_options = gb.build()

    AgGrid(
        pd.DataFrame(filtered_movies),
        gridOptions=grid_options,
        update_mode=GridUpdateMode.NO_UPDATE,
        fit_columns_on_grid_load=True,
        theme="streamlit",  # or "streamlit", "alpine"
        height=500,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False
    )
else:
    st.warning("No movies match the selected filters.")
