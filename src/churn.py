"""Leakage-aware churn snapshot construction and classification."""
from pathlib import Path
import json
import math
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline

FEATURE_COLUMNS = [
    "recency_days", "tenure_days", "orders_lifetime", "paid_value_lifetime",
    "orders_30d", "orders_90d", "orders_180d",
    "paid_value_30d", "paid_value_90d", "paid_value_180d",
    "items_180d", "item_price_180d", "freight_paid_180d",
    "avg_order_value_180d", "avg_items_per_order_180d",
    "purchase_gap_mean_days", "purchase_gap_std_days",
]


def build_features_at_cutoff(order_level: pd.DataFrame, cutoff_date: pd.Timestamp,
                              active_lookback_days: int = 180) -> pd.DataFrame:
    """Build features using delivered transactions available on/before cutoff only."""
    cutoff = pd.Timestamp(cutoff_date)
    history = order_level.loc[order_level["order_purchase_timestamp"].le(cutoff)].copy()
    if history.empty:
        return pd.DataFrame(columns=["customer_unique_id", "snapshot_date", *FEATURE_COLUMNS])
    last = history.groupby("customer_unique_id")["order_purchase_timestamp"].max()
    active_ids = last[last.ge(cutoff - pd.Timedelta(days=active_lookback_days))].index
    history = history[history["customer_unique_id"].isin(active_ids)].copy()
    if history.empty:
        return pd.DataFrame(columns=["customer_unique_id", "snapshot_date", *FEATURE_COLUMNS])
    base = history.groupby("customer_unique_id").agg(
        first_purchase=("order_purchase_timestamp", "min"),
        last_purchase=("order_purchase_timestamp", "max"),
        orders_lifetime=("order_id", "nunique"),
        paid_value_lifetime=("paid_order_value", "sum"),
    )
    base["recency_days"] = (cutoff - base["last_purchase"]).dt.total_seconds() / 86400
    base["tenure_days"] = (cutoff - base["first_purchase"]).dt.total_seconds() / 86400
    for days in (30, 90, 180):
        window = history.loc[history["order_purchase_timestamp"].gt(cutoff - pd.Timedelta(days=days))]
        agg = window.groupby("customer_unique_id").agg(
            **{f"orders_{days}d": ("order_id", "nunique"),
               f"paid_value_{days}d": ("paid_order_value", "sum")}
        )
        base = base.join(agg, how="left")
    window_180 = history.loc[history["order_purchase_timestamp"].gt(cutoff - pd.Timedelta(days=180))]
    basket = window_180.groupby("customer_unique_id").agg(
        items_180d=("item_count", "sum"), item_price_180d=("item_price_total", "sum"),
        freight_paid_180d=("freight_paid", "sum")
    )
    base = base.join(basket, how="left")
    # prepare_order_level sorts once; filtering preserves customer/date order.
    # Avoid sorting the full historical table again at every monthly snapshot.
    history["gap_days"] = history.groupby("customer_unique_id")["order_purchase_timestamp"].diff().dt.total_seconds() / 86400
    gap_stats = history.groupby("customer_unique_id")["gap_days"].agg(
        purchase_gap_mean_days="mean", purchase_gap_std_days="std"
    )
    base = base.join(gap_stats, how="left")
    base["avg_order_value_180d"] = base["paid_value_180d"] / base["orders_180d"]
    base["avg_items_per_order_180d"] = base["items_180d"] / base["orders_180d"]
    result = base.reset_index()
    result["snapshot_date"] = cutoff
    for col in FEATURE_COLUMNS:
        if col not in result:
            result[col] = np.nan
    return result[["customer_unique_id", "snapshot_date", *FEATURE_COLUMNS]]


def build_churn_snapshots(order_level: pd.DataFrame, analysis_end: pd.Timestamp,
                          horizon_days: int = 240, active_lookback_days: int = 180,
                          feature_lookback_days: int = 180) -> pd.DataFrame:
    """Create active-customer snapshots with complete future churn labels."""
    data = order_level.loc[order_level["order_purchase_timestamp"].le(analysis_end)].copy()
    if data.empty:
        raise ValueError("No delivered orders exist on or before analysis_end.")
    first_cutoff = data["order_purchase_timestamp"].min() + pd.Timedelta(days=feature_lookback_days)
    last_cutoff = pd.Timestamp(analysis_end) - pd.Timedelta(days=horizon_days)
    cutoffs = pd.date_range(first_cutoff.normalize(), last_cutoff.normalize(), freq="MS")
    snapshots = []
    for cutoff in cutoffs:
        features = build_features_at_cutoff(data, cutoff, active_lookback_days)
        if features.empty:
            continue
        future_end = cutoff + pd.Timedelta(days=horizon_days)
        future = data.loc[data["order_purchase_timestamp"].gt(cutoff)
                          & data["order_purchase_timestamp"].le(future_end)]
        returners = set(future["customer_unique_id"].unique())
        features["churned_240d"] = (~features["customer_unique_id"].isin(returners)).astype(int)
        future_value = future.groupby("customer_unique_id")["paid_order_value"].sum()
        features["future_paid_value"] = features["customer_unique_id"].map(future_value).fillna(0.0)
        snapshots.append(features)
    if not snapshots:
        raise ValueError("No complete churn snapshots. Check date coverage and horizon_days.")
    return pd.concat(snapshots, ignore_index=True)


def _ranking_metrics(y_true: pd.Series, probabilities: np.ndarray, fraction: float = 0.10) -> dict:
    n = len(y_true)
    k = max(1, int(math.ceil(n * fraction)))
    ranked = np.argsort(probabilities)[::-1][:k]
    labels = np.asarray(y_true).astype(int)
    captured = int(labels[ranked].sum())
    positives = int(labels.sum())
    precision_k = captured / k
    prevalence = positives / n if n else 0.0
    return {
        "precision_at_10pct": float(precision_k),
        "recall_at_10pct": float(captured / positives) if positives else 0.0,
        "lift_at_10pct": float(precision_k / prevalence) if prevalence else None,
    }


def train_and_score_churn(snapshots: pd.DataFrame, scoring_features: pd.DataFrame,
                          model_dir: str | Path = "models") -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """Evaluate chronologically, refit on all labels, then score active customers."""
    if len(snapshots) < 100 or snapshots["churned_240d"].nunique() < 2:
        raise ValueError("Insufficient churn training rows or target classes.")
    dates = sorted(pd.to_datetime(snapshots["snapshot_date"]).unique())
    if len(dates) < 3:
        raise ValueError("At least three distinct historical snapshot dates are required.")
    test_count = max(1, math.ceil(len(dates) * 0.20))
    test_dates = set(dates[-test_count:])
    train = snapshots[~pd.to_datetime(snapshots["snapshot_date"]).isin(test_dates)]
    test = snapshots[pd.to_datetime(snapshots["snapshot_date"]).isin(test_dates)]
    if train["churned_240d"].nunique() < 2 or test["churned_240d"].nunique() < 2:
        raise ValueError("Temporal holdout does not contain both target classes.")
    estimator = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=20,
                                         class_weight=None, n_jobs=2, random_state=42)),
    ])
    estimator.fit(train[FEATURE_COLUMNS], train["churned_240d"])
    test_prob = estimator.predict_proba(test[FEATURE_COLUMNS])[:, 1]
    metrics = {
        "target": "No delivered purchase in the next 240 days among customers active in the previous 180 days",
        "train_rows": int(len(train)), "test_rows": int(len(test)),
        "train_snapshot_start": str(pd.to_datetime(train["snapshot_date"]).min().date()),
        "train_snapshot_end": str(pd.to_datetime(train["snapshot_date"]).max().date()),
        "test_snapshot_start": str(pd.to_datetime(test["snapshot_date"]).min().date()),
        "test_snapshot_end": str(pd.to_datetime(test["snapshot_date"]).max().date()),
        "test_churn_prevalence": float(test["churned_240d"].mean()),
        "average_precision": float(average_precision_score(test["churned_240d"], test_prob)),
        "roc_auc": float(roc_auc_score(test["churned_240d"], test_prob)),
        "brier_score": float(brier_score_loss(test["churned_240d"], test_prob)),
        "average_precision_prevalence_baseline": float(test["churned_240d"].mean()),
        "brier_score_prevalence_baseline": float(brier_score_loss(
            test["churned_240d"],
            np.repeat(train["churned_240d"].mean(), len(test)),
        )),
        **_ranking_metrics(test["churned_240d"], test_prob),
        "validation_note": "Chronological snapshot holdout; a customer can appear in multiple dates, so this is not an independent customer-group holdout.",
        "quality_note": "Interpret average precision relative to prevalence. High prevalence with lift@10% close to 1 indicates weak targeting discrimination.",
    }
    estimator.fit(snapshots[FEATURE_COLUMNS], snapshots["churned_240d"])
    score = scoring_features.copy()
    if not score.empty:
        score["p_churn_240d"] = estimator.predict_proba(score[FEATURE_COLUMNS])[:, 1]
        score = score.sort_values("p_churn_240d", ascending=False).reset_index(drop=True)
        score["risk_percentile"] = score["p_churn_240d"].rank(pct=True)
        score["risk_band"] = np.where(score["risk_percentile"] >= 0.90, "High",
                               np.where(score["risk_percentile"] >= 0.70, "Medium", "Lower"))
    directory = Path(model_dir)
    directory.mkdir(parents=True, exist_ok=True)
    joblib.dump(estimator, directory / "churn_model.joblib")
    with (directory / "churn_metrics.json").open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    importance = pd.DataFrame({"feature": FEATURE_COLUMNS,
                               "importance": estimator.named_steps["model"].feature_importances_})
    return score, metrics, importance.sort_values("importance", ascending=False)
