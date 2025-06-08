# import json
# from sqlalchemy.sql import text
# from datetime import date
# import base64

# Dependencies for Gemini AI prompt
import streamlit as st
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

def gemini_ai_api(input, temp):
    client = genai.Client(
        api_key=st.secrets["gemini_api_key"],
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input), # Query to generate meals based on user preferences
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=(temp+1)/10,
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
                                type = genai.types.Type.STRING,
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
                                type = genai.types.Type.STRING,
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

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return response.text

