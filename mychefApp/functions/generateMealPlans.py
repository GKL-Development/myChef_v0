import streamlit as st
import time, json
from mychefApp.ai_api.recipeGenerator import gemini_ai_api
from mychefApp.ai_api.imageGenerator import imageGenerator, uploadImageToCloud
from mychefApp.functions.db_insert_functions import databaseRecipesStorage, databaseIngredientsStorage, databaseImageStorage
from mychefApp.functions.authentication import fetch_user_info
from mychefApp.functions.connection import configure_cloudinary

############################## GENERATE MEAL PLAN ##############################

"""This file goal is only to define a function that generate meals for the week"""

@st.dialog("Tell MyChef about your preferences")
def selectMealPref():
    st.info("For simplicity in this test version, we won't ask about your allergens, diet or dislikes, " \
        "but we'll still provide allergen information, whether it contains meat or fish, and a full ingredient list.")
    
    # Implement meal days storage in db to render meal cards with correct meals
    days_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = st.pills("Number of meals:", options=days_options, selection_mode='multi', key="days")

    # User to select total time for meal prep
    time_options = ['10 min', '20 min', '30 min', '40 min', '50 min', '1 hour']
    total_time = st.pills("How much time will you spend prepping and cooking each meal?",options=time_options, selection_mode='single', key="tot_time")

    # User to select household composition for meal planning yield
    count_options = [1, 2, 3, 4, 5]
    adults = st.pills("How many adults are you cooking for?", options=count_options, selection_mode='single', key="adults")
    childs = st.pills("How many childrens are you cooking for?", options=count_options, selection_mode='single', key="childs")

    # User to select budget for meals
    budget_options = ['Low', 'Medium', 'High']
    budget = st.pills("Budget for your meal:", options=budget_options, selection_mode='single', key="budget")

    # User to select MyChef creativity
    creativity = st.slider("Handle MyChef creativity:", 0, 10, 8)

    # Submitting preferences 
    if st.button("Generate Now!", use_container_width=True, type='primary'):
        st.session_state["mealPreferences"] = {
            "days": days,
            "total_time": total_time,
            "adults": adults,
            "childs": childs,
            "budget": budget,
            "creativity": creativity
            }
        st.rerun()

def generateImage(meal_id, ingredient_list):
    """
    Orchestrates the entire process of image generation: generate, upload, store link.
    """
    configure_cloudinary()
    
    image_data = imageGenerator(meal=meal_id, ingredient_list=ingredient_list)
    # Corrected check for image generation failure
    if image_data is False:
        st.error('Failed generating meals image. Please contact us: admin@gkldevelopment.com')
        print("Workflow failed: Image generation failed.")
        return None
    cloudinary_response = uploadImageToCloud(image_data)
    if cloudinary_response is None:
        print("Workflow failed: Cloudinary upload failed.")
        return None
    cloudinary_public_id = cloudinary_response.get("public_id")
    image_link = cloudinary_response.get("secure_url")
    if not image_link or not cloudinary_public_id:
        print("Workflow failed: Missing public ID or secure URL from Cloudinary.")
        return None
    db_record_id = databaseImageStorage(cloudinary_pub_id=cloudinary_public_id, image_url=image_link, meal_id=meal_id)
    if db_record_id is None:
        print("Workflow failed: Storing in Neon DB failed.")
        return None
    return True
    
def generateMealPlan(userId):
    """
    Pipeline for the full meal planning generation process. 
    Handles AI generation tasks, database insertions and session_state updating.
    """
    user = int(userId)
    ss = st.session_state
    ssp = ss["mealPreferences"]
    # Crafting prompt
    prompt_text = f"""
    Number of recipes: {7 if len(ssp["days"]) == 0 else len(ssp["days"])}
    Cooking technique focus: {ss.preferences['technique']}
    Dietary preferences: {ss.preferences['diet']}
    Allergy Constraints: {ss.preferences['allergy']}
    Disliked Ingredients: {ss.preferences['dislikes']}
    Seasonal/Regional Focus: Early summer in Europe.
    Household Composition: {ssp["adults"]} adults, {ssp["childs"] if ssp["childs"] is not None else 0} child
    Meal Type: Dinner
    Maximum Total Time: {ssp["total_time"]}.
    Budget Consideration: {ssp["budget"]}.
    Suitability/Effort Level: {ss.preferences['efforts']}
    Meal to Avoid: None
    Maximum % of Recipes with Meat/Fish: 40"""

    try:
        # Generating meals from Gemini API 
        with st.status("MyChef is cooking!", expanded=True) as status:
            # Instanciating the prompting and meal generation process
            st.write("Providing informations to MyChef...")
            time.sleep(2)
            
            # Prompting MyChef
            st.write("Generating your meal plan...")
            structured_output = gemini_ai_api(prompt_text, ssp["creativity"])
            
            # Extracting the output as a Python dictionnary
            st.write("Saving your meals...")
            if structured_output:
                recipesData = json.loads(structured_output)
            else:
                st.error("Failed to generate meal plan. " \
                "An issue might be going on our side. " \
                "Please try again in a couple hours or contact us: admin@gkldevelopment.com.")
                status.update(label="Failed to generate meal plan. Please try again", state="error", expanded=False)
                st.stop()
            # Saving shopping list
            mealId = databaseRecipesStorage(recipesData=recipesData, userId=user)
            if mealId:
                st.write("Crafting your shopping list...")
            else:
                status.update(label="Failed to save your meal plan. Please try again", state="error", expanded=False)
                st.stop()

            # Uploading Ingredients to DB
            ingredients_uploaded = databaseIngredientsStorage(recipesData=recipesData, meal_id_dict=mealId, userId=user)
            if ingredients_uploaded:    
                st.write("Generating meals images...")
            else:
                status.update(label="Failed to save your ingredients. Please try again", state="error", expanded=False)
                st.stop()
            # # Add these lines to debug
            # print("--- Debugging Data ---")
            # print("mealId Dictionary:", mealId)
            # print("recipesData List:", recipesData['recipes'][0]["Recipe Title"])
            # print("----------------------")
            # Generating Meals Images
            recipesList = recipesData['recipes']
            for index in range(len(recipesList)):
                try:
                    recipeId = mealId[recipesList[index]["Recipe Title"]]
                    recipeIngredients = recipesList[index]["Ingredients List"]
                    # Check if the ingredients list is not empty
                    if not recipeIngredients:
                        print(f"Skipping image generation for meal ID: {recipeId} - No ingredients found.")
                        continue # Move to the next recipe
                    # Convert the list of ingredients to a string
                    ingredientsList = ", ".join(item["Ingredient Name"] for item in recipeIngredients if "Ingredient Name" in item)
                    # Ensure the list is not empty after filtering
                    if not ingredientsList:
                        print(f"Skipping image generation for meal ID: {recipeId} - No valid ingredient names found.")
                        continue
                    print(f"Generating image for meal ID: {recipeId} with ingredients: {ingredientsList}")
                    # Call the image generation function
                    image_generation_success = generateImage(meal_id=recipeId, ingredient_list=ingredientsList)
                    # Check if image generation failed
                    if not image_generation_success:
                        status.update(label="Failed to generate and upload your images. Please try again", state="error", expanded=False)
                        st.stop()
                except KeyError as e:
                    print(f"An error occurred: Missing key {e} for recipe at index {index}.")
                    # Optionally, update the status and stop or continue
                    status.update(label=f"An error occurred while processing recipes. Missing data: {e}", state="error", expanded=False)
                    st.stop()
                except Exception as e:
                    print(f"An unexpected error occurred at index {index}: {e}")
                    status.update(label="An unexpected error occurred. Please try again.", state="error", expanded=False)
                    st.stop()
            del ss.user_instance
            if fetch_user_info(email=ss["email"]):
                status.update(label="Meal plan generated!", state="complete", expanded=False)
            else:
                status.update(label="Failed to generate and upload your images. Please try again", state="error", expanded=False)
                st.stop()
        st.success("Your weekly meal plan will be displayed shortly.")
        time.sleep(2)
        st.rerun()
    except Exception as e:
        st.error("We couldn't generate your meal. Please try again or contact us: admin@gkldevelopment.com")
        # st.warning(f"Failed because of: {e}") | ONLY FOR DEBUG PURPOSES
        print(e)
        st.stop()

