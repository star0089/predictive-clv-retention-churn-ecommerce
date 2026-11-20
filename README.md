# Predictive Customer Lifetime Value, Retention & Churn Intelligence

An end-to-end customer analytics portfolio project built on the **Olist Brazilian E-Commerce Public Dataset**. The project connects customer behavior, retention, churn risk and predicted future customer-paid value, with clear limits around profitability and marketing attribution.

## Project objective

Build a reproducible workflow that answers:

1. Which customers are purchasing and how often?
2. Which customer cohorts return over time?
3. Which active customers are unlikely to purchase again?
4. What customer-paid order value may be generated over future horizons?
5. How should CRM teams prioritize customers while respecting the limits of the available evidence?

## Current verified exploratory findings

These figures are from the earlier hands-on exploratory notebooks. They are not presented as outputs from the newer canonical pipeline, which uses delivered orders only and may produce different counts.

- Persistent customer IDs observed: **96,096**
- More-than-one-order customers: **2,997**
- Exploratory repeat-customer rate: **about 3.12%**
- First-order review association: repeat rate ranged from **1.71% (1-star)** to **2.18% (5-star)**; this is observational, not causal.
- RFM exploratory segments: New / Recent **38,481 (40.04%)**; Lost / Inactive **38,358 (39.92%)**; High Value **7,552 (7.86%)**.
- High Value segment contributed **13.40%** of exploratory customer-paid value.
- Monthly activity retention: Month 1 **0.48%**, Month 2 **0.31%**, Month 3 **0.25%**.
- Comparable Month-1 retention was broadly flat: 2017 about **0.51%**, Jan-Jul 2018 about **0.49%**.

### Working churn definition

Behavioral repeat gaps longer than seven days produced the following observed coverage:

| Inactivity threshold | Behavioral repeat gaps within threshold |
|---:|---:|
| 180 days | 74.42% |
| 210 days | 79.96% |
| 240 days | 84.04% |
| 270 days | 87.68% |

The project uses **240 days** as its working no-return horizon. Customers are eligible for scoring when they purchased within the previous **180 days**. This is a project-specific behavioral definition, not a universal churn standard.

## Actual dataset run — 2026-11-20

The complete pipeline was executed against the Olist archive supplied for this project.

| Measure | Verified result |
|---|---:|
| Delivered orders | **96,478** |
| Persistent customers | **93,358** |
| Customers with multiple delivered orders | **2,801** |
| Repeat-customer rate | **3.00%** |
| RFM segments | **7** |
| Churn training snapshots | **168,970** |
| Active customers scored | **37,559** |

Canonical results use delivered orders and an analysis end of **2018-08-29 15:00:00**, the latest delivered purchase timestamp available before the configured 2018-08-31 cutoff.

### Model validation summary

The churn target has **98.27%** prevalence in the temporal test set. ROC-AUC is **0.612** and lift@10% is **1.009**. The current churn model is not sufficiently discriminative for production retention targeting.

Future paid-value models show some ranking signal: their top 10% capture about **20.5%–25.1%** of future paid value. However, pointwise MAE is worse than a zero-value baseline, and R² is near zero. Treat these models as exploratory ranking baselines, not accurate individual CLV estimates.

See [reports/model_evaluation.md](reports/model_evaluation.md) and [reports/dataset_run_summary.md](reports/dataset_run_summary.md) for complete results.

## Repository structure

```text
predictive-clv-retention-churn-ecommerce/
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_customer_behavior.ipynb
│   ├── 03_rfm_analysis.ipynb
│   ├── 04_retention_analysis.ipynb
│   ├── 05_churn_definition.ipynb
│   ├── 06_feature_engineering.ipynb
│   ├── 07_churn_modeling.ipynb
│   ├── 08_predictive_customer_value.ipynb
│   └── 09_business_economics_and_dashboard.ipynb
├── src/
│   ├── data_loader.py
│   ├── analytics.py
│   ├── churn.py
│   ├── clv.py
│   ├── marketing.py
│   └── pipeline.py
├── tests/
├── docs/
├── reports/
├── dashboard/
│   ├── measures.dax
│   └── report_layout.md
├── run_pipeline.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Quick start (Windows PowerShell)

1. Download the Olist dataset and place its original CSV files in a local folder named data_raw at the repository root. At minimum:

   - olist_customers_dataset.csv
   - olist_orders_dataset.csv
   - olist_order_items_dataset.csv
   - olist_order_payments_dataset.csv

2. Create the environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

3. Run the complete pipeline from the repository root:

```powershell
python run_pipeline.py
```

4. Run automated checks:

```powershell
pytest
```

See [docs/reproducibility.md](docs/reproducibility.md) for details.

## Pipeline outputs

Generated locally in outputs/ (not committed):

- data_quality_report.csv
- customer_master_rfm.csv
- rfm_segment_summary.csv
- cohort_retention.csv
- monthly_kpis.csv
- churn_training_snapshots.csv
- churn_risk_predictions.csv (if model training succeeds)
- future_paid_value_predictions.csv (for successfully trained horizons)
- customer_dashboard.csv
- model metric JSON files

Fitted models are stored in models/ and are also excluded from Git.

## Modeling design

- Completed-purchase population: delivered orders.
- Customer grain: customer_unique_id.
- Payment installments are aggregated to order_id before joining.
- Churn target: no delivered purchase in the next 240 days among customers active in the previous 180 days.
- Churn features use transactions on or before the snapshot date only.
- Churn evaluation uses a chronological snapshot holdout and reports average precision, ROC-AUC, Brier score, precision@10%, recall@10% and lift@10%.
- Future paid-value models target 90, 180 and 365 days separately.
- A 730-day / 24-month value model is intentionally not estimated because reliable follow-up is insufficient.

## Important data limitations

The standard Olist dataset does not provide complete product cost, fulfilment cost, refund/return cost, customer-support cost, campaign spend, customer-level CAC or campaign exposure. Therefore:

- predicted paid value is **not** contribution-margin CLV or profit;
- CAC and ROAS are unavailable unless genuine external marketing data is supplied;
- churn probability × predicted paid value is only a value-at-risk ranking proxy, not expected saved value;
- causal retention impact requires controlled experiments or uplift modeling.

The optional marketing input schema is documented in [docs/limitations.md](docs/limitations.md). Never invent missing business data.

## Documentation

- [Data dictionary](docs/data_dictionary.md)
- [Modeling strategy](docs/modeling_strategy.md)
- [Data and model limitations](docs/limitations.md)
- [Dashboard specification](docs/dashboard_spec.md)
- [Reproducibility guide](docs/reproducibility.md)
- [Project progress log](reports/progress_log.md)

## Project status

The repository contains the end-to-end pipeline, nine practice notebooks, reusable source modules, documentation, dashboard specification, and automated tests. The complete pipeline has been run against the supplied archive and **5 automated tests pass**. Customer-level outputs and fitted models remain local and are not committed. Model weaknesses and unavailable business-economics fields are documented rather than hidden.
