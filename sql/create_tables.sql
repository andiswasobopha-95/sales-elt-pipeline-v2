-- TODO: Design the raw schema for this pipeline.
--
-- You'll need at least three tables:
--   1. products      — from the Fake Store API (id, title, price, category, etc.)
--   2. orders        — synthetic order headers (order id, customer id, date, status)
--   3. order_items   — synthetic line items (links an order to a product + quantity)
--
-- Questions to think through:
--   - What's the primary key for each table?
--   - Which columns should NOT be null?
--   - How does order_items reference orders and products? (foreign keys)
--   - Should you put these in a dedicated schema (e.g. `raw`) rather than `public`?
--
-- Reference: the Fake Store API response looks like this for one product:
-- {
--   "id": 1,
--   "title": "Fjallraven Backpack",
--   "price": 109.95,
--   "category": "men's clothing",
--   "description": "...",
--   "rating": { "rate": 3.9, "count": 120 }
-- }

CREATE SCHEMA IF NOT EXISTS raw;

-- CREATE TABLE raw.products ( ... );

-- CREATE TABLE raw.orders ( ... );

-- CREATE TABLE raw.order_items ( ... );
