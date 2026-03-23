# load_db.py
from db import create_database, load_all_csvs

if __name__ == "__main__":
    conn = create_database()
    load_all_csvs(conn)
    conn.close()
    print("Database ready: retail.db")
