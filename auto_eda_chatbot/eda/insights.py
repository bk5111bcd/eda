def generate_insights(df):
    insights = []

    # Missing data
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            insights.append(f"Column '{col}' has {count} missing values")

    # Strong correlations
    numeric_cols = df.select_dtypes(include='number')
    corr_matrix = numeric_cols.corr()
    for col1 in corr_matrix.columns:
        for col2 in corr_matrix.columns:
            if col1 != col2 and abs(corr_matrix[col1][col2]) > 0.8:
                insights.append(f"Columns '{col1}' and '{col2}' are strongly correlated ({corr_matrix[col1][col2]:.2f})")

    return insights
