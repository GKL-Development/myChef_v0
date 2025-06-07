import streamlit as st
import bcrypt
from sqlalchemy.sql import text
import time
from authentication import init_connection

@st.cache_data(max_entries=200, ttl=3600)
def fetch_user_recipes(userId, date):
    """Fetching recipes informations from the database to return user meal plan"""
    if userId and date:
        _, week, _ = date.isocalendar()
        recipeQuery = """
            SELECT meal_id, 
            recipetitle, 
            yield, 
            preptime, 
            cooktime, 
            mychefnotes, 
            equipment, 
            instructions, 
            allergens, 
            ismeatorfish, 
            recipeimg,
            totaltime
            FROM meals
            WHERE 1=1
            AND creator_id = :user 
            AND DATE_PART('week', creationdate) = :week
        """
        params = {
            "user": userId,
            "week": week
        }
        conn = init_connection()
        recipes = conn.query(recipeQuery, params=params, show_spinner=False)
        if not recipes.empty:
            weeklyPlanDict = {}
            for recipeNum in range(len(recipes)):
                weeklyPlanDict[recipeNum] = {column : recipes[column].iloc[recipeNum] for column in recipes.columns}
            recipesId = recipes["meal_id"].tolist()
            return weeklyPlanDict, recipesId
        else:
            st.error("Cannot fetch weekly plan. Please reload the page and contact us if the error persist" \
            "Contact: admin@gkldevelopment.com")
            st.stop()
    else:
        st.error("Invalid user or date")

@st.cache_data(max_entries=200, ttl=3600)
def fetch_recipes_ingredients(userId, recipesId):
    """Fetching recipes ingredients from the database to return user weekly shopping list"""
    if userId and recipesId:
        ingredientsQuery = """
            SELECT
            quantity,
            unit,
            ingredient_name
            FROM ingredients
            WHERE 1=1
            AND recipe_id IN :recipeIdList
        """
        params = {"recipeIdList": recipesId}
        conn = init_connection()
        ingredients = conn.query(ingredientsQuery, params=params, show_spinner=False)
        if not ingredients.empty:
            for ingredient in range(len(ingredients)):
                st.checkbox(ingredients.iloc[ingredient].tolist())
        else:
            st.error("Cannot fetch shopping list ingredients. Please reload the page and contact us if the error persist" \
            "Contact: admin@gkldevelopment.com")
    else:
        st.error("Invalid user or date")