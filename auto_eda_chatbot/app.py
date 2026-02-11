"""
Enhanced Auto EDA Chatbot with Authentication & PDF Export
Complete redesign with professional UI/UX - Fixed Auth Integration
"""

from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import io
import tempfile

# 🔧 FIX 1: Corrected Import (added get_user_info, removed get_current_user)
from chat.qa_engine import answer_question, load_dataset
from eda.visualizer import show_charts
from auth import init_session, is_authenticated, show_login_page, show_logout_button, get_user_info
from pdf_generator import generate_pdf_report, get_pdf_bytes

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="📊 Auto EDA Studio Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark glassmorphism design
st.markdown("""
<style>
    :root {
        --bg-primary: #0a0e27;
        --accent-cyan: #00d9ff;
        --accent-magenta: #d946ef;
        --text-primary: #ffffff;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
        color: var(--text-primary);
    }
    /* ... (rest of your extensive CSS remains exactly the same) ... */
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION - STEP 1
# ═════════════════════════════════════════════════════════════════════════════

init_session()

if not is_authenticated():
    show_login_page()
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATED USER INTERFACE
# ═════════════════════════════════════════════════════════════════════════════

# Header with user info
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown("### 📊 Auto EDA Studio Pro")

with col3:
    # 🔧 FIX 2 & 3: Correct variable and 'username' key
    user_info = get_user_info()
    st.markdown(f"""
    <div style='text-align: right; padding: 10px; background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 8px;'>
        <small style='color: #00d9ff;'>👤 {user_info.get('username', 'User')}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("**Professional Exploratory Data Analysis Platform**")
st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR & DATA LOADING (Remains as designed)
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎛️ Controls Panel")
    uploaded_file = st.file_uploader("Upload Dataset", type=['csv', 'xlsx', 'xls'])
    use_default = st.checkbox("📋 Use Sample Data", value=True)
    st.divider()
    show_logout_button()

df = None
dataset_name = "Sample Dataset"

# (Data loading logic logic remains the same...)
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name
    df = load_dataset(tmp_path)
    dataset_name = uploaded_file.name
    os.unlink(tmp_path)
elif use_default:
    df = load_dataset("data/sample.csv") # Assuming path exists

if df is not None:
    st.markdown("## 📋 Dataset Overview")
    # ... (Metrics display logic) ...

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 EDA Dashboard", "📊 Data Inspector", "💬 Chat Analysis", "📄 PDF Report", "⚙️ Settings"])

    # ... (Tabs 1, 2, 3 remain the same) ...

    with tab4:
        st.markdown("### 📄 Generate PDF Report")
        if st.button("📥 Generate PDF"):
            with st.spinner("🔄 Generating PDF report..."):
                # 🔧 FIX 3: Changed 'name' to 'username' to match auth.py
                pdf = generate_pdf_report(df, username=user_info.get('username'), dataset_name=dataset_name)
                pdf_bytes = get_pdf_bytes(pdf)
                st.download_button(
                    label="💾 Download PDF",
                    data=pdf_bytes,
                    file_name=f"Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

    with tab5:
        st.markdown("### ⚙️ Application Settings")
        # 🔧 Final Fix: Displaying correct username in settings
        st.write(f"**Authenticated Username:** {user_info.get('username', 'N/A')}")
        st.write(f"**Email:** {user_info.get('email', 'N/A')}")

else:
    st.warning("⚠️ Please upload a dataset to begin.")

st.divider()
st.markdown("<div style='text-align: center; color: #999;'>© 2026 Auto EDA Studio Pro</div>", unsafe_allow_html=True)
