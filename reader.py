import pandas as pd

def read_csv(path):
    df = pd.read_csv(path)
    return df

import pandas as pd

def read_csv(path: str) -> pd.DataFrame:
    """Read a CSV file."""
    return pd.read_csv(path)