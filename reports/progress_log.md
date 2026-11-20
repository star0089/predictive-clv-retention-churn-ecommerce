# Project Progress Log

## 2026-10-10 — Data understanding
- Established the Olist data relationships and customer grain.
- Corrected order timestamp parsing after inspecting the source date format.
- Investigated missing order lifecycle timestamps.
- Measured naive repeat behavior and first-to-second purchase gaps.
- Identified same-day / very short repeat orders as potentially belonging to the same shopping episode.
- Investigated review-table key and cardinality issues.

## 2026-10-11 — Customer behavior and RFM
- Built a right-censoring-aware repeat-after-7-days target.
- Completed first-order review score vs repeat-purchase analysis.
- Observed first-order review repeat rates from 1.71% (1-star) to 2.18% (5-star); interpreted as association only.
- Built a 96,096-row exploratory customer master.
- Completed exploratory RFM scoring and business segmentation.
- Identified 38,481 New / Recent customers (40.04%) and 38,358 Lost / Inactive customers (39.92%).
- High Value customers were 7.86% of customers and contributed 13.40% of exploratory paid value.

## 2026-10-13 — Cohort retention
- Completed monthly cohort-retention matrix and month-index analysis.
- Observed average Month-1 retention of 0.48%, Month-2 0.31%, Month-3 0.25%.
- Corrected the 2018 comparison for incomplete end-of-dataset cohorts; comparable Month-1 retention was broadly flat.

## 2026-10-14 — Churn definition
- Examined 3,345 raw inter-purchase gaps; median gap 28 days.
- Removed gaps of seven days or less for behavioral threshold selection.
- Behavioral repeat-gap count: 2,111; median 83 days; 75th percentile 183.5 days; 80th percentile 211 days.
- Threshold coverage: 180d 74.42%, 210d 79.96%, 240d 84.04%, 270d 87.68%.
- Selected 240 days as the working no-return horizon and 180 days as the active-customer lookback.

## 2026-11-20 — End-to-end implementation build
- Inspected the connected repository and preserved the existing exploratory notebooks and findings.
- Added reusable data loading, customer analytics, churn, future paid-value, optional marketing and pipeline modules.
- Added a root-level pipeline runner, project packaging configuration and automated tests.
- Added feature engineering, churn modeling, predictive customer value and dashboard practice notebooks.
- Added data dictionary, modeling strategy, limitations, dashboard specification and reproducibility documentation.
- Updated the README to distinguish exploratory findings from canonical delivered-order pipeline outputs.
- Added an explicit 240-day churn target and 180-day active lookback to the modeling workflow.
- Added 90-, 180- and 365-day future customer-paid-value modeling; 730-day value remains unavailable due to insufficient reliable follow-up.
- Raw datasets, generated outputs and fitted models remain excluded from Git.

## Validation status
The repository implementation has been authored but has **not yet been run end-to-end against the user's local Olist CSV files**. No pipeline metrics, model scores or generated customer outputs are claimed until that run succeeds.
