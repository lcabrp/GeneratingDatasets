#!/usr/bin/env python3
"""
One‑stop script that creates the 3 datasets.
"""

import csv
import os
import random
import sys
from typing import List
from db import create_database, load_all_csvs

from config import (
    DEFAULT_CUSTOMERS,
    DEFAULT_INVENTORY,
    MAX_TRANSACTIONS,
    DEFAULT_TRANSACTIONS,
    CUSTOMERS_CSV,
    INVENTORY_CSV,
    TRANSACTIONS_CSV,
)
from customers import generate_customers_csv
from inventory import generate_inventory_csv
from transactions import build_transactions
from faker import Faker

fake = Faker()


def read_customers() -> List[dict]:
    """Load customers so that transactions can reference real IDs."""
    customers = []
    with open(CUSTOMERS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            customers.append(row)
    return customers


def main() -> None:
    # ------------- 1️⃣ Create the customers ----------
    print(f"Generating {DEFAULT_CUSTOMERS} customers → {CUSTOMERS_CSV}")
    generate_customers_csv(DEFAULT_CUSTOMERS)

    # ------------- 2️⃣ Create the inventory ----------
    print(f"Generating {DEFAULT_INVENTORY} inventory items → {INVENTORY_CSV}")
    products = generate_inventory_csv(DEFAULT_INVENTORY)

    # ------------- 3️⃣ Determine transaction count ----------
    # Pick a realistic number but never > MAX_TRANSACTIONS
    num_trans = random.randint(50_000, MAX_TRANSACTIONS)
    if num_trans > DEFAULT_TRANSACTIONS:
        num_trans = DEFAULT_TRANSACTIONS
    print(f"Generating {num_trans} transactions → {TRANSACTIONS_CSV}")

    # ------------- 4️⃣ Load customers for reference ----------
    customers = read_customers()

    # ------------- 5️⃣ Generate transactions ----------
    build_transactions(customers, products, num_trans)

    print("\nAll three datasets are ready!")
    print(f"Customers  → {CUSTOMERS_CSV}")
    print(f"Inventory  → {INVENTORY_CSV}")
    print(f"Transactions → {TRANSACTIONS_CSV}")
    
    # ---------- 6️⃣  Store data in SQLite ----------
    db_conn = create_database()           # creates retail.db in the current folder
    load_all_csvs(db_conn)                # bulk‑import CSVs
    db_conn.close()

    print("\n✅ All data have been stored in retail.db")


if __name__ == "__main__":
    main()
