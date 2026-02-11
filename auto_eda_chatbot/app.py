"""
Enhanced Auto EDA Chatbot with Authentication & PDF Export
Complete redesign with professional UI/UX
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

# Import custom modules 
# Updated import line to include get_user_info
from chat.qa_engine import answer_question, load_dataset
from eda.visualizer import show_charts
from auth import init_session, is_authenticated, show_login_page, show_logout_button, get_current_user, get_user_info
from pdf_generator import generate_pdf_report, get_pdf_bytes

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION - MODERN DESIGN
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="📊 Auto EDA Studio Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "Auto EDA Studio Pro v2.0"
    }
)

# Custom CSS for modern dark glassmorphism design
st.markdown("""
<style>
    /* Root color variables */
    :root {
        --bg-primary: #0a0e27;
        --bg-secondary: #111829;
        --bg-tertiary: #1a1f3a;
        --accent-cyan: #00d9ff;
        --accent-teal: #00f5dd;
        --accent-blue: #667eea;
        --accent-magenta: #d946ef;
        --accent-purple: #764ba2;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(17, 24, 41, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 217, 255, 0.1);
    }
    
    h1, h2, h3 {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-magenta) 50%, var(--accent-teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Card/Container styling */
    [data-testid="stVerticalBlock"] > [data-testid="column"] {
        background: rgba(26, 31, 58, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.15);
        border-radius: 20px;
        padding: 1.5rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #d946ef 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION LOGIC
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
    user_info = get_user_info()
    st.markdown(f"""
    <div style='text-align: right; padding: 10px; background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 8px;'>
        <small style='color: #00d9ff;'>👤 {user_info.get('name', 'User')}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("**Professional Exploratory Data Analysis Platform**")
st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR CONTROLS
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎛️ Controls Panel")
    
    st.markdown("### 📂 Dataset Management")
    uploaded_file = st.file_uploader("Upload Dataset", type=['csv', 'xlsx', 'xls'])
    use_default = st.checkbox("📋 Use Sample Data", value=not uploaded_file)
    
    st.divider()
    
    st.markdown("### ⚙️ Analysis Settings")
    show_eda = st.checkbox("🔍 Auto EDA Dashboard", value=True)
    show_raw_data = st.checkbox("📊 Show Raw Data", value=False)
    show_statistics = st.checkbox("📈 Show Statistics", value=True)
    
    st.divider()
    
    st.markdown("### 📥 Export Options")
    export_pdf = st.checkbox("📄 Generate PDF Report", value=True)
    
    st.divider()
    show_logout_button()

# ═════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═════════════════════════════════════════════════════════════════════════════

df = None
dataset_name = "Sample Dataset"

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        
        try:
            df = load_dataset(tmp_path)
            dataset_name = uploaded_file.name
            st.success(f"✅ Dataset loaded: {uploaded_file.name}")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")

elif use_default:
    sample_paths = ["data/sample.csv", "data/dataset.csv"]
    for path in sample_paths:
        if os.path.exists(path):
            df = load_dataset(path)
            dataset_name = "Sample Dataset"
            break
    if df is None:
        st.info("💡 Please upload a CSV file to begin.")

# ═════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═════════════════════════════════════════════════════════════════════════════

if df is not None:
    # Key Metrics
    st.markdown("## 📋 Dataset Overview")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("📊 Total Rows", f"{len(df):,}")
    m2.metric("🏷️ Columns", len(df.columns))
    m3.metric("🔢 Numeric", len(df.select_dtypes(include=[np.number]).columns))
    m4.metric("📝 Categorical", len(df.select_dtypes(include=['object']).columns))
    m5.metric("❌ Missing %", f"{(df.isnull().sum().sum() / df.size * 100):.1f}%")
    
    st.divider()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 EDA Dashboard", "📊 Data Inspector", "💬 Chat Analysis", "📄 PDF Report", "⚙️ Settings"
    ])
    
    with tab1:
        if show_eda:
            show_charts(df)
        else:
            st.info("Enable the EDA Dashboard in the sidebar to view charts.")

    with tab2:
        st.markdown("### 📊 Data Inspector")
        st.dataframe(df.head(50))
        
        st.divider()
        col_to_test = st.selectbox("Column Analysis", df.columns)
        if col_to_test:
            st.write(df[col_to_test].describe())

    with tab3:
        st.markdown("### 💬 Chat-Based Data Analysis")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask a question about this data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = answer_question(df, prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    with tab4:
        st.markdown("### 📄 Generate PDF Report")
        if export_pdf:
            if st.button("📥 Build & Download PDF"):
                with st.spinner("Generating..."):
                    pdf = generate_pdf_report(df, username=user_info.get('name'), dataset_name=dataset_name)
                    pdf_bytes = get_pdf_bytes(pdf)
                    st.download_button(
                        label="💾 Save PDF",
                        data=pdf_bytes,
                        file_name=f"Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
        else:
            st.warning("Enable PDF Export in the sidebar.")

    with tab5:
        st.markdown("### ⚙️ Account & Session")
        curr_user = get_user_info()
        st.write(f"**Authenticated as:** {curr_user.get('name')}")
        st.write(f"**Email:** {curr_user.get('email')}")
        st.write(f"**Session Start:** {st.session_state.get('login_time', 'Unknown')}")

else:
    st.info("Waiting for data input. Use the sidebar to upload a file or use sample data.")

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px; padding: 50px;'>
        © 2026 Auto EDA Studio Pro | Secure Data Analysis Environment
    </div>
""", unsafe_allow_html=True)
