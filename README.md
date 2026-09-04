# Sales Analytics ELT Pipeline (Starter)

This is a **skeleton** for a portfolio ELT pipeline project. The goal: build a
pipeline that extracts product data from a public API, generates synthetic
order data, loads it into PostgreSQL, transforms it with dbt into a star
schema, and orchestrates the whole thing with Airflow — containerized with
Docker.

Nothing here works yet. That's the point — you're building it.

## Target architecture

```
Fake Store API --> extract (Python) --> data/raw/*.json
                                              |
                                              v
                            load (Python + synthetic orders) --> Postgres (raw schema)
                                              |
                                              v
                                   dbt staging models (cleaned)
                                              |
                                              v
                              dbt mart models (star schema: dim/fct tables)

  Orchestrated end-to-end by an Airflow DAG.
```

## Build order (recommended)

Work through these roughly in order — each stage depends on the previous one
actually working.

1. **`sql/create_tables.sql`** — Design the raw schema. What tables do you need
   to store products, orders, and order line items? What columns, types, and
   relationships?
2. **`src/utils/db.py`** — Write a function to connect to Postgres using
   environment variables.
3. **`src/extract/extract_api.py`** — Call the Fake Store API
   (`https://fakestoreapi.com/products`), save the response as JSON to
   `data/raw/`.
4. **`src/load/load_to_postgres.py`** — Read the raw JSON, generate some
   synthetic orders/order_items on top of it, and load everything into
   Postgres.
5. **`tests/`** — Write pytest tests for extract and load logic.
6. **`dbt_project/`** — Once data is loading, build staging models (1:1
   cleaned views), then mart models (a proper star schema: dimension +
   fact tables).
7. **`dags/sales_pipeline_dag.py`** — Wire extract → load → dbt run → dbt test
   into an Airflow DAG.
8. **`docker-compose.yml`** — Containerize Postgres + Airflow so the whole
   thing runs with one command.
9. **`.github/workflows/ci.yml`** — Add CI: lint, run tests, validate dbt
   compiles, on every push.

## Stack
Python · PostgreSQL · dbt · Apache Airflow · Docker Compose · pytest · GitHub Actions

## Notes to self
_(Use this space to jot down design decisions, things you got stuck on, or
things you'd do differently next time — good material for interview
discussions later.)_
