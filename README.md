# Predictive CLV, Retention & Churn Intelligence

Portfolio data science project using the Olist Brazilian E-Commerce dataset.

## Current verified progress

- Unique customers: **96,096**
- Naive repeat rate: **~3.12%**
- First-order review repeat rate: **1.71% (1★)** to **2.18% (5★)**; association only
- RFM segmentation: **completed**
- Cohort retention analysis: **completed**
- Churn definition: **in progress**

### RFM highlights
- New / Recent Customers: **38,481 (40.04%)**
- Lost / Inactive: **38,358 (39.92%)**
- High Value: **7,552 (7.86%)**, contributing **13.40% of revenue**
- Champions: **34**, avg frequency **4.97**, avg monetary **851.88**

### Cohort retention highlights
Average monthly activity retention:
- Month 1: **0.48%**
- Month 2: **0.31%**
- Month 3: **0.25%**
- Later months: generally around **0.2–0.3%**

Comparable Month-1 retention is broadly flat between 2017 and 2018 after accounting for incomplete end-of-dataset cohorts.

### Churn-definition work
Observed repeat-purchase gaps:
- Median: **28 days**
- 75th percentile: **119 days**
- 80th percentile: **151 days**
- 90th percentile: **241 days**

Candidate inactivity thresholds capture:
- 60 days: **62.87%**
- 90 days: **69.63%**
- 120 days: **75.43%**
- 180 days: **83.86%**

**Working churn threshold: 180 days**, pending validation on behavioral repeat gaps (>7 days) and a leakage-safe observation/prediction-window design.

## Repository structure

```text
notebooks/
  01_data_understanding.ipynb
  02_customer_behavior.ipynb
  03_rfm_analysis.ipynb
  04_retention_analysis.ipynb
  05_churn_definition.ipynb
src/
docs/
reports/
dashboard/
.gitignore
README.md
requirements.txt
```

## Next
1. Finalize churn definition
2. Feature engineering
3. Churn prediction
4. Predictive CLV
5. CLV × churn strategy
6. Profitability / CAC / ROAS
7. Power BI
8. Executive recommendations

Raw datasets, secrets, caches, checkpoints, and temporary files are intentionally excluded.
