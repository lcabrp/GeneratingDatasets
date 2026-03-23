"""
Application‑wide configuration.
"""
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣  Where all files will live
# ---------------------------------------------------------
DATA_DIR = Path("data")        # <-- change this to any folder you want
DATA_DIR.mkdir(parents=True, exist_ok=True)   # create it on import

# ---------------------------------------------------------
# 2️⃣  CSV file names (full paths)
# ---------------------------------------------------------
CUSTOMERS_CSV   = DATA_DIR / "customers.csv"
INVENTORY_CSV   = DATA_DIR / "inventory.csv"
TRANSACTIONS_CSV = DATA_DIR / "transactions.csv"

# ---------------------------------------------------------
# 3️⃣  SQLite file (full path)
# ---------------------------------------------------------
DATABASE_FILE = DATA_DIR / "retail.db"

# ------------------------------------------------------------------
# Dataset sizes – edit these numbers to get the dataset you want
# ------------------------------------------------------------------
DEFAULT_CUSTOMERS = 1_000         # ≤ 10 000 recommended
DEFAULT_INVENTORY = 500           # ≤ 5 000 recommended
MAX_TRANSACTIONS = 5_000_000      # capped by program logic
DEFAULT_TRANSACTIONS = 250_000    # <- actual value will be min(...)

# ------------------------------------------------------------------
# Filenames (change paths if you want them elsewhere)
# ------------------------------------------------------------------
CUSTOMERS_CSV = "customers.csv"
INVENTORY_CSV = "inventory.csv"
TRANSACTIONS_CSV = "transactions.csv"

# ------------------------------------------------------------------
# Column names – keep in sync with generators
# ------------------------------------------------------------------
CUSTOMERS_COLUMNS = [
    "customer_id", "first_name", "last_name", "email", "phone",
    "address", "city", "state", "zip_code", "country",
    "date_of_birth", "gender", "signup_date",
]

INVENTORY_COLUMNS = [
    "product_id", "sku", "name", "category", "brand",
    "price", "weight", "stock_qty", "rating",
    "description", "created_at",
]

TRANSACTIONS_COLUMNS = [
    "order_id", "order_date", "customer_id",
    "shipping_address", "status", "total_amount",
    "shipping_cost", "payment_method",
    "coupon_code", "items",
]

