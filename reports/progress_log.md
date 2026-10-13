# Project Progress Log

## 2026-10-10
- Established data-model relationships and customer grain.
- Corrected order timestamp parsing.
- Investigated missing lifecycle timestamps.
- Measured naive repeat behavior and first-to-second purchase gaps.
- Identified same-session repeat-order behavior.
- Investigated review-table key/cardinality issues.

## 2026-10-11
- Built a right-censoring-aware repeat-after-7-days target.
- Completed first-order review vs repeat-purchase analysis.
- Built the 96,096-row customer master table.
- Started RFM feature engineering and scoring.
- Converted project work into reproducible notebooks and reusable Python helpers.

## 2026-10-13
- Completed RFM scoring, segmentation, and segment revenue analysis.
- New / Recent Customers: 38,481 (40.04%); Lost / Inactive: 38,358 (39.92%).
- High Value customers: 7,552 (7.86%) and 13.40% of revenue.
- Completed cohort retention analysis.
- Average Month-1 retention: 0.48%; Month-2: 0.31%; Month-3: 0.25%.
- Corrected the 2018 retention comparison for incomplete end-of-dataset cohorts; comparable Month-1 retention is broadly flat versus 2017.
- Started churn-definition analysis from inter-purchase gaps.
- 60/90/120/180-day thresholds capture 62.87% / 69.63% / 75.43% / 83.86% of observed repeat gaps.
- 180 days is the current working churn threshold, pending behavioral-gap validation and leakage-safe label design.

## Current focus
Validate the 180-day threshold using gaps greater than 7 days, then define observation and prediction windows.
