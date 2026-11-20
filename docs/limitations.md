# Data and Model Limitations

## Source coverage

The project uses Olist public marketplace data with order history primarily spanning 2016–2018. The late 2018 tail was sparse in exploratory monthly counts; the default analysis end is 2018-08-31.

## Missing business economics

The source does not provide complete COGS, platform fulfilment costs, returns-processing costs, customer-support costs, marketing spend, customer-level CAC, campaign exposure or attribution. Therefore the project cannot truthfully claim contribution margin, true profit CLV, CAC, ROAS, campaign ROI or retention uplift from Olist alone.

## Optional external marketing inputs

If genuine external data is obtained, the optional pipeline inputs are:

- marketing_spend.csv: channel, spend, attributed_revenue
- customer_acquisition.csv: customer_unique_id, acquisition_channel

These files are not part of Olist. Use only traceable, real records. CAC is calculated as channel spend divided by distinct acquired customers; ROAS is attributed revenue divided by spend. These metrics remain attribution-dependent and should not be treated as causal incrementality.

## Value terminology

The models predict future customer-paid order value over observed horizons. This is not net revenue, gross margin, contribution margin or profit. Dashboard labels must retain the term paid value unless cost data is added.

## Long-horizon CLV

A 24-month outcome cannot be properly trained and held out with the available history. The pipeline estimates 90-, 180- and 365-day paid value only when there are enough complete snapshots. The 730-day field is explicitly left unavailable.

## Churn definition

The 240-day inactivity rule is based on observed repeat gaps longer than seven days. It is a pragmatic behavioral definition for this dataset. It does not prove that a customer is permanently lost; some buyers return after longer gaps.

## Observational analysis

Review score, purchase frequency, recency and spend are observational. Correlation does not establish causation. Customer identity resolution is limited to the provided customer_unique_id and cannot guarantee household/person-level deduplication.

## Model evaluation

The historical dataset is small relative to a production marketplace and contains very few repeat buyers. Time-based snapshot evaluation can still contain repeated customer identities across snapshots. Performance should be considered portfolio research, not production-grade evidence.


## Observed model limitations from the supplied archive

- The 240-day no-return target had **98.27%** positive prevalence in the chronological test set. ROC-AUC was **0.612** and lift@10% was **1.009**. The current churn model is not sufficiently discriminative for CRM targeting.
- Future paid-value targets are sparse: only **0.77%**, **1.34%** and **2.56%** of 90-, 180- and 365-day test rows had non-zero future paid value.
- Pointwise MAE was worse than the zero-value baseline for all three horizons. Top-decile value capture was **20.52%**, **25.08%** and **23.21%**, respectively. This may support exploratory ranking but is not evidence of accurate individual CLV.
- The 365-day evaluation uses one held-out monthly snapshot and is especially fragile.
- The churn and CLV snapshot validation can contain the same customer in multiple dates; it is chronological but not customer-group independent.
- The Olist archive includes seller-side marketing-qualified leads and closed deals. These are not buyer-level acquisition-cost or campaign-spend records and cannot be used as buyer CAC/ROAS.

