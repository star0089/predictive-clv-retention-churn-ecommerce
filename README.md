# Predictive CLV, Retention & Churn Intelligence

An Olist e-commerce customer analytics portfolio investigating repeat purchasing and the decisions that could eventually support retention and customer value.

**Status:** Documentation foundation; exploratory findings reported by the author. Analysis code and reproducible outputs are not yet committed.

## Business objective

Acquiring customers creates value only when their subsequent purchases justify the investment. This project aims to connect purchasing behavior, customer experience, retention, churn risk and customer lifetime value.

The Olist Brazilian E-Commerce Public Dataset provides historical marketplace transactions. It does not provide a complete acquisition-cost or profit model. Customer acquisition channels, CAC, ROAS and true profitability cannot be calculated from the current evidence.

Key questions:
- How often do customers return after their first order?
- Is first-order review score associated with a later repeat purchase?
- Which customer segments might merit retention investment?
- How should observation windows shape churn and CLV definitions?

These are investigation questions, not completed business recommendations.

## Reported exploratory findings

The original README is the source of the following figures. **None has been independently reproduced from committed code or data.**

| Metric | Reported value | Working definition | Qualification |
| --- | ---: | --- | --- |
| Unique customers | 96,096 | Persistent identity: `customer_unique_id` | Exact filters and denominator need executable documentation |
| Customers with multiple orders | 2,997 | More than one order | May include closely spaced orders |
| Naive repeat rate | ~3.12% | 2,997 / 96,096 | Descriptive; unequal follow-up time |
| Behavioral repeat customers | 1,900 | Second purchase more than seven days after first | Working threshold; not a validated churn definition |
| Behavioral repeat rate | ~1.98% | 1,900 / 96,096 | Sensitive to observation window and threshold |

The author also reports lifecycle timestamp anomalies, missing timestamps, multiple reviews per order and duplicated review IDs. Counts and examples are not yet committed.

## Analytical decisions

- Use `customer_unique_id` for persistent customer identity; `customer_id` is an order-linked identifier.
- Investigate missing timestamps against order status before excluding records.
- Reduce reviews to one deterministic record per order before joining; the precise selection rule still needs to be recorded.
- Validate join cardinality to prevent row multiplication.
- Separate closely spaced orders from the working seven-day behavioral repeat definition.
- Account for right-censoring: customers acquired near the dataset end have less opportunity to return.
- Avoid using information recorded after a prediction cutoff as a predictor.

See [methodology and decisions](docs/methodology.md) and [limitations](docs/limitations.md).

## Delivery status and roadmap

| Phase | Status | Evidence / next deliverable |
| --- | --- | --- |
| Data understanding and quality exploration | Reported; not reproducible here | Original README notes; upload the existing exploratory notebook |
| Repeat-purchase exploration | Reported; not reproducible here | Figures above; document filters and reproduce counts |
| First-order reviews vs behavioral repeat | Next planned analysis | Customer-level table, fixed follow-up window, group counts and uncertainty |
| Customer master, RFM and cohort retention | Planned | Explicit grain, cardinality checks and censoring rules |
| Churn definition and features | Planned | Business horizon, eligible population and time cutoffs |
| Churn prediction and predictive CLV | Planned | Baselines, temporal evaluation and stated assumptions |
| SQL, Power BI and recommendations | Planned | Evidence-backed outputs after analysis is available |

No predictive model, dashboard or measured intervention impact is currently available in this repository.

## Repository guide

| File | Purpose |
| --- | --- |
| [data/README.md](data/README.md) | Dataset acquisition, expected files and licensing checks |
| [docs/business_problem.md](docs/business_problem.md) | Business concepts and decision scope |
| [docs/methodology.md](docs/methodology.md) | Working definitions and next-analysis specification |
| [docs/limitations.md](docs/limitations.md) | Evidence and measurement boundaries |
| [docs/repository_audit.md](docs/repository_audit.md) | Baseline audit, priorities, scores and validation |
| [.gitignore](.gitignore) | Exclude local data, environments and notebook checkpoints |

## Reproducibility and technology

This repository currently contains Markdown documentation only. No executable pipeline, notebook, dependency specification or supported Python version has been established.

Python, pandas, NumPy, Matplotlib and Jupyter were listed in the original README, but their use cannot be verified from committed artifacts. SQL, scikit-learn and Power BI are planned, not demonstrated.

To inspect the project:

```bash
git clone https://github.com/star0089/predictive-clv-retention-churn-ecommerce.git
cd predictive-clv-retention-churn-ecommerce
```

Follow [dataset instructions](data/README.md). Execution commands and dependencies will be added with the first runnable analysis. Do not interpret downloading the data as reproducing the reported findings.

## Limitations

Historical marketplace transactions do not establish causality, permanent customer loss or true profit. The seven-day threshold is provisional. Late-acquired customers are right-censored, and timestamp formats must be checked against the actual source export. See [full limitations](docs/limitations.md).

## Author

**Mahesh Vyas** — B.Tech, Artificial Intelligence & Data Science  
Career focus: Data Analytics · Business Intelligence · Data Science

[LinkedIn](https://www.linkedin.com/in/data-mahesh/) · [GitHub](https://github.com/star0089)
