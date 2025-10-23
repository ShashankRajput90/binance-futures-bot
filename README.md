# 🚀 Binance Futures Trading Bot

A professional, feature-rich trading bot for Binance USDT-M Futures with a beautiful Streamlit UI interface.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Testnet](https://img.shields.io/badge/testnet-enabled-orange)

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Order Types](#order-types)
- [Screenshots](#screenshots)
- [Logging](#logging)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Features (Mandatory)
- ✅ **Market Orders**: Execute trades immediately at current market price
- ✅ **Limit Orders**: Place orders at specific price levels
- ✅ **Input Validation**: Comprehensive validation of symbols, quantities, and prices
- ✅ **Error Handling**: Robust exception handling with detailed error messages
- ✅ **Logging System**: Structured logging with timestamps and trade history

### Advanced Features (Bonus)
- ✅ **Stop-Limit Orders**: Conditional orders triggered at stop price
- ✅ **OCO (One-Cancels-the-Other)**: Simultaneous take-profit and stop-loss orders
- ✅ **TWAP Strategy**: Time-Weighted Average Price execution
- ✅ **Grid Trading**: Automated buy-low/sell-high within price ranges

### UI Features
- 🎨 **Beautiful Streamlit Interface**: Professional, responsive web UI
- 📊 **Real-time Balance Display**: Live USDT balance tracking
- 📜 **Order History**: View recent order executions
- 🎯 **Multiple Trading Modes**: Tabbed interface for different order types
- 🔐 **Secure API Management**: Protected credential input

## 📦 Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- API Key and Secret from Binance Testnet

## 🔧 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/binance-futures-bot.git
cd binance-futures-bot
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Get Binance Testnet API Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Log in with your Binance account or GitHub
3. Navigate to **API Management**
4. Click **Create API** and save your credentials
5. You'll receive 15,000 USDT in virtual funds

### Configure Environment Variables (Optional)

```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🚀 Usage

### Method 1: Streamlit UI (Recommended)

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

#### Using the UI:

1. **Connect to Binance**:
   - Enter your API Key and Secret in the sidebar
   - Click "Connect to Binance"
   - Verify your balance is displayed

2. **Place Orders**:
   - Navigate to the desired order type tab
   - Enter symbol (e.g., BTCUSDT), quantity, and price
   - Click the order button
   - View order confirmation and details

### Method 2: Python CLI

```python
from src.bot_core import BinanceFuturesBot

# Initialize bot
bot = BinanceFuturesBot(
    api_key="your_api_key",
    api_secret="your_api_secret",
    testnet=True
)

# Place market order
result = bot.place_market_order(
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.01
)

# Place limit order
result = bot.place_limit_order(
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.01,
    price=50000.0
)
```

## 📁 Project Structure

```
binance-futures-bot/
│
├── src/
│   ├── bot_core.py              # Core bot functionality
│   └── advanced/
│       ├── __init__.py
│       ├── stop_limit.py        # Stop-limit orders
│       ├── oco.py               # OCO orders
│       ├── twap.py              # TWAP strategy
│       └── grid_strategy.py     # Grid trading
│
├── logs/                        # Log files (auto-generated)
│   └── bot_YYYYMMDD.log
│
├── app.py                       # Streamlit UI application
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 📊 Order Types

### 1. Market Orders
Execute immediately at current market price.

**Use Case**: Quick entry/exit when price is acceptable

**Example**:
```python
bot.place_market_order("BTCUSDT", "BUY", 0.01)
```

### 2. Limit Orders
Execute only at specified price or better.

**Use Case**: Buy/sell at specific price levels

**Example**:
```python
bot.place_limit_order("BTCUSDT", "BUY", 0.01, 50000.0)
```

### 3. Stop-Limit Orders
Trigger a limit order when stop price is reached.

**Use Case**: Stop-loss or breakout trades

**Example**:
```python
from src.advanced import place_stop_limit_order
place_stop_limit_order(bot, "BTCUSDT", "SELL", 0.01, 48000.0, 47900.0)
```

### 4. OCO (One-Cancels-the-Other)
Place take-profit and stop-loss simultaneously.

**Use Case**: Risk management for open positions

**Example**:
```python
from src.advanced import place_oco_order
place_oco_order(bot, "BTCUSDT", "SELL", 0.01, 52000.0, 48000.0)
```

### 5. TWAP (Time-Weighted Average Price)
Split large orders into smaller chunks over time.

**Use Case**: Reduce market impact for large orders

**Example**:
```python
from src.advanced import execute_twap_order
execute_twap_order(bot, "BTCUSDT", "BUY", 0.1, num_orders=5, interval_seconds=10)
```

### 6. Grid Trading
Automated buy-low/sell-high within a price range.

**Use Case**: Range-bound market conditions

**Example**:
```python
from src.advanced import create_grid_orders
create_grid_orders(bot, "BTCUSDT", 45000.0, 55000.0, grid_levels=10, quantity_per_grid=0.01)
```

## 📝 Logging

All trading activities are logged to `logs/bot_YYYYMMDD.log` with:

- Timestamp
- Log level (INFO, WARNING, ERROR)
- Order details
- API responses
- Error traces

**Example Log Entry**:
```
2025-10-23 11:30:45 - __main__ - INFO - Bot initialized in TESTNET mode
2025-10-23 11:31:12 - __main__ - INFO - Placing MARKET BUY order: BTCUSDT | Quantity: 0.01
2025-10-23 11:31:13 - __main__ - INFO - Order placed successfully: 12345678
```

## 🧪 Testing

### Test on Binance Testnet

Always test with testnet before using real funds:

```python
bot = BinanceFuturesBot(api_key, api_secret, testnet=True)  # Safe testing
```

### Verify Orders

Check your testnet account at [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

## 🔍 Troubleshooting

### Common Issues

**Issue**: `APIError(code=-1111): Precision is over the maximum`

**Solution**: The bot automatically handles precision, but ensure your quantity matches symbol requirements

---

**Issue**: `APIError(code=-2021): Order would immediately trigger`

**Solution**: For stop orders, ensure stop price is appropriate for market direction

---

**Issue**: `Connection Error`

**Solution**: Check your API credentials and testnet URL

---

**Issue**: `Insufficient Balance`

**Solution**: Ensure you have enough USDT in your testnet account

### Enable Debug Logging

Modify `bot_core.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # More verbose logs
```

## 📧 Submission

For the assignment submission:

1. Create a ZIP file: `[your_name]_binance_bot.zip`
2. Include:
   - All source code
   - `bot.log` file with execution logs
   - `report.pdf` with screenshots and analysis
   - This README.md

3. Email to:
   - saami@bajarangs.com
   - nagasai@bajarangs.com
   - chetan@bajarangs.com
   - CC: sonika@primetrade.ai

4. Subject: **"Junior Python Developer – Crypto Trading Bot"**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This bot is for educational purposes and Binance Futures Testnet only. Always test thoroughly before using with real funds. Trading cryptocurrencies carries risk.

---

## 📚 Resources

- [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [python-binance Documentation](https://python-binance.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built with ❤️ for the Binance Futures Trading Bot Assignment**

*For questions or support, please open an issue on GitHub*
