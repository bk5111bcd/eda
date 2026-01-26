import pandas as pd
import re
import os
from typing import Optional


def load_dataset(file_path: str) -> pd.DataFrame:
    """Load dataset from CSV or Excel file with automatic normalization"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # GOLDEN FIX: Normalize all data
        # Strip whitespace and convert to lowercase for string columns
        df.columns = df.columns.str.strip().str.lower()
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                df[col] = df[col].astype(str).str.strip().str.lower()
        
        return df
    except Exception as e:
        raise Exception(f"Error loading dataset: {str(e)}")


def classify_question(question, df):
    """
    CLASSIFY QUESTION TYPE:
    - "data_retrieval": Use Pandas only (fact-based)
    - "analysis": Use LLM with context (interpretation-based)
    """
    q = question.lower()
    
    # DATA RETRIEVAL SIGNALS
    retrieval_keywords = ['salary', 'age', 'department', 'experience', 'designation', 'role', 'city',
                         'max', 'min', 'average', 'mean', 'count', 'list', 'who', 'which']
    
    # ANALYSIS SIGNALS
    analysis_keywords = ['pattern', 'trend', 'why', 'how', 'compare', 'analyze', 'insight', 
                        'relationship', 'correlation', 'increase', 'decrease', 'reason', 'explain']
    
    # Check for analysis keywords first (stronger signal)
    for keyword in analysis_keywords:
        if keyword in q:
            return "analysis"
    
    # Check for data retrieval keywords
    for keyword in retrieval_keywords:
        if keyword in q:
            # But make sure it's asking for a specific value or stat
            if any(word in q for word in ['of ', 'for ', 'what is', 'show', 'list', 'average', 'max', 'min']):
                return "data_retrieval"
    
    # Default to analysis for unclear questions
    return "analysis"


def retrieve_from_dataset(df, question):
    """
    Dataset-agnostic retrieval function.
    Returns data if found, None if analysis-type question (route to LLM)
    """
    # Safety check: ensure question is a string
    if isinstance(question, pd.DataFrame):
        return "❌ Internal error: DataFrame passed instead of question text"
    if not isinstance(question, str):
        return f"❌ Internal error: question must be text, got {type(question)}"
    
    # Normalize question (strip and lowercase)
    q = question.lower().strip()
    
    # CHECK FOR MULTIPLE PEOPLE QUERY FIRST (HIGHEST PRIORITY)
    if " and " in q:
        names = extract_multiple_names(question, df)
        if len(names) >= 2:
            print(f"[RETRIEVE] Multiple people detected: {names}")
            # Find which column they're asking about
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            for col in numeric_cols:
                col_lower = col.lower()
                if col_lower in q:
                    result = retrieve_multiple_people_data(df, question, col)
                    if result:
                        return result
            
            # Also check categorical columns
            for col in df.columns:
                col_lower = col.lower()
                if col_lower in q and col != 'name':
                    result = retrieve_multiple_people_data(df, question, col)
                    if result:
                        return result
    
    # CHECK FOR PERSON COMPARISON (SECOND PRIORITY)
    comparison = detect_person_comparison(question, df)
    if comparison:
        person1, person2 = comparison
        print(f"[RETRIEVE] Person comparison detected: {person1} vs {person2}")
        return f"__COMPARISON__{person1}__AND__{person2}__"

    # ANALYSIS KEYWORDS - These MUST go to LLM, NOT pandas
    analysis_keywords = [
        "pattern", "patterns", "trend", "trends",
        "analyze", "analysis", "summary", "summarize",
        "why", "why ", "insight", "insights", "describe", "compare", "comparison",
        "key statistics", "overview", "overview",
        "correlat", "relationship", "relationships",
        "anomal", "outlier", "outliers",
        "quality", "what are the",
    ]

    # If question contains analysis keywords → route to LLM
    for keyword in analysis_keywords:
        if keyword in q:
            print(f"[RETRIEVE] Analysis keyword found: '{keyword}' → routing to LLM")
            return None  # This triggers LLM routing

    # Handle "list" queries
    if "list" in q or ("show" in q and "all" in q):
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in q:
                values = df[col].unique()
                if len(values) <= 20:
                    return f"✓ {col}: {', '.join(str(v) for v in values)}"
                else:
                    return f"✓ {col}: {len(values)} unique values"

    # SCOPE BINDING: Extract person name FIRST to determine aggregation scope
    extracted_entity = extract_name(question, df)
    print(f"[RETRIEVE] DEBUG NAME: {extracted_entity}")
    
    if extracted_entity:
        # Person found - bind statistics to this person's data, NOT global data
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # Check if asking for statistics on this person
        if "average" in q or "mean" in q:
            for col in numeric_cols:
                col_lower = col.lower()
                if " " + col_lower + " " in " " + q + " ":
                    person_data = df[df['name'].str.lower() == extracted_entity.lower()][col]
                    if len(person_data) > 1:
                        avg_val = person_data.mean()
                        return f"✓ {extracted_entity}'s average {col}: {avg_val:.2f}"
                    elif len(person_data) == 1:
                        value = person_data.iloc[0]
                        return f"✓ {extracted_entity} has only one record: {col} = {value}"
                    else:
                        return f"❌ No records found for {extracted_entity}"
        
        if "max" in q or "maximum" in q or "highest" in q:
            for col in numeric_cols:
                col_lower = col.lower()
                if col_lower in q:
                    person_data = df[df['name'].str.lower() == extracted_entity.lower()][col]
                    if len(person_data) > 0:
                        return f"✓ {extracted_entity}'s max {col}: {person_data.max()}"
        
        if "min" in q or "minimum" in q or "lowest" in q:
            for col in numeric_cols:
                col_lower = col.lower()
                if col_lower in q:
                    person_data = df[df['name'].str.lower() == extracted_entity.lower()][col]
                    if len(person_data) > 0:
                        return f"✓ {extracted_entity}'s min {col}: {person_data.min()}"
        
        # If no statistics keyword, try to find specific column
        for col in df.columns:
            if col != 'name':
                col_lower = col.lower()
                q_words = q.split()
                if col_lower in q_words or col_lower in q:
                    mask = df['name'].str.lower() == extracted_entity.lower()
                    if mask.any():
                        result_value = df.loc[mask, col].values[0]
                        return f"✓ {extracted_entity}'s {col}: {result_value}"
        
        # Person found but can't determine what to extract → let LLM handle it
        return None

    # NO person name found - compute statistics on ENTIRE dataset (global scope)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if "average" in q or "mean" in q:
        for col in numeric_cols:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Average {col}: {df[col].mean():.2f}"
    
    if "max" in q or "maximum" in q or "highest" in q:
        for col in numeric_cols:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Max {col}: {df[col].max()}"
    
    if "min" in q or "minimum" in q or "lowest" in q:
        for col in numeric_cols:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Min {col}: {df[col].min()}"
    
    if "sum" in q or "total" in q:
        for col in numeric_cols:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Sum of {col}: {df[col].sum()}"
    
    if "count" in q:
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Count of {col}: {df[col].nunique()} unique values"

    # Default: route unmatched questions to LLM for analysis
    print("[RETRIEVE] No specific pattern matched → routing to LLM")
    return None


def extract_multiple_names(question: str, df: pd.DataFrame) -> list:
    """
    Extract multiple names from a question joined by 'and'
    Returns list of names found
    """
    if 'name' not in df.columns:
        return []
    
    q = question.lower()
    all_names = [name.lower() for name in df['name'].unique()]
    found_names = []
    
    for name in all_names:
        if name in q:
            found_names.append(name)
    
    return found_names


def retrieve_multiple_people_data(df, question: str, column: str) -> Optional[str]:
    """
    Retrieve data for multiple people at once
    Example: "What is the age of ravi kumar and anjali"
    """
    names = extract_multiple_names(question, df)
    
    if len(names) < 2:
        return None
    
    col_lower = column.lower()
    results = []
    
    for name in names:
        person_data = df[df['name'].str.lower() == name.lower()]
        if len(person_data) > 0:
            value = person_data[column].values[0]
            results.append(f"{name.title()}: {value}")
    
    if results:
        return f"✓ {column.title()}:\n  " + "\n  ".join(results)
    
    return None


def extract_name(question: str, df: pd.DataFrame) -> Optional[str]:
    """Extract person/entity name from question - works with any ID column"""
    q = question.lower()
    for name in df['name']:
        if name.lower() in q:
            return name
    return None


def extract_column_from_question(question: str, df: pd.DataFrame) -> Optional[str]:
    """Extract column name from question - works with any DataFrame"""
    q = question.lower()
    
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in q:
            return col
    
    return None


def parse_visualization_request(question: str, df: pd.DataFrame) -> Optional[tuple]:
    """
    Parse visualization requests from questions
    Returns: (visualization_type, column_name) or None
    """
    q = question.lower()
    column = extract_column_from_question(question, df)
    
    if not column:
        return None
    
    viz_types = {
        'histogram': ['histogram', 'distribution', 'dist'],
        'boxplot': ['boxplot', 'box', 'outlier'],
        'countplot': ['count', 'frequency', 'categorical'],
    }
    
    for viz_type, keywords in viz_types.items():
        if any(kw in q for kw in keywords):
            return (viz_type, column)
    
    return None


def detect_person_comparison(question: str, df: pd.DataFrame) -> Optional[tuple]:
    """
    Detect if user is asking for comparison between two people.
    Returns: (person1, person2) or None
    
    Examples:
    - "Compare ravi kumar and anjali sharma"
    - "Show difference between ravi and pooja"
    - "ravi vs anjali"
    """
    q = question.lower()
    
    # Comparison keywords
    comparison_keywords = ['compare', 'vs', 'versus', 'difference', 'between', 'vs.', 'v/s']
    
    # Check if question contains comparison intent
    has_comparison = any(kw in q for kw in comparison_keywords)
    if not has_comparison:
        return None
    
    # Get all available person names from dataset
    if 'name' not in df.columns:
        return None
    
    all_names = [name.lower() for name in df['name'].unique()]
    
    # Find which two names are mentioned in the question
    found_names = []
    for name in all_names:
        if name in q:
            found_names.append(name)
    
    # Return if exactly 2 people found
    if len(found_names) == 2:
        return (found_names[0], found_names[1])
    
    return None


def create_person_comparison_chart(df, person1: str, person2: str):
    """
    Create a comparison visualization for two people.
    Returns: (fig, data_dict) for both chart and detailed data
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Filter data for both people
        p1_data = df[df['name'].str.lower() == person1.lower()]
        p2_data = df[df['name'].str.lower() == person2.lower()]
        
        if len(p1_data) == 0 or len(p2_data) == 0:
            return None, None
        
        # Get numeric columns for comparison
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            return None, None
        
        # Prepare data for visualization
        fig, axes = plt.subplots(1, len(numeric_cols), figsize=(15, 5))
        if len(numeric_cols) == 1:
            axes = [axes]
        
        comparison_data = {}
        
        # Create individual charts for each numeric column
        for idx, col in enumerate(numeric_cols):
            p1_val = p1_data[col].values[0]
            p2_val = p2_data[col].values[0]
            
            comparison_data[col] = {
                person1: float(p1_val),
                person2: float(p2_val)
            }
            
            # Create bar chart
            names = [person1.title(), person2.title()]
            values = [p1_val, p2_val]
            colors = ['#667eea', '#764ba2']
            
            axes[idx].bar(names, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
            axes[idx].set_title(f'{col.title()} Comparison', fontsize=12, fontweight='bold')
            axes[idx].set_ylabel(col.title(), fontsize=10)
            
            # Add value labels on bars
            for i, v in enumerate(values):
                axes[idx].text(i, v, f'{v:.0f}', ha='center', va='bottom', fontweight='bold')
            
            # Styling
            axes[idx].set_facecolor('#1a1f3a')
            axes[idx].grid(axis='y', alpha=0.3, linestyle='--')
            for spine in axes[idx].spines.values():
                spine.set_color('#00d9ff')
                spine.set_linewidth(1.5)
        
        fig.patch.set_facecolor('#0a0e27')
        fig.suptitle(f'Comparison: {person1.title()} vs {person2.title()}', 
                    fontsize=14, fontweight='bold', color='white', y=1.02)
        plt.tight_layout()
        
        return fig, comparison_data
    
    except Exception as e:
        print(f"Error creating comparison chart: {e}")
        return None, None


def answer_question(df, question):
    """Router: Pandas first, LLM second. NO LOGIC, NO CONDITIONS."""
    # Debug output
    print(f"[ROUTER] Question Type: {type(question)} | Value Type Check: {isinstance(question, str)}")
    
    # Safety check: ensure question is a string
    if isinstance(question, pd.DataFrame):
        return "❌ Internal error: DataFrame passed instead of question text"
    if not isinstance(question, str):
        return f"❌ Internal error: question must be text, got {type(question)}"
    
    print(f"[ROUTER] 🎯 Question: {question.upper()}")
    result = retrieve_from_dataset(df, question)

    if result is None:
        return ask_llm_for_analysis(question, df)
    else:
        return result


def ask_llm_for_analysis(question, df):
    """
    Call OpenAI GPT-4 for advanced analysis - provides deep insights with statistical rigor.
    Falls back to Gemini if OpenAI is unavailable.
    Dataset-agnostic approach - only summaries, no raw data.
    """
    print(">>> ENTERING LLM ANALYSIS <<<")
    
    # Try OpenAI first (preferred)
    openai_response = _ask_openai_for_analysis(question, df)
    if openai_response:
        print("✅ Using OpenAI response")
        return openai_response
    
    print("⚠️ OpenAI failed or unavailable, trying Gemini...")
    
    # Fallback to Gemini if OpenAI is unavailable
    gemini_response = _ask_gemini_for_analysis(question, df)
    if gemini_response:
        print("✅ Using Gemini response")
        return gemini_response
    
    print("❌ Both APIs failed, generating basic response from data...")
    
    # Last resort: Generate basic response from data statistics
    return _generate_basic_response(question, df)


def _ask_openai_for_analysis(question, df):
    """Call OpenAI GPT-4 API for advanced analysis"""
    print(">>> ROUTED TO OPENAI GPT-4 <<<")
    
    try:
        from openai import OpenAI
        
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ OPENAI_API_KEY not found in environment")
            return None
        
        print(f"✓ API Key found (length: {len(api_key)})")
        
        # Initialize client with proper error handling
        try:
            client = OpenAI(api_key=api_key)
            print("✓ OpenAI client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            return None
        
        # Build rich context with statistical analysis
        context = _build_data_context(df)
        print(f"✓ Data context built ({len(context)} chars)")
        
        # Create a sophisticated prompt for data analysis
        system_prompt = """You are an expert data analyst like ChatGPT. Your responses should be:
- Clear, concise, and well-structured
- Specific with numbers and statistics
- Actionable and insightful
- Professional yet conversational
- Use markdown formatting for better readability"""
        
        user_prompt = f"""Analyze this dataset and answer the following question:

QUESTION: {question}

DATASET STATISTICS:
{context}

Please provide a comprehensive, ChatGPT-style response with clear sections and actionable insights."""
        
        print("🔄 Calling OpenAI API...")
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
            top_p=0.95,
            timeout=30.0
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ OpenAI Success! Response: {len(result)} chars")
        return result
    
    except Exception as e:
        print(f"❌ OpenAI Error: {type(e).__name__}: {str(e)}")
        return None


def _ask_gemini_for_analysis(question, df):
    """Call Google Gemini API for analysis - fallback option"""
    print(">>> ROUTED TO GEMINI (FALLBACK) <<<")
    
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY not set - skipping Gemini fallback")
            return None
        
        print("✓ Configuring Gemini...")
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        context = _build_data_context(df)
        print(f"✓ Data context built ({len(context)} chars)")
        
        system_prompt = """You are a ChatGPT-like data analyst. Your responses should be:
- Clear and well-structured with sections
- Specific with numbers and statistics from the provided data
- Insightful and actionable
- Use markdown formatting
- Professional yet conversational"""
        
        prompt = f"""{system_prompt}

DATASET STATISTICS:
{context}

USER QUESTION: {question}

Please provide a comprehensive analysis similar to how ChatGPT would respond. Use clear sections and specific numbers."""
        
        print("🔄 Calling Gemini API...")
        response = model.generate_content(prompt)
        result = response.text.strip()
        print(f"✅ Gemini Success! Response: {len(result)} chars")
        return result
    
    except Exception as e:
        print(f"❌ Gemini Error: {type(e).__name__}: {str(e)}")
        return None


def _build_data_context(df):
    """Build comprehensive statistical context from the dataset"""
    context = f"📊 Dataset Overview: {len(df):,} rows, {len(df.columns)} columns\n\n"
    
    # Numeric column analysis
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        context += "📈 NUMERIC COLUMNS (Statistical Summary):\n"
        for col in numeric_cols:
            try:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    context += f"  • {col.upper()}:\n"
                    context += f"      - Count: {len(col_data):,} values\n"
                    context += f"      - Min: {col_data.min():.2f}\n"
                    context += f"      - Q1 (25%): {col_data.quantile(0.25):.2f}\n"
                    context += f"      - Median: {col_data.median():.2f}\n"
                    context += f"      - Q3 (75%): {col_data.quantile(0.75):.2f}\n"
                    context += f"      - Max: {col_data.max():.2f}\n"
                    context += f"      - Mean: {col_data.mean():.2f}\n"
                    context += f"      - Std Dev: {col_data.std():.2f}\n"
            except:
                pass
        context += "\n"
    
    # Categorical column analysis
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        context += "🏷️ CATEGORICAL COLUMNS:\n"
        for col in categorical_cols:
            unique_count = df[col].nunique()
            context += f"  • {col.upper()}: {unique_count} unique values\n"
            # Show top 5 categories
            top_values = df[col].value_counts().head(5)
            for idx, (val, count) in enumerate(top_values.items(), 1):
                pct = (count / len(df)) * 100
                context += f"      {idx}. {val}: {count} ({pct:.1f}%)\n"
        context += "\n"
    
    # Missing data summary
    missing = df.isnull().sum()
    if missing.sum() > 0:
        context += "⚠️ MISSING DATA:\n"
        for col in missing[missing > 0].index:
            pct = (missing[col] / len(df)) * 100
            context += f"  • {col}: {missing[col]} missing ({pct:.1f}%)\n"
        context += "\n"
    
    # Data quality metrics
    context += "✅ DATA QUALITY:\n"
    context += f"  • Total cells: {len(df) * len(df.columns):,}\n"
    context += f"  • Complete cells: {(len(df) * len(df.columns)) - df.isnull().sum().sum():,}\n"
    context += f"  • Completeness: {((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100):.1f}%\n"
    
    return context


def _generate_basic_response(question, df):
    """Generate a basic response from data statistics when APIs are unavailable"""
    print(">>> GENERATING BASIC RESPONSE <<<")
    
    try:
        response = f"""## Analysis of Your Dataset

Based on your question: **{question}**

### 📊 Dataset Overview
- **Total Rows:** {len(df):,}
- **Total Columns:** {len(df.columns)}
- **Data Size:** {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

### 📈 Numeric Columns Analysis
"""
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            response += f"Found {len(numeric_cols)} numeric columns:\n"
            for col in numeric_cols[:5]:  # Show first 5
                col_data = df[col].dropna()
                response += f"\n**{col}:**\n"
                response += f"- Min: {col_data.min():.2f}\n"
                response += f"- Max: {col_data.max():.2f}\n"
                response += f"- Mean: {col_data.mean():.2f}\n"
                response += f"- Median: {col_data.median():.2f}\n"
        
        response += f"\n### 🏷️ Categorical Columns Analysis\n"
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        if cat_cols:
            response += f"Found {len(cat_cols)} categorical columns\n"
            for col in cat_cols[:3]:  # Show first 3
                unique_count = df[col].nunique()
                response += f"- **{col}:** {unique_count} unique values\n"
        
        response += f"\n### ⚠️ Data Quality\n"
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        response += f"- Missing data: {missing_pct:.1f}%\n"
        response += f"- Data completeness: {100 - missing_pct:.1f}%\n"
        
        response += "\n*Note: This is a basic analysis. For more detailed insights, please ensure your API keys are properly configured.*"
        
        return response
    
    except Exception as e:
        print(f"Error generating basic response: {e}")
        return f"⚠️ Unable to generate analysis. Error: {str(e)}\n\nPlease check your API configuration or try a different question."


