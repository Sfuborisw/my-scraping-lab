import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import json
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="POE2 Market Pro", layout="wide")

CSV_FILE = "poe2_market_history.csv"
JSON_FILE = "latest_market_data.json"
NINJA_BASE_URL = "https://web.poecdn.com"

def load_market_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(), {}
    
    try:
        df = pd.read_csv(CSV_FILE, on_bad_lines='warn')
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
        df = df.dropna(subset=["Timestamp"])
        # We store Price_in_Divine (e.g., Chaos = 0.00625)
        # 1 / 0.00625 = 160 (Exchange Rate)
        df["Exchange_Rate"] = 1 / df["Price_in_Divine"]
        df["Inverse_Rate"] = df["Price_in_Divine"] # X to 1 Divine
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return pd.DataFrame(), {}
    
    icon_map = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Combine core and general items for the icon map
            all_items = data.get("core", {}).get("items", []) + data.get("items", [])
            for item in all_items:
                icon_map[item["id"]] = f"{NINJA_BASE_URL}{item['image']}"
                
    return df, icon_map

# --- UI Setup ---
st.title("💎 POE2 Market Pro Analytics")
df, icon_map = load_market_data()

if df.empty:
    st.warning("Please wait for data to be collected...")
else:
    # --- Sidebar Controls ---
    st.sidebar.header("Navigation")
    all_currencies = sorted(df["ID"].unique().tolist())
    selected_id = st.sidebar.selectbox("Select Currency", all_currencies)
    
    st.sidebar.divider()
    # THE TOGGLE BUTTON
    view_mode = st.sidebar.radio(
        "Display Mode:",
        ["1 Divine ➔ X Item", "X Item ➔ 1 Divine"]
    )

    # --- Data Logic based on Toggle ---
    currency_df = df[df["ID"] == selected_id].sort_values("Timestamp")
    latest_val = currency_df.iloc[-1]
    divine_icon = icon_map.get("divine", "")
    target_icon = icon_map.get(selected_id, "")

    # --- Header Section ---
    col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
    
    if view_mode == "1 Divine ➔ X Item":
        display_price = latest_val["Exchange_Rate"]
        left_icon, right_icon = divine_icon, target_icon
        title_text = f"1 Divine = {display_price:.2f} {selected_id.upper()}"
        y_label = f"Amount of {selected_id}"
        chart_val = "Exchange_Rate"
    else:
        display_price = latest_val["Inverse_Rate"]
        left_icon, right_icon = target_icon, divine_icon
        title_text = f"1 {selected_id.upper()} = {display_price:.4f} Divine"
        y_label = "Price in Divine"
        chart_val = "Inverse_Rate"

    with col1:
        if left_icon: st.image(left_icon, width=45)
    with col2:
        st.markdown("<h2 style='text-align: center; margin-top: 5px;'>➔</h2>", unsafe_allow_html=True)
    with col3:
        if right_icon: st.image(right_icon, width=45)
    with col4:
        st.subheader(title_text)

    # --- Chart ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=currency_df["Timestamp"], 
        y=currency_df[chart_val],
        mode='lines+markers',
        line=dict(color='#00ffcc', width=4),
        marker=dict(size=8, color='#ffffff'),
        hovertemplate='%{y:.4f}<extra></extra>'
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Time (UTC)",
        yaxis_title=y_label,
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- Quick Info Metrics ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Latest Rate", f"{display_price:.4f}")
    with m2:
        # Calculate simple 24h change (if data exists)
        if len(currency_df) > 1:
            change = display_price - currency_df.iloc[-2][chart_val]
            st.metric("Last Move", f"{change:.4f}", delta=f"{change:.6f}")