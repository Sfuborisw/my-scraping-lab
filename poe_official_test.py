import requests
import json
import os

# Professional User-Agent is REQUIRED for GGG API
USER_AGENT = "POE2DataTracker/1.0 (Contact: Sfuborisw via GitHub)"


def test_official_api():
    # The 'trade2/data/static' endpoint contains all item IDs used by the official trade site
    url = "https://www.pathofexile.com/api/trade2/data/static"

    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    try:
        print("Connecting to Path of Exile Official API...")
        response = requests.get(url, headers=headers)

        # Handle common API errors gracefully
        if response.status_code == 403:
            print("❌ Error 403: Access Denied. Check your User-Agent or IP block.")
            return
        elif response.status_code == 429:
            print("❌ Error 429: Too Many Requests. GGG is asking you to slow down!")
            return

        response.raise_for_status()  # Raise error for other 4xx/5xx codes
        data = response.json()

        print("✅ Successfully connected to GGG Official API!")

        # Explore the structure: data['result'] is a list of categories
        # Category 0 is usually 'Currency'
        if "result" in data:
            currency_group = data["result"][0]
            print(f"\nGroup Label: {currency_group.get('label')}")

            # Print the first 10 official currency IDs
            print("First 10 Official Currency Entries:")
            entries = currency_group.get("entries", [])[:10]
            for entry in entries:
                print(f" - ID: {entry.get('id')} | Name: {entry.get('text')}")

            # Save the full map for future reference
            with open("official_static_map.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(
                f"\n📁 Full static map saved to: {os.path.abspath('official_static_map.json')}"
            )

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Failed: {e}")


if __name__ == "__main__":
    test_official_api()
