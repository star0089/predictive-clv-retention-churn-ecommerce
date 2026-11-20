# Dataset Run Summary

**Run date:** 2026-11-20  
**Source:** Olist Brazilian E-Commerce Public Dataset supplied as data_raw.zip

## Canonical analysis population

| Measure | Result |
|---|---:|
| Raw orders in source | 99,441 |
| Delivered orders through analysis end | 96,478 |
| Persistent customers | 93,358 |
| Customers with more than one delivered order | 2,801 |
| Repeat-customer rate | 3.00% |
| First included delivered purchase | 2016-09-15 12:16:00 |
| Last included delivered purchase | 2018-08-29 15:00:00 |

The pipeline uses delivered orders as completed purchases, aggregates payment installments to order_id, and groups customers by customer_unique_id. The analysis end is the latest delivered purchase timestamp actually present before the configured 2018-08-31 cutoff.

## Source tables

The loader reads the core order/customer/payment/item tables and available review, product, seller, category translation, marketing-qualified-lead and closed-deal tables. It drops four blank Unnamed export columns from order_items. The large geolocation file is not loaded because geographic mapping is outside the current CLV/retention scope.

See data_quality_report.csv for table-level row counts, missing cells and duplicate full rows.

## RFM segments

| Segment | Customers | Customer share | Paid-value share |
|---|---:|---:|---:|
| Lost / Inactive | 37,272 | 39.92% | 39.84% |
| New / Recent Customers | 37,222 | 39.87% | 40.59% |
| Regular Customers | 11,256 | 12.06% | 5.27% |
| High Value | 7,380 | 7.91% | 13.55% |
| Loyal Customers | 125 | 0.13% | 0.37% |
| At Risk | 71 | 0.08% | 0.20% |
| Champions | 32 | 0.03% | 0.18% |

RFM paid value is based on aggregated customer payment value. It is not contribution margin or profit.

## Cohort retention

For cohorts with at least 100 customers and an observed month-1 period:
- 2017: 12 cohorts; mean month-1 purchase activity retention 0.491%.
- 2018: 7 cohorts; mean month-1 purchase activity retention 0.449%.

Cohort retention measures monthly purchase activity, not continuous survival. A customer can skip a month and return later.
