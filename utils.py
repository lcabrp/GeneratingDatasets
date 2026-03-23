"""
Common helper functions used by multiple generators.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List

from faker import Faker

fake = Faker()


def uuid4_str() -> str:
    """Return a formatted uuid4 string."""
    return str(uuid.uuid4())


def random_price(low=5.0, high=500.0) -> str:
    """Return a price string with two decimals."""
    return f"{random.uniform(low, high):.2f}"


def random_weight(low=0.1, high=10.0) -> str:
    """Return a weight string with one decimal."""
    return f"{random.uniform(low, high):.1f}"


def random_stock_qty() -> int:
    return random.randint(0, 1_000)


def random_rating() -> float:
    return round(random.uniform(1.0, 5.0), 1)


def random_status() -> str:
    return random.choice(
        ["delivered", "shipped", "processing", "canceled", "returned"]
    )


def random_payment_method() -> str:
    return random.choice(["credit_card", "paypal", "stripe", "bank_transfer"])


def random_coupon_code() -> str:
    return fake.bothify(text="????-####") if random.random() < 0.2 else ""


def random_date(start_days_ago: int = 365, end_days_ago: int = 0) -> str:
    """Random date in the past ‘start_days_ago’ to ‘end_days_ago’."""
    end_date = datetime.now() - timedelta(days=end_days_ago)
    start_date = datetime.now() - timedelta(days=start_days_ago)
    return fake.date_between(start_date=start_date, end_date=end_date).isoformat()


def random_json_items(products: List[dict], max_items=5) -> str:
    """
    Build a JSON‑like string for transaction items.
    Each item: product_id, quantity, unit_price
    """
    import json

    num_items = random.randint(1, max_items)
    chosen = random.sample(products, k=num_items)
    items = []
    for prod in chosen:
        qty = random.randint(1, 5)
        items.append(
            {
                "product_id": prod["product_id"],
                "quantity": qty,
                "unit_price": prod["price"],
            }
        )
    return json.dumps(items)
