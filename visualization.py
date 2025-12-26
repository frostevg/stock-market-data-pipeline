import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/stock_daily_prices.csv")
df['price_date'] = pd.to_datetime(df['price_date'])

symbols = df['symbol'].unique()[:5] # first 5 tickers

plt.figure(figsize=(12,6))
for s in symbols:
    plot_df = df[df['symbol'] == s].sort_values("price_date")
    plt.plot(plot_df["price_date"], plot_df["close_price"], label=s)

plt.title("Stock Closing Prices Over Time")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.tight_layout()

plt.savefig("docs/dashboard_overview.png")
plt.close()

print("Visualization saved to docs/dashboard_overview.png")


