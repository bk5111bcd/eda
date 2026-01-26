"""
Authentication module for Auto EDA Chatbot
Handles user login and session management
"""

import streamlit as st
import json
import hashlib
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load .env if present so credentials can be provided via environment
load_dotenv()

# Default credentials (in production, use a proper database)
DEFAULT_USERS = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "email": "admin@autoeda.com",
        "name": "Administrator"
    },
    "user": {
        "password": hashlib.sha256("user123".encode()).hexdigest(),
        "email": "user@autoeda.com",
        "name": "Demo User"
    }
}

# Allow overriding or providing users via environment variables for easy setup:
# - If `AUTH_USERS_JSON` is set, it should be a JSON string mapping usernames to
#   dicts with keys: password (plain text or sha256 hex), email, name.
# - Or set `ADMIN_USER` and `ADMIN_PASS` to define a single admin account.
env_users = os.getenv("AUTH_USERS_JSON")
if env_users:
    try:
        parsed = json.loads(env_users)
        for u, info in parsed.items():
            pwd = info.get("password", "")
            # if password appears to be raw (not 64 hex chars), hash it
            if len(pwd) != 64 or not all(c in '0123456789abcdef' for c in pwd.lower()):
                pwd = hashlib.sha256(pwd.encode()).hexdigest()
            DEFAULT_USERS[u] = {
                "password": pwd,
                "email": info.get("email", f"{u}@example.com"),
                "name": info.get("name", u)
            }
    except Exception:
        # ignore invalid env JSON and keep defaults
        pass

admin_user = os.getenv("ADMIN_USER")
admin_pass = os.getenv("ADMIN_PASS")
if admin_user and admin_pass:
    DEFAULT_USERS[admin_user] = {
        "password": hashlib.sha256(admin_pass.encode()).hexdigest(),
        "email": os.getenv("ADMIN_EMAIL", f"{admin_user}@example.com"),
        "name": os.getenv("ADMIN_NAME", admin_user)
    }

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def login_user(username: str, password: str) -> bool:
    """Authenticate a user"""
    if username in DEFAULT_USERS:
        if verify_password(password, DEFAULT_USERS[username]["password"]):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_info = DEFAULT_USERS[username]
            st.session_state.login_time = datetime.now()
            return True
    return False

def logout_user():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_info = None
    st.session_state.login_time = None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def get_current_user() -> str:
    """Get the current authenticated username"""
    return st.session_state.get("username", None)

def get_user_info() -> dict:
    """Get current user information"""
    user_info = st.session_state.get("user_info", {})
    return user_info if user_info is not None else {}

def init_session():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "login_time" not in st.session_state:
        st.session_state.login_time = None

def show_login_page():
    """Display login page"""
    init_session()
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        st.markdown("## 🔐 Auto EDA Chatbot Login")
        st.markdown("---")
        
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🔓 Login", width="stretch"):
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                elif login_user(username, password):
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        with col_register:
            if st.button("📝 Demo Credentials", width="stretch"):
                st.info("""
                **Demo Accounts:**
                - Username: `admin` | Password: `admin123`
                - Username: `user` | Password: `user123`
                """)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>
        🛡️ Secure Login | 📊 Auto EDA Analysis | 📄 PDF Export
        </div>
        """, unsafe_allow_html=True)

def show_logout_button():
    """Display logout button in sidebar"""
    with st.sidebar:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_info = get_user_info()
            st.markdown(f"**👤 {user_info.get('name', 'User')}**")
            st.caption(f"📧 {user_info.get('email', '')}")
        
        st.divider()
        
        if st.button("🚪 Logout", width="stretch"):
            logout_user()
            st.rerun()
