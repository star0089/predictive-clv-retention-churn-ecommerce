# Data Dictionary and Source Coverage

## Dataset
The project uses the public Olist Brazilian E-Commerce dataset. The raw CSV files are stored locally in data_raw and are intentionally excluded from Git.

## Tables used by the pipeline

| Source file | Grain | Main keys | Pipeline use |
|---|---|---|---|
| olist_customers_dataset.csv | Customer/order-location record | customer_id, customer_unique_id | Persistent customer identity |
| olist_orders_dataset.csv | One row per order | order_id, customer_id | Purchase timestamps and order status |
| olist_order_items_dataset.csv | One row per order item | order_id, product_id, seller_id | Product/category analysis extensions |
| olist_order_payments_dataset.csv | One row per payment installment | order_id | Sum payment_value to order-level paid value |
| olist_order_reviews_dataset.csv | Review record | review_id, order_id | Exploratory experience analysis |
| olist_products_dataset.csv | Product | product_id | Optional category enrichment |
| olist_sellers_dataset.csv | Seller | seller_id | Optional seller analysis |
| product_category_name_translation.csv | Category translation | product_category_name | Optional readable category names |

## Key grain decisions

- order_id is the transaction key.
- customer_id links an order to a customer record.
- customer_unique_id is the persistent customer key used for customer-level RFM, retention and CLV.
- Payment rows are aggregated to order_id before joining to orders to prevent row multiplication.
- The reproducible pipeline uses delivered orders as completed purchases. Earlier exploratory notebooks may include broader order statuses; their counts can therefore differ from pipeline outputs.

## Financial definitions

The pipeline calls the sum of order payment_value paid_order_value. It is customer-paid order value, not contribution margin or profit. It may include freight and other paid components. Olist does not provide product cost of goods, platform fulfilment cost, customer-service cost, or reliable refund/return cost fields in the core public tables.

## Sources not present in the public dataset

The standard Olist dataset does not contain the following business tables from the fictional NovaCart brief:

- marketing_spend / campaign spend and exposure
- customer acquisition cost by customer or channel
- customer-support tickets and CSAT
- a complete returns/refunds event ledger
- product cost of goods and true fulfilment cost
- loyalty membership lifecycle

These must not be fabricated. The project documents their absence and provides a place to add compatible external data if legitimately obtained.
