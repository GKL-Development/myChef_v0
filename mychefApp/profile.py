import streamlit as st
from functions.askUserPreferences import askUserPreferences
from functions.authentication import fetch_user_info

ss_user = st.session_state.user_instance
ss_pref = st.session_state.preferences
required_keys = {"technique", "diet", "allergy", "dislikes", "efforts"}

####################################### Profile ####################################################
st.title(f"{ss_user.firstName}'s profile 👤")
# st.html("<br>")

info, food_pref = st.tabs(["Informations 🪪", "Preferences 🍽️"])

with info:
    st.subheader("Credential Information:")
    # Name columns
    firstname, lastname, _ = st.columns(3, vertical_alignment="top", gap="small", border=False)
    firstname.text_input("Firstname:", value=ss_user.firstName)
    lastname.text_input("Lastname:", value=ss_user.lastName)

    # Other personnal info columns
    age, username, _ = st.columns(3, vertical_alignment="top", gap="small", border=False)
    age.date_input("Birthdate:", value=ss_user.birthdate)
    username.text_input("Username:", value=ss_user.userName)
    # sex.selectbox("Gender:", ("Male", "Female", "Other", "Don't specify")) // Not implemented 

    # Login credentials
    email, _ = st.columns([2, 1], vertical_alignment="top", gap="small", border=False)
    email.text_input("Email:", value=ss_user.email)
    pwd, confirm_pwd, pwd_error = st.columns(3, vertical_alignment="bottom", gap="small", border=False)
    password = pwd.text_input("Password:", value="", type='password')
    password_confirm = confirm_pwd.text_input("Confirm Password:", value="", type='password')
    with pwd_error:
        if password != password_confirm:
            st.error("Password must match!")

with food_pref:
    # Food preferences
    st.subheader("Food Preferences:")
    if required_keys.isdisjoint(ss_pref):
        st.write("It seems like you never set your preferences for your eating habits. Click the button below to set this up!")
        if st.button("Let us know more about you!", key="selectPrefOnProfile", type="primary"):
            askUserPreferences()
            if not fetch_user_info():
                st.warning("Failed to fetch updated informations. Please consider refreshing the web page.")

# Save and commit changes to db
st.divider()
st.info("Saving changes is not yet functionnal. Do not try saving.")
l_, mid, r_ = st.columns([3,1,3], border=False, vertical_alignment="top")
if mid.button("Save", type="primary", use_container_width=True):
    st.warning("Changes cannot be saved yet. Try another time.")