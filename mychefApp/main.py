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
    ]
    # "Ressources":[
    #     st.Page(
    #         "", 
    #         title="About Us"
    #         ),
    #     st.Page(
    #         "",
    #         title="Profile"
    #     )
    # ]
}

pg=st.navigation(pages)
pg.run()