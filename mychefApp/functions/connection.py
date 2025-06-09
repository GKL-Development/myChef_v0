import streamlit as st
# Creates a db connection and cache it
@st.cache_resource()
def init_connection():
    return st.connection('neon', type='sql')