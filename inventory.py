"""
Generate the inventory CSV.
"""

import csv

from config import (
    INVENTORY_CSV,
    INVENTORY_COLUMNS,
    DEFAULT_INVENTORY,
)
from utils import (
    random_price,
    random_weight,
    random_stock_qty,
    random_rating,
)
from faker import Faker

fake = Faker()


def build_product() -> dict:
    # Create a *deterministic* product_id for items referenced from transactions
    product_id = fake.uuid4()
    return {
        "product_id": product_id,
        "sku": fake.bothify(text="???-####"),
        "name": fake.catch_phrase(),
        "category": fake.bs().split()[0].capitalize(),
        "brand": fake.company(),
        "price": random_price(5.0, 499.99),
        "weight": random_weight(0.1, 10.0),
        "stock_qty": random_stock_qty(),
        "rating": random_rating(),
        "description": fake.text(max_nb_chars=200),
        "created_at": fake.date_between(start_date="-2y", end_date="today").isoformat(),
    }


def generate_inventory_csv(num_rows: int = DEFAULT_INVENTORY) -> list[dict]:
    """
    Return a list of product dictionaries so that
    the calling script can reference them for the transaction data.
    """
    products = []
    with open(INVENTORY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INVENTORY_COLUMNS)
        writer.writeheader()
        for _ in range(num_rows):
            prod = build_product()
            writer.writerow(prod)
            products.append(prod)
    return products
