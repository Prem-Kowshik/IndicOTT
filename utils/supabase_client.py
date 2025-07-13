# utils/supabase_client.py
import streamlit as st
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """Initializes and returns a Supabase client."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = get_supabase_client()