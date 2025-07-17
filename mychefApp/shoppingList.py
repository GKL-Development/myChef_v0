# Import packages and dependencies
import streamlit as st
from db_fetch_functions import fetch_recipes_ingredients

ss = st.session_state
####################################### Shopping List ####################################################

# Header
with st.container():
    st.title('Shopping List 🗒️')
    st.text('All you need to cook your weekly meals for you and your family! 🧑‍🍳')
st.divider()

if "recipesId" not in st.session_state:
    with st.container():
            st.write("_No meals have been generated yet. Jump into the homepage to get your weekly meal planned!_")
            st.html("<br>")
            _, mid, _ = st.columns([3, 1, 3], border=False, vertical_alignment="center")
            mid.page_link(page="./dashboard.py", label="**Go to MyChef 🏠**", use_container_width=False)
else :
    with st.container():
        ingredients = fetch_recipes_ingredients(ss.user_instance.user_id, ss.recipesId)
        for i in range(len(ingredients)):
            # Formatizing ingredients display in shopping list
            if ingredients['unit'].iloc[i] in ("tablespoon", "tablespoons", "teaspoon", "teaspoons", "cup", "cups"):
                ingredient = ingredients['ingredient_name'].iloc[i]#.split(", ")[0]
            elif ingredients['quantity'].iloc[i] != 0:
                ingredient = str(int(ingredients['quantity'].iloc[i])) + " " + ingredients['unit'].iloc[i] + " " + ingredients['ingredient_name'].iloc[i]#.split(", ")[0]
            else: 
                ingredient = ingredients['unit'].iloc[i] + " " + ingredients['ingredient_name'].iloc[i]#.split(", ")[0]
            # Returning ingredient checkbox
            st.checkbox(ingredient, key=i)


    