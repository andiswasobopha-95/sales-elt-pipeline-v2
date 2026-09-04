"""
Extract stage: pull the product catalog from the public Fake Store API
and save it as raw JSON in data/raw/.

TODO:
1. Write `fetch_products(api_url)` — use the `requests` library to GET
   https://fakestoreapi.com/products, raise an error on bad status codes,
   and return the parsed JSON (a list of product dicts).
2. Write `save_raw(products)` — write the list to a JSON file in data/raw/.
   Consider: should the filename include a timestamp? Should you also save
   a stable "latest" copy for the load step to read from?
3. Write `run()` that calls both, and add `if __name__ == "__main__": run()`
   so this can be executed directly with `python -m src.extract.extract_api`.

Test it by running the script and checking data/raw/ for output.
"""
import json
import os
from pathlib import Path

import requests

API_URL = os.environ.get("FAKE_STORE_API_URL", "https://fakestoreapi.com/products")
DATA_DIR = Path(os.environ.get("RAW_DATA_DIR", "data/raw"))


def fetch_products(api_url: str = API_URL):
    # TODO: implement this
    raise NotImplementedError


def save_raw(products, data_dir: Path = DATA_DIR):
    # TODO: implement this
    raise NotImplementedError


def run():
    products = fetch_products()
    return save_raw(products)


if __name__ == "__main__":
    run()
