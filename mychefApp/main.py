import streamlit as st
from functions.authentication import authenticate

# Logo image
st.logo("./img/logo/row_no_sentence.png", size = "large")

# if "authenticated" not in st.session_state: # To be replaced by -> if not st.user.authenticated:
#     st.session_state["authenticated"] = False
#     st.session_state["username"] = None

if st.session_state["authenticated"]:
    if "user_instance" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.error("Database connection failed. Try login again or contact support at admin@gkldevelopment.com")
        st.rerun() # Rerun to show login form
    if st.sidebar.button("Check our crowdfunding!", use_container_width=True):
        st.sidebar.warning("Not yet live. Come back in a couple of days!")
    if st.sidebar.button("Logout", use_container_width=True, type="primary"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.success("Logged out successfully!")
        st.rerun() # Rerun to show login form
    # st.sidebar.divider()
    # st.sidebar.markdown("<i>MyChef© by GKL Development</i>", unsafe_allow_html=True)

    # Defining navigation
    pages = {
        "MyChef":[
            st.Page(
                "dashboard.py",
                title='Dashboard',
                icon="🏠",
                default=True
            ),
            st.Page(
                "shoppingList.py",
                title='Shopping List',
                icon="🗒️"
            )
        ],
        "Ressources":[
            st.Page(
                "about.py", 
                title="About Us",
                icon='🌐'
                ),
            st.Page(
                "profile.py",
                title="Profile",
                icon="👤"
            ),
            st.Page(
                "testing.py",
                title="Testing",
                icon='🧪'
            )
        ]
    }

    pg=st.navigation(pages)
    pg.run()
else:
    authenticate()