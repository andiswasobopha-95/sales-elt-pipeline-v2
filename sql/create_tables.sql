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

CREATE SCHEMA IF NOT EXISTS raw;

-- 1. Products Table
-- Maps directly to the Fake Store API response.
CREATE TABLE raw.products (
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    -- Flattening the nested JSON rating object for standard relational querying
    rating_rate NUMERIC(3, 1), 
    rating_count INT
);

-- 2. Orders Table
-- Synthetic order headers.
CREATE TABLE raw.orders (
    order_id INT PRIMARY KEY, -- Can be changed to SERIAL/GENERATED ALWAYS AS IDENTITY if auto-generating in the DB
    customer_id INT NOT NULL,
    order_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL
);

-- 3. Order Items Table
-- Links orders and products. Uses a composite primary key since a specific product 
-- should generally only appear once per order.
CREATE TABLE raw.order_items (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    
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