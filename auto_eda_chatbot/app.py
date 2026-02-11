"""
Enhanced Auto EDA Chatbot with Authentication & PDF Export
Complete redesign with professional UI/UX - STABLE VERSION
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
from chat.qa_engine import answer_question, load_dataset
from eda.visualizer import show_charts

# 🔧 FIX 1: Corrected Import (using get_user_info instead of get_current_user)
from auth import init_session, is_authenticated, show_login_page, show_logout_button, get_user_info
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
    /* ═══════════════════════════════════════════════════════════════ */
    /* DARK GLASSMORPHISM THEME - FUTURISTIC FINTECH DESIGN */
    /* ═══════════════════════════════════════════════════════════════ */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
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
        --glow-cyan: 0 0 20px rgba(0, 217, 255, 0.4);
        --glow-magenta: 0 0 20px rgba(217, 70, 239, 0.4);
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
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-magenta) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #d946ef 100%);
        color: white;
        border-radius: 14px;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(217, 70, 239, 0.4);
    }
    /* ... (Your full design system continues here) ... */
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION - STEP 1
# ═════════════════════════════════════════════════════════════════════════════
init_session()

# Check if user is logged in
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
    # 🔧 FIX 2: Correct variable assignment
    user_info = get_user_info()
    # 🔧 FIX 3: Use 'username' key as defined in your auth.py dictionary
    st.markdown(f"""
    <div style='text-align: right; padding: 10px; background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 8px;'>
        <small style='color: #00d9ff;'>👤 {user_info.get('username', 'User')}</small>
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
    use_default = st.checkbox("📋 Use Sample Data", value=True)
    st.divider()
    
    st.markdown("### ⚙️ Analysis Settings")
    show_eda = st.checkbox("🔍 Auto EDA Dashboard", value=True)
    show_raw_data = st.checkbox("📊 Show Raw Data", value=False)
    show_statistics = st.checkbox("📈 Show Statistics", value=True)
    
    st.markdown("### 📥 Export Options")
    export_pdf = st.checkbox("📄 Generate PDF Report", value=True)
    st.divider()
    
    show_logout_button()

# ═════════════════════════════════════════════════════════════════════════════
# DATA ENGINE
# ═════════════════════════════════════════════════════════════════════════════
df = None
dataset_name = "Sample Dataset"

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        df = load_dataset(tmp_path)
        dataset_name = uploaded_file.name.split('.')[0]
        st.success(f"✅ Loaded: {uploaded_file.name}")
        os.unlink(tmp_path)
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
elif use_default:
    try:
        df = load_dataset("data/sample.csv")
        dataset_name = "Sample Dataset"
    except:
        st.warning("⚠️ Sample data not found. Please upload a file.")

if df is not None:
    # METRICS BAR
    st.markdown("## 📋 Dataset Overview")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("📊 Total Rows", f"{len(df):,}")
    m2.metric("🏷️ Columns", len(df.columns))
    m3.metric("🔢 Numeric", len(df.select_dtypes(include=[np.number]).columns))
    m4.metric("📝 Categorical", len(df.select_dtypes(include=['object']).columns))
    m5.metric("❌ Missing %", f"{(df.isnull().sum().sum()/(df.size)*100):.1f}%")
    st.divider()

    # MAIN TABS
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 EDA Dashboard", "📊 Data Inspector", "💬 Chat Analysis", "📄 PDF Report", "⚙️ Settings"])

    with tab1:
        if show_eda:
            show_charts(df)
        else:
            st.info("Enable EDA Dashboard in the sidebar to view charts.")

    with tab2:
        st.markdown("### 📊 Raw Data Preview")
        st.dataframe(df.head(100), use_container_width=True)
        st.markdown("### 📈 Statistical Summary")
        st.write(df.describe())

    with tab3:
        st.markdown("### 💬 Chat with your Data")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask something (e.g., 'What are the correlations?')"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = answer_question(df, prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    with tab4:
        st.markdown("### 📄 Export PDF Report")
        if export_pdf:
            if st.button("📥 Generate Final Report"):
                with st.spinner("Building PDF..."):
                    # 🔧 FIX 3: Correct key usage for PDF generation
                    username_val = user_info.get('username', 'User')
                    pdf = generate_pdf_report(df, username=username_val, dataset_name=dataset_name)
                    pdf_bytes = get_pdf_bytes(pdf)
                    st.download_button(
                        label="💾 Download PDF",
                        data=pdf_bytes,
                        file_name=f"Report_{dataset_name}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
        else:
            st.warning("Enable PDF Generation in the sidebar.")

    with tab5:
        st.markdown("### ⚙️ Account Details")
        col_a, col_b = st.columns(2)
        with col_a:
            # 🔧 FIX 3: Consistent dictionary key usage
            st.write(f"**Username:** {user_info.get('username', 'N/A')}")
            st.write(f"**Email:** {user_info.get('email', 'N/A')}")
        with col_b:
            st.write(f"**Session Start:** {datetime.now().strftime('%H:%M:%S')}")
            st.write("**Status:** Active ✅")

else:
    st.warning("⚠️ Please upload a dataset to begin.")

# FOOTER
st.divider()
st.markdown("<div style='text-align: center; color: #666;'>© 2026 Auto EDA Studio Pro | Powered by Gemini 3 Flash</div>", unsafe_allow_html=True)
