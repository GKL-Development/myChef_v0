import streamlit as st
from datetime import date
from functions.db_fetch_functions import fetch_user_recipes
import math

################################## Variable, classes and functions ########################################

ss = st.session_state

# @st.cache_data(max_entries=200)
def mealCards(lastMeal):
    '''
    The function render meal cards with the weekly plan content.
    If the user has not yet generated a meal planning the it will prompt user for generation 
    '''
    if lastMeal is not None:
        today = date.today() # Defining today date
        todayYear, todayWeek, _ = today.isocalendar() # retrieving today week and year
        mealYear, mealWeek, _ = lastMeal.isocalendar() # Retrieving year and weekNum from user lastMeal generation date

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

        # Verifying if last meal has been generated this week
        if mealWeek == todayWeek and mealYear == todayYear:
            # Defining page header
            st.subheader('Your Weekly Meals!')
            st.text(f'Never miss a meal with our highly personnalized planner and enjoy cooking seasonal ingredients with your own style!')
            st.markdown("""<br>""", unsafe_allow_html=True)

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
                    cols = st.columns([1, 1], gap='small', vertical_alignment='top', border=True)
                    for i in range(column_in_row):
                        with cols[i]:
                            recipe_day = st.subheader(weekDays[current_col])
                            st.image('./img/weeklyMealImg/placeholder.jpg', caption=weeklyPlan[current_col]['recipetitle'], use_container_width=True, width=300)
                            st.markdown(f"{":green-badge[:material/check: Allergen Free]" if weeklyPlan[current_col]['allergens'] == "['None']" else f":orange-badge[⚠️{weeklyPlan[current_col]['allergens']}]"} :blue-badge[🕒 Ready in {weeklyPlan[current_col]['totaltime']}")
                            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
                            if recipe_details:
                                st.warning("Not functional yet. Try again later.")
                        current_col += 1

            
            # with col6:
            #     # Saturday meal card
            #     recipe_day = st.subheader("Saturday")
            #     st.image('./img/weeklyMealImg/halloumi_strawberries.jpg', caption='Pan-Fried Halloumi with Spinach and Strawberries', use_container_width=True, width=300)
            #     st.markdown(
            #         ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            #     )
            #     recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
        else:
            # Defining page header
            st.subheader('No Meals Generated Yet...')
            st.text("Let's see what on MyChef has planned for you this week! Click the button below to generate your meals and your shopping list.")
            st.markdown("""<br>""", unsafe_allow_html=True)
            if st.button('Plan your weekly meals!', icon='📅', use_container_width=True):
                st.warning("Function currently unavailable... Follow us on instagram to keep track of our latest updates!") 
    else:
        st.subheader("You have never generated meal plan.")
        st.text("We would love to know a bit more about your food preferences before generating your first meal plan")
        st.markdown("""<br>""", unsafe_allow_html=True)
        if st.button('Your weekly plan are a just a click away', icon='📅', use_container_width=True):
            st.warning("Function currently unavailable... Follow us on instagram to keep track of our latest updates!")
# def mealPlanGenerator(userId):
