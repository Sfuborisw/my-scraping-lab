💎 POE2 Market Analysis Tool (Poe.ninja Edition)
This project is a professional-grade market monitoring system for Path of Exile 2. It focuses on macro-economic trends by aggregating data from the Poe.ninja API, logging historical fluctuations, and generating visual analytics to help players make informed trading decisions.

🚀 Project Overview
The tool has evolved from a direct scraping attempt to a robust API-driven analysis suite. It tracks the exchange rates of various currencies (Exalted, Chaos, Alchemy, etc.) relative to the Divine Orb.

Key Features:
Automated Logging: Hourly data fetching with randomized jitters to prevent IP rate-limiting.

Historical Accuracy: Stores data in a structured CSV format, handling mixed date formats seamlessly.

Visual Analytics: Generates trend charts (Inverted Rates: 1 Divine = X Currency) and saves them in an organized plots/ directory.

Clean Architecture: Minimalist codebase focused on stability and performance in a Linux/Ubuntu environment.

🛠️ Getting Started
1. Environment Setup
Developed on Windows 11 using WARP (Ubuntu Terminal).

Bash
# Create Virtual Environment
python -m venv venv

# Activate Environment
source venv/bin/activate

# Install Required Packages
pip install requests pandas matplotlib
2. Running the Data Collector
The collector runs indefinitely until stopped.

Bash
python poe_analytics.py
Interval: 1 hour + random jitter (3600-3630s).

Target: poe2_market_history.csv

3. Generating Trend Visuals
Generate charts for specific currencies by passing arguments:

Bash
# General usage: python plot_trends.py [currency_id]
python plot_trends.py exalted
python plot_trends.py chaos
Output: All charts are saved as PNG files in the /plots folder.

Logic: Automatically inverts values to show the intuitive "1 Divine = X" format.

📂 Project Structure
Plaintext
.
├── plots/                  # Generated trend charts (.png)
├── venv/                   # Python virtual environment
├── poe2_market_history.csv # The core database (CSV)
├── poe_analytics.py        # Main data fetching script
├── plot_trends.py          # Visualization & graphing tool
├── README.md               # Documentation
└── .gitignore              # Git ignore rules

🔮 Future Vision: Market Web Portal
The next major phase of this project is to move beyond the terminal. I am planning to develop a Web-based Dashboard to provide a more interactive experience:

Live Web View: A responsive frontend to observe price movements in real-time.

Advanced Analytics: Integration of moving averages, volatility indicators, and "Buy/Sell" signals.

Comparison Engine: Overlaying multiple currency trends on a single interactive graph.

Data Export: Ability to filter historical data and export custom reports.

⚠️ Important Notes
Data Integrity: If you have mixed date formats from previous versions, the current tool uses format='mixed' to ensure compatibility.

Rate Limits: Do not manually decrease the fetching interval below 1 minute to avoid being flagged by Poe.ninja.

📖 Future Research: Official API Integration
While the current version utilizes the stable Poe.ninja API, the long-term goal includes exploring the Path of Exile Developer Documentation.

https://www.pathofexile.com/developer/docs

Objective: Study OAuth2 authentication and Rate Limit management to potentially integrate direct trade data or private stash monitoring.

Status: In the research phase to understand the specific data structures provided by the official POE2 endpoints.