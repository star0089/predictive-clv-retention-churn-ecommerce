# Power BI Dashboard Specification

The pipeline writes local CSV tables into outputs/. Connect Power BI Desktop to these files after running the pipeline.

## Pages

### 1. Executive overview
- Delivered orders
- Unique customers
- Customer-paid order value
- Average order value
- RFM segment mix
- Predicted churn risk (only when a model is trained)
- Predicted future paid value (90d / 180d / 365d, when models are trained)

### 2. Customer segments
Source: customer_dashboard.csv and rfm_segment_summary.csv
- Customer count and share by RFM segment
- Average recency, frequency and paid value
- Total paid value and paid-value share

### 3. Cohort retention
Source: cohort_retention.csv
- Rows: cohort_month
- Columns: cohort_index
- Values: retention_pct
- Filter by cohort month and follow-up month
- Clearly label this as monthly purchase activity retention, not continuous survival.

### 4. Churn risk
Source: churn_risk_predictions.csv and churn_model_metrics.json
- Risk probability distribution
- High/medium/lower relative rank bands (not calibrated business thresholds)
- Precision@10%, recall@10%, lift@10%, average precision and Brier score
- Show the observed 98.27% churn prevalence and weak ROC-AUC (0.612) / lift@10% (1.009) beside scores; current model is not production-ready
- Never show the risk score without its 240-day target definition.

### 5. Future customer value
Source: future_paid_value_predictions.csv and paid_value_model_metrics.json
- Predicted 90d, 180d and 365d customer-paid value
- Show the zero-value baseline comparison and top-decile value capture; do not imply pointwise forecast accuracy
- Paid value at risk proxy = churn probability × predicted 365d paid value
- 730d / 24-month value is unavailable and must not be visualized as zero.

## Suggested measures

- Delivered Orders = DISTINCTCOUNT(order_id)
- Customers = DISTINCTCOUNT(customer_unique_id)
- Customer Paid Value = SUM(paid_order_value)
- Average Order Value = DIVIDE([Customer Paid Value], [Delivered Orders])
- Customer Share = DIVIDE([Customers in Segment], [All Customers])
- Paid Value Share = DIVIDE([Paid Value in Segment], [Total Paid Value])

## Important dashboard footnote

Olist does not provide full cost, marketing spend, CAC, campaign exposure, support or refund data. Do not label paid value as profit or CLV as contribution margin.
