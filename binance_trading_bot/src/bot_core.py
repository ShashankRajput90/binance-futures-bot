"""
Binance Futures Trading Bot - Core Module
Author: [Your Name]
Date: October 2025
"""

import os
import logging
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *

class BinanceFuturesBot:
    """Core trading bot class for Binance Futures USDT-M"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the Binance Futures Bot
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (True) or production (False)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Initialize client
        if testnet:
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.API_URL = 'https://testnet.binancefuture.com'
        else:
            self.client = Client(api_key, api_secret)
        
        # Setup logging
        self.setup_logging()
        self.logger.info(f"Bot initialized in {'TESTNET' if testnet else 'PRODUCTION'} mode")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'bot_{datetime.now().strftime("%Y%m%d")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    def test_connection(self) -> dict:
        """
        Test API connection and credentials
        
        Returns:
            dict with status and message
        """
        try:
            # Test basic connectivity
            self.client.ping()
            
            # Test API credentials
            account = self.client.futures_account()
            
            return {
                'success': True,
                'message': 'Connection successful! API credentials are valid.',
                'balance': float(account.get('totalWalletBalance', 0))
            }
        except BinanceAPIException as e:
            error_msg = f"API Error {e.code}: {e.message}"
            if e.code == -1022:
                error_msg += "\n\n FIX: This is a signature error. Common causes:\n"
                error_msg += "1. Invalid API Key or Secret - Double check your credentials\n"
                error_msg += "2. Time sync issue - The bot will try to auto-sync\n"
                error_msg += "3. Wrong testnet/production setting\n"
                error_msg += "4. API key doesn't have Futures permission enabled"
            return {
                'success': False,
                'message': error_msg
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Connection error: {str(e)}"
            }
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists and is tradable"""
        try:
            info = self.client.futures_exchange_info()
            symbols = [s['symbol'] for s in info['symbols'] if s['status'] == 'TRADING']
            return symbol in symbols
        except Exception as e:
            self.logger.error(f"Error validating symbol: {e}")
            return False
    
    def get_symbol_info(self, symbol: str) -> dict:
        """Get symbol precision and filters"""
        try:
            info = self.client.futures_exchange_info()
            for s in info['symbols']:
                if s['symbol'] == symbol:
                    return s
            return None
        except Exception as e:
            self.logger.error(f"Error getting symbol info: {e}")
            return None
    
    def round_step_size(self, quantity: float, step_size: float) -> float:
        """Round quantity to step size"""
        precision = len(str(step_size).split('.')[-1].rstrip('0'))
        return round(quantity - (quantity % step_size), precision)
    
    def get_account_balance(self) -> float:
        """Get USDT balance"""
        try:
            balance = self.client.futures_account_balance()
            for asset in balance:
                if asset['asset'] == 'USDT':
                    return float(asset['balance'])
            return 0.0
        except Exception as e:
            self.logger.error(f"Error getting balance: {e}")
            return 0.0
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Place a market order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            
        Returns:
            Order response dict
        """
        try:
            # Validate inputs
            if not self.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if side not in ['BUY', 'SELL']:
                raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")
            
            if quantity <= 0:
                raise ValueError(f"Invalid quantity: {quantity}. Must be positive")
            
            # Get symbol info for precision
            symbol_info = self.get_symbol_info(symbol)
            if not symbol_info:
                raise ValueError(f"Could not get info for {symbol}")
            
            # Round quantity
            for filter_item in symbol_info['filters']:
                if filter_item['filterType'] == 'LOT_SIZE':
                    step_size = float(filter_item['stepSize'])
                    quantity = self.round_step_size(quantity, step_size)
            
            self.logger.info(f"Placing MARKET {side} order: {symbol} | Quantity: {quantity}")
            
            # Place order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            
            self.logger.info(f"Order placed successfully: {order['orderId']}")
            self.logger.info(f"Order details: {order}")
            
            return {
                'success': True,
                'order': order,
                'message': f"Market {side} order placed successfully"
            }
            
        except BinanceAPIException as e:
            error_msg = f"Binance API Error: {e.status_code} - {e.message}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except BinanceOrderException as e:
            error_msg = f"Binance Order Error: {e.status_code} - {e.message}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Error placing market order: {str(e)}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """
        Place a limit order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            
        Returns:
            Order response dict
        """
        try:
            # Validate inputs
            if not self.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if side not in ['BUY', 'SELL']:
                raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")
            
            if quantity <= 0:
                raise ValueError(f"Invalid quantity: {quantity}. Must be positive")
            
            if price <= 0:
                raise ValueError(f"Invalid price: {price}. Must be positive")
            
            # Get symbol info
            symbol_info = self.get_symbol_info(symbol)
            if not symbol_info:
                raise ValueError(f"Could not get info for {symbol}")
            
            # Round quantity and price
            for filter_item in symbol_info['filters']:
                if filter_item['filterType'] == 'LOT_SIZE':
                    step_size = float(filter_item['stepSize'])
                    quantity = self.round_step_size(quantity, step_size)
                elif filter_item['filterType'] == 'PRICE_FILTER':
                    tick_size = float(filter_item['tickSize'])
                    price = self.round_step_size(price, tick_size)
            
            self.logger.info(f"Placing LIMIT {side} order: {symbol} | Quantity: {quantity} | Price: {price}")
            
            # Place order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            
            self.logger.info(f"Order placed successfully: {order['orderId']}")
            self.logger.info(f"Order details: {order}")
            
            return {
                'success': True,
                'order': order,
                'message': f"Limit {side} order placed successfully"
            }
            
        except BinanceAPIException as e:
            error_msg = f"Binance API Error: {e.status_code} - {e.message}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except BinanceOrderException as e:
            error_msg = f"Binance Order Error: {e.status_code} - {e.message}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Error placing limit order: {str(e)}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_current_price(self, symbol: str) -> float:
        """Get current price for symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Error getting price: {e}")
            return 0.0
    
    def get_open_orders(self, symbol: str = None) -> list:
        """Get open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.futures_get_open_orders()
            return orders
        except Exception as e:
            self.logger.error(f"Error getting open orders: {e}")
            return []
    
    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancel an order"""
        try:
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order {order_id} cancelled successfully")
            return {'success': True, 'result': result}
        except Exception as e:
            error_msg = f"Error cancelling order: {str(e)}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
