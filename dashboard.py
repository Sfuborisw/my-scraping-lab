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
GOLD_TAX_FILE = "gold_tax.json"

def load_market_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(), {}
    
    try:
        df = pd.read_csv(CSV_FILE, on_bad_lines='warn')
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='mixed', errors='coerce')
        df = df.dropna(subset=["Timestamp"])
        # Exchange Rate: 1 Divine to X item
        df["Exchange_Rate"] = 1 / df["Price_in_Divine"]
        # Inverse Rate: 1 item to X Divine
        df["Inverse_Rate"] = df["Price_in_Divine"]
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return pd.DataFrame(), {}
    
    icon_map = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Combine items for icon mapping
            all_items = data.get("core", {}).get("items", []) + data.get("items", [])
            for item in all_items:
                icon_map[item["id"]] = f"{NINJA_BASE_URL}{item['image']}"
                
    return df, icon_map

def load_gold_tax():
    if not os.path.exists(GOLD_TAX_FILE):
        return {}
    with open(GOLD_TAX_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("tax_rates", {})

# --- Load Data ---
df, icon_map = load_market_data()
GOLD_TAX_TABLE = load_gold_tax()

# --- UI Setup ---
st.title("💎 POE2 Market Pro Analytics")

if df.empty:
    st.warning("Please wait for data to be collected... Check if poe2_market_history.csv exists.")
else:
    # --- 1. Data Processing (Move this up!) ---
    st.sidebar.header("Navigation")
    all_currencies = sorted(df["ID"].unique().tolist())
    selected_id = st.sidebar.selectbox("Select Currency", all_currencies)

    st.sidebar.divider()
    view_mode = st.sidebar.radio(
        "Display Mode:",
        ["1 Divine ➔ X Item", "X Item ➔ 1 Divine"]
    )

    # Define these BEFORE the calculator needs them
    currency_df = df[df["ID"] == selected_id].sort_values("Timestamp")
    latest_val = currency_df.iloc[-1]

    # --- 2. Sidebar: Arbitrage Calculator Section ---
    st.sidebar.divider()
    st.sidebar.header("📊 Arbitrage Calculator")

    base_investment = st.sidebar.number_input("Investment (Divine)", value=10.0, step=1.0)
    d_to_e = st.sidebar.number_input("D to E Ratio", value=370.0)
    e_to_a = st.sidebar.number_input("E to A Ratio", value=140.0)
    a_to_d = st.sidebar.number_input("A to D Ratio", value=2.0)

    # Logic
    total_e = base_investment * d_to_e
    total_a = total_e / e_to_a
    final_d = total_a * a_to_d
    profit_val = final_d - base_investment
    profit_pct = (profit_val / base_investment) if base_investment != 0 else 0

    # Gold Estimation
    tax_e = GOLD_TAX_TABLE.get("exalted", 100)
    tax_a = GOLD_TAX_TABLE.get("alch", 100) 
    tax_d = GOLD_TAX_TABLE.get("divine", 100)
    total_gold_cost = (total_e * tax_e) + (total_a * tax_a) + (final_d * tax_d)

    # Display Sidebar Results
    st.sidebar.subheader("Results")
    if final_d > base_investment:
        st.sidebar.success(f"📈 Profit: {profit_pct:.1%}")
    else:
        st.sidebar.error(f"📉 Loss: {profit_pct:.1%}")

    st.sidebar.write(f"Final Amount: **{final_d:.4f} D**")
    st.sidebar.write(f"Net Profit: **{profit_val:.4f} D**")
    st.sidebar.divider()
    st.sidebar.subheader("💰 Estimated Gold Fee")
    st.sidebar.write(f"Total Gold Needed: **{total_gold_cost:,.0f}**")

    if profit_val > 0:
        gold_per_1d = total_gold_cost / profit_val
        st.sidebar.info(f"Efficiency: **{gold_per_1d:,.0f} Gold / 1D Profit**")
    else:
        st.sidebar.warning("No profit to calculate efficiency.")

    # --- 3. Main Page UI (Icons & Header) ---
    divine_icon = icon_map.get("divine", "")
    target_icon = icon_map.get(selected_id, "")

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

    # --- 4. Plotly Chart ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=currency_df["Timestamp"],
        y=currency_df[chart_val],
        mode='lines+markers',
        line=dict(color='#00ffcc', width=3),
        marker=dict(size=6, color='#ffffff'),
        hovertemplate='%{y:.4f}<extra></extra>'
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title=y_label,
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 5. Metrics Section ---
    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Latest Rate", f"{display_price:.4f}")
    with m2:
        if len(currency_df) > 1:
            change = display_price - currency_df.iloc[-2][chart_val]
            st.metric("Last Move", f"{change:.4f}", delta=f"{change:.6f}")
    with m3:
        tax = GOLD_TAX_TABLE.get(selected_id.lower(), "N/A")
        st.metric("Gold Fee (per Unit)", f"{tax}")
    with m4:
        if tax != "N/A":
            total_tax_display = tax * 100
            st.metric("Gold for 100 Units", f"{total_tax_display:,}")