"""
Generate the transactions (orders) CSV.
"""

import csv
from typing import List
import random

from config import (
    TRANSACTIONS_CSV,
    TRANSACTIONS_COLUMNS,
    MAX_TRANSACTIONS,
    DEFAULT_TRANSACTIONS,
    CUSTOMERS_CSV,
)
from utils import (
    random_date,
    random_status,
    random_payment_method,
    random_coupon_code,
    random_json_items,
    uuid4_str,
)
from customers import build_customer  # to get list of customer IDs
import json
import csv


def build_transactions(
    customers: List[dict], products: List[dict], num_records: int
) -> None:
    with open(TRANSACTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRANSACTIONS_COLUMNS)
        writer.writeheader()

        for _ in range(num_records):
            customer = random.choice(customers)
            # Generate one order per iteration
            items = random_json_items(products)
            # Calculate total_amount from items (parsing json back)
            total = 0
            for item in json.loads(items):
                total += float(item["unit_price"]) * item["quantity"]
            shipping_cost = round(random.uniform(3, 15), 2)

            writer.writerow(
                {
                    "order_id": uuid4_str(),
                    "order_date": random_date(365, 0),
                    "customer_id": customer["customer_id"],
                    "shipping_address": customer["address"],
                    "status": random_status(),
                    "total_amount": f"{total:.2f}",
                    "shipping_cost": f"{shipping_cost:.2f}",
                    "payment_method": random_payment_method(),
                    "coupon_code": random_coupon_code(),
                    "items": items,
                }
            )
