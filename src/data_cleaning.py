"""Reusable cleaning helpers for the Olist customer analytics project."""

import pandas as pd

ORDER_DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

def parse_order_dates(orders: pd.DataFrame) -> pd.DataFrame:
    """Parse Olist order timestamps using the observed source format."""
    cleaned = orders.copy()
    for col in ORDER_DATE_COLUMNS:
        cleaned[col] = pd.to_datetime(
            cleaned[col],
            format="%d-%m-%Y %H:%M",
            errors="coerce",
        )
    return cleaned

def one_review_per_order(order_reviews: pd.DataFrame) -> pd.DataFrame:
    """Keep one deterministic review record per order."""
    reviews = order_reviews.copy()
    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"],
        errors="coerce",
    )
    return (
        reviews.sort_values(["order_id", "review_answer_timestamp"])
        .drop_duplicates("order_id", keep="last")
    )
