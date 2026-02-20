import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Constants
CSV_FILE = "poe2_market_history.csv"
OUTPUT_DIR = "plots"

def plot_currency_trend(target_id="exalted"):
    """
    Reads market data and saves an inverted trend plot into the plots/ folder.
    """
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} does not exist. Run poe_analytics.py first.")
        return

    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    try:
        df = pd.read_csv(CSV_FILE)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='mixed')
    except Exception as e:
        print(f"Read error: {e}")
        return

    currency_df = df[df["ID"] == target_id].copy()

    if currency_df.empty:
        print(f"❌ Data for ID '{target_id}' not found. Available: {df['ID'].unique()}")
        return

    # Inversion Logic: 1 Divine = X Currency
    currency_df["Exchange_Rate"] = 1 / currency_df["Price_in_Divine"]
    currency_df = currency_df.sort_values(by="Timestamp")

    plt.figure(figsize=(12, 6))
    plt.plot(
        currency_df["Timestamp"],
        currency_df["Exchange_Rate"],
        marker="o", linestyle="-", color="green",
        label=f"1 Divine to {target_id.capitalize()}"
    )

    plt.title(f"POE2 Exchange Rate: 1 Divine = X {target_id.capitalize()}", fontsize=14)
    plt.xlabel("Date/Time", fontsize=12)
    plt.ylabel(f"Amount of {target_id.capitalize()} per Divine", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Save filename inside the plots/ folder
    output_path = os.path.join(OUTPUT_DIR, f"divine_to_{target_id}_rate.png")
    plt.savefig(output_path)

    print(f"✅ Plot successfully saved to: {output_path}")
    latest_rate = currency_df["Exchange_Rate"].iloc[-1]
    print(f"📊 Latest Market Rate: 1 Divine = {latest_rate:.2f} {target_id}")

if __name__ == "__main__":
    selected_currency = sys.argv[1] if len(sys.argv) > 1 else "exalted"
    plot_currency_trend(selected_currency)