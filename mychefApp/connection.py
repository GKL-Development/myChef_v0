import streamlit as st
import cloudinary
# Creates a db connection and cache it
@st.cache_resource()
def init_connection():
    return st.connection('neon', type='sql')

@st.cache_resource()
def configure_cloudinary():
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloudinary_cloud_name"],
        api_key = st.secrets["cloudinary"]["cloudinary_api_key"],
        api_secret = st.secrets["cloudinary"]["cloudinary_api_secret"]
    )