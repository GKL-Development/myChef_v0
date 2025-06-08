# Import packages and dependencies
import streamlit as st
# from functions.authentication import User
from functions.displayMeals import mealCards

####################################### Dashboard ####################################################

# Header
with st.container():
    st.title(f'''Hello {st.session_state.user_instance.firstName} 🔆''', anchor=False)
    st.text('Explore and cook delicious recipes for your family and yourself! 🥘')

st.divider()

# Defining CSS rules
st.markdown(
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
        # background-color: #e6e4d4;
        box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #c5c5c5;
        text-align: center;
        border-radius: 8px;
        padding: 10px 20px 20px 20px;
        max-width: 49%;
        justify-content: space-between;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Meal content starts here

mealCards(st.session_state.user_instance.lastMeal)