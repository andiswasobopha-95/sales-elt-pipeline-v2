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

-- 1. Products Table
-- Maps directly to the Fake Store API response.
CREATE TABLE IF NOT EXISTS raw.products (
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    -- Flattening the nested JSON rating object for standard relational querying
    rating_rate NUMERIC(3, 1),
    rating_count INT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Orders Table
-- Synthetic order headers.
CREATE TABLE IF NOT EXISTS raw.orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. Order Items Table
-- Links orders and products. Composite primary key: a product appears at most
-- once per order. unit_price records the price paid at order time, so later
-- product price changes don't rewrite history.
CREATE TABLE IF NOT EXISTS raw.order_items (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price NUMERIC(10, 2) NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk_order
        FOREIGN KEY (order_id)
        REFERENCES raw.orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_quantity
        CHECK (quantity > 0)
);