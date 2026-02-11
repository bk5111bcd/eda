import streamlit as st

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = {
            "username": "",
            "email": ""
        }

def login(username, password):
    # demo users (can be replaced with DB later)
    if username == "admin" and password == "1234":
        st.session_state.authenticated = True
        st.session_state.user = {
            "username": "admin",
            "email": "admin@eda.ai"
        }
        return True
    return False

def is_authenticated():
    return st.session_state.get("authenticated", False)

def get_current_user():
    return st.session_state.user.get("username", "")

def get_user_info():
    return st.session_state.user

def show_login_page():
    st.title("Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.success("Logged in")
            st.rerun()
        else:
            st.error("Invalid credentials")

def show_logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
