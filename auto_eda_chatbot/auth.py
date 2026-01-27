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
    """Display creative login page with video background"""
    init_session()
    
    # Creative login page with modern design and video background
    st.markdown("""
    <style>
        /* Hide default streamlit elements */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
        }
        
        /* Video background styling */
        .login-container {
            position: relative;
            width: 100%;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
            overflow: hidden;
        }
        
        .video-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.3;
        }
        
        .video-background video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: blur(2px) brightness(0.4);
        }
        
        /* Animated background gradient overlay */
        .gradient-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
            animation: gradientShift 15s ease infinite;
            background-size: 400% 400%;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Floating particles animation */
        .particle {
            position: fixed;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle::before {
            content: '';
            display: block;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(0, 217, 255, 0.5) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(1px);
        }
        
        /* Login card styling */
        .login-card {
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            background: rgba(17, 24, 41, 0.85);
            border: 2px solid rgba(0, 217, 255, 0.3);
            border-radius: 20px;
            padding: 60px 50px;
            width: 100%;
            max-width: 450px;
            box-shadow: 
                0 8px 32px rgba(0, 217, 255, 0.2),
                inset 0 0 60px rgba(0, 217, 255, 0.05),
                0 0 60px rgba(0, 217, 255, 0.1);
            position: relative;
            z-index: 10;
            animation: slideInUp 0.8s ease-out;
            border-top: 1px solid rgba(0, 245, 221, 0.2);
            border-left: 1px solid rgba(0, 245, 221, 0.1);
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .login-title {
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #00d9ff 0%, #00f5dd 50%, #d946ef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        
        .login-subtitle {
            font-size: 0.95em;
            color: #a0aec0;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 500;
        }
        
        .input-group {
            margin-bottom: 25px;
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        .input-group:nth-child(1) { animation-delay: 0.1s; }
        .input-group:nth-child(2) { animation-delay: 0.2s; }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .input-label {
            display: block;
            margin-bottom: 10px;
            font-size: 0.9em;
            font-weight: 600;
            color: #00d9ff;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        }
        
        .login-input {
            width: 100%;
            padding: 16px 20px;
            background: rgba(10, 14, 39, 0.5);
            border: 2px solid rgba(0, 217, 255, 0.2);
            border-radius: 12px;
            color: #ffffff;
            font-size: 1em;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
        }
        
        .login-input:focus {
            border-color: #00d9ff;
            background: rgba(10, 14, 39, 0.8);
            box-shadow: 
                0 0 25px rgba(0, 217, 255, 0.4),
                inset 0 0 20px rgba(0, 217, 255, 0.05);
            outline: none;
        }
        
        .login-input::placeholder {
            color: #4a5568;
        }
        
        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        
        .login-btn {
            padding: 14px 28px;
            background: linear-gradient(135deg, #00d9ff 0%, #00f5dd 100%);
            border: none;
            border-radius: 10px;
            color: #0a0e27;
            font-weight: 700;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .login-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 50px rgba(0, 217, 255, 0.6);
            letter-spacing: 2px;
        }
        
        .login-btn:active {
            transform: translateY(-1px);
        }
        
        .demo-btn {
            padding: 14px 28px;
            background: rgba(217, 70, 239, 0.2);
            border: 2px solid rgba(217, 70, 239, 0.5);
            border-radius: 10px;
            color: #d946ef;
            font-weight: 700;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .demo-btn:hover {
            background: rgba(217, 70, 239, 0.4);
            border-color: #d946ef;
            transform: translateY(-3px);
            box-shadow: 0 0 30px rgba(217, 70, 239, 0.4);
        }
        
        .footer-text {
            text-align: center;
            margin-top: 35px;
            padding-top: 25px;
            border-top: 1px solid rgba(0, 217, 255, 0.1);
            font-size: 0.85em;
            color: #718096;
            line-height: 1.6;
        }
        
        .footer-text strong {
            color: #00d9ff;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        }
        
        .demo-info {
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.9em;
            color: #a0aec0;
            line-height: 1.6;
        }
        
        .demo-info strong {
            color: #00d9ff;
            display: block;
            margin-bottom: 8px;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        }
        
        .demo-cred {
            background: rgba(10, 14, 39, 0.8);
            padding: 8px 12px;
            border-radius: 6px;
            margin: 5px 0;
            font-family: 'Courier New', monospace;
            border-left: 3px solid #00d9ff;
        }
    </style>
    
    <div class="login-container">
        <div class="gradient-overlay"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create login form
    col1, col2, col3 = st.columns([1, 2.2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-card">
            <div class="login-header">
                <div class="login-title">🔐 AUTO EDA</div>
                <div class="login-subtitle">Studio Pro Authentication</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Username input
        username = st.text_input(
            "👤 Username",
            placeholder="Enter your username",
            key="login_username_creative"
        )
        
        # Password input
        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password",
            key="login_password_creative"
        )
        
        # Login button
        col_login, col_demo = st.columns(2)
        
        with col_login:
            if st.button("🚀 LOGIN", use_container_width=True, key="btn_login_creative"):
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                elif login_user(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try demo account")
        
        with col_demo:
            if st.button("📋 DEMO", use_container_width=True, key="btn_demo_creative"):
                st.info("""
                **🎯 Demo Accounts Available:**
                
                👑 **Admin Account**
                - Username: `admin`
                - Password: `admin123`
                
                👤 **User Account**
                - Username: `user`
                - Password: `user123`
                """)
        
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(0, 217, 255, 0.1); color: #718096; font-size: 0.85em;'>
            <p>🛡️ <strong style='color: #00d9ff;'>Secure Login</strong> | 📊 <strong style='color: #00f5dd;'>Advanced Analytics</strong> | 📄 <strong style='color: #d946ef;'>PDF Export</strong></p>
            <p style='margin-top: 10px; font-size: 0.8em;'>Auto EDA Studio Pro v2.0 | Enterprise Analytics Platform</p>
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
