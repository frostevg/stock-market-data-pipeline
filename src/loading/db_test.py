import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "stock_db"),
        user=os.getenv("DB_USER", "stock_user"),
        password=os.getenv("DB_PASSWORD", "stock_pass"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM stocks;")
            count = cur.fetchone()[0]
            print(f"Connected OK. stocks row count = {count}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()

