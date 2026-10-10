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
- Introduced a working behavioral-retention definition where the second purchase occurs **more than 7 days** after the first.
- Behavioral repeat customers under this rule: **1,900 (~1.98%)**.

### 4. Review data quality
- Found that some orders contain multiple review records.
- Found duplicated `review_id` values even though there are no fully duplicated rows.
- Identified that `review_id` cannot be assumed to be a perfectly unique primary key.
- Working rule for order-level analysis: reduce reviews to one deterministic record per order before joining.

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

## Next Analysis

**First-order review score → probability of a behavioral repeat purchase**

Then:
1. Customer master table
2. RFM segmentation
3. Cohort retention
4. Churn definition
5. Feature engineering
6. Churn prediction
7. Predictive CLV
8. CLV × churn strategy
9. CAC / ROAS / profitability
10. Power BI dashboard
11. Executive recommendations

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
