# Import packages and dependencies
import streamlit as st
import pandas as pd
from dependencies import User, firstName, n


if "user_instance" not in st.session_state:
    # Instanciating session 
    st.session_state.user_instance = User(firstName)

####################################### Streamlit Web App ####################################################

# Header
with st.container():
    st.title(f'''Hello {st.session_state.user_instance.userName} 🔆''', anchor=False)
    st.text('Explore and cook delicious recipes for your family and yourself! 🥘')

st.divider()

st.subheader('Your Weekly Meals!')
st.text(f'Never miss a meal with our highly personnalized planner and enjoy cooking seasonal ingredients with your own style!')
st.markdown("""<br>""", unsafe_allow_html=True)

# Weekly meals columns generation
col1, col2, col3 = st.columns(spec=3, gap="small", vertical_alignment="top", border=True)
col4, col5, col6 = st.columns(spec=3, gap="small", vertical_alignment="top", border=True)

# Defining CSS rules
st.markdown(
    """
    <style>
    /* Target images specifically within the 'stImage' container */
    div[data-testid="stImage"] img {
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        border: 1px solid #c5c5c5;
    }

    div[data-testid="stColumn"] {
        # background-color: #e6e4d4;
        box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #c5c5c5;

    }
    </style>
    """,
    unsafe_allow_html=True
)

# Defining meal cards
with col1:
    # Monday meal card
    st.subheader("Monday")
    st.image('./img/weeklyMealImg/chicken.jpg', caption='One-Pan Lemon-Thyme Chicken with Spring Vegetables', use_container_width=True, width=300)
    st.markdown(
        ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
    )
    # st.button(label='Cook now!', use_container_width=True)

with col2:
    # Tuesday meal card
    st.subheader("Tuesday")
    st.image('./img/weeklyMealImg/asparagus_egg.jpg', caption='White Asparagus with Poached Eggs and Lemon-Butter Sauce', use_container_width=True, width=300)
    st.markdown(
        ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
    )
    # st.button(label='Cook now!', use_container_width=True)

with col3:
    # Wednesday meal card
    st.subheader("Wednesday")
    st.image('./img/weeklyMealImg/favabeans_soup.jpg', caption='Spring Vegetable Soup with Fava Beans and Mint', use_container_width=True, width=300)
    st.markdown(
        ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
    )
    # st.button(label='Cook now!', use_container_width=True)

with col4:
    # Thursday meal card
    st.subheader("Thursday")
    st.image('./img/weeklyMealImg/salmon.jpg', caption='Steamed Salmon with Spring Vegetables and Dill Dressing', use_container_width=True, width=300)
    st.markdown(
        ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
    )
    # st.button(label='Cook now!', use_container_width=True)

with col5:
    # Friday meal card
    st.subheader("Friday")
    st.image('./img/weeklyMealImg/frittata.jpg', caption='Ramp and Potato Frittata', use_container_width=True, width=300)
    st.markdown(
        ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
    )
    # st.button(label='Cook now!', use_container_width=True)

with col6:
    # Saturday meal card
    st.subheader("Saturday")
    st.image('./img/weeklyMealImg/halloumi_strawberries.jpg', caption='Pan-Fried Halloumi with Spinach and Strawberries', use_container_width=True, width=300)
    st.markdown(
        ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
    )
    # st.button(label='Cook now!', use_container_width=True)

# with col7:
#     # Sunday meal card
#     st.subheader("Sunday")
#     st.image('./img/weeklyMealImg/lamb_carrot.jpg', caption='Roasted Spring Lamb Chops with Carrots and Rosemary', use_container_width=True, width=300)
#     st.markdown(
#         ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
#     )
#     st.button(label='Cook now!', use_container_width=True)
