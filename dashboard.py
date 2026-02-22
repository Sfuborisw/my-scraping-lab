import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="POE2 Market Pro Analytics", layout="wide")

CSV_FILE = "poe2_market_history.csv"

def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()
    df = pd.read_csv(CSV_FILE)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='mixed')
    # 1 Divine = X Currency
    df["Exchange_Rate"] = 1 / df["Price_in_Divine"]
    return df

st.title("💎 POE2 Market Pro Analytics")
st.markdown("Advanced market trend tracking with interactive visualization.")

df = load_data()

if df.empty:
    st.warning("No data found. Ensure the scraper is running.")
else:
    # --- Sidebar Control ---
    st.sidebar.header("Market Controls")
    all_currencies = df["ID"].unique().tolist()

    # Allow multiple selection for comparison
    selected_ids = st.sidebar.multiselect(
        "Select Currencies to Compare",
        options=all_currencies,
        default=["exalted", "chaos"] if "exalted" in all_currencies else all_currencies[:1]
    )

    # --- Metrics Section ---
    st.subheader("Current Market Snapshots")
    cols = st.columns(len(selected_ids) if selected_ids else 1)

    for i, cid in enumerate(selected_ids):
        c_data = df[df["ID"] == cid].sort_values("Timestamp")
        if len(c_data) >= 1:
            latest_val = c_data.iloc[-1]["Exchange_Rate"]
            delta = 0
            if len(c_data) > 1:
                delta = latest_val - c_data.iloc[-2]["Exchange_Rate"]

            cols[i].metric(
                label=f"1 Div to {cid.upper()}",
                value=f"{latest_val:.2f}",
                delta=f"{delta:.2f}"
            )

    # --- Interactive Plotly Chart ---
    st.divider()
    st.subheader("Interactive Price History")

    fig = go.Figure()

    for cid in selected_ids:
        c_data = df[df["ID"] == cid].sort_values("Timestamp")
        fig.add_trace(go.Scatter(
            x=c_data["Timestamp"],
            y=c_data["Exchange_Rate"],
            mode='lines+markers',
            name=cid.capitalize(),
            hovertemplate='%{x}<br>Rate: %{y:.2f} ' + cid.capitalize()
        ))

    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        xaxis_title="Time (PST)",
        yaxis_title="Exchange Rate",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20),
        height=500
    )

    # Show the interactive plot
    st.plotly_chart(fig, use_container_width=True)

    # --- Moving Average Logic (Extra Detail) ---
    if st.sidebar.checkbox("Show 24h Moving Average"):
        st.info("💡 Moving averages help filter out 'market noise' to show long-term trends.")
        # Note: This requires more data points to be meaningful

# Footer info
st.caption(f"Backend Synchronized | Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")