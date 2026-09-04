"""
TODO: Write unit tests for src/load/load_to_postgres.py.

Ideas:
- Test load_raw_products() reads a JSON file correctly (use tmp_path fixture
  to create a fake JSON file).
- Test load_raw_products() raises a clear error if the file doesn't exist.
- (Harder, optional) Test upsert/order generation logic without a real DB
  connection — e.g. by mocking the cursor.

Run with: pytest tests/ -v
"""
