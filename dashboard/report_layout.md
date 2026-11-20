# Power BI Report Layout

## Data model

Import the pipeline CSVs from the local `outputs/` folder:

- `customer_dashboard.csv` — customer-level RFM, churn scores and predicted paid-value estimates.
- `monthly_kpis.csv` — monthly delivered-order and customer-paid-value totals.
- `rfm_segment_summary.csv` — aggregated RFM segment measures.
- `cohort_retention.csv` — cohort-month activity retention.
- `churn_model_metrics.json` and `paid_value_model_metrics.json` — validation metrics; import manually or copy key values into a small manually maintained metrics table.

Use `customer_unique_id` as the customer key. The customer dashboard file is a local generated output and must not be committed to the public repository.

## Page 1 — Executive overview

- KPI cards: delivered orders, customers, repeat-customer rate, customer-paid value.
- Monthly trend: orders, customers and paid value from `monthly_kpis`.
- RFM segment mix and paid-value share.
- Add a visible note that paid value is not contribution margin or profit.

## Page 2 — RFM segments

- Customer count and customer share by RFM segment.
- Paid-value share by segment.
- Average recency, frequency and paid value.
- Detail table filtered by segment.

## Page 3 — Cohort retention

- Matrix: cohort_month by cohort_index, values = retention_pct.
- Label it **monthly purchase activity retention**, not survival probability.
- Hide or distinguish incomplete future periods.

## Page 4 — Churn diagnostics

- Show target definition, test prevalence, ROC-AUC, Brier score and lift@10%.
- Current test prevalence is 98.27%, ROC-AUC 0.612 and lift@10% 1.009.
- Clearly mark the current churn model as **not ready for operational targeting**.
- Relative risk bands are score percentiles, not calibrated business thresholds.

## Page 5 — Future customer-paid value

- Compare predicted 90d, 180d and 365d paid value.
- Show zero-baseline errors and top-decile value capture.
- State that pointwise MAE is worse than the zero baseline.
- Do not display a 730d estimate as zero; it is unavailable.

## Business-economics guardrails

The source does not provide buyer-level marketing spend, CAC, full product costs, fulfilment costs or customer-service costs. Do not label any measure as profit CLV, contribution margin, CAC, ROAS or incremental saved value.
