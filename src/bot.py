# src/bot.py
from binance import Client
from binance.exceptions import BinanceAPIException
from src.config import API_KEY, API_SECRET
from src.logger_setup import logger

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initializes the Binance Client."""
        self.client = Client(api_key, api_secret)
        
        # --- FIX: Set the Futures Testnet URL ---
        # We must set the 'FUTURES_URL' attribute, not 'API_URL'
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        
        logger.info("Bot initialized. Testing connectivity...")
        try:
            # --- FIX: Use futures_account() instead of fapi_account() ---
            self.client.futures_account() # Check futures account connectivity
            logger.info("Connection successful.")
        except BinanceAPIException as e:
            logger.error(f"Failed to connect to Binance API: {e}")
            raise
    
    def place_market_order(self, symbol, side, quantity):
        """Places a market order (Core Requirement)"""
        try:
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}...")
            
            # --- FIX: Use futures_create_order() ---
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(), # 'BUY' or 'SELL'
                type='MARKET',
                quantity=quantity
            )
            logger.info(f"Market order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Market order failed: {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """Places a limit order (Core Requirement)"""
        try:
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} @ {price}...")

            # --- FIX: Use futures_create_order() ---
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC' # Good 'Til Canceled
            )
            logger.info(f"Limit order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Limit order failed: {e}")
            return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Places a Stop-Limit order (Bonus)"""
        try:
            logger.info(f"Placing STOP-LIMIT {side} order for {quantity} {symbol}...")

            # --- FIX: Use futures_create_order() ---
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='STOP', # 'STOP' is for Stop-Market. 'STOP_LIMIT' is correct.
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price, # This makes it a Stop-Limit
                timeInForce='GTC'
            )
            logger.info(f"Stop-Limit order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Stop-Limit order failed: {e}")
            return None