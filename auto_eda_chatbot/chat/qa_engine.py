import pandas as pd
import re
import os
from typing import Optional


def load_dataset(file_path: str) -> pd.DataFrame:
    """Load dataset from CSV or Excel file"""
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
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
    Works with any DataFrame structure.
    """
    # Safety check: ensure question is a string
    if isinstance(question, pd.DataFrame):
        return "❌ Internal error: DataFrame passed instead of question text"
    if not isinstance(question, str):
        return f"❌ Internal error: question must be text, got {type(question)}"
    
    q = question.lower()

    # Words that mean "analysis"
    analysis_keywords = [
        "pattern", "patterns", "trend", "trends",
        "analyze", "analysis", "summary",
        "why", "insight", "describe", "compare"
    ]

    # If analysis intent → DO NOTHING
    if any(word in q for word in analysis_keywords):
        return None   # ← THIS LINE FIXES YOUR BOT

    # Handle "list" queries
    if "list" in q or "show" in q and "all" in q:
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in q:
                values = df[col].unique()
                if len(values) <= 20:
                    return f"✓ {col}: {', '.join(str(v) for v in values)}"
                else:
                    return f"✓ {col}: {len(values)} unique values"

    # Handle individual row lookups first (high priority)
    # Pattern: "X's [column]" or "[column] of X"
    for id_col in df.columns:
        id_col_lower = id_col.lower()
        if id_col_lower in ['name', 'id', 'employee', 'person', 'user']:
            for value in df[id_col].unique():
                value_str = str(value).lower()
                if value_str in q:
                    # Found entity - now find what column they're asking about
                    for col in df.columns:
                        col_lower = col.lower()
                        if col_lower != id_col_lower and col_lower in q:
                            # Convert column to string first, then apply .lower()
                            mask = df[id_col].astype(str).str.lower() == value_str
                            if mask.any():
                                result_value = df.loc[mask, col].values[0]
                                return f"✓ {value}'s {col}: {result_value}"

    # Handle statistics queries (min, max, average, mean)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if "average" in q or "mean" in q:
        for col in numeric_cols:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Average {col}: {df[col].mean():.2f}"
    
    if "max" in q or "maximum" in q:
        for col in numeric_cols:
            col_lower = col.lower()
            if col_lower in q:
                return f"✓ Max {col}: {df[col].max()}"
    
    if "min" in q or "minimum" in q:
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

    return "❌ Cannot parse question"


def extract_name(question: str, df: pd.DataFrame) -> Optional[str]:
    """Extract person/entity name from question - works with any ID column"""
    q = question.lower()
    
    # Try to match against values in ID-like columns
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['name', 'id', 'employee', 'person', 'user']:
            for value in df[col].unique():
                if str(value).lower() in q:
                    return str(value)
    
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


def answer_question(df, question):
    """Router: Pandas first, LLM second. NO LOGIC, NO CONDITIONS."""
    # Safety check: ensure question is a string
    if isinstance(question, pd.DataFrame):
        return "❌ Internal error: DataFrame passed instead of question text"
    if not isinstance(question, str):
        return f"❌ Internal error: question must be text, got {type(question)}"
    
    result = retrieve_from_dataset(df, question)

    if result is None:
        return ask_llm_for_analysis(question, df)
    else:
        return result


def ask_llm_for_analysis(question, df):
    """Call LLM for analysis - only summaries, no raw data. Dataset-agnostic."""
    print(">>> ROUTED TO LLM <<<")  # DEBUG LINE - MANDATORY
    
    try:
        from llama_cpp import Llama
        
        # Find model path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_root = os.path.dirname(current_dir)
        model_path = os.path.join(app_root, "models", "TinyLlama-1.1B-Chat-Q4_K_M.gguf")
        
        if not os.path.exists(model_path):
            return None
        
        # Build dataset-agnostic context with only summaries
        context = f"Dataset: {len(df)} rows, {len(df.columns)} columns\n\n"
        
        # Numeric summaries
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            context += "NUMERIC COLUMNS SUMMARY:\n"
            for col in numeric_cols:
                context += f"  {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}\n"
            context += "\n"
        
        # Categorical summaries
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            context += "CATEGORICAL COLUMNS SUMMARY:\n"
            for col in categorical_cols:
                context += f"  {col}: {df[col].nunique()} unique values\n"
            context += "\n"
        
        # Full statistical summary
        context += "DETAILED STATISTICS:\n"
        context += df.describe(include='all').to_string()
        
        prompt = f"""You are a data analyst.
Only use the dataset information below.
Answer the user's question based ONLY on the provided data.
Do NOT invent data or statistics.
Be concise and accurate.

DATASET INFORMATION:
{context}

USER QUESTION:
{question}

ANSWER:"""
        
        llm = Llama(
            model_path=model_path,
            n_ctx=512,
            n_threads=4,
            verbose=False
        )
        
        response = llm(prompt, max_tokens=150, temperature=0.2)
        return response['choices'][0]['text'].strip()
    
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return None

