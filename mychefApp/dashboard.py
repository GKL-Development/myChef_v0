# Import packages and dependencies
import streamlit as st
import pandas as pd


################################## Variable, classes and functions ########################################

# Temporary hard-coded variables
firstName = 'Louis'

# Defining user class
class User:
    def __init__(self, userName, userAllerg=None, userDislike=None, userDiet=None):
        self.userName = userName
        self.userAllerg = userAllerg
        self.userDiet= userDiet
        self.userDislike = userDislike

if "user_instance" not in st.session_state:
    # Instanciating session 
    st.session_state.user_instance = User(firstName)


####################################### Streamlit Web App ####################################################

# Logo image
st.logo("./img/logo/row_no_sentence.png", size = "large")

# Title
with st.container():
    st.title(f'''Hello {st.session_state.user_instance.userName}''', anchor=False)
    st.text('Explore and cook delicious recipes for your family and yourself! 🥘')

st.divider()

# Daily recipe
with st.container():
    st.subheader('Today', anchor='todayMeal')
    st.image("./img/weeklyMealImg/mondayMeal.jpg")

