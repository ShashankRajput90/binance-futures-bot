"""
OCO (One-Cancels-the-Other) Order Implementation
Note: Binance Futures doesn't support native OCO, so we simulate it
"""

import logging
from binance.enums import *
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)

def place_oco_order(bot, symbol: str, side: str, quantity: float,
                   take_profit_price: float, stop_loss_price: float) -> dict:
    """
    Simulate OCO order by placing take-profit and stop-loss orders

    Args:
        bot: BinanceFuturesBot instance
        symbol: Trading pair
        side: 'BUY' or 'SELL' (for closing position)
        quantity: Order quantity
        take_profit_price: Take profit price
        stop_loss_price: Stop loss price

    Returns:
        Order response dict with both orders
    """
    try:
        # Validate inputs
        if not bot.validate_symbol(symbol):
            raise ValueError(f"Invalid symbol: {symbol}")

        if side not in ['BUY', 'SELL']:
            raise ValueError(f"Invalid side: {side}")

        if quantity <= 0 or take_profit_price <= 0 or stop_loss_price <= 0:
            raise ValueError("All values must be positive")

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
                take_profit_price = bot.round_step_size(take_profit_price, tick_size)
                stop_loss_price = bot.round_step_size(stop_loss_price, tick_size)

        logger.info(f"Placing OCO orders for {symbol}")
        logger.info(f"TP: {take_profit_price} | SL: {stop_loss_price}")

        # Place Take Profit Market Order
        tp_order = bot.client.futures_create_order(
            symbol=symbol,
            side=side,
            type='TAKE_PROFIT_MARKET',
            quantity=quantity,
            stopPrice=take_profit_price
        )

        logger.info(f"Take Profit order placed: {tp_order['orderId']}")

        # Place Stop Loss Market Order
        sl_order = bot.client.futures_create_order(
            symbol=symbol,
            side=side,
            type='STOP_MARKET',
            quantity=quantity,
            stopPrice=stop_loss_price
        )

        logger.info(f"Stop Loss order placed: {sl_order['orderId']}")

        return {
            'success': True,
            'take_profit_order': tp_order,
            'stop_loss_order': sl_order,
            'message': 'OCO orders (TP & SL) placed successfully'
        }

    except BinanceAPIException as e:
        error_msg = f"Binance API Error: {e.status_code} - {e.message}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = f"Error placing OCO orders: {str(e)}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
