import streamlit as st
from datetime import date
from functions.generateMealPlan import generateMealPlan, selectMealPref
from functions.displayMeals import mealCards
from functions.askUserPreferences import askUserPreferences

####################################### Dashboard ####################################################
ss = st.session_state
lastMeal = st.session_state.user_instance.lastMeal
# Header
with st.container():
    st.title(f'''Hello {st.session_state.user_instance.firstName} 🔆''', anchor=False)
    st.text('Explore and cook delicious recipes for your family and yourself! 🥘')

st.divider()

# Defining CSS rules
st.html(
    """
    <style>
    /* Target images specifically within the 'stImage' container */
    div[data-testid="stImage"] img {
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        border: 0px solid #c5c5c5;
        border-radius: 0px;
        height: 200px;
        object-fit: cover;
    }

    div[data-testid="stColumn"] {
        background-color: #f5f1e6;
        box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #c5c5c5;
        text-align: center;
        border-radius: 8px;
        padding: 10px 20px 20px 20px;
        max-width: 49%;
        justify-content: space-between;
    }

    # div.stButton > button {
    #     max-width: 300px;
    #     width: 100%;
    #     margin: 0 50% 0 50%
    # }
    </style>
    """
)

# Meal content starts here
today = date.today() # Defining today date
todayYear, todayWeek, _ = today.isocalendar() # retrieving today week and year
if lastMeal is not None:
    mealYear, mealWeek, _ = lastMeal.isocalendar() # Retrieving year and weekNum from user lastMeal generation date
    if mealWeek == todayWeek and mealYear == todayYear:
        # Defining page header
        st.subheader('Your Weekly Meals!')
        st.text(f'Never miss a meal with our highly personnalized planner and enjoy cooking seasonal ingredients with your own style!')
        st.html("<br>")
        mealCards()
elif lastMeal is not None or "userPref" in ss or ss.user_instance.hasPref == 'True':
    # Defining page header
    st.subheader('No Meals Generated Yet...')
    st.text("Let's see what on MyChef has planned for you this week! Click the button below to generate your meals and your shopping list.")
    st.html("<br>")
    if "preferences" not in st.session_state:
        if st.button('Plan your weekly meals!', icon='📅', use_container_width=True):
            selectMealPref()
    else:
        generateMealPlan(ss.user_instance.user_id)
else:
    st.subheader("Welcome to MyChef!")
    st.text("We're excited to craft a meal plan that's just right for you! To make it truly personalized, could you share a little more about yourself?")
    st.html("<br>")
    if st.button("Enter the Preferences Form", use_container_width=True, key='prefBtn', type='secondary'):
        askUserPreferences()
        

        