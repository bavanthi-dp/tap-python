
import pandas as pd

from reader import read_csv
from validator import validate_columns
from transformer import calculate_order_totals


# Test 1
def test_read_csv():
    df = read_csv(r"C:\Users\Bavanthika\Desktop\tap-python\data\order_items.csv")
    assert len(df) > 0


# Test 2
def test_validate_columns():
    df = pd.DataFrame({"order_id": [101], "price": [100]})
    assert validate_columns(df, ["order_id", "price"])


# Test 3
def test_calculate_order_totals():
    data = [
        {"order_id": "101", "price": 100},
        {"order_id": "101", "price": 200}
    ]

    result = calculate_order_totals(data)
    assert result == {"101": 300}
