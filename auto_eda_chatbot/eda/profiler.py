def profile_data(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().to_dict(),
        "column_types": df.dtypes.apply(str).to_dict()
    }
