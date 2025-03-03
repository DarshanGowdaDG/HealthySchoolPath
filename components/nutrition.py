import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json

from database import update_progress, get_progress
from ai_helper import get_nutrition_facts

def show_nutrition_section():
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("Nutrition Management")

    tab1, tab2, tab3 = st.tabs([
        "Daily Tracking",
        "Nutritional Information",
        "Meal Planning"
    ])

    with tab1:
        show_daily_tracking()

    with tab2:
        show_nutritional_info()

    with tab3:
        show_meal_planning()

    st.markdown('</div>', unsafe_allow_html=True)

def show_daily_tracking():
    st.header("Daily Nutrition Tracking")

    # Calorie and macro tracking
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Calorie Intake")
        calories = st.number_input(
            "Enter calories consumed",
            min_value=0,
            max_value=5000,
            value=0,
            help="Enter your total calorie intake for the day"
        )

        if st.button("Log Calories"):
            update_progress(
                st.session_state.username,
                "nutrition",
                "calories",
                calories
            )
            st.success("Calories logged successfully!")

    with col2:
        st.subheader("Macronutrients")
        protein = st.number_input("Protein (g)", min_value=0, value=0)
        carbs = st.number_input("Carbohydrates (g)", min_value=0, value=0)
        fats = st.number_input("Fats (g)", min_value=0, value=0)

        if st.button("Log Macros"):
            try:
                update_progress(st.session_state.username, "nutrition", "protein", protein)
                update_progress(st.session_state.username, "nutrition", "carbs", carbs)
                update_progress(st.session_state.username, "nutrition", "fats", fats)
                st.success("Macronutrients logged successfully!")
            except Exception as e:
                st.error("Failed to log macronutrients. Please try again.")

    # Progress visualization
    st.subheader("Nutrition Progress")
    try:
        df = get_progress(st.session_state.username, "nutrition")

        if df.empty:
            dates = [datetime.now() - timedelta(days=x) for x in range(7)]
            calories = [2000, 1800, 2200, 1900, 2100, 1950, 2050]
            df = pd.DataFrame({
                'date': dates,
                'value': calories
            })

        # Calorie intake chart
        fig1 = px.line(
            df,
            x='date',
            y='value',
            title='Calorie Intake Over Time'
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Macronutrient distribution pie chart
        if protein > 0 or carbs > 0 or fats > 0:
            macro_data = pd.DataFrame({
                'Nutrient': ['Protein', 'Carbs', 'Fats'],
                'Grams': [protein, carbs, fats]
            })
            fig2 = px.pie(
                macro_data,
                values='Grams',
                names='Nutrient',
                title='Macronutrient Distribution'
            )
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.warning("Unable to display progress charts. Start tracking to see your progress!")

def show_nutritional_info():
    st.header("Nutritional Information Database")

    with st.container():
        food_item = st.text_input("Search for food item (e.g., 'apple', 'chicken breast')")

        if food_item:
            try:
                with st.spinner("Fetching nutritional information..."):
                    nutrition_data = json.loads(get_nutrition_facts(food_item))

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("#### Basic Information")
                        st.info(f"Serving Size: {nutrition_data['serving_size']}")
                        st.info(f"Calories: {nutrition_data['calories']}")

                        st.markdown("#### Macronutrients")
                        st.info(f"Protein: {nutrition_data['protein']}")
                        st.info(f"Carbohydrates: {nutrition_data['carbs']}")
                        st.info(f"Fats: {nutrition_data['fats']}")

                    with col2:
                        st.markdown("#### Vitamins and Minerals")
                        for vitamin, amount in nutrition_data['vitamins'].items():
                            st.info(f"{vitamin}: {amount}")
            except Exception as e:
                st.error("Unable to fetch nutritional information at the moment.")
                show_sample_nutrition_data(food_item)

def show_sample_nutrition_data(food_item):
    st.info(f"Showing sample data for {food_item}")
    st.markdown("""
    Note: This is example data. Actual nutritional values may vary.

    **Serving Size:** 100g
    **Calories:** 150

    **Macronutrients:**
    - Protein: 5g
    - Carbohydrates: 25g
    - Fats: 3g

    **Vitamins & Minerals:**
    - Vitamin A: 10% DV
    - Vitamin C: 15% DV
    - Iron: 8% DV
    """)

def show_meal_planning():
    st.header("Meal Planning")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_day = st.selectbox("Select day", days)

    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]

    if 'meal_plans' not in st.session_state:
        st.session_state.meal_plans = {}

    if selected_day not in st.session_state.meal_plans:
        st.session_state.meal_plans[selected_day] = {
            meal: "" for meal in meals
        }

    st.subheader(f"Meal Plan for {selected_day}")

    for meal in meals:
        with st.expander(f"{meal} Plan", expanded=True):
            meal_input = st.text_area(
                f"Enter {meal.lower()} details",
                value=st.session_state.meal_plans[selected_day][meal],
                key=f"{selected_day}_{meal}"
            )
            st.session_state.meal_plans[selected_day][meal] = meal_input

            st.markdown("**Suggested Healthy Options:**")
            suggestions = {
                "Breakfast": [
                    "Oatmeal with fruits and nuts",
                    "Greek yogurt with granola",
                    "Whole grain toast with avocado"
                ],
                "Lunch": [
                    "Quinoa salad with vegetables",
                    "Grilled chicken sandwich",
                    "Vegetable soup with whole grain bread"
                ],
                "Dinner": [
                    "Grilled fish with roasted vegetables",
                    "Lean protein with brown rice",
                    "Vegetarian stir-fry"
                ],
                "Snacks": [
                    "Fresh fruits",
                    "Mixed nuts",
                    "Vegetable sticks with hummus"
                ]
            }

            for suggestion in suggestions[meal]:
                st.markdown(f"• {suggestion}")

    if st.button("Save Meal Plan"):
        st.success(f"Meal plan for {selected_day} saved successfully!")
        st.balloons()

    # Weekly Overview
    st.subheader("Weekly Overview")
    st.write("Your planned meals for the week:")

    for day in days:
        if day in st.session_state.meal_plans:
            with st.expander(day):
                for meal, plan in st.session_state.meal_plans[day].items():
                    if plan:
                        st.markdown(f"**{meal}:** {plan}")