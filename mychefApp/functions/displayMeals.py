import streamlit as st
from datetime import date
from functions.db_fetch_functions import fetch_user_recipes
import math

################################## Variable, classes and functions ########################################

ss = st.session_state

# @st.cache_data(max_entries=200)
def mealCards():
    # Defining weekdays for column generation
    weekDays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    today = date.today()           
    # Fetching meal plan recipes
    weeklyPlan, recipesId = fetch_user_recipes(ss.user_instance.user_id, today)
    ss["recipesId"] = recipesId 
    # Starting columns generation
    numberOfRecipes = len(weeklyPlan) # Defines the number of recipes for the column generation
    max_columns = 2 # Defining the max recipes columns per row 
    num_of_row = math.ceil(numberOfRecipes / max_columns) # Calculating row needed
    current_col = 0 # Set the current col number for weeklyPlan dict parsing
    for row in range(num_of_row):
        # Calculates the number of columns needed to fill the current row // It will take max_columns if there are more than 3 to be processed
        column_in_row = min(max_columns, numberOfRecipes - current_col)
        if column_in_row > 0: # Creates a new row only if they are still columns to be processed
            cols = st.columns(column_in_row, vertical_alignment='top')
            for i in range(column_in_row):
                with cols[i]:
                    recipe_day = st.subheader(weekDays[current_col])
                    st.image('./img/weeklyMealImg/placeholder.jpg', caption=weeklyPlan[current_col]['recipetitle'], use_container_width=True, width=300)
                    st.markdown(f"{":green-badge[:material/check: Allergen Free]" if "None" in weeklyPlan[current_col]['allergens'] else f":orange-badge[⚠️{weeklyPlan[current_col]['allergens']}]"} :blue-badge[🕒 Ready in {weeklyPlan[current_col]['totaltime']}]")
                    recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
                    if recipe_details:
                        st.warning("Not functional yet. Try again later.")
                current_col += 1