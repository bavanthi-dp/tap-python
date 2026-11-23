def validate_columns(df, required_columns):
    return all(column in df.columns for column in required_columns)

import pandas as pd

def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """Check required columns."""
    return all(col in df.columns for col in required_columns)