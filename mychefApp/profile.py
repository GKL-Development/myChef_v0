import streamlit as st

ss_user = st.session_state.user_instance

####################################### Profile ####################################################
st.title(f"{ss_user.firstName}'s profile 👤")
st.divider()
st.subheader("My Information:")
firstname, lastname = st.columns(2, vertical_alignment="top", gap="large", border=False)
firstname.text_input("Firstname:", value=ss_user.firstName)
lastname.text_input("Lastname", value=ss_user.lastName)
