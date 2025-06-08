# Import packages and dependencies
import streamlit as st
from functions.db_fetch_functions import fetch_recipes_ingredients

ss = st.session_state
####################################### Shopping List ####################################################

# Header
with st.container():
    st.title('Shopping List 🗒️')
    st.text('All you need to cook your weekly meals for you and your family! 🧑‍🍳')
st.divider()

with st.container():
    ingredients = fetch_recipes_ingredients(ss.user_instance.user_id, ss.recipesId)
    for i in range(len(ingredients)):
        ingredient = str(int(ingredients['quantity'].iloc[i])) + " " + ingredients['unit'].iloc[i] + " " + ingredients['ingredient_name'].iloc[i]
        st.checkbox(ingredient, key=i)