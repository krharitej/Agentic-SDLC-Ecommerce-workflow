import sqlite3
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
DB_PATH = Path("ecommerce.db")

TABLE_SPECS = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            city TEXT
        )
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL
        )
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """,
    "payments": """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            method TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    """,
}


def create_tables(cursor: sqlite3.Cursor) -> None:
    for ddl in TABLE_SPECS.values():
        cursor.execute(ddl)


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Missing data directory: {DATA_DIR.resolve()}")

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        create_tables(cur)
        conn.commit()

        csv_table_pairs = [
            ("users.csv", "users"),
            ("products.csv", "products"),
            ("orders.csv", "orders"),
            ("order_items.csv", "order_items"),
            ("payments.csv", "payments"),
        ]

        for csv_name, table in csv_table_pairs:
            csv_path = DATA_DIR / csv_name
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing CSV file: {csv_path}")

            df = pd.read_csv(csv_path)
            df.to_sql(table, conn, if_exists="replace", index=False)

        print("Ingestion complete")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

