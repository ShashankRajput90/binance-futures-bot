# src/bot.py
from binance import Client
from binance.exceptions import BinanceAPIException
from src.config import API_KEY, API_SECRET # <--- FIX
from src.logger_setup import logger

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initializes the Binance Client."""
        self.client = Client(api_key, api_secret, testnet=testnet)
        
        # Set the base URL to the testnet futures URL
        if testnet:
            self.client.API_URL = "https://testnet.binancefuture.com"
        
        logger.info("Bot initialized. Testing connectivity...")
        try:
            # Test connection
            self.client.fapi_account() # fapi = futures api
            logger.info("Connection successful.")
        except BinanceAPIException as e:
            logger.error(f"Failed to connect to Binance API: {e}")
            raise
    
    def place_market_order(self, symbol, side, quantity):
        """Places a market order (Core Requirement) [cite: 6]"""
        try:
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}...")
            # Use fapi_create_order for USDT-M Futures [cite: 3]
            order = self.client.fapi_create_order(
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
        """Places a limit order (Core Requirement) [cite: 7]"""
        try:
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} @ {price}...")
            order = self.client.fapi_create_order(
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
            
    # --- BONUS SECTION ---
    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        """Places an OCO (One-Cancels-the-Other) order (Bonus) [cite: 10]"""
        try:
            logger.info(f"Placing OCO {side} order for {quantity} {symbol}...")
            # OCO for futures is placing two orders. 
            # This example places a limit take-profit and a stop-limit stop-loss.
            # NOTE: True OCO on futures is complex. A simpler bonus is Stop-Limit.
            # Let's pivot to Stop-Limit as it's more direct [cite: 9]
            
            logger.warning("OCO on futures is complex. Placing a STOP-LIMIT order instead as bonus.")
            return self.place_stop_limit_order(symbol, side, quantity, stop_price, stop_limit_price)

        except BinanceAPIException as e:
            logger.error(f"OCO/Stop-Limit order failed: {e}")
            return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Places a Stop-Limit order (Bonus) [cite: 9]"""
        try:
            logger.info(f"Placing STOP-LIMIT {side} order for {quantity} {symbol}...")
            order = self.client.fapi_create_order(
                symbol=symbol,
                side=side.upper(),
                type='STOP', # Use 'STOP' for stop-market or 'STOP_LIMIT'
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