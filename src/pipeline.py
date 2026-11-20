"""End-to-end Olist customer analytics pipeline."""
from pathlib import Path
import json
import pandas as pd
from .data_loader import load_olist_data, build_data_quality_report
from .analytics import (prepare_order_level, build_customer_master, add_rfm_scores,
                        build_rfm_segment_summary, build_cohort_retention)
from .churn import build_features_at_cutoff, build_churn_snapshots, train_and_score_churn
from .clv import run_clv_models
from .marketing import build_channel_economics


def run_pipeline(data_dir: str = "data_raw", output_dir: str = "outputs",
                 model_dir: str = "models", analysis_end: str = "2018-08-31 23:59:59") -> dict:
    """Run analytics and write outputs locally; no model result is fabricated.

    The default analysis end excludes the sparse Sep-Oct 2018 tail observed during
    exploratory work. Change it only after checking data completeness.
    """
    root = Path(data_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    data = load_olist_data(root)
    quality = build_data_quality_report(data)
    order_level = prepare_order_level(data)
    observed_end = order_level["order_purchase_timestamp"].max()
    end = min(observed_end, pd.Timestamp(analysis_end))
    order_level = order_level.loc[order_level["order_purchase_timestamp"].le(end)].copy()
    if order_level.empty:
        raise ValueError("No delivered order records remain after applying analysis_end.")

    customer_master = build_customer_master(order_level)
    customer_master_rfm = add_rfm_scores(customer_master)
    segment_summary = build_rfm_segment_summary(customer_master_rfm)
    cohort_retention = build_cohort_retention(order_level)
    monthly_kpis = (
        order_level.assign(order_month=order_level["order_purchase_timestamp"].dt.to_period("M").astype(str))
        .groupby("order_month")
        .agg(orders=("order_id", "nunique"), customers=("customer_unique_id", "nunique"),
             paid_order_value=("paid_order_value", "sum"))
        .reset_index()
    )
    quality.to_csv(output / "data_quality_report.csv", index=False)
    customer_master_rfm.to_csv(output / "customer_master_rfm.csv", index=False)
    segment_summary.to_csv(output / "rfm_segment_summary.csv", index=False)
    cohort_retention.to_csv(output / "cohort_retention.csv", index=False)
    monthly_kpis.to_csv(output / "monthly_kpis.csv", index=False)

    statuses = {}
    churn_predictions = pd.DataFrame(columns=["customer_unique_id", "p_churn_240d", "risk_band"])
    try:
        churn_snapshots = build_churn_snapshots(order_level, end, horizon_days=240)
        churn_snapshots.to_csv(output / "churn_training_snapshots.csv", index=False)
        scoring_features = build_features_at_cutoff(order_level, end, active_lookback_days=180)
        churn_predictions, churn_metrics, churn_importance = train_and_score_churn(
            churn_snapshots, scoring_features, model_dir=model_dir
        )
        churn_predictions.to_csv(output / "churn_risk_predictions.csv", index=False)
        churn_importance.to_csv(output / "churn_feature_importance.csv", index=False)
        with (output / "churn_model_metrics.json").open("w", encoding="utf-8") as handle:
            json.dump(churn_metrics, handle, indent=2)
        statuses["churn_model"] = {"status": "trained", **churn_metrics}
    except (ValueError, KeyError) as error:
        statuses["churn_model"] = {"status": "not_trained", "reason": str(error)}

    clv_predictions = pd.DataFrame(columns=["customer_unique_id"])
    try:
        clv_predictions, clv_metrics, clv_importance = run_clv_models(
            order_level, end, model_dir=model_dir
        )
        clv_predictions.to_csv(output / "future_paid_value_predictions.csv", index=False)
        if not clv_importance.empty:
            clv_importance.to_csv(output / "paid_value_feature_importance.csv", index=False)
        with (output / "paid_value_model_metrics.json").open("w", encoding="utf-8") as handle:
            json.dump(clv_metrics, handle, indent=2)
        statuses["future_paid_value_models"] = clv_metrics
    except (ValueError, KeyError) as error:
        statuses["future_paid_value_models"] = {"status": "not_trained", "reason": str(error)}

    dashboard = customer_master_rfm.copy()
    if not churn_predictions.empty and "p_churn_240d" in churn_predictions:
        dashboard = dashboard.merge(
            churn_predictions[["customer_unique_id", "p_churn_240d", "risk_band"]],
            on="customer_unique_id", how="left", validate="one_to_one"
        )
    if not clv_predictions.empty:
        dashboard = dashboard.merge(
            clv_predictions.drop(columns=["snapshot_date"], errors="ignore"),
            on="customer_unique_id", how="left", validate="one_to_one"
        )
    if "p_churn_240d" in dashboard and "predicted_paid_value_365d" in dashboard:
        dashboard["paid_value_at_risk_365d_proxy"] = (
            dashboard["p_churn_240d"] * dashboard["predicted_paid_value_365d"]
        )
    dashboard.to_csv(output / "customer_dashboard.csv", index=False)

    marketing_path = root / "marketing_spend.csv"
    acquisition_path = root / "customer_acquisition.csv"
    if marketing_path.exists() and acquisition_path.exists():
        marketing_metrics = build_channel_economics(
            pd.read_csv(marketing_path), pd.read_csv(acquisition_path)
        )
        marketing_metrics.to_csv(output / "channel_economics.csv", index=False)
        statuses["marketing_economics"] = {"status": "calculated_from_user_supplied_files"}
    else:
        statuses["marketing_economics"] = {
            "status": "unavailable",
            "reason": "Olist does not include campaign spend or customer acquisition cost. Supply both optional files using docs/limitations.md schema before calculating CAC or ROAS.",
        }

    summary = {
        "analysis_end": str(end),
        "delivered_orders": int(order_level["order_id"].nunique()),
        "unique_customers": int(customer_master_rfm["customer_unique_id"].nunique()),
        "rfm_segments": int(customer_master_rfm["RFM_segment"].nunique()),
        "churn_horizon_days": 240,
        "active_lookback_days": 180,
        "paid_value_horizons_days": [90, 180, 365],
        "24_month_value_status": "not_estimable_from_available_follow_up",
        "business_value_warning": "Paid order value is not contribution margin, profit or fully adjusted CLV.",
        "model_status": statuses,
    }
    with (output / "pipeline_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, default=str)
    return summary
