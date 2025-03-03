import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from database import update_progress, get_progress

def show_mental_section():
    st.title("Mental Health & Wellness")

    tab1, tab2, tab3 = st.tabs([
        "Mood Tracking",
        "Stress Management",
        "Focus & Productivity"
    ])

    with tab1:
        show_mood_tracking()

    with tab2:
        show_stress_management()

    with tab3:
        show_focus_tracking()

def show_mood_tracking():
    st.header("Daily Mood Tracker")

    # Mood selection
    mood_options = {
        "😊 Happy": 5,
        "😌 Calm": 4,
        "😐 Neutral": 3,
        "😕 Stressed": 2,
        "😢 Sad": 1
    }

    selected_mood = st.selectbox(
        "How are you feeling today?",
        list(mood_options.keys())
    )

    mood_notes = st.text_area("Add any notes about your mood")

    if st.button("Log Mood"):
        update_progress(
            st.session_state.username,
            "mental",
            "mood",
            mood_options[selected_mood]
        )
        if mood_notes:
            update_progress(
                st.session_state.username,
                "mental",
                "mood_notes",
                mood_notes
            )
        st.success("Mood logged successfully!")

    # Show mood history
    try:
        df = get_progress(st.session_state.username, "mental")
        if not df.empty:
            fig = px.line(
                df,
                x='date',
                y='value',
                title='Mood Trends'
            )
            st.plotly_chart(fig)
    except Exception as e:
        st.info("Start tracking your mood to see trends here!")

def show_stress_management():
    st.header("Stress Management Tools")

    # Breathing exercise
    with st.expander("🫁 Guided Breathing Exercise", expanded=True):
        st.markdown("""
        Follow this simple breathing exercise:
        1. Inhale for 4 seconds
        2. Hold for 4 seconds
        3. Exhale for 4 seconds
        4. Repeat 5 times
        """)

        if st.button("Start Breathing Exercise"):
            import time
            for i in range(5):
                st.markdown(f"Round {i+1}")
                with st.spinner("Inhale... 💨"):
                    time.sleep(4)
                with st.spinner("Hold... ✋"):
                    time.sleep(4)
                with st.spinner("Exhale... 😮‍💨"):
                    time.sleep(4)
            st.success("Exercise complete! Great job!")

    # Stress triggers
    with st.expander("🎯 Identify Stress Triggers"):
        triggers = st.multiselect(
            "What triggers stress for you?",
            ["Academic pressure", "Time management", "Social situations",
             "Health concerns", "Future planning", "Other"]
        )

        if triggers:
            st.markdown("### Recommended Coping Strategies:")
            for trigger in triggers:
                if trigger == "Academic pressure":
                    st.markdown("- Break large tasks into smaller ones")
                    st.markdown("- Use the Pomodoro technique")
                elif trigger == "Time management":
                    st.markdown("- Create a daily schedule")
                    st.markdown("- Set realistic goals")
                else:
                    st.markdown("- Practice mindfulness")
                    st.markdown("- Talk to someone you trust")

def show_focus_tracking():
    st.header("Focus & Productivity Tracking")

    # Study session timer
    st.subheader("📚 Study Session Timer")
    duration = st.slider("Session duration (minutes)", 5, 60, 25)

    # Initialize session state for timer
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = None

    # Start/Stop button
    if not st.session_state.timer_running:
        if st.button("Start Study Session"):
            st.session_state.timer_running = True
            st.session_state.start_time = datetime.now()
            st.session_state.time_remaining = duration * 60  # Convert to seconds
            st.rerun()
    else:
        if st.button("Stop Study Session"):
            st.session_state.timer_running = False

            # Record completed session
            elapsed_minutes = duration - (st.session_state.time_remaining // 60)
            if elapsed_minutes > 0:
                update_progress(
                    st.session_state.username,
                    "mental",
                    "focus_session",
                    elapsed_minutes
                )
                st.success(f"Completed {elapsed_minutes} minute focus session!")
            st.rerun()

    # Display timer if running
    if st.session_state.timer_running:
        # Calculate time elapsed and remaining
        time_elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        time_remaining = max(0, duration * 60 - time_elapsed)
        st.session_state.time_remaining = time_remaining

        # Display progress bar and time remaining
        progress = 1 - (time_remaining / (duration * 60))
        st.progress(progress)

        mins, secs = divmod(int(time_remaining), 60)
        time_display = st.empty()
        time_display.markdown(f"### ⏱️ Time Remaining: {mins:02d}:{secs:02d}")

        # Force rerun to update timer
        if time_remaining > 0:
            import time
            time.sleep(1)
            st.rerun()

        # Check if timer completed
        if time_remaining <= 0:
            st.session_state.timer_running = False
            update_progress(
                st.session_state.username,
                "mental",
                "focus_session",
                duration
            )
            st.balloons()
            st.success(f"Completed {duration} minute focus session!")
            st.rerun()

    # Productivity tips
    st.subheader("💡 AI-Powered Productivity Tips")
    st.markdown("""
    Based on your patterns:
    1. Your peak productivity time appears to be in the morning
    2. You focus best in 25-minute intervals
    3. Taking short breaks improves your performance
    """)

    # Quiz section for mental health
    st.subheader("🧠 Mental Health Quiz")

    questions = [
        {
            "question": "Which of the following is NOT a recommended stress management technique?",
            "options": ["Deep breathing", "Progressive muscle relaxation", "Avoiding all social contact", "Mindfulness meditation"],
            "correct": 2,
            "explanation": "While temporary solitude can be helpful, completely avoiding social contact is not recommended for stress management. Social support is important for mental health."
        },
        {
            "question": "How many hours of sleep are generally recommended for adults?",
            "options": ["4-5 hours", "6-7 hours", "7-9 hours", "10-12 hours"],
            "correct": 2,
            "explanation": "Most adults need 7-9 hours of sleep per night for optimal health."
        },
        {
            "question": "Which of these is a sign of burnout?",
            "options": ["Occasional tiredness", "Feeling energized by challenges", "Persistent emotional exhaustion", "Taking on more responsibilities"],
            "correct": 2,
            "explanation": "Persistent emotional exhaustion is a key sign of burnout, along with cynicism and reduced professional efficacy."
        },
        {
            "question": "What is the 'fight or flight' response related to?",
            "options": ["Martial arts training", "The body's stress response", "A psychological therapy technique", "A conflict resolution strategy"],
            "correct": 1,
            "explanation": "The 'fight or flight' response is the body's physiological reaction to perceived threats, triggering hormones like adrenaline and cortisol."
        },
        {
            "question": "Which activity is most effective for reducing anxiety in most people?",
            "options": ["Consuming caffeine", "Regular aerobic exercise", "Checking social media", "Working longer hours"],
            "correct": 1,
            "explanation": "Regular aerobic exercise has been consistently shown to reduce anxiety and improve mood through the release of endorphins and other benefits."
        },
        {
            "question": "What is 'cognitive restructuring' in cognitive behavioral therapy?",
            "options": ["Brain surgery", "Changing your physical environment", "Identifying and challenging negative thought patterns", "Memorization exercises"],
            "correct": 2,
            "explanation": "Cognitive restructuring involves identifying negative or distorted thinking patterns and replacing them with more balanced, realistic thoughts."
        },
        {
            "question": "Which of the following is a mindfulness practice?",
            "options": ["Planning tomorrow's activities", "Worrying about past events", "Focusing on your breathing in the present moment", "Multitasking efficiently"],
            "correct": 2,
            "explanation": "Mindfulness involves paying attention to the present moment without judgment. Focusing on breathing is a common mindfulness technique."
        }
    ]

    for i, question in enumerate(questions):
        st.markdown(f"**{i+1}. {question['question']}**")
        for j, option in enumerate(question['options']):
            st.radio(option, key=f"q{i}_option{j}", options=[True, False])
        st.markdown(f"<details><summary>Answer and Explanation</summary>{question['explanation']}</details>", unsafe_allow_html=True)