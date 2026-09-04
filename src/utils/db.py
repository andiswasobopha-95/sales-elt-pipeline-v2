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


def get_connection():
    # TODO: implement this
    raise NotImplementedError
