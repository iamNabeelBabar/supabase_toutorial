import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# ---------------- AUTH FUNCTIONS ---------------- #

def sign_up(email: str, password: str):
    """Sign up a new user with email and password."""
    try:
        return supabase.auth.sign_up({
            "email": email,
            "password": password
        })
    except Exception as e:
        st.error(f"Error signing up: {e}")
        return None


def sign_in(email: str, password: str):
    """Sign in an existing user."""
    try:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    except Exception as e:
        st.error(f"Error signing in: {e}")
        return None


def sign_out():
    """Sign out the current user."""
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Error signing out: {e}")

# ---------------- UI ---------------- #

def main_app(user_email: str):
    st.title("Welcome to the Main App")
    st.write(f"Hello, **{user_email}** 👋")

    if st.button("Sign Out"):
        sign_out()


def auth_screen():
    st.title("Streamlit & Supabase Auth App")

    option = st.selectbox("Choose an option", ["Sign In", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Sign In":
        if st.button("Sign In"):
            user = sign_in(email, password)
            if user:
                st.session_state.user_email = email
                st.success("Signed in successfully!")
                st.rerun()

    else:
        if st.button("Sign Up"):
            user = sign_up(email, password)
            if user:
                st.success("Signed up successfully! Please sign in.")

# ---------------- SESSION HANDLING ---------------- #

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    auth_screen()
