import requests
import pandas as pd
from datetime import datetime
import os

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_to_csv(data):
    rows = []
    for coin in data:
        rows.append({
            "name": coin["name"],
            "symbol": coin["symbol"].upper(),
            "price_usd": coin["current_price"],
            "market_cap": coin["market_cap"],
            "24h_change_%": round(coin["price_change_percentage_24h"], 2),
            "volume_24h": coin["total_volume"],
            "scraped_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        })

    df = pd.DataFrame(rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/results.csv", index=False)
    print(f"✅ Saved {len(df)} coins to data/results.csv")
    print(df.to_string(index=False))

if __name__ == "__main__":
    print("🔍 Fetching crypto prices from CoinGecko...")
    data = fetch_crypto_prices()
    save_to_csv(data)
