"""
TWAP (Time-Weighted Average Price) Strategy
Splits large orders into smaller chunks over time
"""

import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def execute_twap_order(bot, symbol: str, side: str, total_quantity: float,
                      num_orders: int, interval_seconds: int) -> dict:
    """
    Execute TWAP strategy - split order into smaller chunks

    Args:
        bot: BinanceFuturesBot instance
        symbol: Trading pair
        side: 'BUY' or 'SELL'
        total_quantity: Total quantity to trade
        num_orders: Number of orders to split into
        interval_seconds: Time interval between orders

    Returns:
        Dict with all executed orders
    """
    try:
        # Validate inputs
        if not bot.validate_symbol(symbol):
            raise ValueError(f"Invalid symbol: {symbol}")

        if side not in ['BUY', 'SELL']:
            raise ValueError(f"Invalid side: {side}")

        if total_quantity <= 0 or num_orders <= 0 or interval_seconds <= 0:
            raise ValueError("All values must be positive")

        # Calculate quantity per order
        quantity_per_order = total_quantity / num_orders

        # Get symbol info for rounding
        symbol_info = bot.get_symbol_info(symbol)
        if not symbol_info:
            raise ValueError(f"Could not get info for {symbol}")

        for filter_item in symbol_info['filters']:
            if filter_item['filterType'] == 'LOT_SIZE':
                step_size = float(filter_item['stepSize'])
                quantity_per_order = bot.round_step_size(quantity_per_order, step_size)

        logger.info(f"Starting TWAP execution for {symbol}")
        logger.info(f"Total: {total_quantity} | Orders: {num_orders} | Interval: {interval_seconds}s")
        logger.info(f"Quantity per order: {quantity_per_order}")

        executed_orders = []

        for i in range(num_orders):
            logger.info(f"Executing order {i+1}/{num_orders}")

            # Place market order
            result = bot.place_market_order(symbol, side, quantity_per_order)

            if result['success']:
                executed_orders.append(result['order'])
                logger.info(f"Order {i+1} executed successfully")
            else:
                logger.error(f"Order {i+1} failed: {result.get('error')}")
                break

            # Wait before next order (except for last order)
            if i < num_orders - 1:
                logger.info(f"Waiting {interval_seconds} seconds...")
                time.sleep(interval_seconds)

        return {
            'success': True,
            'executed_orders': executed_orders,
            'total_executed': len(executed_orders),
            'message': f'TWAP executed: {len(executed_orders)}/{num_orders} orders'
        }

    except Exception as e:
        error_msg = f"Error executing TWAP: {str(e)}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
