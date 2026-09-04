"""
Airflow DAG: sales_elt_pipeline

TODO: Build a DAG that chains these tasks:
  extract_products  ->  load_to_postgres  ->  dbt_run  ->  dbt_test

Hints:
- Use PythonOperator for extract_products and load_to_postgres (call the
  `run()` functions from src/extract/extract_api.py and
  src/load/load_to_postgres.py).
- Use BashOperator for dbt_run and dbt_test — run `dbt run` and `dbt test`
  from the dbt_project directory.
- Set a schedule (e.g. "@daily"), a start_date (use timezone-aware
  datetime — ruff will flag naive datetimes), and catchup=False.
- Chain tasks with >>
"""
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# TODO: define the DAG and its tasks here
