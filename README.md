💎 POE2 Market Analysis Tool (Fate of the Vaal)
This project is a dedicated market monitoring system for Path of Exile 2. It automates data collection from the POE.Ninja API, logs the history into CSV files, and generates visual price trend charts.

🚀 Getting Started (Step-by-Step)
1. Environment Setup
Ensure your Python environment is isolated and clean:

Create Environment: python -m venv venv

Activate (Git Bash): source venv/Scripts/activate

Install Dependencies:

Bash
pip install requests pandas matplotlib
2. Run the Data Logger
Start the automated process to record market data:

Command: python poe_analytics.py

How it works: The script fetches currency prices for the Fate of the Vaal league every hour.

Storage: Data is appended to poe2_market_history.csv with timestamps.

Stop: Press Ctrl + C to safely close the logger.

3. Generate Trend Charts
Once you have collected at least two data points, you can visualize the trends:

Command: python plot_trends.py

Function: It reads your CSV and opens a window showing the price curve for specific currencies (e.g., Divine Orbs or Alchemy Orbs).

🔍 Development Notes
How to Update the API URL
If the league changes (e.g., to Settlers2), follow these steps:

Open poe.ninja in your browser.

Press F12 -> Network Tab -> Filter by overview or exchange.

Locate the JSON response and copy the Request URL.

Update the URL variable in poe_analytics.py.

Data Mapping Logic
ID Mapping: Since the API returns short IDs (e.g., alch), the script uses an id_map dictionary to convert them into readable names like Alchemy Orb.

Price Calculation: The primaryValue represents the relative value (e.g., 1 small currency unit per 1 Divine). The script calculates 1 / value to get the actual exchange ratio (e.g., 1 Divine = 500 Alch).

⚠️ Best Practices & Warnings
Rate Limiting: The default interval is 3600 seconds (1 hour). Do not set the wait time below 60 seconds, or you risk being IP-banned by POE.Ninja.

Git Management: It is recommended to add *.csv to your .gitignore to avoid pushing large, outdated data files to GitHub.

Uptime: Do not close the Git Bash window while the logger is running, as it will terminate the process.

🛠️ Roadmap
[ ] Implement Price Alerts (e.g., notify when Divine price drops).

[ ] Add support for Unique Item price tracking.

[ ] Auto-generate daily PDF market reports.