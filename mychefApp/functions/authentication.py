import streamlit as st
import bcrypt
from sqlalchemy.sql import text
import pandas as pd # Check whether this makes app crash or not // if not then remove
import time
from streamlit_cookies_controller import CookieController

# Instanciating cookies controller 
cookie_controller = CookieController()

######################## USER DATA ########################

# Creates a db connection and cache it
@st.cache_resource()
def init_connection():
    return st.connection('neon', type='sql')

# Defining user class for session state variable
class User:
    def __init__(self, firstName, lastName, userAllerg=None, userDislike=None, userDiet=None, hasMenu=False):
        self.firstName = firstName
        self.lastName = lastName
        self.userAllerg = userAllerg
        self.userDiet= userDiet
        self.userDislike = userDislike
        self.hasMenu = hasMenu

def fetch_user_info(email):
    """Fetch user information in the database to enrich 
    st.session_state.user_instance with the User class"""
    if email:
        fetching_query = ("""
            SELECT firstname, lastname, allergens, diet, dislikes, hasmeal FROM users WHERE email = :email
        """)
        # Establishing connection with database
        conn = init_connection()
        try:
            user_db = conn.query(fetching_query, params={"email": email}, show_spinner=False)
            if not user_db.empty:
                st.session_state.user_instance = User(
                    firstName=user_db["firstname"].iloc[0], 
                    lastName=user_db['lastname'].iloc[0],
                    userAllerg=user_db["allergens"].iloc[0], 
                    userDiet=user_db["diet"].iloc[0], 
                    userDislike=user_db["dislikes"].iloc[0], 
                    hasMenu=user_db["hasmeal"].iloc[0]
                )
                return True
            else:
                st.error("User not found in the database")
                return False
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return False
    else:
        st.error("Contact customer support at admin@gkldevelopment.com")
        return False

######################## AUTHENTICATION & REGISTRATION ########################

# Authentication logic below - To be changed with SSO authentication

# Password hashing
def hash_password(password):
    """Hashing the password for db storage"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Credential verification for user authentication
def credentials(email, password):
    """Verifying users credentials for authentication"""
    if not email or not password:
        return False
    verification_query = ("""
        SELECT password FROM users WHERE email = :email
    """)
    # Establishing connection with database
    conn = init_connection()
    try:
        user_pwd = conn.query(verification_query, params={"email": email}, ttl=5, show_spinner=False)
        # Check if the query is not empty
        if not user_pwd.empty: 
            return bcrypt.checkpw(password.encode("utf-8"), user_pwd["password"].iloc[0].encode("utf-8"))
        else:
            # Email or Username not found
            return False 
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

# Registration protocol
def registration_protocol(email, password, firstname, lastname, sex, birthdate, username, hasmeal=False):
    """Registration protocol for user inscription in database"""
    if not email or not password:
        return False
    usr_variable_dict = {
        "email": email,
        "password": hash_password(password=password),
        "firstname": firstname,
        "lastname": lastname,
        "sex": sex,
        "birthdate": birthdate,
        "hasmeal": hasmeal,
        "username": username
    }
    registration_query = ("""
        INSERT INTO users(
        user_id,
        firstname,
        lastname,
        sex,
        birthdate,
        email,
        hasmeal,
        password,
        username,
        allergens,
        diet,
        dislikes
        )
        VALUES (
        DEFAULT,
        :firstname,
        :lastname,
        :sex,
        :birthdate,
        :email,
        :hasmeal,
        :password,
        :username,
        NULL,
        NULL,
        NULL
        )
    """)
    conn = init_connection()
    with conn.session as s:
        try:
            s.execute(text(registration_query), usr_variable_dict)
            s.commit()
        except Exception as e:
            st.error(f"Invalid email or password... Please try again or contact us {e}")
            st.stop()
    return True

@st.dialog("Please complete credentials information:")
def registration_dialog(email, password):
    # Defining gender dictionnary for user informations
    gender_dict = {
        "Male": "M",
        "Female": "F",
        ":rainbow[Other]": "O",
        "Don't Specify": None
    }
    # Sarting dialog form
    st.write("Thank you for signing up!" \
    "We want to get to know you a bit more before you can access the app.")

    # Prompting user for information
    firstname = st.text_input("What is your firstname?")
    lastname = st.text_input("What is your lastname?")
    username = st.text_input("Enter a username:")
    birthdate = st.date_input("When's your birthdate?", value=None, min_value="1900-01-01")
    gender_choice = st.radio("What gender are you?",["Male", "Female", ":rainbow[Other]", "Don't Specify"])
    sex = gender_dict[gender_choice]
    if st.button("Submit", use_container_width=True):
        if not firstname or not lastname or not birthdate or not sex:
            st.warning("One of the information has not been filled.")
        else:
            if registration_protocol(email=email, password=password, firstname=firstname, lastname=lastname, birthdate=birthdate, sex=sex, username=username):
                # Useless design for database communication waiting time
                progress_text = "Registration in progress..."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(0,100):
                    my_bar.progress(percent_complete+1, text=progress_text)
                    time.sleep(0.02)
                time.sleep(1)
                my_bar.empty
                st.success("Registered successfully!")
                # Fetching user info on db
                if fetch_user_info(email=email):
                    st.session_state["authenticated"] = True
                    st.session_state["email"] = email
                    st.rerun()
                else:
                    st.error("Failed to fetch user information after registration. Please try logging in manually.")
            else:
                st.error("Registration failed. Please try again or contact support.")

# Registration function for visual form and onboarding
def register():
    """User are going to be onboarded through this function and the information are pushed to the database through registration protocol"""
    # with st.("Not registered yet? Create an account now!"):
    # st.subheader("Not registered yet? Create an account now!")
    with st.form("Register", enter_to_submit=True):
        email = st.text_input(label="Enter your email:", type="default").lower()
        password = st.text_input(label="Enter your password:", type="password")
        confirm_pwd = st.text_input(label="Confirm your password:", type="password")
        if st.form_submit_button("Register now!", use_container_width=True):    
            if password == confirm_pwd: 
                registration_dialog(email=email, password=password)
            else:
                st.warning("Passwords must match! Please check if there is no typos.")

# Authentication function for login
def authenticate():
    """User are being signed in after credential verification protocol with database user informations"""
    with st.form("Login", enter_to_submit=True):
        email = st.text_input(label="Enter your email:", type="default").lower()
        password = st.text_input(label="Enter your password:", type="password")
        st.checkbox("Remember Me", on_change=cookie_controller.set("user_email", email))
        if st.form_submit_button("Login", use_container_width=True):
            if credentials(email=email, password=password):
                # Useless design for database communication waiting time
                progress_text = "Registration in progress..."
                my_bar = st.progress(0, text=progress_text)
                my_bar.progress(0, text=progress_text)
                time.sleep(0.01)
                my_bar.progress(30, text=progress_text)
                time.sleep(0.01)
                my_bar.progress(70, text=progress_text)
                time.sleep(0.01)
                my_bar.progress(100, text=progress_text)
                time.sleep(1)
                my_bar.empty
                st.success("Logged in successfully!")
                # Fetching user info on db
                if fetch_user_info(email=email):
                    st.session_state["authenticated"] = True
                    st.session_state["email"] = email
                    st.rerun()
                else:
                    st.error("Failed to fetch user information after registration. Please try logging in manually.")
            else: 
                st.error("Invalid email or password...")