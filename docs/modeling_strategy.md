# Modeling Strategy

## 1. Customer-level analytics

The analytical grain is one row per customer_unique_id. Delivered orders are the default completed-purchase population. Payment installments are summed to order_id before customer aggregation.

## 2. Churn target

The current project rule is:

- A customer is eligible for scoring if their most recent delivered purchase is within the previous 180 days.
- Churn outcome equals 1 if they make no delivered purchase in the next 240 days after the snapshot date.
- Churn outcome equals 0 if they make at least one delivered purchase in that 240-day period.

This is an inactivity/return definition for a non-contractual marketplace, not subscription cancellation.

Behavioral repeat-gap analysis (>7-day gaps) found:

| Inactivity horizon | Observed eventual repeat gaps within horizon |
|---:|---:|
| 180 days | 74.42% |
| 210 days | 79.96% |
| 240 days | 84.04% |
| 270 days | 87.68% |

240 days is selected as a practical balance: it captures about 84% of observed behavioral repeat gaps while avoiding the additional delay of a 270-day rule. It remains a project assumption to monitor, not a universal churn standard.

## 3. Leakage controls

For every historical snapshot:

- features use only delivered orders on or before the snapshot date;
- customers must have a purchase in the preceding 180 days;
- the target uses purchases strictly after the snapshot date and no later than snapshot + 240 days;
- only snapshots with a complete 240-day follow-up inside the configured analysis end are retained;
- customer IDs, future outcomes and future paid value are never model features.

The current configured analysis end is 2018-08-31 23:59:59 because exploratory work found the Sep-Oct 2018 tail sparse. Recheck completeness before changing it.

## 4. Churn model

The baseline model is an unweighted Random Forest with median imputation. Class weighting was avoided because it distorted probability calibration in this highly imbalanced dataset. Evaluation uses a chronological snapshot holdout and reports average precision, ROC-AUC, Brier score, precision@10%, recall@10% and lift@10%. The evaluation note flags that customers can appear in multiple historical snapshots; this is not a fully independent customer-group holdout.

The scored population is ranked by predicted 240-day churn probability. Risk bands are relative ranks (top 10% High, next 20% Medium), not calibrated business thresholds. In the supplied run, churn prevalence was 98.27%, ROC-AUC was 0.612 and lift@10% was 1.009; the model is not ready for operational targeting.

## 5. Future customer value

Separate resource-bounded Random Forest regressors estimate future customer-paid order value over 90, 180 and 365 days. Training is capped at 30,000 sampled historical snapshots per fit to keep execution practical on ordinary hardware. These are revenue proxies, not contribution-margin CLV. A 730-day estimate is deliberately not produced because the dataset does not provide sufficient reliable follow-up to train and validate a 24-month target.

## 6. Decision support

A simple paid-value-at-risk proxy is calculated as churn probability multiplied by predicted 365-day paid value. This is a prioritization signal, not incremental saved value. True treatment selection requires randomized retention experiments or causal uplift estimation.

## 7. Model governance

- Compare models to simple baselines.
- Track class prevalence and ranking metrics, not accuracy alone.
- Inspect calibration before treating probabilities as literal risk percentages.
- Revalidate after any change to order population, time cutoff, feature windows or churn horizon.
- Do not interpret feature importance as causality.


### Observed value-model diagnostics

In the supplied run, only 0.77%, 1.34% and 2.56% of 90-, 180- and 365-day test targets were non-zero. Pointwise MAE was worse than a zero-value baseline; R² was near zero. Top-decile value capture was 20.52%, 25.08% and 23.21%. Treat the model as an exploratory ranking baseline, not an accurate individual value forecast. The 365-day holdout covers one monthly snapshot only.
