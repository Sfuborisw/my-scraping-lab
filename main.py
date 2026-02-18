import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import os


def save_to_csv(data):
    file_name = "stock_data.csv"
    # Create a DataFrame from the new data
    df_new = pd.DataFrame([data])

    # If file exists, append without header. Otherwise, create new file with header.
    if not os.path.isfile(file_name):
        df_new.to_csv(file_name, index=False)
    else:
        df_new.to_csv(file_name, mode="a", header=False, index=False)
    print(f"Data saved to {file_name}")


def get_stock_price(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})

        if price_tag:
            price = price_tag.get_text()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data_row = {"Timestamp": timestamp, "Symbol": symbol, "Price": price}
            print(f"Fetched: {data_row}")
            save_to_csv(data_row)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_stock_price("NVDA")
