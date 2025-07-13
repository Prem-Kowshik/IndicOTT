import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load Supabase credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🎬 Movie Index", layout="wide")
st.title("🎬 Movie Index")

# Define your cleaned genre list manually
STANDARD_GENRES = ["Action", "Romance", "Drama", "Comedy", "Thriller", "Horror", "Sci-Fi", "Melodrama", "Adventure", "Historical Romance", "Musical", "Mythological", "Social", "War", "Social Guidance", "Crime", "Documentary", "Short", "Animation", "Fantasy", "History", "Family", "Historical", "Social"]
STANDARD_LANGUAGE = ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Marathi", "Bengali"]

# Fetch all movies
@st.cache_data(ttl=300)
def fetch_all_movies():
    try:
        response = supabase.table("Video_movies").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching movie data: {e}")
        return []

movies = fetch_all_movies()

# Extract unique directors/languages/casts (no cleanup yet)
def get_unique_values(field):
    return sorted(set([item[field] for item in movies if item.get(field)]))

# Sidebar Filters
st.sidebar.header("🔎 Filter Movies")

# Genre filter only from curated genres
selected_genre = st.sidebar.selectbox("Genre", ["All"] + STANDARD_GENRES)
selected_director = st.sidebar.selectbox("Director", ["All"] + get_unique_values("director"))
selected_language = st.sidebar.selectbox("Language", ["All"] + STANDARD_LANGUAGE)
selected_cast = st.sidebar.selectbox("Cast", ["All"] + get_unique_values("cast"))

# Filtering logic
filtered_movies = movies

# Genre filtering using substring match for flexibility
if selected_genre != "All":
    filtered_movies = [
        m for m in filtered_movies
        if selected_genre.lower() in (m.get("genre") or "").lower()
    ]

if selected_director != "All":
    filtered_movies = [m for m in filtered_movies if m.get("director") == selected_director]

if selected_language != "All":
    filtered_movies = [m for m in filtered_movies if m.get("language") == selected_language]

if selected_cast != "All":
    filtered_movies = [m for m in filtered_movies if m.get("cast") == selected_cast]

# Display movie titles
if filtered_movies:
    st.success(f"🎞️ Found {len(filtered_movies)} movie(s).")
    for movie in sorted(filtered_movies, key=lambda x: x.get("title", "")):
        st.markdown(f"- **{movie.get('title')}**")
else:
    st.warning("No movies match the selected filters.")
