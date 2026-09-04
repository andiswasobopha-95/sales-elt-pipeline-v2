# Mart models — TODO

Build a star schema on top of your staging models:

- `dim_products.sql` — product dimension
- `dim_dates.sql` — date dimension (hint: Postgres `generate_series` over a
  date range is a common way to build this)
- `fct_orders.sql` — order-grain fact table (one row per order, aggregate
  order totals from order_items)
- `fct_order_items.sql` — line-item grain fact table, joining stg_order_items
  to stg_orders and stg_products — this is usually your main analytics table

Add a `_marts.yml` with tests on primary keys (`unique`, `not_null`) for each
model.

Think about: what question should this schema make easy to answer? (e.g.
"revenue by category by month") — model toward that.
