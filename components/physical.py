
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import json
import pandas as pd

from database import update_progress, get_progress, update_streak
from ai_helper import generate_exercise_guide

def show_physical_section():
    st.title("Physical Health")
    
    # Difficulty selection
    difficulty = st.radio(
        "Select difficulty level",
        ["Easy", "Intermediate", "Hard"]
    )
    
    # Exercise schedule
    st.subheader("Weekly Exercise Schedule")
    show_exercise_schedule(difficulty)
    
    # Progress tracking
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Calories Burned")
        show_calories_chart()
        
    with col2:
        st.subheader("Water Intake")
        show_water_tracking()
    
    # Exercise guide
    st.subheader("Exercise Guide")
    show_exercise_guide()

def show_exercise_schedule(difficulty):
    exercises = {
        "Easy": {
            "Monday": ["Walking (20 min)", "Stretching (10 min)"],
            "Tuesday": ["Light Yoga (15 min)", "Basic Squats (10 reps)"],
            "Wednesday": ["Swimming (15 min)", "Arm Circles (2 sets)"],
            "Thursday": ["Walking (20 min)", "Wall Push-ups (10 reps)"],
            "Friday": ["Light Yoga (15 min)", "Leg Raises (10 reps)"]
        },
        "Intermediate": {
            "Monday": ["Jogging (30 min)", "Push-ups (15 reps)"],
            "Tuesday": ["Strength Training (30 min)", "Core Workout"],
            "Wednesday": ["HIIT (20 min)", "Yoga (20 min)"],
            "Thursday": ["Running (25 min)", "Body Weight Exercises"],
            "Friday": ["Circuit Training (30 min)", "Stretching"]
        },
        "Hard": {
            "Monday": ["HIIT (45 min)", "Advanced Strength Training"],
            "Tuesday": ["Sprint Intervals (30 min)", "Power Yoga"],
            "Wednesday": ["CrossFit WOD", "Heavy Lifting"],
            "Thursday": ["Endurance Training (60 min)", "Plyometrics"],
            "Friday": ["Advanced Circuit Training", "Core Challenge"]
        }
    }
    
    current_day = datetime.now().strftime("%A")
    
    for day, workout in exercises[difficulty].items():
        with st.expander(f"{day} {'(Today)' if day == current_day else ''}"):
            for exercise in workout:
                if st.button(f"Complete {exercise}", key=f"btn_{day}_{exercise}"):
                    update_progress(
                        st.session_state.username,
                        "physical",
                        exercise,
                        1
                    )
                    update_streak(st.session_state.username, "daily_exercise")
                    st.success(f"Completed {exercise}!")

def show_calories_chart():
    # Get calorie data from database
    df = get_progress(st.session_state.username, "physical")
    
    # Create sample data if none exists
    if df.empty:
        dates = [datetime.now() - timedelta(days=x) for x in range(7)]
        calories = [300, 250, 400, 350, 300, 450, 350]
        df = pd.DataFrame({
            'date': dates,
            'value': calories
        })
    
    fig = px.line(df, x='date', y='value', title='Calories Burned Over Time')
    st.plotly_chart(fig)

def show_water_tracking():
    st.write("Track your daily water intake")
    
    target_intake = 8  # glasses
    current_intake = st.number_input(
        "Glasses of water consumed today",
        min_value=0,
        max_value=20,
        value=0
    )
    
    progress = (current_intake / target_intake) * 100
    st.progress(min(progress / 100, 1.0))
    
    if st.button("Log Water Intake"):
        update_progress(
            st.session_state.username,
            "physical",
            "water_intake",
            current_intake
        )
        st.success(f"Logged {current_intake} glasses of water!")

def show_exercise_guide():
    exercise = st.selectbox(
        "Select exercise to learn proper form",
        ["Push-ups", "Squats", "Planks", "Burpees", "Mountain Climbers"]
    )
    
    if exercise:
        guide = json.loads(generate_exercise_guide(exercise))
        
        st.write("### Proper Form")
        st.write(guide["proper_form"])
        
        st.write("### Common Mistakes")
        st.write(guide["common_mistakes"])
        
        st.write("### Benefits")
        st.write(guide["benefits"])
        
        st.write("### Recommended Sets and Reps")
        st.write(guide["recommended_sets_reps"])
