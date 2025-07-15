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
st.title("🎬 Movie Index")

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
    try:
        response = supabase.table("Video_movies").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"❌ Error fetching movie data: {e}")
        return []

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
