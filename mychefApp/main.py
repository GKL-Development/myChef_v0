import streamlit as st
# import dashboard, shoppingList

# Logo image
st.logo("./img/logo/row_no_sentence.png", size = "large")

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