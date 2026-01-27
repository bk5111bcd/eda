"""
Simple Authentication module for Auto EDA Chatbot
Session-based login - no database needed
"""

import streamlit as st
import hashlib

# Default credentials
DEFAULT_USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user": hashlib.sha256("user123".encode()).hexdigest(),
}

def hash_password(password: str) -> str:
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password"""
    return hash_password(password) == hashed

def login_user(username: str, password: str) -> bool:
    """Authenticate user"""
    if username in DEFAULT_USERS:
        if verify_password(password, DEFAULT_USERS[username]):
            st.session_state.authenticated = True
            st.session_state.username = username
            return True
    return False

def logout_user():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None

def is_authenticated() -> bool:
    """Check if user is logged in"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def get_current_user() -> str:
    """Get current username"""
    return st.session_state.get("username", None)

def init_session():
    """Initialize session variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None

def show_login_page():
    """Display simple working login page"""
    init_session()
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🔐 Login")
        st.markdown("---")
        
        # Username input
        username = st.text_input(
            "Username",
            placeholder="Enter username",
            key="login_username"
        )
        
        # Password input
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password",
            key="login_password"
        )
        
        # Login button
        if st.button("🔓 Login", use_container_width=True):
            if not username or not password:
                st.error("❌ Please enter both username and password")
            elif login_user(username, password):
                st.success("✅ Login successful!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        # Demo credentials info
        st.markdown("---")
        st.info("""
        **Demo Credentials:**
        - Username: `admin` | Password: `admin123`
        - Username: `user` | Password: `user123`
        """)

def show_logout_button():
    """Show logout button in sidebar"""
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout_user()
        st.rerun()
