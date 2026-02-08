import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_FILE = "poe2_market_history.csv"


def plot_currency_trend(target_id="divine"):
    if not os.path.exists(CSV_FILE):
        print(
            f"Error: {CSV_FILE} does not exist. Please run poe_analytics.py to collect data first."
        )
        return

    df = pd.DataFrame()
    try:
        df = pd.read_csv(CSV_FILE)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    except Exception as e:
        print(f"Read error: {e}")
        return

    currency_df = df[df["ID"] == target_id]

    if currency_df.empty:
        print(f"Data for ID '{target_id}' not found.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(
        currency_df["Timestamp"],
        currency_df["Price_in_Divine"],
        marker="o",
        linestyle="-",
        color="b",
        label=f"{target_id.capitalize()} Price",
    )

    plt.title(
        f"POE2 {target_id.capitalize()} Price Trend (Fate of the Vaal)", fontsize=14
    )
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Price (Relative Value)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    print("Generating Plot...")
    plt.show()


if __name__ == "__main__":
    plot_currency_trend("alch")
