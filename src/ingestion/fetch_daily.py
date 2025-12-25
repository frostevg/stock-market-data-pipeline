import os
import time
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

DB_PARAMS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "stock_db"),
    "user": os.getenv("DB_USER", "stock_user"),
    "password": os.getenv("DB_PASSWORD", "stock_pass"),
}


def get_symbols():
    """
    Read all stock symbols from the stocks table.
    """
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT symbol FROM stocks ORDER BY symbol;")
            rows = cur.fetchall()
        return [r[0] for r in rows]
    finally:
        conn.close()


def fetch_daily_prices(symbol: str):
    """
    Fetch daily prices for a given stock symbol from Alpha Vantage.
    Returns a list of tuples: (symbol, date, open, close, high, low, volume).
    """
    if not API_KEY:
        raise RuntimeError("ALPHA_VANTAGE_KEY is not set in .env")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # free endpoint
        "symbol": symbol,
        "apikey": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print(f"[{symbol}] Error fetching data: {data}")
        return []

    prices = []
    time_series = data["Time Series (Daily)"]

    for date, values in time_series.items():
        prices.append(
            (
                symbol,
                date,
                float(values["1. open"]),
                float(values["4. close"]),
                float(values["2. high"]),
                float(values["3. low"]),
                int(float(values["5. volume"])),
            )
        )

    print(f"[{symbol}] Fetched {len(prices)} daily records.")
    return prices


def save_prices(prices):
    """
    Insert price data into stock_prices table.
    Uses symbol to look up stock_id in stocks.
    """
    if not prices:
        print("No prices to save.")
        return

    conn = psycopg2.connect(**DB_PARAMS)
    try:
        with conn.cursor() as cur:
            for symbol, date, open_p, close_p, high, low, volume in prices:
                cur.execute(
                    """
                    INSERT INTO stock_prices (
                        stock_id, price_date, open_price, close_price,
                        high_price, low_price, volume
                    )
                    SELECT stock_id, %s, %s, %s, %s, %s, %s
                    FROM stocks
                    WHERE symbol = %s
                    ON CONFLICT (stock_id, price_date) DO NOTHING;
                    """,
                    (date, open_p, close_p, high, low, volume, symbol),
                )
        conn.commit()
        print(f"Saved {len(prices)} records (duplicates skipped where needed).")
    finally:
        conn.close()


def main():
    symbols = get_symbols()
    print(f"Found symbols in DB: {symbols}")

    for symbol in symbols:
        print(f"\n=== Processing {symbol} ===")
        prices = fetch_daily_prices(symbol)
        save_prices(prices)

        # Respect Alpha Vantage free rate limits (5 calls/min, 25 per day)
        time.sleep(15)  # safe cushion between calls


if __name__ == "__main__":
    main()

