# Methodology and analytical decisions

## Evidence status

Existing exploration is reported in the original README. There are no notebooks, source files or dataset outputs to reproduce it. The procedures below are specifications for future implementation, not completed checks.

## Working definitions to preserve

- Persistent customer identity: `customer_unique_id`.
- Naive repeat: customer has more than one order.
- Behavioral repeat: the second purchase occurs **more than seven days** after the first.
- Working analysis period reported previously: roughly January 2017–August 2018. Exact boundaries and inclusion criteria remain unresolved.
- One review per order is required for an order-level join. No tie-breaking rule is yet committed.

Changing any definition must be documented and accompanied by a comparison to the original figures. The original behavioral definition concerns the second order; it is not equivalent to any later purchase beyond seven days.

## Next analysis: first-order review and repeat purchasing

1. Establish one row per order and validate unique order IDs. Map customers with a many-to-one join and check for unmatched records.
2. Specify eligible order statuses, timestamp handling and the exact analysis window.
3. Sort orders per persistent customer by purchase timestamp with a deterministic tie-breaker. Retain first and second purchase times.
4. Investigate duplicate reviews. Choose and document a deterministic per-order selection rule before joining; report missing-review coverage.
5. Select a fixed follow-up horizon before comparing groups. Require enough observation time after the first order; exclude or separately describe censored customers.
6. Construct the seven-day repeat indicator within that horizon. Report the horizon-qualified population separately from historical README counts.
7. Compare first-order review groups using customer counts, repeat counts, rates and uncertainty. Describe missing reviews separately.
8. Consider cohort, timing and delivery-experience differences. Describe associations rather than causal effects.

For a future prediction task, review availability must precede the prediction cutoff. A review submitted after the repeat purchase cannot be used as a pre-purchase predictor. Any review-landmark design changes the eligible population and must be explicit.

## Reproducible delivery requirements

Commit the actual exploratory notebook, relative data paths, dependencies and a supported Python version. Preserve original calculations before extracting reusable functions. Add tests for implemented customer identity, threshold boundaries and cardinality handling when that logic exists.

For modeling, define features and labels using separate time windows; compare a baseline with temporal holdout evaluation. Metrics, imbalance treatment, calibration and CLV assumptions must follow the business objective rather than presentation goals.
