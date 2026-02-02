import pandas as pd


# Load the data from your CSV file
def analyze_stocks():
    file_name = "stock_data.csv"

    try:
        # Read the CSV
        df = pd.read_csv(file_name)

        # 1. Clean data: Convert Price to numeric (in case it's a string)
        df["Price"] = pd.to_numeric(df["Price"].replace(",", "", regex=True))

        # 2. Simple Calculation: Get the average price
        avg_price = df["Price"].mean()
        max_price = df["Price"].max()
        min_price = df["Price"].min()

        print("--- Stock Analysis Report ---")
        print(f"Total entries: {len(df)}")
        print(f"Average Price: ${avg_price:.2f}")
        print(f"Highest Price: ${max_price:.2f}")
        print(f"Lowest Price:  ${min_price:.2f}")

    except FileNotFoundError:
        print("CSV file not found. Run main.py first to collect some data!")


if __name__ == "__main__":
    analyze_stocks()
