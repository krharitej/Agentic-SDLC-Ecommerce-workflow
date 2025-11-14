import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = Path("ecommerce.db")
QUERY_PATH = Path("query.sql")


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Missing database: {DB_PATH.resolve()}")
    if not QUERY_PATH.exists():
        raise FileNotFoundError(f"Missing SQL file: {QUERY_PATH.resolve()}")

    query = QUERY_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    if df.empty:
        print("Query returned no rows.")
    else:
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()

