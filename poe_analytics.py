import random
import requests
import pandas as pd
import time
import os
from datetime import datetime

URL = "https://poe.ninja/poe2/api/economy/exchange/current/overview?league=Fate+of+the+Vaal&type=Currency"
CSV_FILE = "poe2_market_history.csv"


def fetch_and_save():
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching POE2 data...")
        response = requests.get(URL, headers=headers)
        data = response.json()
        lines = data.get("lines", [])

        if not lines:
            print("No data found.")
            return

        # 1. Extract data
        # Based on your previous RAW DATA, we take id and primaryValue
        extracted = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for line in lines:
            extracted.append(
                {
                    "Timestamp": timestamp,
                    "ID": line.get("id"),
                    "Price_in_Divine": line.get("primaryValue"),
                }
            )

        df_new = pd.DataFrame(extracted)

        # 2. Save to CSV
        # If the file does not exist, write with Header
        # If the file exists, append (mode='a') without Header
        file_exists = os.path.isfile(CSV_FILE)
        df_new.to_csv(CSV_FILE, mode="a", index=False, header=not file_exists)

        print(f"Successfully saved {len(df_new)} items to {CSV_FILE}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    print("--- POE2 Market Logger Started ---")
    print(f"Targeting CSV: {CSV_FILE}")
    print("Press Ctrl+C to stop the script.")

    try:
        while True:
            fetch_and_save()

            # 3. Set wait time
            # 1 hour = 60 minutes * 60 seconds = 3600 seconds
            print("Waiting for 1 hour for the next update...")
            wait_time = 3600 + random.randint(1, 30)
            print(f"Next update in {wait_time} seconds...")
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
