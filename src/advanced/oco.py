"""
OCO (One-Cancels-the-Other) Order Implementation
Simulates OCO by placing Take Profit and Stop Loss orders
"""

import logging
from binance.enums import *
from binance.exceptions import BinanceAPIException

logger = logging.getLogger('BinanceBot')

def place_oco_order(bot, symbol: str, side: str, quantity: float,
                   take_profit_price: float, stop_loss_price: float) -> dict:
    """
    Simulate OCO order with TP and SL orders
    
    Args:
        bot: BasicBot instance
        symbol: Trading symbol (e.g., 'BTCUSDT')
        side: 'BUY' or 'SELL' (for closing position)
        quantity: Order quantity
        take_profit_price: Take profit trigger price
        stop_loss_price: Stop loss trigger price
        
    Returns:
        Response dict with both orders or error
    """
    try:
        # Validate inputs
        if not bot.validate_symbol(symbol):
            return {'success': False, 'error': f'Invalid symbol: {symbol}'}
        
        if side not in ['BUY', 'SELL']:
            return {'success': False, 'error': 'Side must be BUY or SELL'}
        
        if quantity <= 0 or take_profit_price <= 0 or stop_loss_price <= 0:
            return {'success': False, 'error': 'All values must be positive'}
        
        # Validate and round values
        result = bot.validate_and_round(symbol, quantity, take_profit_price)
        if not result:
            return {'success': False, 'error': 'Failed to validate parameters'}
        
        quantity, take_profit_price = result
        _, stop_loss_price = bot.validate_and_round(symbol, quantity, stop_loss_price)
        
        logger.info(f"Placing OCO orders for {symbol}")
        logger.info(f"TP: {take_profit_price} | SL: {stop_loss_price}")
        
        # Place Take Profit order
        tp_order = bot.client.futures_create_order(
            symbol=symbol,
            side=side,
            type='TAKE_PROFIT_MARKET',
            quantity=quantity,
            stopPrice=take_profit_price
        )
        
        logger.info(f"✓ Take Profit order placed: {tp_order['orderId']}")
        
        # Place Stop Loss order
        sl_order = bot.client.futures_create_order(
            symbol=symbol,
            side=side,
            type='STOP_MARKET',
            quantity=quantity,
            stopPrice=stop_loss_price
        )
        
        logger.info(f"✓ Stop Loss order placed: {sl_order['orderId']}")
        
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
