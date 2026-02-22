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

Then, launch the web dashboard in a new terminal:
Bash
streamlit run dashboard.py

3. Generating Trend Visuals
Generate charts for specific currencies by passing arguments:

Bash
# General usage: python plot_trends.py [currency_id]
python plot_trends.py exalted
python plot_trends.py chaos
Output: All charts are saved as PNG files in the /plots folder.

Logic: Automatically inverts values to show the intuitive "1 Divine = X" format.


🏗️ Production Roadmap (Next Steps)
This project is currently in Phase 1 (MVP). To transition into a full-scale production system, the following architecture is planned:

Phase 2: Cloud Integration & Persistence
AWS Lambda Migration: Convert the standalone Python scraper into a serverless AWS Lambda function triggered by EventBridge (cron job).

S3 Data Lake: Store historical CSVs and JSON snapshots in Amazon S3 for long-term persistence and cross-region accessibility.

Phase 3: Frontend Modernization
React Migration: Replace the Streamlit frontend with a React.js application for better performance, custom UI components, and sub-second interaction latency.

FastAPI Backend: Implement a robust REST API using FastAPI to serve data from S3/Database to the React frontend.

Phase 4: Full Cloud Deployment
Containerization: Dockerize the backend services.

CI/CD: Implement GitHub Actions for automated testing and deployment to AWS Amplify (Frontend) and AWS App Runner (Backend).


⚠️ Important Notes
Data Integrity: If you have mixed date formats from previous versions, the current tool uses format='mixed' to ensure compatibility.
Rate Limits: Do not manually decrease the fetching interval below 1 minute to avoid being flagged by Poe.ninja.


📖 Future Research: Official API Integration
While the current version utilizes the stable Poe.ninja API, the long-term goal includes exploring the Path of Exile Developer Documentation.

https://www.pathofexile.com/developer/docs

Objective: Study OAuth2 authentication and Rate Limit management to potentially integrate direct trade data or private stash monitoring.

Status: In the research phase to understand the specific data structures provided by the official POE2 endpoints.