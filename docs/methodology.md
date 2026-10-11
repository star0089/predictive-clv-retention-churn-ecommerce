# Methodology Notes

This document records analytical decisions made during hands-on project work.

## Customer grain
The persistent customer identifier is `customer_unique_id`. Transaction-level analysis uses `order_id`, while customer-level retention, RFM and CLV use one row per `customer_unique_id`.

## Behavioral repeat definition
A naive repeat customer is anyone with more than one order. Because many second purchases occur within hours of the first order, the working behavioral definition is stricter:

> A behavioral repeat customer has any later purchase more than 7 days after the first purchase.

This is a project rule for analysis, not a universal definition of retention.

## Right-censoring
Customers whose first purchase occurs too close to the dataset end are not given enough opportunity to return. These customers are excluded from short-horizon repeat targets.

## Reviews
The review table does not behave like a perfect one-review-per-order table. Some orders have multiple review rows, and `review_id` is not perfectly unique. For order-level analysis, the project uses the latest `review_answer_timestamp` as a deterministic reduction rule.

## Causality caution
Observed differences in repeat rates by review score are associations. Product category, seller quality, delivery experience, price, customer need and other variables may confound the relationship.

## RFM scoring
Recency and Monetary are scored using quantile-based bins. Frequency is scored with business rules because the distribution is extremely concentrated at one order.
