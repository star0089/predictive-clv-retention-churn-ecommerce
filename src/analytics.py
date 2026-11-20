"""Customer master, RFM and cohort-retention calculations."""
import numpy as np
import pandas as pd


def prepare_order_level(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create one row per delivered order with persistent customer ID and order economics.

    payment_value and freight_value are customer-paid amounts. They are not profit
    or contribution margin. Delivered orders are treated as completed purchases.
    """
    orders = data["orders"].copy()
    customers = data["customers"][["customer_id", "customer_unique_id"]].drop_duplicates("customer_id")
    delivered = orders.loc[orders["order_status"].eq("delivered")].copy()
    merged = delivered.merge(customers, on="customer_id", how="left", validate="many_to_one")
    payments = (
        data["payments"].groupby("order_id", as_index=False)["payment_value"]
        .sum().rename(columns={"payment_value": "paid_order_value"})
    )
    merged = merged.merge(payments, on="order_id", how="left", validate="one_to_one")
    items = data["order_items"].copy()
    item_agg = items.groupby("order_id").agg(
        item_count=("order_item_id", "count"),
        item_price_total=("price", "sum"),
        freight_paid=("freight_value", "sum"),
        unique_products=("product_id", "nunique"),
        unique_sellers=("seller_id", "nunique"),
    ).reset_index()
    merged = merged.merge(item_agg, on="order_id", how="left", validate="one_to_one")
    for column in ["paid_order_value", "item_count", "item_price_total", "freight_paid",
                   "unique_products", "unique_sellers"]:
        merged[column] = merged[column].fillna(0.0)
    merged = merged.dropna(subset=["customer_unique_id", "order_purchase_timestamp"])
    return merged.sort_values(["customer_unique_id", "order_purchase_timestamp"]).reset_index(drop=True)


def build_customer_master(order_level: pd.DataFrame) -> pd.DataFrame:
    """Aggregate delivered orders to one row per persistent customer."""
    master = (
        order_level.groupby("customer_unique_id")
        .agg(
            first_purchase=("order_purchase_timestamp", "min"),
            last_purchase=("order_purchase_timestamp", "max"),
            frequency=("order_id", "nunique"),
            monetary=("paid_order_value", "sum"),
            average_order_value=("paid_order_value", "mean"),
            total_items=("item_count", "sum"),
            freight_paid_total=("freight_paid", "sum"),
        ).reset_index()
    )
    master["customer_lifetime_days"] = (master["last_purchase"] - master["first_purchase"]).dt.days
    analysis_date = order_level["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    master["recency"] = (analysis_date - master["last_purchase"]).dt.days
    return master


def _quintile_score(series: pd.Series, labels: list[int]) -> pd.Series:
    ranked = series.rank(method="first")
    return pd.qcut(ranked, q=5, labels=labels).astype(int)


def frequency_score(value: int) -> int:
    if value <= 1:
        return 1
    if value == 2:
        return 2
    if value == 3:
        return 3
    if value <= 5:
        return 4
    return 5


def assign_rfm_segment(row: pd.Series) -> str:
    r, f, m = int(row["R_score"]), int(row["F_score"]), int(row["M_score"])
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal Customers"
    if r >= 4 and f <= 2:
        return "New / Recent Customers"
    if r <= 2 and f >= 3:
        return "At Risk"
    if r <= 2 and f <= 2:
        return "Lost / Inactive"
    if m >= 4:
        return "High Value"
    return "Regular Customers"


def add_rfm_scores(customer_master: pd.DataFrame) -> pd.DataFrame:
    result = customer_master.copy()
    result["R_score"] = _quintile_score(result["recency"], [5, 4, 3, 2, 1])
    result["M_score"] = _quintile_score(result["monetary"], [1, 2, 3, 4, 5])
    result["F_score"] = result["frequency"].apply(frequency_score)
    result["RFM_score"] = result["R_score"].astype(str) + result["F_score"].astype(str) + result["M_score"].astype(str)
    result["RFM_total"] = result[["R_score", "F_score", "M_score"]].sum(axis=1)
    result["RFM_segment"] = result.apply(assign_rfm_segment, axis=1)
    return result


def build_rfm_segment_summary(customer_master_rfm: pd.DataFrame) -> pd.DataFrame:
    summary = (
        customer_master_rfm.groupby("RFM_segment")
        .agg(customers=("customer_unique_id", "nunique"),
             avg_recency=("recency", "mean"), avg_frequency=("frequency", "mean"),
             avg_monetary=("monetary", "mean"), total_paid_value=("monetary", "sum"))
        .reset_index()
    )
    total = summary["total_paid_value"].sum()
    summary["paid_value_share_pct"] = np.where(total > 0, summary["total_paid_value"] / total * 100, 0.0)
    summary["customer_share_pct"] = summary["customers"] / summary["customers"].sum() * 100
    return summary.sort_values("total_paid_value", ascending=False).reset_index(drop=True)


def build_cohort_retention(order_level: pd.DataFrame) -> pd.DataFrame:
    """Build long-form monthly activity retention by first delivered-purchase month."""
    frame = order_level[["customer_unique_id", "order_purchase_timestamp"]].copy()
    frame["order_month"] = frame["order_purchase_timestamp"].dt.to_period("M")
    first_month = frame.groupby("customer_unique_id")["order_month"].min().rename("cohort_month")
    frame = frame.merge(first_month, on="customer_unique_id", how="left", validate="many_to_one")
    frame["cohort_index"] = ((frame["order_month"].dt.year - frame["cohort_month"].dt.year) * 12
                             + frame["order_month"].dt.month - frame["cohort_month"].dt.month)
    counts = frame.groupby(["cohort_month", "cohort_index"])["customer_unique_id"].nunique().rename("active_customers").reset_index()
    sizes = counts.loc[counts["cohort_index"].eq(0), ["cohort_month", "active_customers"]].rename(columns={"active_customers": "cohort_size"})
    result = counts.merge(sizes, on="cohort_month", how="left", validate="many_to_one")
    result["retention_pct"] = result["active_customers"] / result["cohort_size"] * 100
    result["cohort_month"] = result["cohort_month"].astype(str)
    return result.sort_values(["cohort_month", "cohort_index"]).reset_index(drop=True)
