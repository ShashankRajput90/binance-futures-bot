# src/app.py
import streamlit as st
from src.bot import BasicBot
from src.bot import BasicBot             # <--- FIX
from src.config import API_KEY, API_SECRET # <--- FIX
from src.logger_setup import logger    # <--- FIX
import time
# Use st.cache_resource to initialize the bot only once
@st.cache_resource
def get_bot():
    try:
        bot = BasicBot(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
        return bot
    except Exception as e:
        st.error(f"Failed to initialize bot: {e}")
        return None

# Function to read the log file
def get_log_content():
    try:
        with open("bot.log", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Log file not found."

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("📈 Binance Futures Trading Bot (Testnet)")

# Initialize bot
bot = get_bot()
if bot is None:
    st.stop()

# Create tabs for different order types and logs
tab_market, tab_limit, tab_bonus, tab_logs = st.tabs([
    "Market Order", 
    "Limit Order", 
    "Bonus (Stop-Limit)", 
    "Bot Logs"
])

# --- Market Order Tab ---
with tab_market:
    st.header("Place a Market Order")
    with st.form("market_order_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            market_symbol = st.text_input("Symbol (e.g., BTCUSDT)", "BTCUSDT")
        with col2:
            market_side = st.selectbox("Side", ["BUY", "SELL"], key="market_side")
        with col3:
            market_quantity = st.number_input("Quantity", min_value=0.001, value=0.001, format="%.3f")
        
        market_submitted = st.form_submit_button("Place Market Order")
        
        if market_submitted:
            with st.spinner("Placing market order..."):
                order = bot.place_market_order(market_symbol, market_side, market_quantity)
                if order:
                    st.success("Market order placed successfully!")
                    st.json(order)
                else:
                    st.error("Failed to place market order. Check logs for details.")

# --- Limit Order Tab ---
with tab_limit:
    st.header("Place a Limit Order")
    with st.form("limit_order_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            limit_symbol = st.text_input("Symbol (e.g., BTCUSDT)", "BTCUSDT", key="limit_symbol")
        with col2:
            limit_side = st.selectbox("Side", ["BUY", "SELL"], key="limit_side")
        with col3:
            limit_quantity = st.number_input("Quantity", min_value=0.001, value=0.001, format="%.3f", key="limit_qty")
        with col4:
            limit_price = st.number_input("Limit Price", min_value=0.01, value=50000.0, format="%.2f")
            
        limit_submitted = st.form_submit_button("Place Limit Order")

        if limit_submitted:
            with st.spinner("Placing limit order..."):
                order = bot.place_limit_order(limit_symbol, limit_side, limit_quantity, limit_price)
                if order:
                    st.success("Limit order placed successfully!")
                    st.json(order)
                else:
                    st.error("Failed to place limit order. Check logs for details.")

# --- Bonus (Stop-Limit) Order Tab ---
with tab_bonus:
    st.header("Place a Stop-Limit Order (Bonus)")
    with st.form("stop_limit_order_form"):
        st.info("This places a Limit order (at 'Limit Price') once the 'Stop Price' is reached.")
        col1, col2, col3 = st.columns(3)
        with col1:
            sl_symbol = st.text_input("Symbol (e.g., BTCUSDT)", "BTCUSDT", key="sl_symbol")
        with col2:
            sl_side = st.selectbox("Side", ["BUY", "SELL"], key="sl_side")
        with col3:
            sl_quantity = st.number_input("Quantity", min_value=0.001, value=0.001, format="%.3f", key="sl_qty")
        
        col4, col5 = st.columns(2)
        with col4:
            sl_stop_price = st.number_input("Stop Price (Trigger)", min_value=0.01, value=40000.0, format="%.2f")
        with col5:
            sl_limit_price = st.number_input("Limit Price (Order)", min_value=0.01, value=39990.0, format="%.2f")

        sl_submitted = st.form_submit_button("Place Stop-Limit Order")

        if sl_submitted:
            with st.spinner("Placing stop-limit order..."):
                order = bot.place_stop_limit_order(sl_symbol, sl_side, sl_quantity, sl_stop_price, sl_limit_price)
                if order:
                    st.success("Stop-Limit order placed successfully!")
                    st.json(order)
                else:
                    st.error("Failed to place stop-limit order. Check logs for details.")

# --- Log Display Tab ---
with tab_logs:
    st.header("Real-time Bot Logs")
    log_placeholder = st.empty()
    
    # Auto-refreshing log display
    while True:
        log_content = get_log_content()
        log_placeholder.code(log_content, language="log")
        time.sleep(2) # Refresh every 2 seconds