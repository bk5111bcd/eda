import pandas as pd

def load_data(file_path):
    """
    Load CSV file and clean it.
    """
    df = pd.read_csv(file_path)

    # Basic cleaning
    df.drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)  # replace missing values
    return df

def preprocess_data(df):
    """
    Preprocess the DataFrame:
    - Convert simple categorical columns (Yes/No) to numeric (1/0)
    """
    for col in df.columns:
        if df[col].dtype == object:
            unique_vals = set(df[col].dropna().unique())
            if unique_vals <= {"Yes", "No"}:
                df[col] = df[col].map({"Yes": 1, "No": 0})
    return df

