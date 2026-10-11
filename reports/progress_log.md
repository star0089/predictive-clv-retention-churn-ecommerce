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
- Observed repeat rates from 1.71% for 1-star first orders to 2.18% for 5-star first orders.
- Built the 96,096-row customer master table.
- Started RFM feature engineering and scoring.
- Converted project work into reproducible notebooks and reusable Python helpers.

## Current focus
Finish RFM validation and business segmentation.
