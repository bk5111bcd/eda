"""
Simple Streamlit Session Authentication
Cloud-safe, no database, no hashing
"""

import streamlit as st


# ---------------- SESSION INIT ----------------

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""


# ---------------- LOGIN LOGIC ----------------

def login_user(username: str, password: str) -> bool:
    # Hardcoded demo credentials
    if username == "admin" and password == "1234":
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False


def logout_user():
    st.session_state.authenticated = False
    st.session_state.username = ""


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def get_current_user() -> str:
    return st.session_state.get("username", "")


# ---------------- UI ----------------

def show_login_page():
    init_session()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("# 🔐 Login")
        st.markdown("---")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")


def show_logout_button():
    if st.sidebar.button("🚪 Logout"):
        logout_user()
        st.rerun()
