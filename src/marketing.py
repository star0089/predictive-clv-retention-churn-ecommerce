"""Optional channel economics for externally supplied campaign/acquisition data."""
import pandas as pd


def build_channel_economics(marketing_spend: pd.DataFrame,
                            customer_acquisition: pd.DataFrame) -> pd.DataFrame:
    """Calculate CAC and ROAS only when the user supplies actual source data.

    marketing_spend columns: channel, spend, attributed_revenue
    customer_acquisition columns: customer_unique_id, acquisition_channel
    """
    spend_required = {"channel", "spend", "attributed_revenue"}
    acquisition_required = {"customer_unique_id", "acquisition_channel"}
    if not spend_required.issubset(marketing_spend.columns):
        raise ValueError(f"marketing_spend must contain {sorted(spend_required)}")
    if not acquisition_required.issubset(customer_acquisition.columns):
        raise ValueError(f"customer_acquisition must contain {sorted(acquisition_required)}")
    spend = marketing_spend.groupby("channel").agg(
        spend=("spend", "sum"), attributed_revenue=("attributed_revenue", "sum")
    ).reset_index()
    acquired = customer_acquisition.groupby("acquisition_channel")["customer_unique_id"].nunique()
    spend["new_customers"] = spend["channel"].map(acquired).fillna(0).astype(int)
    spend["cac"] = spend["spend"].div(spend["new_customers"].where(spend["new_customers"].gt(0)))
    spend["roas"] = spend["attributed_revenue"].div(spend["spend"].where(spend["spend"].gt(0)))
    return spend.sort_values("spend", ascending=False).reset_index(drop=True)
