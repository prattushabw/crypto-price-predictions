import os
import pandas as pd
import json
import matplotlib.pyplot as plt

actual_data_path = "./cryptocurrency_data/"
predicted_data_path = "./predictions/"

comparison_date = "12-3-2024"

actual_file = os.path.join(actual_data_path, f"{comparison_date} data.json")
predicted_file = os.path.join(predicted_data_path, f"{comparison_date} prediction.json")

if not os.path.exists(actual_file):
    print(f"Actual data file for {comparison_date} not found!")
elif not os.path.exists(predicted_file):
    print(f"Prediction file for {comparison_date} not found!")
else:
    with open(actual_file, 'r') as f:
        actual_data = json.load(f)

    with open(predicted_file, 'r') as f:
        predicted_data = json.load(f)

    actual_df = pd.DataFrame(actual_data)
    predicted_df = pd.DataFrame(predicted_data)

    merged_df = pd.merge(
        actual_df[['name', 'price_usd']], 
        predicted_df[['name', 'predicted_price']], 
        on='name', 
        suffixes=('_actual', '_predicted')
    )

    merged_df['abs_error'] = (merged_df['price_usd'] - merged_df['predicted_price']).abs()
    mae = merged_df['abs_error'].mean()

    print(f"Comparison for {comparison_date}:")
    print(merged_df)
    print(f"\nMean Absolute Error (MAE): {mae}")

    ax = merged_df.plot(
        kind='bar', 
        x='name', 
        y=['price_usd', 'predicted_price'], 
        figsize=(12, 6),
        logy=True
    )
    plt.title(f"Actual vs Predicted Prices ({comparison_date}) [Log Scale]")
    plt.xlabel("Cryptocurrency")
    plt.ylabel("Price (USD) [Log Scale]")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
