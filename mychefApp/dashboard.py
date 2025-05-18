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

# Streamlit web page
st.title(f'''Hello {st.session_state.user_instance.userName}''')
st.write('Your meal planning organization, in one place')
