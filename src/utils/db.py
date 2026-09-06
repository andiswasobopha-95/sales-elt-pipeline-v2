"""
TODO: Write a function `get_connection()` that returns a psycopg2 connection
to the Postgres database.

Hints:
- Use `psycopg2.connect(host=..., port=..., dbname=..., user=..., password=...)`
- Don't hardcode credentials — read them from environment variables
  (os.environ.get(...)), with sensible local defaults so it "just works"
  when someone clones the repo and copies .env.example to .env.
- Env vars you'll probably want: APP_DB_HOST, APP_DB_PORT, APP_DB_NAME,
  APP_DB_USER, APP_DB_PASSWORD.
"""
import os

import psycopg2


# def get_connection():
    # TODO: implement this
    # raise NotImplementedError



def get_connection():
    """
    Returns a psycopg2 connection to the PostgreSQL database using
    environment variables or sensible local defaults.
    """
    # Fetch environment variables with sensible defaults for local development
    host = os.environ.get("APP_DB_HOST", "localhost")
    port = os.environ.get("APP_DB_PORT", "5432")
    dbname = os.environ.get("APP_DB_NAME", "postgres")
    user = os.environ.get("APP_DB_USER", "postgres")
    password = os.environ.get("APP_DB_PASSWORD", "postgres")

    # Establish and return the database connection
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )