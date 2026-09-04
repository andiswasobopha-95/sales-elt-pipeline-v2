# Staging models — TODO

Build one staging model per raw table:
- `stg_products.sql`
- `stg_orders.sql`
- `stg_order_items.sql`

Each should be a simple `select` over `{{ source('raw', 'table_name') }}` that:
- Renames columns to clear, consistent names
- Casts types where needed
- Does NOT contain joins or business logic (that belongs in marts)

You'll also need a `_staging.yml` file declaring your sources (so
`{{ source(...) }}` works) and column tests (`unique`, `not_null`,
`relationships`, `accepted_values`).
