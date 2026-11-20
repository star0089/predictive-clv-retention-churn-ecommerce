"""Observed-horizon future paid-value models (revenue proxy, not profit CLV)."""
from pathlib import Path
import json
import math
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from .churn import FEATURE_COLUMNS, build_features_at_cutoff


def build_value_snapshots(order_level: pd.DataFrame, analysis_end: pd.Timestamp,
                          horizon_days: int, active_lookback_days: int = 180,
                          feature_lookback_days: int = 180) -> pd.DataFrame:
    """Create active-customer snapshots with fully observed future paid-value labels."""
    data = order_level.loc[order_level["order_purchase_timestamp"].le(analysis_end)].copy()
    first_cutoff = data["order_purchase_timestamp"].min() + pd.Timedelta(days=feature_lookback_days)
    last_cutoff = pd.Timestamp(analysis_end) - pd.Timedelta(days=horizon_days)
    cutoffs = pd.date_range(first_cutoff.normalize(), last_cutoff.normalize(), freq="MS")
    rows = []
    for cutoff in cutoffs:
        features = build_features_at_cutoff(data, cutoff, active_lookback_days)
        if features.empty:
            continue
        end = cutoff + pd.Timedelta(days=horizon_days)
        future = data.loc[
            data["order_purchase_timestamp"].gt(cutoff)
            & data["order_purchase_timestamp"].le(end)
        ]
        value = future.groupby("customer_unique_id")["paid_order_value"].sum()
        features[f"future_paid_value_{horizon_days}d"] = (
            features["customer_unique_id"].map(value).fillna(0.0)
        )
        rows.append(features)
    if not rows:
        return pd.DataFrame(columns=["customer_unique_id", "snapshot_date", *FEATURE_COLUMNS,
                                     f"future_paid_value_{horizon_days}d"])
    return pd.concat(rows, ignore_index=True)


def train_clv_horizon(snapshots: pd.DataFrame, scoring_features: pd.DataFrame,
                      horizon_days: int, model_dir: str | Path = "models") -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    target = f"future_paid_value_{horizon_days}d"
    if len(snapshots) < 100 or snapshots[target].nunique() < 2:
        raise ValueError(f"Insufficient observations or target variation for {horizon_days}-day value model.")
    dates = sorted(pd.to_datetime(snapshots["snapshot_date"]).unique())
    if len(dates) < 3:
        raise ValueError(f"At least three historical snapshots are required for {horizon_days}-day value model.")
    test_count = max(1, math.ceil(len(dates) * 0.20))
    test_dates = set(dates[-test_count:])
    train = snapshots[~pd.to_datetime(snapshots["snapshot_date"]).isin(test_dates)]
    test = snapshots[pd.to_datetime(snapshots["snapshot_date"]).isin(test_dates)]
    if train.empty or test.empty:
        raise ValueError(f"Unable to create chronological holdout for {horizon_days}-day value model.")
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("regressor", RandomForestRegressor(
            n_estimators=250, max_depth=12, min_samples_leaf=20,
            n_jobs=-1, random_state=42,
        )),
    ])
    model.fit(train[FEATURE_COLUMNS], train[target])
    test_prediction = np.maximum(model.predict(test[FEATURE_COLUMNS]), 0)
    baseline = np.repeat(float(train[target].median()), len(test))
    r2_value = r2_score(test[target], test_prediction) if len(test) > 1 else None
    metrics = {
        "horizon_days": int(horizon_days),
        "target": target,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "train_snapshot_start": str(pd.to_datetime(train["snapshot_date"]).min().date()),
        "train_snapshot_end": str(pd.to_datetime(train["snapshot_date"]).max().date()),
        "test_snapshot_start": str(pd.to_datetime(test["snapshot_date"]).min().date()),
        "test_snapshot_end": str(pd.to_datetime(test["snapshot_date"]).max().date()),
        "mae": float(mean_absolute_error(test[target], test_prediction)),
        "rmse": float(mean_squared_error(test[target], test_prediction) ** 0.5),
        "r2": float(r2_value) if r2_value is not None and np.isfinite(r2_value) else None,
        "median_baseline_mae": float(mean_absolute_error(test[target], baseline)),
        "interpretation": "Predicted future customer-paid order value; not contribution margin or net profit CLV.",
    }
    model.fit(snapshots[FEATURE_COLUMNS], snapshots[target])
    score = scoring_features[["customer_unique_id", "snapshot_date", *FEATURE_COLUMNS]].copy()
    score[f"predicted_paid_value_{horizon_days}d"] = np.maximum(
        model.predict(score[FEATURE_COLUMNS]), 0
    ) if not score.empty else []
    directory = Path(model_dir)
    directory.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, directory / f"paid_value_model_{horizon_days}d.joblib")
    importance = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": model.named_steps["regressor"].feature_importances_,
        "horizon_days": horizon_days,
    }).sort_values("importance", ascending=False)
    return score[["customer_unique_id", "snapshot_date", f"predicted_paid_value_{horizon_days}d"]], metrics, importance


def run_clv_models(order_level: pd.DataFrame, analysis_end: pd.Timestamp,
                   model_dir: str | Path = "models") -> tuple[pd.DataFrame, list[dict], pd.DataFrame]:
    """Fit 90d/180d/365d paid-value models; 730d is intentionally not estimated."""
    scoring = build_features_at_cutoff(order_level, analysis_end, active_lookback_days=180)
    predictions = scoring[["customer_unique_id", "snapshot_date"]].copy()
    metrics_list = []
    importances = []
    for horizon in (90, 180, 365):
        snapshots = build_value_snapshots(order_level, analysis_end, horizon)
        try:
            result, metrics, importance = train_clv_horizon(
                snapshots, scoring, horizon, model_dir=model_dir
            )
            predictions = predictions.merge(
                result.drop(columns="snapshot_date"), on="customer_unique_id",
                how="left", validate="one_to_one"
            )
            metrics_list.append(metrics)
            importances.append(importance)
        except ValueError as error:
            metrics_list.append({"horizon_days": horizon, "status": "not_trained", "reason": str(error)})
    importance_frame = pd.concat(importances, ignore_index=True) if importances else pd.DataFrame()
    predictions["predicted_paid_value_730d"] = np.nan
    predictions["730d_status"] = "not_estimable_from_available_follow_up"
    return predictions, metrics_list, importance_frame
