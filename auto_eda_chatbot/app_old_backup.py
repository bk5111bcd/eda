import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from chat.qa_engine import answer_question, load_dataset, parse_visualization_request
from eda.visualizer import show_charts

# Page config
st.set_page_config(
    page_title="🤖 Auto EDA Chatbot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Auto EDA Chatbot with Analytics")

# Sidebar: Dataset Upload
with st.sidebar:
    st.header("📁 Dataset Management")
    
    # Option 1: Upload new file
    uploaded_file = st.file_uploader(
        "Upload Dataset (CSV or Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a CSV or Excel file to analyze"
    )
    
    # Option 2: Use default dataset
    use_default = st.checkbox("Use Default Sample Dataset", value=True)
    
    st.divider()
    st.header("⚙️ Settings")
    auto_eda = st.checkbox("Auto-Generate EDA", value=False, help="Automatically show visualizations")
    show_raw_data = st.checkbox("Show Raw Data", value=True, help="Display first rows of dataset")

# Load dataset
df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ Dataset loaded: {uploaded_file.name}")
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        df = None

elif use_default:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "data", "dataset.csv")
        df = pd.read_csv(csv_path)
        st.info("Using default sample dataset")
    except Exception as e:
        st.error(f"❌ Error loading default dataset: {str(e)}")
        df = None

# Main app logic
if df is not None:
    # Dataset Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Rows", len(df))
    with col2:
        st.metric("📋 Columns", len(df.columns))
    with col3:
        st.metric("🔢 Numeric", len(df.select_dtypes(include=['number']).columns))
    with col4:
        st.metric("🏷️ Categorical", len(df.select_dtypes(include=['object']).columns))
    
    st.divider()
    
    # Show raw data
    if show_raw_data:
        with st.expander("📋 View Raw Data", expanded=False):
            st.dataframe(df, use_container_width=True)
    
    # Auto EDA
    if auto_eda:
        st.divider()
        show_charts(df)
    
    st.divider()
    
    # Chat interface
    st.header("💬 Ask Questions About Your Data")
    
    question = st.text_input(
        "Type your question here...",
        placeholder="e.g., 'What is the average salary?', 'Show patterns in the data', 'List all names'"
    )
    
    if question:
        # Regular question answering
        answer = answer_question(df, question)
        
        if answer:
            if "❌" in answer:
                st.error(answer)
            elif "✓" in answer:
                st.success(answer)
            else:
                st.info(f"💡 {answer}")
        else:
            st.warning("⚠️ Cannot process this question")

else:
    st.warning("⚠️ Please upload a dataset or enable the sample dataset to get started")


