# Predictive CLV, Retention & Churn Intelligence

Portfolio data science project using the Olist Brazilian E-Commerce dataset to study customer behavior, retention, churn, customer lifetime value (CLV), and profitability.

## Project Objective

Build an end-to-end customer analytics system that connects:

**Customer acquisition → purchase behavior → retention → churn → CLV → profitability**

The project is designed as a realistic business case rather than only a machine-learning exercise.

## Current Progress

### 1. Data understanding
- Identified the main Olist tables and their relationships.
- Distinguished `customer_id` from `customer_unique_id`.
- Established `customer_unique_id` as the persistent customer identity for retention, RFM, and CLV analysis.

### 2. Order data quality
- Validated order-status distributions.
- Corrected timestamp parsing using the source `DD-MM-YYYY HH:MM` format.
- Investigated missing approval and delivery timestamps instead of blindly dropping records.
- Identified lifecycle anomalies such as delivered orders with missing delivery timestamps.
- Established a working usable analysis period of roughly Jan 2017–Aug 2018 because the dataset edges are sparse/incomplete.

### 3. Repeat purchase behavior
- Total unique customers: **96,096**
- Customers with more than one order: **2,997**
- Naive repeat-customer rate: **~3.12%**
- Found that a large share of second purchases happen within the same hour/day.
- Introduced a working behavioral-retention definition where a customer makes **any later purchase more than 7 days after the first purchase**.
- Earlier second-order-only analysis identified **1,900 (~1.98%)** customers returning after 7 days; the project now uses the more robust any-later-purchase definition for retention targets.

### 4. Review data quality
- Found that some orders contain multiple review records.
- Found duplicated `review_id` values even though there are no fully duplicated rows.
- Identified that `review_id` cannot be assumed to be a perfectly unique primary key.
- Working rule for order-level analysis: keep one deterministic review record per order using the latest `review_answer_timestamp`.

### 5. First-order review vs repeat purchase
A right-censoring-aware target was built to test whether first-order review score is associated with returning after 7 days.

| First-order review | Customers | Repeat customers | Repeat rate |
|---:|---:|---:|---:|
| 1★ | 10,994 | 188 | 1.71% |
| 2★ | 3,035 | 57 | 1.88% |
| 3★ | 7,856 | 144 | 1.83% |
| 4★ | 18,497 | 352 | 1.90% |
| 5★ | 54,977 | 1,197 | 2.18% |

**Finding:** 5-star first-order customers show the highest observed repeat rate. The relationship is positive but weak and not strictly monotonic, so this is treated as an association rather than a causal effect.

### 6. Customer master table
A customer-level analytical table has been created with **96,096 rows**, where:

> **1 row = 1 unique customer**

Current features:
- first purchase
- last purchase
- order frequency
- monetary value
- customer lifetime in days

RFM feature construction is now in progress.

## Important Analytical Concepts Learned

- Data grain
- Primary and foreign keys
- Join cardinality and row multiplication
- Missingness vs true zero
- Right-censoring
- Operational repeat vs behavioral repeat
- Feature/predictor vs target/outcome
- Data leakage
- Confounding
- Association vs causation
- Aggregate-before-comparing logic
- Key reliability
- Deterministic deduplication rules

## Roadmap

1. Complete RFM scoring and segmentation
2. Cohort retention analysis
3. Define churn observation and prediction windows
4. Feature engineering
5. Churn prediction
6. Predictive CLV
7. CLV × churn customer strategy
8. CAC / ROAS / profitability
9. Power BI dashboard
10. Executive recommendations

## Planned Repository Structure

```text
predictive-clv-retention-churn-ecommerce/
├── notebooks/
├── src/
├── docs/
├── reports/
├── dashboard/
├── .gitignore
├── README.md
└── requirements.txt
```

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- SQL
- Scikit-learn
- Power BI
- Jupyter Notebook

## Dataset

Olist Brazilian E-Commerce Public Dataset.

Raw data files are intentionally not committed to this repository. The repository will contain analysis notebooks, reusable code, documentation, and final outputs.
