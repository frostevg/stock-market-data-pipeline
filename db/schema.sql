CREATE TABLE IF NOT EXISTS stocks (
    stock_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    company_name VARCHAR(100),
    exchange VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS stock_prices (
    price_id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES stocks(stock_id),
    price_date DATE NOT NULL,
    open_price NUMERIC(10,2),
    close_price NUMERIC(10,2),
    high_price NUMERIC(10,2),
    low_price NUMERIC(10,2),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (stock_id, price_date)

);

