def validate_columns(df, required_columns):
    return all(column in df.columns for column in required_columns)

