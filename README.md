# Crypto Price Predictions (CoinMarketCap + Perplexity)

This project:
1) pulls the top 100 cryptocurrencies from CoinMarketCap,
2) sends that data to Perplexity to generate next-day price predictions,
3) compares predicted vs actual prices for a given date, and optionally saves a graph.

The project stores outputs in three folders:
- `cryptocurrency_data/` (real market snapshots)
- `predictions/` (next-day predictions from Perplexity)
- `graphs/` (saved charts)

## API Keys / Setup
CMC_API_KEY=your_coinmarketcap_key
PPLX_API_KEY=your_perplexity_key

The Flow (How the 3 scripts work together)
1) generate_predictions.py

This is the main “daily” script.

Step A: Fetch today’s real data

Calls CoinMarketCap endpoint: /v1/cryptocurrency/listings/latest

Extracts fields like name, rank, price, market cap, percent changes, and volume

Saves the results in: cryptocurrency_data/<TODAY>.json

(see fetch_and_save_data() in the file)

generate_predictions

Step B: Predict tomorrow

Loads the JSON file that was just saved

Sends the entire dataset to Perplexity (/chat/completions) with a prompt

Saves the prediction output in: predictions/<TOMORROW> prediction.json

(see generate_predictions(data_file) in the file)

generate_predictions

Run it:

python generate_predictions.py


What it produces:

cryptocurrency_data/MM-DD-YYYY.json

predictions/MM-DD-YYYY prediction.json (tomorrow’s date)

2) compare_actual_vs_predicted.py

This script is for comparing actual vs predicted for a specific date.

What it does:

Reads:

./cryptocurrency_data/<DATE> data.json

./predictions/<DATE> prediction.json

Builds a dataframe of:

actual price_usd

predicted predicted_price

Computes Mean Absolute Error (MAE)

Displays a log-scale bar chart (does not save by default)

(see full script)

compare_actual_vs_predicted

Important: You must set:

comparison_date = "12-3-2024"


to the date you want to compare.

Run it:

python compare_actual_vs_predicted.py

3) plot_predictions.py

This script does the same comparison as above, but it also saves the chart as a PNG.

What it does:

Reads:

./cryptocurrency_data/<DATE> data.json

./predictions/<DATE> prediction.json

Computes MAE

Creates the log-scale bar chart

Saves the chart to an output folder as <DATE>.png

(see full script)

plot_predictions

Important: In the current file, output_folder is an absolute Windows path:

output_folder = "C:/Users/khuwa/Cse_Project/graphs"


To use the repo’s graphs/ folder, set it to:

output_folder = "./graphs"


Also update:

comparison_date = "12-4-2024"


Run it:

python plot_predictions.py
