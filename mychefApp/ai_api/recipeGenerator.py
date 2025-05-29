import json
import streamlit as st
from sqlalchemy.sql import text
from datetime import date

# Activates when user need to generate a meal planning. 
# It will prompt Gemini AI using the API and return a JSON structured output that will be sent to Neon Database to be stored

def api_call():
    '''Start a AI prompt for meal plan - TBD'''
    return

def databaseStorage(recipesData, userId=1):
    if userId and recipesData:
        # Insert SQL scripts
        insert_sql = """
        INSERT INTO meals (
            creator_id,
            meal_id,
            creationDate,
            recipeTitle,
            yield,
            prepTime,
            cookTime,
            ingredientsList,
            myChefNotes,
            equipment,
            instructions,
            myChefTips,
            allergens,
            allergensSafetyNote,
            isMeatOrFish
        ) VALUES (
            :creator_id,
            :meal_id,
            :creationDate,
            :recipeTitle,
            :yield,
            :prepTime,
            :cookTime,
            :ingredientsList,
            :myChefNotes,
            :equipment,
            :instructions,
            :myChefTips,
            :allergens,
            :allergensSafetyNote,
            :isMeatOrFish
        );
        """
        
        # Passing data to JSON - Temporary waiting for AI API calls
        data = json.loads(recipesData)
        recipes = data['recipes']

        # Defining date in int for meal_id
        today = date.today()
        str_date = today.strftime("%Y%m%d")
        
        # Establishing connection with database
        conn = st.connection('neon', type='sql')
        with conn.session as s:
            try:
                for i, recipe in enumerate(recipes):
                    meal_data = {
                        "creator_id": userId,
                        "meal_id": int(str_date + str(i) + str(userId)), # The meal ID is a composition of the meal number, the date and the user ID
                        "creationDate": today, # Stores the date of the creation of the recipes to verify if user has created a meal today
                        "recipeTitle": recipe.get("Recipe Title"),
                        "yield": json.dumps(recipe.get("Yield")), # Convert list to JSON string for TEXT column
                        "prepTime": recipe.get("Prep time"),
                        "cookTime": recipe.get("Cook time"),
                        "ingredientsList": json.dumps(recipe.get("Ingredients List")),
                        "myChefNotes": recipe.get("MyChef Note"),
                        "equipment": recipe.get("Equipment"),
                        "instructions": json.dumps(recipe.get("Instructions")),
                        "myChefTips": json.dumps(recipe.get("MyChef Tips")),
                        "allergens": json.dumps(recipe.get("Allergens", [])), # Provide empty list if key not found
                        "allergensSafetyNote": recipe.get("Allergen Safety Note"),
                        "isMeatOrFish": recipe.get("Is Meat Or Fish")
                    }
                    s.execute(text(insert_sql), meal_data)
                s.execute(text("UPDATE users SET hasmeal = True WHERE user_id = :user_id"), {"user_id": userId})
                s.commit()
                st.success(f"Successfully inserted {len(recipes)} recipes for User ID: {1}")
            except Exception as e:
                st.error(f"The following error occured during insertion to database: {e}")
                s.rollback()
    else:
        st.error("One of the data provided is not valid...")