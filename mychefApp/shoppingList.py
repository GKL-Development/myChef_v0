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

if ss.recipesId:
    with st.container():
        ingredients = fetch_recipes_ingredients(ss.user_instance.user_id, ss.recipesId)
        for i in range(len(ingredients)):
            ingredient = str(int(ingredients['quantity'].iloc[i] if ingredients['quantity'].iloc[i] != 0 else None)) + " " + ingredients['unit'].iloc[i] + " " + ingredients['ingredient_name'].iloc[i]
            st.checkbox(ingredient, key=i)
else:
    with st.container():
        st.text("No meals have been generated yet. Jump into the homepage to get your weekly meal planned!")
        if st.button("Go to MyChef!"):
            pass # Button to homepage