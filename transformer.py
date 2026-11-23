import re

def to_snake_case(column_name):
    column_name = column_name.strip().lower()
    column_name = re.sub(r"[^a-z0-9]+", "_", column_name)
    return column_name.strip("_")


def calculate_order_totals(data):
    order_totals = {}

    for row in data:
        order_id = row["order_id"]
        price = float(row["price"])
        order_totals[order_id] = order_totals.get(order_id, 0) + price

    return order_totals

