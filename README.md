Stock Market Data Engineering Pipeline

This project is a practical end-to-end data engineering pipeline for collecting and managing stock market pricing data.
It fetches real stock prices from the Alpha Vantage API, stores them in a PostgreSQL database running in Docker, and prepares the data for future analysis and dashboarding (Power BI, Tableau, etc.).

The goal is to create a clean, scalable workflow that simulates a real-world data engineering environment.

What this project does

Pulls real-time and historical stock prices automatically

Stores everything inside a PostgreSQL database (running in Docker)

Tracks daily updates while avoiding duplicate entries

Provides a clear ETL structure (Ingestion → Transform → Load)

Easy to extend with more tickers or scheduled jobs

Designed to support analytics dashboards later on

Tech used
Area	Tools
Language	Python
Database	PostgreSQL
Containers	Docker + Docker Compose
Data Source	Alpha Vantage API
Config	.env environment variables
Future Add-ons	BI dashboards (Power BI/Tableau), scheduling, more data sources
Project layout
stock-market-data-pipeline/
│
├── data/                     # Raw & processed data if needed
│   ├── raw/
│   └── processed/
│
├── src/                      # Main pipeline code
│   ├── ingestion/            # API data collection
│   │   └── fetch_daily.py
│   ├── transformation/       # (coming soon)
│   └── loading/              # DB tests/connection helpers
│       └── db_test.py
│
├── db/
│   └── schema.sql            # Database tables
│
├── docker/
│   └── docker-compose.yml     # PostgreSQL container config
│
├── requirements.txt
└── README.md

Database model
stocks

Basic info about each company / ticker.

stock_id (PK)
symbol (UNIQUE)
company_name
exchange

stock_prices

Daily price records linked to a stock.

price_id (PK)
stock_id (FK → stocks)
price_date
open_price
close_price
high_price
low_price
volume
UNIQUE(stock_id, price_date)


This setup keeps metadata separate from price history, avoids duplicate daily entries, and works well for analytics.# stock-market-data-pipeline
