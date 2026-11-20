"""Load and validate the public Olist CSV files."""
from pathlib import Path
import pandas as pd

FILE_MAP = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
    "marketing_qualified_leads": "olist_marketing_qualified_leads_dataset.csv",
    "closed_deals": "olist_closed_deals_dataset.csv",
}
REQUIRED = {"customers", "orders", "order_items", "payments"}
ORDER_DATE_COLUMNS = [
    "order_purchase_timestamp", "order_approved_at",
    "order_delivered_carrier_date", "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

def parse_source_datetime(series: pd.Series) -> pd.Series:
    """Parse both the observed day-first export and standard ISO Olist timestamps."""
    values = series.astype("string").str.strip()
    parsed = pd.to_datetime(values, format="%d-%m-%Y %H:%M", errors="coerce")
    missing = parsed.isna() & values.notna() & values.ne("")
    if missing.any():
        parsed.loc[missing] = pd.to_datetime(values.loc[missing], format="ISO8601", errors="coerce")
        remaining = parsed.isna() & values.notna() & values.ne("")
        if remaining.any():
            parsed.loc[remaining] = pd.to_datetime(
                values.loc[remaining], format="mixed", dayfirst=True, errors="coerce"
            )
    return parsed

def load_olist_data(data_dir: str | Path = "data_raw") -> dict[str, pd.DataFrame]:
    """Load required Olist tables and any optional tables present in data_dir."""
    root = Path(data_dir)
    if not root.exists():
        raise FileNotFoundError(f"Data directory not found: {root.resolve()}")
    data: dict[str, pd.DataFrame] = {}
    missing = []
    for name, filename in FILE_MAP.items():
        path = root / filename
        if not path.exists():
            if name in REQUIRED:
                missing.append(filename)
            continue
        data[name] = pd.read_csv(path)
    if missing:
        raise FileNotFoundError(
            "Missing required Olist files in " + str(root.resolve()) + ": " + ", ".join(missing)
        )
    orders = data["orders"].copy()
    for column in ORDER_DATE_COLUMNS:
        if column in orders.columns:
            orders[column] = parse_source_datetime(orders[column])
    data["orders"] = orders
    if "order_items" in data:
        items = data["order_items"].copy()
        empty_columns = [
            column for column in items.columns
            if column.startswith("Unnamed")
            and items[column].astype("string").str.strip().replace("", pd.NA).isna().all()
        ]
        data["order_items"] = items.drop(columns=empty_columns)
    if "reviews" in data:
        reviews = data["reviews"].copy()
        for column in ("review_creation_date", "review_answer_timestamp"):
            if column in reviews.columns:
                reviews[column] = parse_source_datetime(reviews[column])
        data["reviews"] = reviews
    if "marketing_qualified_leads" in data and "first_contact_date" in data["marketing_qualified_leads"]:
        leads = data["marketing_qualified_leads"].copy()
        leads["first_contact_date"] = pd.to_datetime(
            leads["first_contact_date"], format="%d-%m-%Y", errors="coerce"
        )
        data["marketing_qualified_leads"] = leads
    if "closed_deals" in data and "won_date" in data["closed_deals"]:
        deals = data["closed_deals"].copy()
        deals["won_date"] = parse_source_datetime(deals["won_date"])
        data["closed_deals"] = deals
    return data

def build_data_quality_report(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Return table-level row counts, duplicate counts and missing-cell counts."""
    rows = []
    for name, frame in data.items():
        rows.append({
            "table": name,
            "rows": len(frame),
            "columns": len(frame.columns),
            "duplicate_full_rows": int(frame.duplicated().sum()),
            "missing_cells": int(frame.isna().sum().sum()),
        })
    return pd.DataFrame(rows).sort_values("table").reset_index(drop=True)
