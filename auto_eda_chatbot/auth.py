import streamlit as st

# ---------------- SESSION INIT ----------------

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = {
            "username": "",
            "email": ""
        }

# ---------------- LOGIN LOGIC ----------------

def login_user(username: str, password: str) -> bool:
    # Demo credentials (cloud safe)
    if username == "admin" and password == "1234":
        st.session_state.authenticated = True
        st.session_state.user = {
            "username": "admin",
            "email": "admin@eda.ai"
        }
        return True
    return False

def logout_user():
    st.session_state.authenticated = False
    st.session_state.user = {
        "username": "",
        "email": ""
    }

def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)

def get_current_user() -> str:
    return st.session_state.user.get("username", "")

def get_user_info():
    return st.session_state.user

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
