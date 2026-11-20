# Model Evaluation — Olist Run

**Run date:** 2026-11-20  
**Analysis end actually observed:** 2018-08-29 15:00:00  
**Source:** User-supplied Olist public dataset archive

## Evaluation design

- Churn: no delivered purchase in the next 240 days among customers with a delivered purchase in the previous 180 days.
- Snapshot validation: chronological holdout; the final two monthly snapshots are held out.
- Future paid value: separate 90-, 180- and 365-day customer-paid order-value targets.
- 730-day value is not estimated because there is insufficient fully observed follow-up.
- The same customer may occur in multiple historical snapshots, so these are time-based snapshots, not independent customer-group samples.

## Churn model

| Metric | Result |
|---|---:|
| Training snapshots | 114,512 |
| Test snapshots | 54,458 |
| Test dates | 2017-12-01 to 2018-01-01 |
| Churn prevalence in test | 98.27% |
| Average precision | 0.9879 |
| AP prevalence baseline | 0.9827 |
| ROC-AUC | 0.6125 |
| Brier score | 0.0168 |
| Brier prevalence baseline | 0.0170 |
| Precision@10% | 99.16% |
| Recall@10% | 10.09% |
| Lift@10% | 1.009 |

### Churn interpretation

The target is extremely imbalanced: 98.27% of the test snapshots are labeled churned. Average precision is therefore close to the prevalence baseline and should not be presented as strong performance. ROC-AUC of 0.612 and lift@10% of 1.009 show weak ranking separation. The current model is a working technical baseline, **not production-ready for CRM targeting**.

A next iteration should distinguish first-time buyers from demonstrated repeat buyers, examine longer and category-specific purchase cycles, and consider survival/time-to-next-purchase modeling before fixing an operational churn label.

## Future customer-paid value models

The following are future **customer-paid order value** estimates, not profit CLV.

| Horizon | Test rows | Non-zero targets | MAE | Zero-baseline MAE | RMSE | Zero-baseline RMSE | Top-10% value captured | Top-10% lift |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 90 days | 110,083 | 0.77% | 2.73 | 1.22 | 19.97 | 20.00 | 20.52% | 2.05x |
| 180 days | 93,776 | 1.34% | 4.78 | 2.11 | 25.94 | 26.03 | 25.08% | 2.51x |
| 365 days | 16,582 | 2.56% | 8.13 | 4.33 | 39.61 | 39.92 | 23.21% | 2.32x |

### Future value interpretation

The target is sparse because most customers do not place another order within each forecast horizon. Pointwise MAE is worse than a zero-value baseline for all three horizons; R² is close to zero. The top decile does capture more future value than a random 10% slice, but this is only a weak-to-moderate ranking signal and should not be called accurate individual CLV. The 365-day validation uses only one held-out monthly snapshot, so its estimate is especially fragile.

## Business-economics boundary

The Olist archive contains seller-side marketing-qualified leads and closed-deal tables, but not buyer-level campaign spend, customer acquisition cost, or customer-level marketing exposure. CAC, buyer acquisition ROAS, contribution margin, profit CLV, and retention campaign ROI cannot be calculated from the supplied tables. Do not substitute seller lead-generation data for buyer acquisition economics.
