import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from genre_utils import render_footer as rf 

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

# Custom styles for sidebar dropdowns
st.markdown("""
    <style>
    /* Sidebar dark background (optional) */
    [data-testid="stSidebar"] {
        background-color: #111 !important;
        color: white !important;
    }

    /* Glowing red border dropdowns */
    .stSelectbox > div {
        background-color: #1f1f1f !important;
        color: white !important;
        border: 2px solid #e50914 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 8px #e50914 !important;
        transition: all 0.3s ease-in-out;
    }

    .stSelectbox:hover > div {
        box-shadow: 0 0 15px #e50914 !important;
        transform: scale(1.02);
    }

    .stSelectbox label {
        color: #e50914 !important;
        font-weight: 600;
    }

    /* Dropdown text and popup */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1f1f1f !important;
        color: white !important;
    }

    .stSelectbox div[role="combobox"] {
        color: white !important;
    }

    .stSelectbox div[role="listbox"] {
        background-color: #1f1f1f !important;
    }

    .stSelectbox div[role="option"] {
        color: white !important;
    }
    </style>
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

st.markdown("""
    <style>
    button[data-testid="baseButton-download-csv"] {
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 16px;
        box-shadow: 0 0 10px #e50914;
        transition: all 0.2s ease-in-out;
    }

    button[data-testid="baseButton-download-csv"]:hover {
        background-color: #ff0a16;
        box-shadow: 0 0 20px #e50914;
        transform: scale(1.03);
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
    st.success(f"🎞️ Found {len(filtered_movies)} movie(s).")

    # Prepare AgGrid
    gb = GridOptionsBuilder.from_dataframe(pd.DataFrame(filtered_movies))
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(filterable=True, sortable=True, resizable=True)
    grid_options = gb.build()

    with st.container():
        st.markdown("""
            <div class="netflix-aggrid">
        """, unsafe_allow_html=True)

        AgGrid(
            pd.DataFrame(filtered_movies),
            gridOptions=grid_options,
            update_mode=GridUpdateMode.NO_UPDATE,
            fit_columns_on_grid_load=True,
            theme="streamlit",
            height=500,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False
        )

        st.markdown("</div>", unsafe_allow_html=True)
    # Convert filtered data to DataFrame
    # Convert filtered data to DataFrame
    df_filtered = pd.DataFrame(filtered_movies)
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')

    # CSV download button
    if st.download_button(
        label="📥 Download Filtered Movies as CSV",
        data=csv_data,
        file_name='Movies_Index.csv',
        mime='text/csv',
        key="download-csv",
        help="Download the currently filtered movies as a CSV file.",
    ):
        st.session_state["csv_downloaded"] = True

else:
    st.warning("No movies match the selected filters.")

if st.session_state.get("csv_downloaded"):
    st.markdown("""
        <style>
        .download-success {
            background-color: #e50914;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            animation: slideFade 1.2s ease-in-out;
            margin-top: 1rem;
        }

        @keyframes slideFade {
            0% {opacity: 0; transform: translateY(-10px);}
            50% {opacity: 1; transform: translateY(0);}
            100% {opacity: 0; transform: translateY(10px);}
        }
        </style>
        <div class="download-success">
            ✅ CSV downloaded successfully!
        </div>
    """, unsafe_allow_html=True)

rf()

