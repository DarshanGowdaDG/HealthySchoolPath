import streamlit as st
from database import add_user, verify_user

def check_authentication():
    """
    Check if user is authenticated in current session
    """
    return st.session_state.get('authenticated', False)

def show_login():
    from components.particles import load_particles_js
    load_particles_js()

    st.markdown(
        """
        <style>
        .auth-form {
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.title("Login")

        # Animated form container
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        login_button = st.button("Login", key="login_button")

        if login_button:
            if verify_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.show_login = False  # Ensure login page closes
                st.success("Successfully logged in!")
                # Add slight delay to show success message before redirecting
                import time
                time.sleep(1)  
                st.rerun()  # Redirect to main dashboard
            else:
                st.error("Invalid username or password")

        st.markdown('</div>', unsafe_allow_html=True)

        # Link back to home
        if st.button("← Back to Home", key="back_to_home_login"):
            st.session_state.show_login = False
            st.rerun()

def show_registration():
    st.markdown(
        """
        <style>
        .auth-form {
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.title("Create New Account")

        # Animated form container
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)

        username = st.text_input("Choose Username", key="reg_username")
        password = st.text_input("Choose Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Register", key="register_button"):
            if password != confirm_password:
                st.error("Passwords do not match!")
                return

            if add_user(username, password):
                st.success("Registration successful! Please login.")
                # Switch to login page without directly modifying widget state
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
            else:
                st.error("Username already exists!")

        st.markdown('</div>', unsafe_allow_html=True)

        # Link back to home
        if st.button("← Back to Home", key="back_to_home_register"):
            st.session_state.show_register = False
            st.rerun()

# Placeholder for components.particles module (needs to be created separately)
# This module should contain the load_particles_js function
# and any necessary CSS/JS for particles.js integration.

#Example components/particles.py
# import streamlit as st

# def load_particles_js():
#     st.markdown("""
#         <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
#         <script>
#             particlesJS('particles-js', {
#                 //particle.js configuration here
#             });
#         </script>
#     """, unsafe_allow_html=True)


if __name__ == "__main__":
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


    if not check_authentication():
        if st.button("Login"):
            st.session_state.show_login = True
            st.session_state.show_register = False
            st.rerun()
        if st.button("Register"):
            st.session_state.show_register = True
            st.session_state.show_login = False
            st.rerun()
    else:
        st.title("Welcome, "+st.session_state.username+"!")
        st.write("You are logged in.")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
            

    if st.session_state.show_login:
        show_login()
    elif st.session_state.show_register:
        show_registration()