
import streamlit as st
from datetime import datetime

def send_notification(message):
    """
    Sends a notification to the user using Streamlit's built-in notification system
    """
    st.toast(message)

def format_date(date):
    """
    Formats a date object into a readable string
    """
    return date.strftime("%B %d, %Y")

def calculate_streak(dates):
    """
    Calculates the current streak given a list of dates
    """
    if not dates:
        return 0
        
    dates = sorted(dates)
    current_date = datetime.now().date()
    streak = 1
    
    for i in range(len(dates)-1, 0, -1):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
        else:
            break
    
    return streak

def get_difficulty_multiplier(difficulty):
    """
    Returns a multiplier based on the difficulty level
    """
    multipliers = {
        "Easy": 1.0,
        "Intermediate": 1.5,
        "Hard": 2.0
    }
    return multipliers.get(difficulty, 1.0)

def calculate_calories_burned(activity, duration, difficulty):
    """
    Calculates calories burned based on activity type, duration, and difficulty
    """
    base_calories = {
        "Walking": 5,
        "Running": 10,
        "Swimming": 8,
        "Cycling": 7,
        "HIIT": 12
    }
    
    calories_per_minute = base_calories.get(activity, 5)
    multiplier = get_difficulty_multiplier(difficulty)
    
    return calories_per_minute * duration * multiplier
