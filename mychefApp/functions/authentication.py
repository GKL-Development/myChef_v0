import streamlit as st
import bcrypt
from sqlalchemy.sql import text
import pandas as pd

######################## USER DATA ########################

# # Temporary hard-coded variables
# firstName = 'Louis'
# n = 6

# Defining user class
class User:
    def __init__(self, firstName, userAllerg=None, userDislike=None, userDiet=None, hasMenu=False):
        self.firstName = firstName
        self.userAllerg = userAllerg
        self.userDiet= userDiet
        self.userDislike = userDislike
        self.hasMenu = hasMenu

@st.cache_data
def fetch_user_info(username):
    """Fetch user information in the database to enrich 
    st.session_state.user_instance with the User class"""
    if username:
        fetching_query = ("""
            SELECT firstname, allergens, diet, dislikes, hasmeal FROM users WHERE email = :email
        """)
        # Establishing connection with database
        conn = st.connection('neon', type='sql', ttl=60)
        try:
            user_db = conn.query(fetching_query, params={"email": username}, show_spinner=False)
            if not user_db.empty:
                st.session_state.user_instance = User(
                    firstName=user_db["firstname"].iloc[0], 
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

######################## AUTHENTICATION ########################

# Authentication logic below - To be changed with SSO authentication

# Password hashing
def hash_password(password):
    """Hashing the password for db storage"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Credential verification
@st.cache_data
def credentials(username, password):
    """Verifying users credentials for authentication"""
    if not username or not password:
        return False
    verification_query = ("""
        SELECT password FROM users WHERE email = :email
    """)
    # Establishing connection with database
    conn = st.connection('neon', type='sql', ttl=60)
    try:
        user_pwd = conn.query(verification_query, params={"email": username}, ttl=60, show_spinner=False)
        # Check if the query is not empty
        if not user_pwd.empty: 
            return bcrypt.checkpw(password.encode("utf-8"), user_pwd["password"].iloc[0].encode("utf-8"))
        else:
            # Email or Username not found
            return False 
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

def register():
    return

# Authentication function
def authenticate():
    st.title("Welcome on MyChef")
    st.text("Your weekly meal planner to make cooking meals enjoyable!")
    with st.form("Login"):
        username = st.text_input(label="Enter your email:", type="default")
        password = st.text_input(label="Enter your password:", type="password")
        if st.form_submit_button("Login", use_container_width=True):
            if credentials(username=username, password=password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("Logged in successfully!")
                fetch_user_info(username=username)
                st.rerun()
            else: 
                st.error("Invalid email or password...")
    st.subheader("Not registered yet? Create an account now!")
    if st.button("Register now!"):
        st.warning("Registration is not available. Contact admin@gkldevelopment.com to obtain login credentials!")

