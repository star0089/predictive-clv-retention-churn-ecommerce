"""Feature engineering helpers used in retention and RFM practice."""

import pandas as pd

def build_repeat_after_days(customer_orders: pd.DataFrame, days: int = 7) -> pd.Series:
    """Return a customer-level binary target for any later purchase after N days."""
    first_purchase = (
        customer_orders.groupby("customer_unique_id")["order_purchase_timestamp"]
        .min()
    )
    df = customer_orders.merge(
        first_purchase.rename("first_purchase"),
        on="customer_unique_id",
        how="left",
    )
    df["days_from_first"] = (
        df["order_purchase_timestamp"] - df["first_purchase"]
    ).dt.total_seconds() / 86400

    return (
        df.groupby("customer_unique_id")["days_from_first"]
        .apply(lambda x: (x > days).any())
        .astype(int)
        .rename(f"repeat_after_{days}d")
    )

def frequency_score(x: int) -> int:
    """Business-rule frequency score for the highly skewed Olist order counts."""
    if x == 1:
        return 1
    if x == 2:
        return 2
    if x == 3:
        return 3
    if x <= 5:
        return 4
    return 5
