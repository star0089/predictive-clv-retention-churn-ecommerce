# Dataset setup

Use the **Olist Brazilian E-Commerce Public Dataset**:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Download the original archive from the publisher's dataset page and extract CSVs locally into `data/raw/`. This directory is ignored by Git. No dataset is included here.

Expected tables for the next analysis:
- `olist_orders_dataset.csv`: order lifecycle and purchase timestamps.
- `olist_customers_dataset.csv`: order-linked and persistent customer identifiers.
- `olist_order_reviews_dataset.csv`: order reviews; multiple rows per order must be investigated.

Later revenue analyses may require order items, payments and products. Do not join all tables indiscriminately: items, payments and reviews can each have multiple rows per order.

Before execution, record the download date, actual filenames, row counts, column types, timestamp representation and file hashes. The previous timestamp parsing note referred to an author's export; do not force that format onto a fresh download.

Review the publisher's current dataset license and attribution requirements before redistribution. A code license would not grant rights to this dataset. Raw data must remain local unless redistribution has been explicitly justified.

There is no runnable analysis yet; dependency and execution instructions will accompany committed code.
