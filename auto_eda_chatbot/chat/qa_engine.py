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
    Works with any DataFrame structure.
    """
    # Safety check: ensure question is a string
    if isinstance(question, pd.DataFrame):
        return "❌ Internal error: DataFrame passed instead of question text"
    if not isinstance(question, str):
        return f"❌ Internal error: question must be text, got {type(question)}"
    
    # Normalize question (strip and lowercase)
    q = question.lower().strip()

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

    # SCOPE BINDING: Extract person name FIRST to determine aggregation scope
    extracted_entity = extract_name(question, df)
    print(f"DEBUG NAME: {extracted_entity}")
    
    if extracted_entity:
        # Person found - bind statistics to this person's data, NOT global data
        # "average salary of arun" → arun's average (or single value if only one row)
        # NOT global average
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # Check if asking for statistics on this person
        if "average" in q or "mean" in q:
            for col in numeric_cols:
                col_lower = col.lower()
                # Use word boundary matching to avoid false positives (e.g., "age" in "arun")
                # Check if column name is a whole word in the question
                if " " + col_lower + " " in " " + q + " ":
                    # Get values for THIS PERSON only
                    person_data = df[df['name'].str.lower() == extracted_entity.lower()][col]
                    if len(person_data) > 1:
                        # Multiple records - compute average
                        avg_val = person_data.mean()
                        return f"✓ {extracted_entity}'s average {col}: {avg_val:.2f}"
                    elif len(person_data) == 1:
                        # Only one record - average is not applicable
                        value = person_data.iloc[0]
                        return f"✓ {extracted_entity} has only one record: {col} = {value} (average not applicable for single record)"
                    else:
                        # No records found
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
        
        # If no statistics keyword, just return the person's column value
        for id_col in df.columns:
            if id_col in ['name', 'id', 'employee', 'person', 'user']:
                for col in df.columns:
                    if col != id_col:
                        col_lower = col.lower()
                        q_words = q.split()
                        if col_lower in q_words or col_lower in q.replace("'s", "").replace("of", "").replace("what", "").replace("is", "").replace("the", "").replace("a", ""):
                            mask = df[id_col].str.lower() == extracted_entity.lower()
                            if mask.any():
                                result_value = df.loc[mask, col].values[0]
                                return f"✓ {extracted_entity}'s {col}: {result_value}"
        
        # If we have a person but no specific column match, return error
        return f"❌ {extracted_entity} found but cannot determine what you're asking for"

    # NO person name found - compute statistics on ENTIRE dataset (global scope)
    # "what is the average salary" → global average
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




    # Last resort: check if someone is asking for a person but extract_name failed
    for id_col in df.columns:
        if id_col in ['name', 'id', 'employee', 'person', 'user']:
            available_names = df[id_col].unique().tolist()
            return f"❌ Person not found. Available: {', '.join(available_names)}"

    return "❌ Cannot parse question"


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
    """Call Gemini API for analysis - only summaries, no raw data. Dataset-agnostic."""
    print(">>> ROUTED TO GEMINI <<<")  # DEBUG LINE - MANDATORY
    
    try:
        import google.generativeai as genai
        
        # Configure Gemini with API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("ERROR: GEMINI_API_KEY environment variable not set")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
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
        
        prompt = f"""You are a professional data analyst.
Only use the dataset information below.
Answer the user's question based ONLY on the provided data.
Do NOT invent data or statistics.
Be concise, logical, and accurate.
Provide structured insights.

DATASET INFORMATION:
{context}

USER QUESTION:
{question}

ANSWER:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Gemini Error: {str(e)}")
        return None

