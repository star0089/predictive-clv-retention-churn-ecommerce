import pandas as pd

from src.data_loader import parse_source_datetime
from src.analytics import build_customer_master, add_rfm_scores, build_cohort_retention
from src.churn import build_features_at_cutoff


def sample_orders():
    dates = pd.to_datetime([
        "2024-01-01", "2024-02-01", "2024-01-15", "2024-03-01",
        "2024-01-20", "2024-02-20", "2024-01-25", "2024-03-20",
        "2024-01-30", "2024-04-01", "2024-02-05", "2024-04-10",
    ])
    rows = []
    for i, date in enumerate(dates):
        rows.append({
            "customer_unique_id": f"c{i // 2:02d}",
            "order_id": f"o{i:02d}",
            "order_purchase_timestamp": date,
            "paid_order_value": float(100 + i),
            "item_count": 1 + (i % 3),
            "item_price_total": float(80 + i),
            "freight_paid": 10.0,
        })
    return pd.DataFrame(rows)


def test_parse_source_datetime_supports_day_first_and_iso():
    values = pd.Series(["24-07-2018 20:41", "2018-07-24 20:41:00"])
    parsed = parse_source_datetime(values)
    assert parsed.notna().all()
    assert parsed.iloc[0].day == 24
    assert parsed.iloc[1].month == 7


def test_customer_master_has_one_row_per_persistent_customer():
    orders = sample_orders()
    master = build_customer_master(orders)
    assert master["customer_unique_id"].is_unique
    assert len(master) == orders["customer_unique_id"].nunique()


def test_rfm_scores_and_segments_are_created():
    master = build_customer_master(sample_orders())
    rfm = add_rfm_scores(master)
    assert {"R_score", "F_score", "M_score", "RFM_total", "RFM_segment"}.issubset(rfm.columns)
    assert rfm[["R_score", "F_score", "M_score"]].min().min() >= 1
    assert rfm[["R_score", "F_score", "M_score"]].max().max() <= 5


def test_cohort_retention_month_zero_is_100_percent():
    retention = build_cohort_retention(sample_orders())
    month_zero = retention.loc[retention["cohort_index"].eq(0), "retention_pct"]
    assert not month_zero.empty
    assert (month_zero.round(6) == 100.0).all()


def test_features_use_only_orders_on_or_before_cutoff():
    orders = sample_orders()
    future = pd.DataFrame([{
        "customer_unique_id": "c00",
        "order_id": "future-order",
        "order_purchase_timestamp": pd.Timestamp("2024-05-01"),
        "paid_order_value": 9999.0,
        "item_count": 1,
        "item_price_total": 9999.0,
        "freight_paid": 0.0,
    }])
    orders = pd.concat([orders, future], ignore_index=True)
    features = build_features_at_cutoff(orders, pd.Timestamp("2024-04-15"), 180)
    customer = features.loc[features["customer_unique_id"].eq("c00")].iloc[0]
    assert customer["paid_value_lifetime"] < 9999.0
    assert customer["recency_days"] >= 0
