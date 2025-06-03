import json
import streamlit as st
from sqlalchemy.sql import text
from datetime import date

# Dependencies for Gemini AI prompt
import base64
import os
from google import genai
from google.genai import types

# Defining prompt instructions file location
prompt_instructions_file_path = os.path.join(
    "mychefApp",
    "ai_api",
    "prompt_instructions",
    "mychef_instructions.txt"
)

# Activates when user need to generate a meal planning. 
# It will prompt Gemini AI using the API and return a JSON structured output that will be sent to Neon Database to be stored

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

def read_prompt_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


################################ GEMINI AI API ################################

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.9,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
        ],
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["recipes"],
            properties = {
                "recipes": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["Recipe Title", "MyChef Note", "Yield", "Prep time", "Cook time", "Total time", "Ingredients List", "Equipment", "Instructions", "MyChef Tips", "Allergen Safety Note", "Is Meat Or Fish", "Allergens"],
                        properties = {
                            "Recipe Title": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "MyChef Note": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Yield": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "Prep time": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Cook time": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Total time": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Ingredients List": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.OBJECT,
                                    required = ["Quantity", "Unit", "Ingredient Name"],
                                    properties = {
                                        "Quantity": genai.types.Schema(
                                            type = genai.types.Type.INTEGER,
                                        ),
                                        "Unit": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                        "Ingredient Name": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                    },
                                ),
                            ),
                            "Equipment": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Instructions": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "MyChef Tips": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.OBJECT,
                                    required = ["Kid-Friendly Adaptation", "Serving Suggestion", "Variations"],
                                    properties = {
                                        "Kid-Friendly Adaptation": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                        "Serving Suggestion": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                        "Variations": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                    },
                                ),
                            ),
                            "Allergen Safety Note": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Is Meat Or Fish": genai.types.Schema(
                                type = genai.types.Type.BOOLEAN,
                            ),
                            "Allergens": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                        },
                    ),
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text=read_prompt_file(prompt_instructions_file_path)), # Returns the prompting file
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
