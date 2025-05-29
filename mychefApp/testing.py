import streamlit as st
from ai_api.recipeGenerator import databaseStorage

####################################### Testing page ####################################################
st.title("Testing Page")
st.text("This page is for backend testing and will be removed from the app. Using this page is not recommended and will likely require admin authentication for interactions.")
st.divider()

# Testing SQL insertion
st.subheader("Recipes insertion to database")
st.text("Fill up the text area with the JSON output of a recipe and your userID and press the button to insert this recipe to the database")
st.markdown("<br>", unsafe_allow_html=True)
json = st.text_area("Input a JSON string here...", height=150, max_chars=None)
userId = st.number_input("Insert your User ID", value=None, placeholder="User ID")
if st.button("Insert JSON recipes to SQL", use_container_width=True, icon="📩"):
    databaseStorage(recipesData=json, userId=int(userId))