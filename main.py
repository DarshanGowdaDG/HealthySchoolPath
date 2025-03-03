import streamlit as st
from auth import check_authentication, show_login, show_registration
from components.physical import show_physical_section
from components.learning import show_learning_section
from components.nutrition import show_nutrition_section
from components.mental import show_mental_section
from components.particles import load_particles_js
from database import init_db
from utils import calculate_streak, send_notification
import base64

# Initialize the database
init_db()

def set_page_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-attachment: fixed;
            background-size: cover;
        }
        .content-section {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
        }
        .sidebar .stButton button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        .hover-lift {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .hover-lift:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), 
                            url("{image_url}");
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Configure Streamlit page
st.set_page_config(
    page_title="Health Education Platform",
    page_icon="🏥",
    layout="wide"
)

# Add styles
set_page_style()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

def show_homepage():
    # Set homepage background
    set_background_image("https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2070")

    st.markdown(
        """
        <div class="content-section fade-in">
            <h1 style='text-align: center; color: #2c3e50; font-size: 3rem; margin-bottom: 2rem;'>
                🌟 Health Education Platform
            </h1>
            <p style='text-align: center; font-size: 1.5rem; color: #34495e; margin-bottom: 3rem;'>
                Transform Your Health Journey with AI-Powered Guidance
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Authentication buttons with improved styling
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login", key="home_login", help="Click to login to your account"):
            st.session_state.show_login = True
            st.rerun()
    with col2:
        if st.button("Register", key="home_register", help="Click to create a new account"):
            st.session_state.show_register = True
            st.rerun()

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.markdown(
                """
                <div class="content-section hover-lift">
                    <h3>🤖 AI-Powered Insights</h3>
                    <ul>
                        <li>Personalized recommendations</li>
                        <li>Real-time health monitoring</li>
                        <li>Smart progress tracking</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        with st.container():
            st.markdown(
                """
                <div class="content-section hover-lift">
                    <h3>🎮 Gamified Learning</h3>
                    <ul>
                        <li>Earn achievement badges</li>
                        <li>Track your progress streaks</li>
                        <li>Compete on leaderboards</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        with st.container():
            st.markdown(
                """
                <div class="content-section hover-lift">
                    <h3>📊 Comprehensive Dashboard</h3>
                    <ul>
                        <li>Physical health metrics</li>
                        <li>Mental wellness tracking</li>
                        <li>Nutrition monitoring</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

def main():
    if st.session_state.show_login:
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")
        show_login()
        return
    elif st.session_state.show_register:
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")
        show_registration()
        return

    if not st.session_state.authenticated:
        show_homepage()
        return

    # Set different background for authenticated sections
    if st.session_state.authenticated:
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")

    # Main navigation for authenticated users
    with st.sidebar:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.title(f"Welcome, {st.session_state.username}! 👋")

        # Show gamification status
        streak = calculate_streak([])  # Pass actual dates here
        st.markdown(f"🔥 Current Streak: {streak} days")
        
        # Health Stats Summary
        st.subheader("📊 Your Health Stats")
        st.markdown("""
        * 💪 Fitness Level: Advanced
        * 🧠 Mental Wellness: 92%
        * 🍎 Nutrition Score: 85%
        * 📚 Learning Progress: 78%
        """)
        
        # Weekly Goals
        st.subheader("🎯 Weekly Goals")
        st.markdown("""
        * Complete 3 workouts ✅
        * Practice mindfulness 20 mins/day ⏳
        * Track all meals ✅
        * Complete 2 health quizzes ⏳
        """)

        # Navigation
        st.subheader("🧭 Navigation")
        nav_selection = st.radio(
            "",
            ["Dashboard", "Physical Health", "Mental Health", "Nutrition", "Learning"]
        )

        if st.button("Logout", key="logout_button"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Content routing with different backgrounds for each section
    if nav_selection == "Dashboard":
        set_background_image("https://images.unsplash.com/photo-1542736667-069246bdbc6d?q=80&w=2070")
        show_dashboard()
    elif nav_selection == "Physical Health":
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")
        show_physical_section()
    elif nav_selection == "Mental Health":
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")
        show_mental_section()
    elif nav_selection == "Learning":
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")
        show_learning_section()
    elif nav_selection == "Nutrition":
        set_background_image("https://i.pinimg.com/736x/7c/cb/01/7ccb010d8fddc4bcd84587ef3c34d100.jpg")
        show_nutrition_section()

def show_dashboard():
    # Load particles.js animation
    load_particles_js()
    
    with st.container():
        st.markdown('<div class="content-section fade-in">', unsafe_allow_html=True)
        st.title("Your Health Dashboard")

        # Welcome message
        st.markdown(f"""
        ### 🎉 Welcome to your personalized health journey!
        
        Your dashboard provides a comprehensive overview of your health and learning progress.
        Continue your streak by engaging with different sections daily.
        """)
        
        # AI Insights
        with st.expander("🤖 AI Health Insights", expanded=True):
            st.markdown("""
            Based on your recent activity:
            - Your physical activity has increased by 15% - keep up the good work!
            - Consider taking more breaks during study sessions to maintain focus
            - Great progress on maintaining a balanced diet! Try to include more vegetables
            - Your sleep pattern shows improvement, aim for 7-8 hours consistently
            """)

        # Health Metrics Overview
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Physical Activity", "85%", "+5%")
            st.metric("Daily Steps", "8,500", "+1,500")
            st.markdown("**Rank:** Best 🏆")
            st.markdown("""
            **Physical Goals:**
            - Reach 10,000 steps daily
            - Complete 30 min exercise 5x/week
            - Improve flexibility
            """)

        with col2:
            st.metric("Mental Wellness", "92%", "+3%")
            st.metric("Study Focus", "75%", "+5%")
            st.markdown("**Rank:** Better ⭐")
            st.markdown("""
            **Mental Goals:**
            - Practice mindfulness daily
            - Complete 3 focus sessions per day
            - Maintain stress levels below 40%
            """)

        with col3:
            st.metric("Nutrition Score", "78%", "+2%")
            st.metric("Water Intake", "2L/3L")
            st.markdown("**Rank:** Good 👍")
            st.markdown("""
            **Nutrition Goals:**
            - Drink 3L water daily
            - Increase protein intake to 80g
            - Reduce processed food consumption
            """)

        # Achievements
        st.subheader("🏅 Recent Achievements")
        achievements = [
            "7-Day Streak Badge",
            "Nutrition Master",
            "Exercise Champion"
        ]
        for achievement in achievements:
            st.markdown(f"✨ {achievement}")
            
        # Upcoming goals section
        st.subheader("🎯 Upcoming Milestones")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **This Week:**
            - Complete 3 quizzes in Learning section
            - Log 5 complete meals in Nutrition tracker
            - Achieve 3 focus sessions of 25+ minutes
            """)
            
        with col2:
            st.markdown("""
            **This Month:**
            - Earn the "Knowledge Explorer" badge
            - Build a 14-day streak
            - Complete all sections of Physical Assessment
            """)

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()