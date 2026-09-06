"""
Load stage: read the raw product JSON, generate synthetic orders/order_items
on top of it (since the public API has no transactional data), and load
everything into the `raw` schema in Postgres.

TODO:
1. Write `load_raw_products(path)` — read and parse the JSON file saved by
   extract_api.py.
2. Write `upsert_products(cur, products)` — insert products into raw.products.
   Think about: what happens if you run this twice? (Hint: look up
   "ON CONFLICT DO UPDATE" / upsert in Postgres.)
3. Write `generate_and_load_orders(cur, product_ids)` — use Python's `random`
   module (or the Faker library) to generate a configurable number of fake
   orders, each with 1-4 line items referencing real product_ids. Consider
   seeding the random generator so results are reproducible.
4. Write `run()` that ties it together: load products from JSON, connect to
   the DB, upsert products, generate orders, commit.

Things to think about:
- Should re-running this duplicate data, or should it be idempotent?
- Should you wrap everything in a transaction so a failure doesn't leave
  the DB half-updated?
"""
import os
from pathlib import Path

from src.utils.db import get_connection

DATA_DIR = Path(os.environ.get("RAW_DATA_DIR", "data/raw"))
ORDER_COUNT = int(os.environ.get("SYNTHETIC_ORDER_COUNT", "500"))
SEED = int(os.environ.get("RANDOM_SEED", "42"))


def load_raw_products(path: Path = DATA_DIR / "products_latest.json"):
    # TODO: implement this
    raise NotImplementedError


def upsert_products(cur, products):
    # TODO: implement this
    raise NotImplementedError


def generate_and_load_orders(cur, product_ids):
    # TODO: implement this
    raise NotImplementedError


def run():
    # TODO: tie it all together
    raise NotImplementedError


if __name__ == "__main__":
    run()
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# psycopg2.extras is helpful for faster bulk inserts
from psycopg2.extras import execute_batch

from src.utils.db import get_connection

DATA_DIR = Path(os.environ.get("RAW_DATA_DIR", "data/raw"))
ORDER_COUNT = int(os.environ.get("SYNTHETIC_ORDER_COUNT", "500"))
SEED = int(os.environ.get("RANDOM_SEED", "42"))


def load_raw_products(path: Path = DATA_DIR / "products_latest.json"):
    """
    Reads the raw product JSON file into memory.
    """
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at {path}. Run extraction first.")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def upsert_products(cur, products):
    """
    Inserts products into the database. If a product with the same ID 
    already exists, it updates the record (idempotent).
    """
    query = """
        INSERT INTO raw.products (id, title, price, category, description, rating_rate, rating_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            price = EXCLUDED.price,
            category = EXCLUDED.category,
            description = EXCLUDED.description,
            rating_rate = EXCLUDED.rating_rate,
            rating_count = EXCLUDED.rating_count;
    """
    
    # Prepare list of tuples for batch execution
    values = []
    for p in products:
        rating = p.get("rating", {})
        values.append((
            p.get("id"),
            p.get("title"),
            p.get("price"),
            p.get("category"),
            p.get("description"),
            rating.get("rate"),
            rating.get("count")
        ))
        
    execute_batch(cur, query, values)
    print(f"Upserted {len(values)} products.")


def generate_and_load_orders(cur, product_ids):
    """
    Generates synthetic orders and order items, and loads them idempotently.
    Seed guarantees the same orders are generated across runs.
    """
    random.seed(SEED)
    
    # Base date for deterministic random dates
    base_date = datetime(2026, 1, 1)
    statuses = ["pending", "shipped", "delivered", "cancelled"]
    
    orders = []
    order_items = []
    
    for order_id in range(1, ORDER_COUNT + 1):
        # 1. Generate Order Header
        customer_id = random.randint(1, 100)
        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 86400)
        order_date = base_date + timedelta(days=random_days, seconds=random_seconds)
        status = random.choice(statuses)
        
        orders.append((order_id, customer_id, order_date, status))
        
        # 2. Generate Order Items
        # Use random.sample to guarantee unique products per order (satisfying the composite PK)
        num_items = random.randint(1, 4)
        chosen_products = random.sample(product_ids, num_items)
        
        for product_id in chosen_products:
            quantity = random.randint(1, 5)
            order_items.append((order_id, product_id, quantity))

    # Upsert Orders
    orders_query = """
        INSERT INTO raw.orders (order_id, customer_id, order_date, status)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (order_id) DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            order_date = EXCLUDED.order_date,
            status = EXCLUDED.status;
    """
    execute_batch(cur, orders_query, orders)
    print(f"Upserted {len(orders)} orders.")

    # Upsert Order Items
    items_query = """
        INSERT INTO raw.order_items (order_id, product_id, quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (order_id, product_id) DO UPDATE SET
            quantity = EXCLUDED.quantity;
    """
    execute_batch(cur, items_query, order_items)
    print(f"Upserted {len(order_items)} order items.")


def run():
    # 1. Load Data from disk
    print("Loading raw product data...")
    products = load_raw_products()
    product_ids = [p["id"] for p in products]

    if not product_ids:
        print("No products to load. Exiting.")
        return

    # 2. Connect to Database and execute transaction
    print("Connecting to database...")
    
    # Using get_connection in a context manager automatically commits on success 
    # and rolls back if an exception occurs
    with get_connection() as conn:
        with conn.cursor() as cur:
            upsert_products(cur, products)
            generate_and_load_orders(cur, product_ids)
            
    print("Load stage completed successfully.")


if __name__ == "__main__":
    run()