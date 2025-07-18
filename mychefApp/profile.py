import streamlit as st
from askUserPreferences import askUserPreferences, update_dialog

ss_user = st.session_state.user_instance
# Deprecated
# ss_pref = st.session_state.preferences
# required_keys = {"technique", "diet", "allergy", "dislikes", "efforts"}

####################################### Profile ####################################################
st.title(f"{ss_user.firstName}'s profile 👤")
# st.html("<br>")

info, food_pref = st.tabs(["Informations 🪪", "Preferences 🍽️"])

with info:
    st.subheader("Email & Password:")
    # Login credentials
    email, _ = st.columns([2, 1], vertical_alignment="top", gap="small", border=False)
    email.text_input("Email:", value=ss_user.email)
    pwd, confirm_pwd, pwd_error = st.columns(3, vertical_alignment="bottom", gap="small", border=False)
    password = pwd.text_input("Password:", value="", type='password')
    password_confirm = confirm_pwd.text_input("Confirm Password:", value="", type='password')
    with pwd_error:
        if password != password_confirm:
            st.error("Password must match!")
    # Save and commit changes to db
    st.divider()
    st.subheader("Informations:")
    l_, mid, r_ = st.columns([1,2,1], border=False, vertical_alignment="top")
    if mid.button("Update Your Credentials", type="primary", use_container_width=True):
        update_dialog()

with food_pref:
    # Food preferences
    st.subheader("Preferences:")
    l_, mid, r_ = st.columns([1,2,1], border=False, vertical_alignment="top")
    if mid.button("Update Your Preferences", type="primary", use_container_width=True):
        askUserPreferences()

