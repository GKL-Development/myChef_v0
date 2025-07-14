import streamlit as st
from sqlalchemy.sql import text
import pandas as pd
from datetime import date
from functions.connection import init_connection

def databaseRecipesStorage(recipesData, userId=1):
    """The function takes recipesData already JSON parsed 
    and deconstruct it to store it in the database"""
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
            myChefNotes,
            equipment,
            instructions,
            allergens,
            allergensSafetyNote,
            isMeatOrFish,
            totalTime
        ) VALUES (
            :creator_id,
            :meal_id,
            :creationDate,
            :recipeTitle,
            :yield,
            :prepTime,
            :cookTime,
            :myChefNotes,
            :equipment,
            :instructions,
            :allergens,
            :allergensSafetyNote,
            :isMeatOrFish,
            :totalTime
        );
        """ # To insert MyChefTips later
        
        # # Loading JSON data
        recipes = recipesData['recipes']

        # Defining date in int for meal_id
        today = date.today()
        str_date = today.strftime("%Y%m%d")
        meal_id_dict = {}
        
        # Establishing connection with database
        conn = init_connection()
        with conn.session as s:
            try:
                for i, recipe in enumerate(recipes):
                    meal_data = {
                        "creator_id": userId,
                        "meal_id": int(str_date + str(i) + str(userId)), # The meal ID is a composition of the meal number, the date and the user ID
                        "creationDate": today, # Stores the date of the creation of the recipes to verify if user has created a meal today
                        "recipeTitle": recipe.get("Recipe Title"),
                        "yield": recipe.get("Yield"), 
                        "prepTime": recipe.get("Prep time"),
                        "cookTime": recipe.get("Cook time"),
                        "myChefNotes": recipe.get("MyChef Note"),
                        "equipment": recipe.get("Equipment"),
                        "instructions": recipe.get("Instructions"),
                        # "myChefTips": json.dumps(recipe.get("MyChef Tips")),
                        "allergens": recipe.get("Allergens", []), # Provide empty list if key not found
                        "allergensSafetyNote": recipe.get("Allergen Safety Note"),
                        "isMeatOrFish": recipe.get("Is Meat Or Fish"),
                        "totalTime": recipe.get("Total time")
                    }
                    meal_id_dict[recipe.get("Recipe Title")] = int(str_date + str(i) + str(userId)) # Defining a dictionnary of meal recipes and their ID for ingredients Database insertion
                    s.execute(text(insert_sql), meal_data)
                s.execute(text("UPDATE users SET lastmeal = :today WHERE user_id = :user_id"), {"user_id": userId, "today": today})
                s.commit()
                # st.success(f"Successfully inserted {len(recipes)} recipes for User ID: {1}") // Not needed for user use
            except Exception as e:
                st.error("An error occured. Please contact us: admin@gkldevelopment.com")
                st.error(e)
                s.rollback()
        return meal_id_dict
    else:
        st.error("Database meal storage error. Contact admin@gkldevelopment.com or try again.")

def databaseIngredientsStorage(recipesData, meal_id_dict, userId=1):
    """The function takes recipesData already JSON parsed 
    and deconstruct it to store it in the database"""
    if userId and recipesData:
        # Insert SQL scripts
        insert_sql = """
        INSERT INTO ingredients (
            pk_ingredients,
            recipe_id,
            quantity,
            unit,
            ingredient_name,
            date            
        ) VALUES (
            DEFAULT,
            :recipe_id,
            :quantity,
            :unit,
            :ingredient_name,
            :date
        );
        """
        
        # # Loading JSON data
        # data = json.loads(ingredientsData)
        recipes = recipesData['recipes']

        # Defining date in int for meal_id
        today = date.today()
        # str_date = today.strftime("%Y%m%d")
        
        # Establishing connection with database
        conn = init_connection()
        with conn.session as s:
            try:
                # JSON Normalizing JSON
                ingredients_df = pd.json_normalize(
                            recipes,
                            record_path='Ingredients List',
                            meta=['Recipe Title'], # To match respective ID from meal_id_dict
                            sep='.',
                            errors='ignore'
                        )
                # Renaming columns
                ingredients_df = ingredients_df.rename(columns={
                    'Quantity': 'quantity',
                    'Unit': 'unit',
                    'Ingredient Name': 'ingredient_name'
                })
                # Adding date to ingredient insertion
                ingredients_df['date'] = today
                # Adding the meal id key to the ingredient
                ingredients_df['recipe_id'] = ingredients_df['Recipe Title'].map(meal_id_dict)
                # Selecting the column in correct order for db insertion
                records_to_insert = ingredients_df[[
                    'recipe_id',
                    'quantity',
                    'unit',
                    'ingredient_name',
                    'date'
                    ]].to_dict(orient='records')
                # Inserting ingredients into DB.
                s.execute(text(insert_sql), records_to_insert)
                s.commit()
                return True
            except Exception as e:
                st.error("An error occured. Please contact us: admin@gkldevelopment.com")
                st.error(e)
                s.rollback()
    else:
        st.error("Database meal storage error. Contact admin@gkldevelopment.com or try again.")

def pushPreferences(technique, diet, allergens, dislikes, efforts, userId):
    """
    Pushing preferences into user table.
    """
    if userId:
        variables_dict = {
            "allergens": allergens,
            "diet": diet,
            "dislikes": dislikes,
            "cooking_efforts": efforts,
            "cooking_technique": technique,
            "user_id": userId
        }

        preferencesQuery = ("""
            UPDATE users
            SET
                allergens = :allergens,
                diet = :diet,
                dislikes = :dislikes,
                cooking_efforts = :cooking_efforts,
                cooking_technique = :cooking_technique,
                haspref = 'True'
            WHERE 
                user_id = :user_id
        """)
        # Establishing connection with database
        conn = init_connection()
        with conn.session as s:
            try:
                s.execute(text(preferencesQuery), params=variables_dict)
                s.commit()
                return True
            except Exception as e:
                st.error("An error occured. Please contact us: admin@gkldevelopment.com")
                st.error(e)
                s.rollback()
                st.stop()
    else:
        st.error("Invalid UserId, please contact us: admin@gkldevelopment.com")

def databaseImageStorage(cloudinary_pub_id, image_url, meal_id, user_id=st.session_state.user_instance.user_id):
    """
    Stores the image (public ID, and URL) in the Neon database.
    """
    if cloudinary_pub_id and image_url and meal_id and user_id:
        variables_dict =  {
            "recipeimg": image_url,
            "cloudinary_public_id": cloudinary_pub_id,
            "meal_id": meal_id,
            "user_id": int(user_id)
        }

        push_query = ("""
            UPDATE meals 
            SET
                recipeimg = :recipeimg,
                cloudinary_public_id = :cloudinary_public_id
            WHERE 1=1
                AND meal_id = :meal_id
                AND creator_id = :user_id;
        """)
        # Establishing connection with database
        conn = init_connection()
        with conn.session as s:
            try:
                s.execute(text(push_query), params=variables_dict)
                s.commit()
                return True
            except Exception as e:
                st.error("An error occured. Please contact us: admin@gkldevelopment.com")
                st.error(e)
                s.rollback()
                st.stop()
    else:
        st.error("Invalid UserId, please contact us: admin@gkldevelopment.com")