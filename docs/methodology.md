# Methodology Notes

This document records the analytical decisions used by the reproducible Olist workflow and distinguishes them from earlier exploratory calculations.

## Customer identity and grain

- order_id is the transaction key.
- customer_id links an order to the Olist customer record.
- customer_unique_id is the persistent customer identifier used for customer-level RFM, retention, churn and future-value work.
- Payment installments are aggregated to order_id before joining to orders.
- The canonical pipeline uses delivered orders as completed purchases. Earlier exploratory notebooks included broader order statuses, so historical counts can differ.

## Financial measure

The sum of order payment_value is called paid_order_value. It is customer-paid order value, not net revenue, gross profit, contribution margin or profit CLV. Freight paid by the customer is not the same as the marketplace's freight cost.

## Behavioral repeat definition

The exploratory analysis found that many repeat orders occurred within hours or the same day. The working behavioral repeat rule is any later purchase more than seven days after the first purchase. This is a project rule, not a universal retention definition.

## Right-censoring

Customers acquired near the dataset end have less opportunity to return. Short-horizon repeat labels and cohort comparisons must exclude incomplete follow-up periods. The default pipeline analysis end is 2018-08-31 23:59:59 because the Sep-Oct 2018 tail was sparse in exploratory monthly counts.

## Reviews and causality

Some orders have multiple review records, and review_id is not a perfectly unique key. For order-level exploratory analysis, the latest review_answer_timestamp is retained as a deterministic reduction rule. Review-score differences in repeat rates are associations, not causal effects.

## RFM scoring

Recency and Monetary are divided into five ranked quantile bands. Frequency uses business rules because the distribution is extremely concentrated at one order. Segment names are rule-based and should be treated as analytical labels rather than universal definitions.

## Cohort retention

Cohorts are based on first delivered-purchase month in the canonical pipeline. The matrix measures monthly purchase activity, not continuous survival. A customer may skip a month and return later, so a later month can show higher activity than an earlier month.

## Churn target

The selected working inactivity horizon is 240 days. Among behavioral repeat gaps longer than seven days, 240 days contains 84.04% of observed repeat gaps. The scoring population is customers with a delivered purchase in the previous 180 days.

For a snapshot date:
- features use delivered orders on or before the snapshot;
- churned_240d = 1 if there is no delivered purchase in the next 240 days;
- churned_240d = 0 if at least one delivered purchase occurs in that future window;
- only snapshots with complete follow-up inside the analysis end are used.

## Predictive customer value

The model targets future customer-paid order value over 90, 180 and 365 days. A 730-day target is not estimated because the dataset does not contain enough reliable follow-up to train and validate a 24-month outcome. This is not contribution-margin CLV.

## Marketing and intervention economics

CAC and ROAS require genuine campaign spend and acquisition data. The Olist dataset does not provide these inputs. Churn probability multiplied by predicted future paid value is a value-at-risk ranking proxy, not expected saved value. Treatment effectiveness requires randomized experiments or uplift modeling.
