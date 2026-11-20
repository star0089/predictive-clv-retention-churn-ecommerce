# Power BI Dashboard

The Power BI dashboard is the presentation layer for the reproducible Python pipeline. First run the project from the repository root:

    python run_pipeline.py

Then connect Power BI Desktop to the generated CSV files in outputs/.

## Planned report pages

1. Executive customer health: delivered orders, customers, paid order value and RFM mix.
2. Customer segments: recency, frequency, monetary value and segment revenue share.
3. Cohort retention: monthly activity retention by first-purchase cohort.
4. Churn risk: 240-day churn probabilities, relative risk bands and model evaluation.
5. Future value: predicted 90-, 180- and 365-day customer-paid order value.

The 730-day/24-month value is unavailable. Olist does not provide full COGS, refunds, fulfilment cost, support cost, CAC, marketing spend or campaign exposures. Do not label paid order value as profit or contribution-margin CLV.
