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

import json
import os
from datetime import datetime
from pathlib import Path



API_URL = os.environ.get("FAKE_STORE_API_URL", "https://fakestoreapi.com/products")
DATA_DIR = Path(os.environ.get("RAW_DATA_DIR", "data/raw"))


def fetch_products(api_url: str = API_URL):
    """
    Fetches the product catalog from the API.
    Raises an exception for bad HTTP status codes.
    """
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error on 4xx/5xx status codes
    return response.json()


def save_raw(products, data_dir: Path = DATA_DIR):
    """
    Saves the raw JSON payload to the data directory.
    Saves both a timestamped version for history and a 'latest' version 
    for the load step to consume easily.
    """
    # Ensure the target directory exists
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp for historical file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_file = data_dir / f"products_{timestamp}.json"
    latest_file = data_dir / "products_latest.json"
    
    # Write the timestamped file
    with open(timestamped_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)
        
    # Write the 'latest' file
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)
        
    print(f"Successfully saved {len(products)} products.")
    print(f" - {timestamped_file}")
    print(f" - {latest_file}")
    
    return latest_file


def run():
    products = fetch_products()
    return save_raw(products)


if __name__ == "__main__":
    run()