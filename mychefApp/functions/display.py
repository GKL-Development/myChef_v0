import streamlit as st

################################## Variable, classes and functions ########################################

def mealCards(hasMenu):
    '''
    The function render meal cards with the weekly plan content.
    If the user has not yet generated a meal planning the it will prompt user for generation 
    '''
    if hasMenu:
        # Defining page header
        st.subheader('Your Weekly Meals!')
        st.text(f'Never miss a meal with our highly personnalized planner and enjoy cooking seasonal ingredients with your own style!')
        st.markdown("""<br>""", unsafe_allow_html=True)
        
        # Weekly meals columns generation
        col1, col2 = st.columns(spec=2, gap="small", vertical_alignment="top", border=True)
        col3, col4 = st.columns(spec=2, gap="small", vertical_alignment="top", border=True)
        col5, col6 = st.columns(spec=2, gap="small", vertical_alignment="top", border=True)

        # Defining meal cards
        with col1:
            # Monday meal card
            recipe_day = st.subheader("Monday")
            st.image('./img/weeklyMealImg/chicken.jpg', caption='One-Pan Lemon-Thyme Chicken with Spring Vegetables', use_container_width=True, width=300)
            st.markdown(
                ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            )
            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)

        with col2:
            # Tuesday meal card
            recipe_day= st.subheader("Tuesday")
            st.image('./img/weeklyMealImg/asparagus_egg.jpg', caption='White Asparagus with Poached Eggs and Lemon-Butter Sauce', use_container_width=True, width=300)
            st.markdown(
                ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            )
            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)

        with col3:
            # Wednesday meal card
            recipe_day = st.subheader("Wednesday")
            st.image('./img/weeklyMealImg/favabeans_soup.jpg', caption='Spring Vegetable Soup with Fava Beans and Mint', use_container_width=True, width=300)
            st.markdown(
                ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            )
            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
        with col4:
            # Thursday meal card
            recipe_day = st.subheader("Thursday")
            st.image('./img/weeklyMealImg/salmon.jpg', caption='Steamed Salmon with Spring Vegetables and Dill Dressing', use_container_width=True, width=300)
            st.markdown(
                ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            )
            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
        with col5:
            # Friday meal card
            recipe_day = st.subheader("Friday")
            st.image('./img/weeklyMealImg/frittata.jpg', caption='Ramp and Potato Frittata', use_container_width=True, width=300)
            st.markdown(
                ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            )
            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
        with col6:
            # Saturday meal card
            recipe_day = st.subheader("Saturday")
            st.image('./img/weeklyMealImg/halloumi_strawberries.jpg', caption='Pan-Fried Halloumi with Spinach and Strawberries', use_container_width=True, width=300)
            st.markdown(
                ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            )
            recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
        # with col7:
            # # Sunday meal card
            # recipe_day = st.subheader("Sunday")
            # st.image('./img/weeklyMealImg/lamb_carrot.jpg', caption='Roasted Spring Lamb Chops with Carrots and Rosemary', use_container_width=True, width=300)
            # st.markdown(
            #     ":green-badge[:material/check: Allergen Free] :blue-badge[🕒 Ready in 23 min]"
            # )
            # recipe_details = st.button("Cook Now!", key=recipe_day, use_container_width=True)
    else:
        # Defining page header
        st.subheader('No Meals Generated Yet...')
        st.text("Let's see what on MyChef has planned for you this week! Click the button below to generate your meals and your shopping list.")
        st.markdown("""<br>""", unsafe_allow_html=True)
        if st.button('Plan your meals!', icon='📅', use_container_width=True):
            st.warning("Function currently unavailable... Follow us on instagram to keep track of our latest updates!") 

# def mealPlanGenerator(userId):
