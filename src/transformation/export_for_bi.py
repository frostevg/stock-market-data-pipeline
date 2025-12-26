import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "stock_db"),
    "user": os.getenv("DB_USER", "stock_user"),
    "password": os.getenv("DB_PASSWORD", "stock_pass"),
}

OUTPUT_PATH = "data/processed/stock_daily_prices.csv"


def ensure_view_exists():
    """
    Create or replace a view that joins stocks and stock_prices.
    """
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE OR REPLACE VIEW stock_daily_prices_view AS
                SELECT
                    sp.price_date,
                    s.symbol,
                    s.company_name,
                    sp.open_price,
                    sp.close_price,
                    sp.high_price,
                    sp.low_price,
                    sp.volume
                FROM stock_prices sp
                JOIN stocks s ON sp.stock_id = s.stock_id;
                """
            )
        conn.commit()
        print("View stock_daily_prices_view ensured/created.")
    finally:
        conn.close()


def export_to_csv():
    """
    Export the view to a CSV file for BI tools.
    """
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        query = "SELECT * FROM stock_daily_prices_view ORDER BY price_date, symbol;"
        df = pd.read_sql(query, conn)
        print(f"Exporting {len(df)} rows to {OUTPUT_PATH}")
        df.to_csv(OUTPUT_PATH, index=False)
    finally:
        conn.close()


def main():
    ensure_view_exists()
    export_to_csv()
    print("Export complete.")


if __name__ == "__main__":
    main()

