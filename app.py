"""
Binance Futures Trading Bot - Streamlit UI
A professional trading interface for Binance Futures Testnet
"""

import streamlit as st
import sys
import os
from datetime import datetime
import json

# Ensure current directory is on sys.path for local imports (works with Streamlit)
sys.path.append(os.path.dirname(__file__))

from binance_trading_bot.src.bot_core import BinanceFuturesBot
from binance_trading_bot.src.advanced.stop_limit import place_stop_limit_order
from binance_trading_bot.src.advanced.oco import place_oco_order
from binance_trading_bot.src.advanced.twap import execute_twap_order
from binance_trading_bot.src.advanced.grid_strategy import create_grid_orders

# Page configuration
st.set_page_config(
    page_title="Binance Futures Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stApp { font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
    .main-header { display:none; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bot' not in st.session_state:
    st.session_state.bot = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'order_history' not in st.session_state:
    st.session_state.order_history = []

# Main header removed per user request

# Sidebar removed the header per user request; keep inputs for API credentials
with st.sidebar:
    api_key = st.text_input("API Key", type="password", help="Enter your Binance Testnet API Key")
    api_secret = st.text_input("API Secret", type="password", help="Enter your Binance Testnet API Secret")
    use_testnet = st.checkbox("Use Testnet", value=True, help="Uncheck for production (NOT RECOMMENDED)")

    if st.button("Connect to Binance", use_container_width=True):
        if api_key and api_secret:
            try:
                with st.spinner("Connecting and syncing time with Binance..."):
                    st.session_state.bot = BinanceFuturesBot(api_key, api_secret, testnet=use_testnet)
                    test_result = st.session_state.bot.test_connection()
                    if test_result['success']:
                        st.session_state.authenticated = True
                        st.success(f"{test_result['message']}")
                        st.info(f"Wallet Balance: ${test_result.get('balance', 0):,.2f} USDT")
                    else:
                        st.error(f"{test_result['message']}")
                        st.session_state.authenticated = False
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
                st.session_state.authenticated = False
        else:
            st.warning("Please enter both API Key and Secret")

    if st.session_state.authenticated:
        try:
            balance = st.session_state.bot.get_account_balance()
            st.metric("USDT Balance", f"${balance:,.2f}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Main content
if not st.session_state.authenticated:
    st.info("👈 Please connect to Binance using your API credentials in the sidebar")

    # Display setup instructions
    st.markdown("### 🚀 Getting Started")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Step 1: Create Testnet Account")
        st.markdown("""
        1. Visit [testnet.binancefuture.com](https://testnet.binancefuture.com)
        2. Log in with your Binance account or GitHub
        3. You'll receive 15,000 USDT in virtual funds
        """)

    with col2:
        st.markdown("#### Step 2: Generate API Keys")
        st.markdown("""
        1. Go to API Management in your testnet account
        2. Click 'Create API'
        3. Save your API Key and Secret securely
        4. Enter them in the sidebar to connect
        """)

else:
    # Trading Interface
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Market Orders", 
        "📈 Limit Orders", 
        "🎯 Stop-Limit", 
        "🔄 OCO Orders",
        "⏱️ TWAP Strategy",
        "📐 Grid Trading"
    ])

    # Tab 1: Market Orders
    with tab1:
        st.markdown('<div class="sub-header">Market Orders</div>', unsafe_allow_html=True)
        st.markdown("Execute orders immediately at current market price")

        col1, col2 = st.columns(2)

        with col1:
            symbol_market = st.text_input("Symbol", value="BTCUSDT", key="market_symbol")
            quantity_market = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.001, key="market_qty")

        with col2:
            side_market = st.selectbox("Side", ["BUY", "SELL"], key="market_side")

            if st.button("🚀 Place Market Order", use_container_width=True):
                with st.spinner("Placing order..."):
                    result = st.session_state.bot.place_market_order(
                        symbol_market, side_market, quantity_market
                    )

                    if result['success']:
                        st.success(result['message'])
                        st.json(result['order'])
                        st.session_state.order_history.append(result['order'])
                    else:
                        st.error(result.get('error', 'Unknown error'))

    # Tab 2: Limit Orders
    with tab2:
        st.markdown('<div class="sub-header">Limit Orders</div>', unsafe_allow_html=True)
        st.markdown("Place orders that execute only at specified price or better")

        col1, col2 = st.columns(2)

        with col1:
            symbol_limit = st.text_input("Symbol", value="BTCUSDT", key="limit_symbol")
            quantity_limit = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.001, key="limit_qty")

        with col2:
            price_limit = st.number_input("Limit Price", min_value=0.01, value=50000.0, step=0.01, key="limit_price")
            side_limit = st.selectbox("Side", ["BUY", "SELL"], key="limit_side")

        if st.button("📝 Place Limit Order", use_container_width=True):
            with st.spinner("Placing order..."):
                result = st.session_state.bot.place_limit_order(
                    symbol_limit, side_limit, quantity_limit, price_limit
                )

                if result['success']:
                    st.success(result['message'])
                    st.json(result['order'])
                    st.session_state.order_history.append(result['order'])
                else:
                    st.error(result.get('error', 'Unknown error'))

    # Tab 3: Stop-Limit Orders
    with tab3:
        st.markdown('<div class="sub-header">Stop-Limit Orders</div>', unsafe_allow_html=True)
        st.markdown("Trigger a limit order when stop price is reached")

        col1, col2 = st.columns(2)

        with col1:
            symbol_sl = st.text_input("Symbol", value="BTCUSDT", key="sl_symbol")
            quantity_sl = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.001, key="sl_qty")
            stop_price = st.number_input("Stop Price", min_value=0.01, value=48000.0, step=0.01, key="sl_stop")

        with col2:
            limit_price_sl = st.number_input("Limit Price", min_value=0.01, value=47900.0, step=0.01, key="sl_limit")
            side_sl = st.selectbox("Side", ["BUY", "SELL"], key="sl_side")

        if st.button("🎯 Place Stop-Limit Order", use_container_width=True):
            with st.spinner("Placing order..."):
                result = place_stop_limit_order(
                    st.session_state.bot, symbol_sl, side_sl, 
                    quantity_sl, stop_price, limit_price_sl
                )

                if result['success']:
                    st.success(result['message'])
                    st.json(result['order'])
                    st.session_state.order_history.append(result['order'])
                else:
                    st.error(result.get('error', 'Unknown error'))

    # Tab 4: OCO Orders
    with tab4:
        st.markdown('<div class="sub-header">OCO (One-Cancels-the-Other) Orders</div>', unsafe_allow_html=True)
        st.markdown("Place take-profit and stop-loss orders simultaneously")

        col1, col2 = st.columns(2)

        with col1:
            symbol_oco = st.text_input("Symbol", value="BTCUSDT", key="oco_symbol")
            quantity_oco = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.001, key="oco_qty")
            tp_price = st.number_input("Take Profit Price", min_value=0.01, value=52000.0, step=0.01, key="oco_tp")

        with col2:
            sl_price = st.number_input("Stop Loss Price", min_value=0.01, value=48000.0, step=0.01, key="oco_sl")
            side_oco = st.selectbox("Side", ["BUY", "SELL"], key="oco_side")

        if st.button("🔄 Place OCO Orders", use_container_width=True):
            with st.spinner("Placing orders..."):
                result = place_oco_order(
                    st.session_state.bot, symbol_oco, side_oco,
                    quantity_oco, tp_price, sl_price
                )

                if result['success']:
                    st.success(result['message'])
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Take Profit Order:**")
                        st.json(result['take_profit_order'])
                    with col_b:
                        st.markdown("**Stop Loss Order:**")
                        st.json(result['stop_loss_order'])
                else:
                    st.error(result.get('error', 'Unknown error'))

    # Tab 5: TWAP Strategy
    with tab5:
        st.markdown('<div class="sub-header">TWAP (Time-Weighted Average Price)</div>', unsafe_allow_html=True)
        st.markdown("Split large orders into smaller chunks over time")

        col1, col2 = st.columns(2)

        with col1:
            symbol_twap = st.text_input("Symbol", value="BTCUSDT", key="twap_symbol")
            total_qty_twap = st.number_input("Total Quantity", min_value=0.001, value=0.1, step=0.01, key="twap_qty")
            num_orders = st.number_input("Number of Orders", min_value=2, value=5, step=1, key="twap_num")

        with col2:
            interval_sec = st.number_input("Interval (seconds)", min_value=1, value=10, step=1, key="twap_interval")
            side_twap = st.selectbox("Side", ["BUY", "SELL"], key="twap_side")

        if st.button("⏱️ Execute TWAP Strategy", use_container_width=True):
            with st.spinner(f"Executing {num_orders} orders..."):
                result = execute_twap_order(
                    st.session_state.bot, symbol_twap, side_twap,
                    total_qty_twap, num_orders, interval_sec
                )

                if result['success']:
                    st.success(result['message'])
                    st.markdown(f"**Executed {result['total_executed']}/{num_orders} orders**")
                    with st.expander("View All Orders"):
                        for idx, order in enumerate(result['executed_orders'], 1):
                            st.markdown(f"**Order {idx}:**")
                            st.json(order)
                else:
                    st.error(result.get('error', 'Unknown error'))

    # Tab 6: Grid Trading
    with tab6:
        st.markdown('<div class="sub-header">Grid Trading Strategy</div>', unsafe_allow_html=True)
        st.markdown("Automated buy-low/sell-high within a price range")

        col1, col2 = st.columns(2)

        with col1:
            symbol_grid = st.text_input("Symbol", value="BTCUSDT", key="grid_symbol")
            lower_price = st.number_input("Lower Price", min_value=0.01, value=45000.0, step=100.0, key="grid_lower")
            upper_price = st.number_input("Upper Price", min_value=0.01, value=55000.0, step=100.0, key="grid_upper")

        with col2:
            grid_levels = st.number_input("Grid Levels", min_value=2, value=10, step=1, key="grid_levels")
            qty_per_grid = st.number_input("Quantity per Grid", min_value=0.001, value=0.01, step=0.001, key="grid_qty")

        if st.button("📐 Create Grid", use_container_width=True):
            with st.spinner("Creating grid orders..."):
                result = create_grid_orders(
                    st.session_state.bot, symbol_grid, lower_price,
                    upper_price, grid_levels, qty_per_grid
                )

                if result['success']:
                    st.success(result['message'])
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Buy Orders: {len(result['buy_orders'])}**")
                        with st.expander("View Buy Orders"):
                            for order in result['buy_orders']:
                                st.json(order)
                    with col_b:
                        st.markdown(f"**Sell Orders: {len(result['sell_orders'])}**")
                        with st.expander("View Sell Orders"):
                            for order in result['sell_orders']:
                                st.json(order)
                else:
                    st.error(result.get('error', 'Unknown error'))

    # Order History removed per user request

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>⚠️ <strong>TESTNET MODE</strong> - No real funds are at risk</p>
        <p>Built for Binance Futures Trading Bot Assignment | Python Developer Role</p>
    </div>
""", unsafe_allow_html=True)
