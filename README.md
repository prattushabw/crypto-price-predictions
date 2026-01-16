# Crypto Price Predictions (CoinMarketCap + Perplexity)

A small pipeline that:
- Fetches the top 100 cryptocurrencies from CoinMarketCap.
- Sends that snapshot to Perplexity to generate next-day price predictions.
- Compares predicted vs actual prices and optionally saves comparison charts.

## Repository layout
- `cryptocurrency_data/` — saved real market snapshots (JSON).
- `predictions/` — Perplexity prediction outputs (JSON).
- `graphs/` — saved charts (PNG).

## Setup
CMC_API_KEY=your_coinmarketcap_key
PPLX_API_KEY=your_perplexity_key
```

2. (Optional) Install dependencies:
```bash
pip install requests pandas matplotlib python-dotenv
```

## Flow of the Code

1. generate_predictions.py (main daily script)
   - Fetches current data from CoinMarketCap `/v1/cryptocurrency/listings/latest`.
   - Saves snapshot: `cryptocurrency_data/<MM-DD-YYYY>.json`.
   - Sends the saved snapshot to Perplexity to produce next-day predictions.
   - Saves predictions: `predictions/<MM-DD-YYYY prediction>.json`.

2. compare_actual_vs_predicted.py
   - Compares actual vs predicted prices for a specified date.

3. plot_predictions.py
   - Same comparison as above, but saves the chart as `<DATE>.png` in `graphs/`.
