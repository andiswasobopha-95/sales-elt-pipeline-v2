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
