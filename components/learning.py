import streamlit as st
import json
from ai_helper import generate_quiz, get_video_content

def show_learning_section():
    st.title("Health Education Learning Center")

    # Topic selection
    topics = {
        "Basics of Nutrition": [
            "Understanding Macronutrients",
            "Importance of Vitamins and Minerals",
            "Healthy Eating Habits"
        ],
        "Physical Fitness": [
            "Cardiovascular Health",
            "Strength Training Fundamentals",
            "Flexibility and Mobility"
        ],
        "Mental Health": [
            "Stress Management",
            "Mindfulness Techniques",
            "Sleep Hygiene"
        ]
    }

    selected_category = st.selectbox("Select Category", list(topics.keys()))
    selected_topic = st.selectbox("Select Topic", topics[selected_category])

    # Content tabs
    tab1, tab2, tab3 = st.tabs(["Learn", "Quiz", "Video Guide"])

    with tab1:
        show_learning_content(selected_topic)

    with tab2:
        show_quiz(selected_topic)

    with tab3:
        show_video_guide(selected_topic)

def show_learning_content(topic):
    st.header(topic)

    content = {
        "Understanding Macronutrients": {
            "introduction": """
            Macronutrients are the nutrients your body needs in large amounts.
            The three main macronutrients are:
            - Proteins
            - Carbohydrates
            - Fats
            """,
            "key_points": [
                "Proteins are essential for building and repairing tissues",
                "Carbohydrates are the body's main source of energy",
                "Healthy fats support brain function and hormone production"
            ],
            "practical_tips": [
                "Include a protein source in every meal",
                "Choose complex carbohydrates over simple sugars",
                "Focus on healthy fats from sources like avocados and nuts"
            ]
        }
    }

    # If content exists for the topic, show it
    if topic in content:
        st.markdown(content[topic]["introduction"])

        st.subheader("Key Points")
        for point in content[topic]["key_points"]:
            st.markdown(f"• {point}")

        st.subheader("Practical Tips")
        for tip in content[topic]["practical_tips"]:
            st.markdown(f"💡 {tip}")
    else:
        # Show generic content structure
        st.info("Learning content for this topic:")
        st.markdown("""
        ### Overview
        This section covers the fundamental concepts and practical applications.

        ### Key Concepts
        • Understanding basic principles
        • Practical applications
        • Safety considerations

        ### Best Practices
        💡 Regular practice
        💡 Proper form
        💡 Consistent progress tracking
        """)

def show_quiz(topic):
    st.header(f"Quiz: {topic}")

    if 'current_quiz' not in st.session_state:
        try:
            quiz_data = json.loads(generate_quiz(topic))
            st.session_state.current_quiz = quiz_data
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
        except Exception as e:
            st.error("Failed to load quiz. Please try again later.")
            return

    if not st.session_state.quiz_submitted:
        for i, q in enumerate(st.session_state.current_quiz["questions"]):
            st.write(f"**Question {i+1}:** {q['question']}")
            st.session_state.quiz_answers[i] = st.radio(
                f"Select answer for question {i+1}:",
                q['options'],
                key=f"q_{i}",
                index=None
            )

        if st.button("Submit Quiz"):
            score = calculate_quiz_score()
            st.session_state.quiz_submitted = True
            st.session_state.quiz_score = score
            st.success(f"Quiz completed! Your score: {score}%")
            show_correct_answers()
    else:
        st.write(f"Your score: {st.session_state.quiz_score}%")
        show_correct_answers()
        if st.button("Try Again"):
            del st.session_state.current_quiz
            del st.session_state.quiz_answers
            del st.session_state.quiz_submitted
            st.experimental_rerun()

def calculate_quiz_score():
    correct = 0
    total = len(st.session_state.current_quiz["questions"])

    for i, q in enumerate(st.session_state.current_quiz["questions"]):
        if st.session_state.quiz_answers[i] == q["correct_answer"]:
            correct += 1

    return (correct / total) * 100

def show_correct_answers():
    st.subheader("Correct Answers")
    for i, q in enumerate(st.session_state.current_quiz["questions"]):
        st.write(f"**Question {i+1}:** {q['question']}")
        st.write(f"Correct Answer: {q['correct_answer']}")

def show_video_guide(topic):
    st.header(f"Video Guide: {topic}")

    video_links = {
        "Understanding Macronutrients": "https://www.youtube.com/embed/ISZLTJH5lYg",
        "Importance of Vitamins and Minerals": "https://www.youtube.com/embed/dBnniua6-oM",
        "Healthy Eating Habits": "https://www.youtube.com/embed/mMHVEFWNLMc",
        "Cardiovascular Health": "https://www.youtube.com/embed/bx99qQoHk5I",
        "Strength Training Fundamentals": "https://www.youtube.com/embed/2tM1LFFxeKg",
        "Flexibility and Mobility": "https://www.youtube.com/embed/sh4HZVbTwR0",
        "Stress Management": "https://www.youtube.com/embed/1vx8iUvfyCY",
        "Mindfulness Techniques": "https://www.youtube.com/embed/w6T02g5hnT4",
        "Sleep Hygiene": "https://www.youtube.com/embed/IzQ2siryQrM"
    }

    if topic in video_links:
        video_url = video_links[topic]
        st.markdown(f"""
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background-color: #F8F9FA; border-radius: 15px; margin: 20px 0;">
            <iframe 
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 15px; border: none;"
                src="{video_url}" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("No video guide available for this topic.")