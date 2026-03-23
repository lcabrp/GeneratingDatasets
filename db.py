"""
SQLite helper module.
Creates a database, builds tables and bulk‑inserts the CSV data.
"""

import csv
import sqlite3
from pathlib import Path
from typing import Iterable, Tuple

from config import (
    CUSTOMERS_COLUMNS,
    INVENTORY_COLUMNS,
    TRANSACTIONS_COLUMNS,
    CUSTOMERS_CSV,
    INVENTORY_CSV,
    TRANSACTIONS_CSV,
    DATABASE_FILE
)

# ------------------------------------------------------------------
# 1️⃣  DATABASE STRUCTURE
# ------------------------------------------------------------------
TABLE_DEFINITIONS = {
    "customers": (
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            date_of_birth TEXT,
            gender TEXT,
            signup_date TEXT
        );
        """,
        CUSTOMERS_COLUMNS,
    ),
    "inventory": (
        """
        CREATE TABLE IF NOT EXISTS inventory (
            product_id TEXT PRIMARY KEY,
            sku TEXT,
            name TEXT,
            category TEXT,
            brand TEXT,
            price REAL,
            weight REAL,
            stock_qty INTEGER,
            rating REAL,
            description TEXT,
            created_at TEXT
        );
        """,
        INVENTORY_COLUMNS,
    ),
    "transactions": (
        """
        CREATE TABLE IF NOT EXISTS transactions (
            order_id TEXT PRIMARY KEY,
            order_date TEXT,
            customer_id TEXT,
            shipping_address TEXT,
            status TEXT,
            total_amount REAL,
            shipping_cost REAL,
            payment_method TEXT,
            coupon_code TEXT,
            items TEXT,                     -- JSON string
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            -- note: product_id is stored inside `items` JSON
        );
        """,
        TRANSACTIONS_COLUMNS,
    ),
}

# Indexes to speed up queries
INDEX_DEFINITIONS = [
    "CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);",
]


# ------------------------------------------------------------------
# 2️⃣  HELPERS
# ------------------------------------------------------------------

def _open_connection(db_path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DATABASE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path.as_posix())

def _execute_many(conn: sqlite3.Connection, sql: str, rows: Iterable[Tuple]) -> None:
    """Execute many rows with SQLite.  Uses a transaction for speed."""
    conn.execute("BEGIN")
    conn.executemany(sql, rows)
    conn.execute("COMMIT")


# ------------------------------------------------------------------
# 3️⃣  PUBLIC API
# ------------------------------------------------------------------
def create_database(db_path: str | None = None) -> sqlite3.Connection:
    """
    Create the SQLite file, build tables and indexes.
    Returns the opened Connection object.
    """
    conn = _open_connection(db_path)
    cursor = conn.cursor()

    # 3.1  Create tables
    for table_name, (create_sql, _) in TABLE_DEFINITIONS.items():
        cursor.executescript(create_sql)

    # 3.2  Create indexes
    for idx_sql in INDEX_DEFINITIONS:
        cursor.executescript(idx_sql)

    conn.commit()
    return conn


def import_csv_to_table(
    conn: sqlite3.Connection,
    table_name: str,
    csv_path: str | Path,
    limit: int | None = None,
) -> None:
    """
    Bulk‑load a CSV into the specified table.
    If `limit` is provided, only import that many rows.
    """
    if table_name not in TABLE_DEFINITIONS:
        raise ValueError(f"Unknown table: {table_name}")

    _, columns = TABLE_DEFINITIONS[table_name]
    placeholders = ", ".join("?" * len(columns))
    insert_sql = f"INSERT OR REPLACE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    rows = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader, start=1):
            # Map the dict to a tuple in column order
            vals = tuple(row[col] for col in columns)
            rows.append(vals)

            if limit and i >= limit:
                break

    if rows:
        _execute_many(conn, insert_sql, rows)  # fast bulk insert


def load_all_csvs(conn: sqlite3.Connection, csv_dir: str | Path = ".") -> None:
    """Convenience wrapper that imports all three CSV datasets."""
    csv_dir = Path(csv_dir)

    import_csv_to_table(
        conn,
        "customers",
        csv_dir / CUSTOMERS_CSV,
    )
    import_csv_to_table(
        conn,
        "inventory",
        csv_dir / INVENTORY_CSV,
    )
    import_csv_to_table(
        conn,
        "transactions",
        csv_dir / TRANSACTIONS_CSV,
    )
