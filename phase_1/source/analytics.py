
import pandas as pd
from sqlalchemy import text

# Reuse the existing Supabase engine.
from database import engine


# Only these predefined SQL queries are permitted.
# This prevents user input from becoming arbitrary SQL.
BUSINESS_QUERIES = {
    "overall_returns": """
        SELECT
            COUNT(*) AS total_orders,
            SUM(returned::int) AS returned_orders,
            ROUND(AVG(returned::int) * 100, 2)
                AS return_rate_percent
        FROM public.orders
    """,

    "category_returns": """
        SELECT
            product_category,
            COUNT(*) AS total_orders,
            SUM(returned::int) AS returned_orders,
            ROUND(AVG(returned::int) * 100, 2)
                AS return_rate_percent
        FROM public.orders
        GROUP BY product_category
        ORDER BY return_rate_percent DESC
    """,

    "shipping_returns": """
        SELECT
            shipping_method,
            COUNT(*) AS total_orders,
            SUM(returned::int) AS returned_orders,
            ROUND(AVG(returned::int) * 100, 2)
                AS return_rate_percent
        FROM public.orders
        GROUP BY shipping_method
        ORDER BY return_rate_percent DESC
    """
}


def run_business_query(query_name: str) -> pd.DataFrame:
    """Run an approved business analytics query against Supabase."""

    # Reject unknown query names before accessing the database.
    if query_name not in BUSINESS_QUERIES:
        raise ValueError(f"Unsupported business query: {query_name}")

    # Execute only the SQL associated with the approved query name.
    with engine.connect() as connection:
        result = pd.read_sql_query(
            text(BUSINESS_QUERIES[query_name]),
            connection
        )

    return result
