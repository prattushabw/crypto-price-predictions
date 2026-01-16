import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()
connection = http.client.HTTPSConnection("pro-api.coinmarketcap.com")
coinMarketCap_api_key = os.getenv("CMC_API_KEY")

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": coinMarketCap_api_key
}

latest_endpoint = "/v1/cryptocurrency/listings/latest"
latest_parameters = "?start=1&limit=50&convert=USD"


connection.request("GET", latest_endpoint + latest_parameters, headers=headers)
latest_response = connection.getresponse()
latest_data = json.loads(latest_response.read().decode("utf-8"))


results = []


print(f"{'Name':<20} {'Rank':<5} {'Market Cap (USD)':<20} {'Price (USD)':<15}")
print("=" * 100)

for currency in latest_data["data"]:
    name = currency["name"]
    rank = currency["cmc_rank"]
    current_price = currency["quote"]["USD"]["price"]
    market_cap = currency["quote"]["USD"]["market_cap"]
   


    print(f"{name:<20} {rank:<5} ${market_cap:<20,.2f} ${current_price:<15,.2f}")

    results.append({
        "name": name,
        "rank": rank,
        "market_cap_usd": market_cap,
        "price_usd": current_price,
    })


output_file = "cryptocurrency_data.json"
with open(output_file, "w") as file:
    json.dump(results, file, indent=4)

print(f"\nResults saved to {output_file}")
