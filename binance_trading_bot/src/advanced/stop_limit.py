"""
Stop-Limit Order Implementation
"""

import logging
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

logger = logging.getLogger(__name__)

def place_stop_limit_order(bot, symbol: str, side: str, quantity: float, 
                          stop_price: float, limit_price: float) -> dict:
    """
    Place a stop-limit order

    Args:
        bot: BinanceFuturesBot instance
        symbol: Trading pair
        side: 'BUY' or 'SELL'
        quantity: Order quantity
        stop_price: Stop trigger price
        limit_price: Limit order price after stop is triggered

    Returns:
        Order response dict
    """
    try:
        # Validate inputs
        if not bot.validate_symbol(symbol):
            raise ValueError(f"Invalid symbol: {symbol}")

        if side not in ['BUY', 'SELL']:
            raise ValueError(f"Invalid side: {side}")

        if quantity <= 0 or stop_price <= 0 or limit_price <= 0:
            raise ValueError("All prices and quantity must be positive")

        # Get symbol info
        symbol_info = bot.get_symbol_info(symbol)
        if not symbol_info:
            raise ValueError(f"Could not get info for {symbol}")

        # Round values
        for filter_item in symbol_info['filters']:
            if filter_item['filterType'] == 'LOT_SIZE':
                step_size = float(filter_item['stepSize'])
                quantity = bot.round_step_size(quantity, step_size)
            elif filter_item['filterType'] == 'PRICE_FILTER':
                tick_size = float(filter_item['tickSize'])
                stop_price = bot.round_step_size(stop_price, tick_size)
                limit_price = bot.round_step_size(limit_price, tick_size)

        logger.info(f"Placing STOP-LIMIT {side} order: {symbol}")
        logger.info(f"Quantity: {quantity} | Stop: {stop_price} | Limit: {limit_price}")

        # Place order
        order = bot.client.futures_create_order(
            symbol=symbol,
            side=side,
            type='STOP',
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price
        )

        logger.info(f"Stop-Limit order placed: {order['orderId']}")

        return {
            'success': True,
            'order': order,
            'message': f"Stop-Limit {side} order placed successfully"
        }

    except BinanceAPIException as e:
        error_msg = f"Binance API Error: {e.status_code} - {e.message}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = f"Error placing stop-limit order: {str(e)}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
