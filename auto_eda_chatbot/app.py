"""Enhanced Auto EDA Chatbot with Authentication & PDF Export
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

# Import custom modules
from chat.qa_engine import answer_question, load_dataset
from eda.visualizer import show_charts
from auth import init_session, is_authenticated, show_login_page, show_logout_button, get_current_user
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
        --glow-cyan: 0 0 20px rgba(0, 217, 255, 0.4);
        --glow-magenta: 0 0 20px rgba(217, 70, 239, 0.4);
        --glow-teal: 0 0 20px rgba(0, 245, 221, 0.4);
    }

    /* Main body background */
    html, body {
        background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
        color: var(--text-primary);
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
        color: var(--text-primary);
    }

    /* Sidebar - Glassmorphism effect */
    [data-testid="stSidebar"] {
        background: rgba(17, 24, 41, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 217, 255, 0.1);
        box-shadow: inset 0 0 50px rgba(0, 217, 255, 0.05);
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        backdrop-filter: blur(10px);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--accent-cyan);
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        font-weight: 700;
    }

    /* Main content area */
    .main {
        background: transparent;
        padding: 2rem;
    }

    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-magenta) 50%, var(--accent-teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        letter-spacing: 0.5px;
        animation: glow-text 3s ease-in-out infinite;
    }

    @keyframes glow-text {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(0, 217, 255, 0.2)); }
        50% { filter: drop-shadow(0 0 20px rgba(217, 70, 239, 0.3)); }
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 217, 255, 0.15);
    }

    h2 {
        font-size: 1.8rem;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 15px rgba(0, 217, 255, 0.1);
    }

    h3 {
        font-size: 1.3rem;
        text-shadow: 0 0 10px rgba(217, 70, 239, 0.1);
    }

    /* Card/Container styling - Glassmorphism */
    [data-testid="stVerticalBlock"] > [data-testid="column"] {
        background: rgba(26, 31, 58, 0.3);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.15);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4),
                    inset 0 0 40px rgba(0, 217, 255, 0.05),
                    0 0 20px rgba(0, 217, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    [data-testid="stVerticalBlock"] > [data-testid="column"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.05) 0%, rgba(217, 70, 239, 0.02) 100%);
        border-radius: 20px;
        pointer-events: none;
    }

    [data-testid="stVerticalBlock"] > [data-testid="column"]:hover {
        background: rgba(26, 31, 58, 0.5);
        border-color: rgba(0, 217, 255, 0.4);
        box-shadow: 0 12px 48px rgba(0, 217, 255, 0.2),
                    inset 0 0 40px rgba(0, 217, 255, 0.08),
                    0 0 30px rgba(217, 70, 239, 0.1);
        transform: translateY(-4px);
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: rgba(26, 31, 58, 0.4) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1.5px solid rgba(217, 70, 239, 0.25);
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 0 30px rgba(217, 70, 239, 0.15),
                    inset 0 0 30px rgba(217, 70, 239, 0.05),
                    0 0 60px rgba(0, 217, 255, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(217, 70, 239, 0.1) 0%, transparent 70%);
        animation: orbit 20s linear infinite;
    }

    @keyframes orbit {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    [data-testid="metric-container"]:hover {
        border-color: rgba(217, 70, 239, 0.5);
        box-shadow: 0 0 40px rgba(217, 70, 239, 0.3),
                    inset 0 0 40px rgba(217, 70, 239, 0.1),
                    0 0 80px rgba(0, 217, 255, 0.15);
        transform: translateY(-4px) scale(1.02);
    }

    /* Buttons - Neon style */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #d946ef 100%);
        color: white;
        border: 1.5px solid rgba(0, 217, 255, 0.4);
        border-radius: 14px;
        padding: 0.8rem 2.2rem;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.6px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4),
                    0 0 40px rgba(217, 70, 239, 0.2),
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
        text-transform: uppercase;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: pulse-glow 3s ease-in-out infinite;
    }

    @keyframes pulse-glow {
        0%, 100% { transform: scale(1); opacity: 0; }
        50% { opacity: 1; }
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #d946ef 50%, #ff006e 100%);
        border-color: var(--accent-magenta);
        box-shadow: 0 0 30px rgba(217, 70, 239, 0.6),
                    0 0 60px rgba(255, 0, 110, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.15);
        transform: translateY(-3px) scale(1.05);
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }

    /* Input fields */
    input, textarea, select {
        background: rgba(17, 24, 41, 0.5) !important;
        border: 1.5px solid rgba(0, 217, 255, 0.2) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.85rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3) !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 25px rgba(0, 217, 255, 0.4),
                    inset 0 0 20px rgba(0, 217, 255, 0.08),
                    inset 0 0 20px rgba(0, 0, 0, 0.3) !important;
        outline: none !important;
        background: rgba(17, 24, 41, 0.8) !important;
        transform: translateY(-2px);
    }

    /* Tabs styling */
    [role="tablist"] {
        background: rgba(26, 31, 58, 0.3);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 217, 255, 0.15);
        border-radius: 14px;
        padding: 0.7rem;
        border-bottom: none;
        gap: 0.7rem;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.1), inset 0 0 30px rgba(0, 217, 255, 0.03);
    }

    [role="tab"] {
        background: rgba(17, 24, 41, 0.5);
        color: var(--text-secondary);
        border: 1px solid rgba(0, 217, 255, 0.12);
        border-radius: 10px;
        padding: 0.8rem 1.6rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
        cursor: pointer;
    }

    [role="tab"]:hover {
        background: rgba(26, 31, 58, 0.6);
        border-color: rgba(0, 217, 255, 0.3);
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.15);
    }

    [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: var(--text-primary) !important;
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 25px rgba(102, 126, 234, 0.5),
                    inset 0 0 15px rgba(0, 217, 255, 0.1) !important;
    }

    /* File uploader */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(0, 217, 255, 0.4);
        border-radius: 12px;
        background: rgba(26, 31, 58, 0.3);
        padding: 2rem;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--accent-cyan);
        background: rgba(0, 217, 255, 0.05);
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
        background: rgba(26, 31, 58, 0.5);
        padding: 1rem;
    }

    /* Success alert */
    .stAlert[data-testid="stSuccessBox"] {
        border-color: var(--accent-teal);
        box-shadow: 0 0 15px rgba(0, 245, 221, 0.2);
    }

    /* Error alert */
    .stAlert[data-testid="stErrorBox"] {
        border-color: #ef4444;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
    }

    /* Warning alert */
    .stAlert[data-testid="stWarningBox"] {
        border-color: #f59e0b;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
    }

    /* Info alert */
    .stAlert[data-testid="stInfoBox"] {
        border-color: var(--accent-blue);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
    }

    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.3), transparent);
        margin: 2rem 0;
    }

    /* Text styling */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: 0.3px;
    }

    p, span, label, div {
        color: var(--text-primary);
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(26, 31, 58, 0.3);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.4);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #d946ef);
        box-shadow: 0 0 15px rgba(217, 70, 239, 0.4);
    }

    /* Expandable sections */
    [data-testid="stExpander"] {
        background: rgba(26, 31, 58, 0.4);
        border: 1px solid rgba(0, 217, 255, 0.1);
        border-radius: 12px;
        transition: all 0.3s ease;
    }

    [data-testid="stExpander"]:hover {
        border-color: rgba(0, 217, 255, 0.3);
        background: rgba(26, 31, 58, 0.6);
    }

    /* Data tables */
    [data-testid="stTable"] {
        background: rgba(26, 31, 58, 0.3) !important;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0, 217, 255, 0.1);
    }

    [data-testid="stTable"] table {
        color: var(--text-primary);
    }

    [data-testid="stTable"] thead {
        background: rgba(17, 24, 41, 0.6);
        border-bottom: 2px solid rgba(0, 217, 255, 0.2);
    }

    [data-testid="stTable"] th {
        color: var(--accent-cyan);
        font-weight: 600;
        padding: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85rem;
    }

    [data-testid="stTable"] td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(0, 217, 255, 0.05);
    }

    [data-testid="stTable"] tbody tr:hover {
        background: rgba(0, 217, 255, 0.05);
    }

    /* Charts container */
    [data-testid="stPlotlyContainer"],
    [data-testid="element-container"] {
        background: rgba(26, 31, 58, 0.3);
        border-radius: 12px;
        border: 1px solid rgba(0, 217, 255, 0.1);
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }

    /* Select box styling */
    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"] {
        background: rgba(17, 24, 41, 0.6);
        border-radius: 10px;
    }

    /* Slider styling */
    [data-testid="stSlider"] {
        padding: 1rem 0;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-magenta));
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.4);
    }

    /* Checkbox styling */
    input[type="checkbox"] {
        width: 20px;
        height: 20px;
        cursor: pointer;
        accent-color: var(--accent-cyan);
    }

    /* Radio button styling */
    input[type="radio"] {
        accent-color: var(--accent-cyan);
        cursor: pointer;
    }

    /* User info badge */
    [style*="background: #f3f4f6"] {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        border-radius: 10px !important;
        color: var(--accent-cyan) !important;
    }

    /* Spinner animation */
    [data-testid="stSpinner"] {
        color: var(--accent-cyan);
    }

    /* Loading animation */
    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.4);
        }
        50% {
            box-shadow: 0 0 40px rgba(0, 217, 255, 0.6), 0 0 80px rgba(0, 217, 255, 0.3);
        }
    }

    /* Glow effect for interactive elements */
    @keyframes neonGlow {
        0%, 100% {
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.5), 0 0 20px rgba(217, 70, 239, 0.3);
        }
        50% {
            text-shadow: 0 0 20px rgba(0, 217, 255, 0.8), 0 0 40px rgba(217, 70, 239, 0.5);
        }
    }

    /* Apply glow to headers */
    h1, h2, h3 {
        animation: neonGlow 3s ease-in-out infinite;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem;
        }

        h2 {
            font-size: 1.4rem;
        }

        .stButton > button {
            padding: 0.6rem 1.5rem;
            font-size: 0.85rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION - STEP 1
# ═════════════════════════════════════════════════════════════════════════════

init_session()

# ════════════════════════════════════════════════════════════════════

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
    <div style='text-align: right; padding: 10px; background: #f3f4f6; border-radius: 8px;'>
        <small>👤 {user_info.get('name', 'User')}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("**Professional Exploratory Data Analysis Platform**")
st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# MAIN INTERFACE - MODERN LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

# Left sidebar for controls
with st.sidebar:
    st.markdown("---")
    st.markdown("## 🎛️ Controls Panel")

    # Dataset upload section
    st.markdown("### 📂 Dataset Management")

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=['csv', 'xlsx', 'xls'],
        help="CSV or Excel files supported"
    )

    use_default = st.checkbox("📋 Use Sample Data", value=True)

    st.markdown("---")

    # Analysis settings
    st.markdown("### ⚙️ Analysis Settings")

    show_eda = st.checkbox("🔍 Auto EDA Dashboard", value=True)
    show_raw_data = st.checkbox("📊 Show Raw Data", value=False)
    show_statistics = st.checkbox("📈 Show Statistics", value=True)

    st.markdown("---")

    # Export settings
    st.markdown("### 📥 Export Options")

    export_pdf = st.checkbox("📄 Generate PDF Report", value=True)

    st.markdown("---")

    # User section
    st.markdown("### 👤 Account")
    show_logout_button()

# ═════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═════════════════════════════════════════════════════════════════════════════

# Load dataset
df = None
dataset_name = "Sample Dataset"

if uploaded_file is not None:
    try:
        # Save uploaded file temporarily to apply load_dataset normalization
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            df = load_dataset(tmp_path)
            dataset_name = uploaded_file.name.replace('.csv', '').replace('.xlsx', '')
            st.success(f"✅ Dataset loaded successfully: {uploaded_file.name}")
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        df = None

elif use_default:
    try:
        # Try multiple paths for the sample data
        sample_paths = [
            "data/sample.csv",
            "auto_eda_chatbot/data/sample.csv",
            "auto_eda_chatbot/data/dataset.csv",
            "data/dataset.csv"
        ]

        df = None
        for path in sample_paths:
            try:
                df = load_dataset(path)
                dataset_name = "Sample Dataset"
                st.success(f"✅ Loaded sample data from {path}")
                break
            except:
                continue

        if df is None:
            st.warning("⚠️ Could not load sample data from any path")
    except Exception as e:
        st.error(f"❌ Error loading sample data: {str(e)}")
        df = None

if df is not None:
    # ═════════════════════════════════════════════════════════════════════════
    # DATASET OVERVIEW SECTION
    # ═════════════════════════════════════════════════════════════════════════

    st.markdown("## 📋 Dataset Overview")

    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("📊 Total Rows", f"{len(df):,}")
    with col2:
        st.metric("🏷️ Total Columns", len(df.columns))
    with col3:
        numeric_cols = len(df.select_dtypes(include=['float64', 'int64']).columns)
        st.metric("🔢 Numeric", numeric_cols)
    with col4:
        cat_cols = len(df.select_dtypes(include=['object']).columns)
        st.metric("📝 Categorical", cat_cols)
    with col5:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        st.metric("❌ Missing %", f"{missing_pct:.1f}%")

    st.divider()

    # ═════════════════════════════════════════════════════════════════════════
    # TABBED INTERFACE - MODERN DESIGN
    # ═════════════════════════════════════════════════════════════════════════

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 EDA Dashboard",
        "📊 Data Inspector",
        "💬 Chat Analysis",
        "📄 PDF Report",
        "⚙️ Settings"
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1: EDA DASHBOARD
    # ─────────────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("### 🔍 Exploratory Data Analysis Dashboard")
        st.markdown("""
        Comprehensive visualizations of your dataset including distributions,
        relationships, correlations, and data quality metrics.
        """)

        if show_eda:
            st.markdown("---")
            show_charts(df)
        else:
            st.info("💡 Enable 'Auto EDA Dashboard' in the settings panel to view visualizations")

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2: DATA INSPECTOR
    # ─────────────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("### 📊 Data Inspector")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📋 Raw Data Preview")
            n_rows = st.slider("Rows to display", 5, 100, 10)
            st.dataframe(df.head(n_rows), width="stretch", height=400)

        with col2:
            st.markdown("#### 📈 Data Summary")

            info_text = f"""
            **Dataset Information**

            • **Name:** {dataset_name}
            • **Rows:** {len(df):,}
            • **Columns:** {len(df.columns)}
            • **Memory:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
            • **Duplicates:** {df.duplicated().sum()} rows

            **Column Types**

            • Numeric: {len(df.select_dtypes(include=['float64', 'int64']).columns)}
            • Categorical: {len(df.select_dtypes(include=['object']).columns)}
            • DateTime: {len(df.select_dtypes(include=['datetime64']).columns)}

            **Data Quality**

            • Missing Values: {df.isnull().sum().sum()}
            • Complete Rows: {(~df.isnull().any(axis=1)).sum():,}
            • Completeness: {((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100):.1f}%
            """

            st.markdown(info_text)

        st.divider()

        # Column details
        st.markdown("#### 🔍 Column Details")

        selected_col = st.selectbox(
            "Select a column to inspect",
            df.columns,
            key="col_select"
        )

        if selected_col:
            col_data = df[selected_col]
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**{selected_col}**")
                st.write(f"Type: `{col_data.dtype}`")
                st.write(f"Non-Null: {col_data.count()} / {len(df)}")
                st.write(f"Unique: {col_data.nunique()}")
                st.write(f"Missing: {col_data.isnull().sum()}")

            with col2:
                if col_data.dtype in ['float64', 'int64']:
                    st.write(f"Min: {col_data.min()}")
                    st.write(f"Max: {col_data.max()}")
                    st.write(f"Mean: {col_data.mean():.2f}")
                    st.write(f"Std: {col_data.std():.2f}")
                else:
                    st.write(f"Top 5 Values:")
                    st.bar_chart(col_data.value_counts().head(5))

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3: CHAT ANALYSIS
    # ─────────────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown("### 💬 Chat-Based Data Analysis")
        st.markdown("Ask questions about your data using natural language")

        st.divider()

        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about your data (e.g., 'What is the average salary?')"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Analyzing..."):
                    try:
                        response = answer_question(df, prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 4: PDF REPORT
    # ─────────────────────────────────────────────────────────────────────────
    with tab4:
        st.markdown("### 📄 Generate PDF Report")
        st.markdown("Create a comprehensive PDF report of your analysis")

        st.divider()

        if export_pdf:
            col1, col2 = st.columns([1, 3])

            with col1:
                if st.button("📥 Generate PDF", width="stretch"):
                    with st.spinner("🔄 Generating PDF report..."):
                        try:
                            # Generate PDF
                            username = get_user_info().get('name', 'User')
                            pdf = generate_pdf_report(df, username=username, dataset_name=dataset_name)
                            pdf_bytes = get_pdf_bytes(pdf)

                            # Create download button
                            st.download_button(
                                label="💾 Download PDF",
                                data=pdf_bytes,
                                file_name=f"EDA_Report_{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                key="pdf_download"
                            )

                            st.success("✅ PDF generated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error generating PDF: {str(e)}")

            with col2:
                st.info("""
                **What's included in the PDF:**
                - 📋 Title page with dataset summary
                - 📊 Data quality metrics
                - 📈 Statistical analysis
                - 🔍 Key insights and findings
                - 🏷️ Column information
                - ⏰ Generation timestamp
                """)
        else:
            st.warning("⚠️ Enable 'Generate PDF Report' in settings to create reports")

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 5: SETTINGS
    # ─────────────────────────────────────────────────────────────────────────
    with tab5:
        st.markdown("### ⚙️ Application Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Display Settings")
            st.write(f"**Theme:** Light Mode 🌞")
            st.write(f"**Layout:** Wide 📐")
            st.write(f"**Language:** English 🇺🇸")

        with col2:
            st.markdown("#### About")
            st.write("""
            **Auto EDA Studio Pro v2.0**

            Professional exploratory data analysis platform with:
            - 🔐 User authentication
            - 📊 Interactive visualizations
            - 💬 AI-powered chat analysis
            - 📄 PDF export

            Built with ❤️ using Streamlit
            """)

        st.divider()

        st.markdown("#### User Information")
        user_info = get_user_info()
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Name:** {user_info.get('name', 'N/A')}")
            st.write(f"**Email:** {user_info.get('email', 'N/A')}")

        with col2:
            st.write(f"**Login Time:** {st.session_state.get('login_time', 'N/A')}")
            st.write(f"**Session:** Active ✅")

else:
    st.warning("⚠️ Please upload a dataset or enable 'Use Sample Data' to begin analysis")

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; color: #999; font-size: 12px; margin-top: 20px;'>
    🛡️ Secure Platform | 📊 Advanced Analytics | 📄 PDF Export | 🤖 AI-Powered

    © 2026 Auto EDA Studio Pro | All rights reserved
    </div>
    """, unsafe_allow_html=True)
