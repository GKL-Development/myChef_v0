# Importing dependencies
import streamlit as st
from ai_api.recipeGenerator import databaseStorage, gemini_ai_api
import pandas as pd
import json, time

# Defining default prompt text - no restrictions
prompt_text = """Number of recipes: 7
Cooking technique focus: oven or pan or boiling
Dietary preferences: None
Allergy Constraints: None
Disliked Ingredients: Curry
Seasonal/Regional Focus: Early summer in Europe.
Household Composition: 2 adults, 1 child (age 2)
Meal Type: Dinner
Maximum Total Time: 30 min.
Budget Consideration: Medium.
Suitability/Effort Level: Quick weekday meal
Meal to Avoid: Curry
Maximum % of Recipes with Meat/Fish: 40"""

####################################### Testing page ####################################################
st.title("Testing Page 🧪")
st.text("This page is for backend testing and will be removed from the app. Using this page is not recommended and will likely require admin authentication for interactions.")
st.html("<br>")

# Authentication for testing
def credentials():
    if st.session_state["passwd"] == st.secrets["testing_password"]:
        st.session_state["tester_logged_in"] = True
    else:
        st.session_state["tester_logged_in"] = False
        st.error("Invalid password...")

def authenticate():
    if "tester_logged_in" not in st.session_state or st.session_state["tester_logged_in"] == False:
        st.text_input(label="Password:", key="passwd", type="password", on_change=credentials)
        return False
    elif st.session_state["tester_logged_in"]:
        return True

recipe_insert, recipe_gen = st.tabs(["Upload Recipe :floppy_disk:", "Recipe Generator - MyChef :cook:"]) 
if authenticate():
    # Testing SQL insertion
    with recipe_insert:
        st.subheader("Recipes insertion to database")
        st.text("Fill up the text area with the JSON output of a recipe and your userID and press the button to insert this recipe to the database")
        st.markdown("<br>", unsafe_allow_html=True)
        json_txt = st.text_area("Input a JSON string here...", height=150, max_chars=None)
        userId = st.number_input("Insert your User ID", value=None, placeholder="User ID")
        if st.button("Insert JSON recipes to SQL", use_container_width=True, icon="📩"):
            databaseStorage(recipesData=json_txt, userId=int(userId))
        st.divider()
        if st.button("Log out!"):
            st.session_state["tester_logged_in"] = False
            st.rerun()
    # Testing Gemini API
    with recipe_gen:
        st.subheader("Try MyChef")
        st.write("Generate a weekly plan using **MyChef**. " \
        "The given pre-filled text is an elaborate _Generative AI_ prompt that is meant to provide enough instructions to MyChef to generate meals for your week.")
        st.markdown("<br>", unsafe_allow_html=True)
        prompt = st.text_area("Prompt MyChef:", value=prompt_text, height=320, max_chars=None)
        creativity = st.slider("Handle MyChef creativity:", 0, 110, 90)
        if st.button("Let MyChef cook!", use_container_width=True, icon="🥘", key="generateRecipes"):
            # Normalize the 'recipes' key from the JSON data
            with st.status("MyChef is cooking!", expanded=True) as status:
                # Instanciating the prompting and meal generation process
                st.write("Providing informations to MyChef...")
                time.sleep(2)
                # Prompting MyChef
                st.write("Generating your meal plan...")
                structured_output = gemini_ai_api(prompt, creativity)
                # Extracting the output as a Python dictionnary
                st.write("Extracting your meals...")
                if structured_output:
                    structured_output_dict = json.loads(structured_output)
                else:
                    st.error("Failed to generate meal plan. An issue my be going on our side. Please try again in a couple hours.")
                    st.stop()
                # Visualizing the meal plan
                st.write("Returning meal plan dataframe!")
                recipe_df = pd.json_normalize(structured_output_dict["recipes"],
                    # Meta-data to include from the main recipe object
                    meta=["Recipe Title", "Allergens", "Cook time", "Prep time", "Total time",
                          "Equipment", "Instructions", "Is Meat Or Fish", "MyChef Note",
                          "Allergen Safety Note", "Yield", "MyChef Tips", "Ingredients List"],
                    # This will create a cartesian product, linking each ingredient to its recipe
                    sep='.')
                status.update(label="Meal plan generated!", state="complete", expanded=False)
            st.dataframe(recipe_df)
            st.dataframe(pd.json_normalize(
                            structured_output_dict["recipes"],
                            record_path='Ingredients List',
                            meta=['Recipe Title'], # Include 'temp_recipe_id' for merging
                            record_prefix='ingredient.', # Prefix column names like 'ingredient.Name'
                            sep='.',
                            errors='ignore'
                        ))
            st.dataframe(pd.json_normalize(
                            structured_output_dict["recipes"],
                            record_path='MyChef Tips',
                            meta=['Recipe Title'], # Include 'temp_recipe_id' for merging
                            record_prefix='mychef_tip.', # Prefix column names like 'mychef_tip.Kid-Friendly Adaptation'
                            sep='.',
                            errors='ignore'
                        ))
