import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import io

# -----------------------------------------------------------------------------
# 1. CLOUD-COMPATIBLE SETUP
# -----------------------------------------------------------------------------
# On Streamlit Cloud, we use st.secrets, locally we use .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # On Cloud, .env might not exist, which is fine if using Secrets

# -----------------------------------------------------------------------------
# 2. IMPORT CUSTOM MODULES (MUST EXIST IN YOUR REPO)
# -----------------------------------------------------------------------------
try:
    from chat.qa_engine import answer_question
    # We define load_dataset here locally if the import fails to prevent crashes
    from chat.qa_engine import load_dataset
    from eda.visualizer import show_charts
    from auth import init_session, is_authenticated, show_login_page, show_logout_button, get_user_info
    from pdf_generator import generate_pdf_report, get_pdf_bytes
except ImportError as e:
    st.error(f"❌ CRITICAL ERROR: Missing module. {e}")
    st.info("Make sure you have uploaded the 'chat', 'eda', 'auth.py', and 'pdf_generator.py' files to GitHub.")
    st.stop()

# -----------------------------------------------------------------------------
# 3. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="📊 Auto EDA Studio Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Insert your Custom CSS here (Keep it in the file for deployment simplicity)
st.markdown("""
<style>
    /* Dark Theme Fixes */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
        color: white;
    }
    [data-testid="stSidebar"] {
        background: rgba(17, 24, 41, 0.9);
        border-right: 1px solid rgba(0, 217, 255, 0.1);
    }
    h1, h2, h3 {
        color: #00d9ff !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. AUTHENTICATION
# -----------------------------------------------------------------------------
init_session()

if not is_authenticated():
    show_login_page()
    st.stop()

# -----------------------------------------------------------------------------
# 5. MAIN APP LOGIC
# -----------------------------------------------------------------------------
# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Auto EDA Studio Pro")
with col2:
    user_info = get_user_info()
    username = user_info.get('username', 'User')
    st.markdown(f"<div style='text-align:right; padding:10px; background:#1a1f3a; border-radius:10px;'>👤 {username}</div>", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("🎛️ Controls")
    uploaded_file = st.file_uploader("Upload Dataset", type=['csv', 'xlsx'])
    use_sample = st.checkbox("Use Sample Data", value=True)
    
    st.divider()
    show_eda = st.checkbox("Show Charts", value=True)
    export_pdf = st.checkbox("Enable PDF Export", value=True)
    st.divider()
    show_logout_button()

# Data Loading (Fixed for Cloud)
@st.cache_data
def get_data(file_obj, is_uploaded=False):
    try:
        if is_uploaded:
            # Streamlit uploads are BytesIO objects, read directly
            if file_obj.name.endswith('.csv'):
                return pd.read_csv(file_obj)
            else:
                return pd.read_excel(file_obj)
        else:
            # Fallback sample data
            if os.path.exists("data/sample.csv"):
                return pd.read_csv("data/sample.csv")
            return None
    except Exception as e:
        return str(e)

df = None
dataset_name = "Sample"

if uploaded_file:
    result = get_data(uploaded_file, is_uploaded=True)
    if isinstance(result, str): # Error caught
        st.error(f"Error loading file: {result}")
    else:
        df = result
        dataset_name = uploaded_file.name
elif use_sample:
    result = get_data(None, is_uploaded=False)
    if isinstance(result, pd.DataFrame):
        df = result
    else:
        st.warning("⚠️ Sample data not found in 'data/sample.csv'")

# Dashboard
if df is not None:
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 EDA", "📊 Data", "💬 Chat", "📄 Report"])

    with tab1:
        if show_eda:
            # SAFETY CHECK: Don't plot if > 50k rows to prevent crash
            if len(df) > 50000:
                st.warning("⚠️ Large dataset: Plotting sampled data (first 10k rows)")
                show_charts(df.head(10000))
            else:
                show_charts(df)
    
    with tab2:
        st.dataframe(df.head(100))
        st.write(df.describe())

    with tab3:
        st.info("💡 Tip: Ask questions like 'What is the average of column X?'")
        # Chat Interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("Ask about your data"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    # Pass the DF to your engine
                    try:
                        response = answer_question(df, prompt)
                        st.write(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"AI Error: {e}")

    with tab4:
        if export_pdf:
            if st.button("Generate PDF"):
                pdf = generate_pdf_report(df, username=username, dataset_name=dataset_name)
                st.download_button("Download PDF", get_pdf_bytes(pdf), "report.pdf", "application/pdf")

else:
    st.info("👈 Upload a file to start")
