# 🚀 Binance Futures Trading Bot

Professional CLI and Streamlit UI for Binance USDT-M Futures trading with market, limit, and OCO orders.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Binance](https://img.shields.io/badge/binance-testnet-yellow)

## ✨ Features

### Core Features (Mandatory)
- ✅ **Market Orders**: Immediate execution at market price
- ✅ **Limit Orders**: Execute at specific price levels
- ✅ **Input Validation**: Comprehensive parameter validation
- ✅ **Error Handling**: Robust exception handling
- ✅ **Structured Logging**: All trades logged to `bot.log`

### Bonus Features
- ✅ **OCO Orders**: Take-profit and stop-loss simultaneously
- ✅ **Streamlit UI**: Beautiful web interface
- ✅ **CLI Support**: Command-line trading

## 📦 Prerequisites

- Python 3.8+
- Binance Futures Testnet account
- API Key and Secret

## 🛠️ Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/ShashankRajput90/Shashank_Lodhi_binance_bot.git
cd Shashank_Lodhi_binance_bot
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

### Streamlit UI (Recommended)

```bash
cd src
streamlit run app.py
```

Open browser at `http://localhost:8501`

**Using the UI:**
1. Enter API Key and Secret in sidebar
2. Click "Connect"
3. View your balance
4. Select order type tab
5. Enter details and place orders

### Python API

```python
from src.bot import BasicBot

Initialize
bot = BasicBot(api_key="your_key", api_secret="your_secret", testnet=True)

Market order
bot.place_market_order("BTCUSDT", "BUY", 0.01)

Limit order
bot.place_limit_order("BTCUSDT", "SELL", 0.01, 50000.0)

OCO order
from src.advanced.oco import place_oco_order
place_oco_order(bot, "BTCUSDT", "SELL", 0.01, 52000.0, 48000.0)
```

## 📁 Project Structure

```
binance-futures-bot/
│
├── src/
│ ├── init.py                     # Package init
│ ├── bot.py                      # BasicBot class
│ ├── config.py                   # Configuration
│ ├── logger_setup.py             # Logging setup
│ ├── app.py                      # Streamlit UI ⭐
│ └── advanced/
│ ├── init.py
│ └── oco.py                      # OCO orders
├── bot.log                       # Trading logs
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
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
