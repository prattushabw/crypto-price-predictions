import os
import datetime
import http.client
import json
import re

from dotenv import load_dotenv

load_dotenv()

def fetch_and_save_data():
    """Fetches cryptocurrency data and saves it to a JSON file."""
    connection = http.client.HTTPSConnection("pro-api.coinmarketcap.com")
    coinMarketCap_api_key = os.getenv("CMC_API_KEY")

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": coinMarketCap_api_key
    }

    latest_endpoint = "/v1/cryptocurrency/listings/latest"
    latest_parameters = "?start=1&limit=100&convert=USD"

    try:
        connection.request("GET", latest_endpoint + latest_parameters, headers=headers)
        latest_response = connection.getresponse()
        if latest_response.status != 200:
            raise Exception(f"Error fetching data: Status code {latest_response.status}")
        latest_data = json.loads(latest_response.read().decode("utf-8"))
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

    today_date = datetime.datetime.now().strftime("%m-%d-%Y")

    output_dir = "cryptocurrency_data"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{today_date}.json")

    results = []
    for currency in latest_data.get("data", []):
        try:
            name = currency["name"]
            rank = currency["cmc_rank"]
            current_price = currency["quote"]["USD"]["price"]
            market_cap = currency["quote"]["USD"]["market_cap"]
            percent_change_1h = currency["quote"]["USD"]["percent_change_1h"]
            percent_change_24h = currency["quote"]["USD"]["percent_change_24h"]
            percent_change_7d = currency["quote"]["USD"]["percent_change_7d"]
            volume_24h = currency["quote"]["USD"]["volume_24h"]

            results.append({
                "name": name,
                "rank": rank,
                "market_cap_usd": market_cap,
                "price_usd": current_price,
                "percent_change_1h": percent_change_1h,
                "percent_change_24h": percent_change_24h,
                "percent_change_7d": percent_change_7d,
                "volume_24h_usd": volume_24h,
            })
        except KeyError as e:
            print(f"Missing data for a currency: {e}")

    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)

    print(f"Data saved to {output_file}")
    return output_file


def generate_predictions(data_file):
    """Generates predictions using an external AI model and saves them to a JSON file."""
    api_host = "api.perplexity.ai"
    api_endpoint = "/chat/completions"
    perplexity_api_key =  os.getenv("PPLX_API_KEY")

    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m-%d-%Y")
    output_dir = "predictions"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{tomorrow_date} prediction.json")

    try:
        with open(data_file, "r") as file:
            cryptocurrency_data = json.load(file)
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    prompt = (
        "Do not provide anything but the JSON array, and ensure all 100 cryptocurrencies are included with ranks."
        "You are an AI model specialized in cryptocurrency market predictions."
        "Using the given cryptocurrency data and factoring in recent shifts in regulatory policies or announcements from major economies, predict the next day's price and market cap for each cryptocurrency."
        "Provide the output as a JSON array with each cryptocurrency's name, rank, predicted market cap in USD, predicted price in USD, percent_change_1h, percent_change_24h, percent_change_7d, and volume_24h_usd."
        "Ensure your predictions reflect the potential influence of these regulatory changes on market sentiment and performance."
        "Again provide nothing more than the JSON Array! Get all 100 companies do not fail the json!"
    )

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI model specialized in cryptocurrency market predictions."
            },
            {
                "role": "user",
                "content": (
                    f"Here is the cryptocurrency data: {json.dumps(cryptocurrency_data)}\n\n"
                    + prompt
                )
            }
        ],
        "max_tokens": 10000,
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": False
    }

    payload_json = json.dumps(payload)

    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }

    try:
        connection = http.client.HTTPSConnection(api_host)
        connection.request("POST", api_endpoint, body=payload_json, headers=headers)
        response = connection.getresponse()

        if response.status != 200:
            print(f"Error: Received status code {response.status}")
            print(f"Response: {response.read().decode('utf-8')}")
            return

        response_data = response.read().decode("utf-8")
        response_json = json.loads(response_data)
        content = response_json["choices"][0]["message"]["content"]
        clean_content = re.sub(r"```json|```", "", content).strip()

        # Add quotes around property names if missing
        clean_content = re.sub(r"(['\w]+):", r'"\1":', clean_content)

        try:
            predictions = json.loads(clean_content)
            with open(output_file, "w") as file:
                json.dump(predictions, file, indent=4)
            print(f"Predictions saved to {output_file}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON Content: {clean_content}")
            raise e

    except Exception as e:
        print(f"An error occurred: {e}")


def daily_task():
    """Runs the daily task of fetching data and generating predictions."""
    print("Running daily task...")
    data_file = fetch_and_save_data()
    if data_file:
        generate_predictions(data_file)


if __name__ == "__main__":
    daily_task()
