# Reproducibility Guide

## 1. Place the Olist CSV files

Download the Olist Brazilian E-Commerce Public Dataset and place the original CSV files in a local folder named data_raw at the repository root. At minimum, provide:

- olist_customers_dataset.csv
- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv

Optional product, seller, review and category-translation files can be added for later analyses.

## 2. Create an environment

Windows PowerShell:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -e ".[dev]"

## 3. Run the pipeline

From the repository root:

    python run_pipeline.py

Optional arguments:

    python run_pipeline.py --data-dir data_raw --output-dir outputs --model-dir models --analysis-end "2018-08-31 23:59:59"

The default analysis end avoids the sparse Sep-Oct 2018 tail observed during exploratory analysis. Change it only after checking completeness.

## 4. Review outputs

Generated local artifacts are written to outputs/ and models/. They are ignored by Git and are not committed:

- data_quality_report.csv
- customer_master_rfm.csv
- rfm_segment_summary.csv
- cohort_retention.csv
- monthly_kpis.csv
- churn_training_snapshots.csv
- churn_risk_predictions.csv (if model training succeeds)
- future_paid_value_predictions.csv (if value models train)
- customer_dashboard.csv
- model metric JSON files

## 5. Run tests

    pytest

The repository does not include raw data or fabricated model outputs. Model metrics are generated only after the pipeline is run against the actual local dataset.
