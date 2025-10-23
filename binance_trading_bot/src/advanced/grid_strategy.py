"""
Grid Trading Strategy
Places buy and sell orders at regular intervals within a price range
"""

import logging
from binance.enums import *

logger = logging.getLogger(__name__)

def create_grid_orders(bot, symbol: str, lower_price: float, upper_price: float,
                      grid_levels: int, quantity_per_grid: float) -> dict:
    """
    Create grid trading orders

    Args:
        bot: BinanceFuturesBot instance
        symbol: Trading pair
        lower_price: Lower bound of price range
        upper_price: Upper bound of price range
        grid_levels: Number of grid levels
        quantity_per_grid: Quantity for each grid order

    Returns:
        Dict with all placed orders
    """
    try:
        # Validate inputs
        if not bot.validate_symbol(symbol):
            raise ValueError(f"Invalid symbol: {symbol}")

        if lower_price >= upper_price:
            raise ValueError("Lower price must be less than upper price")

        if grid_levels < 2:
            raise ValueError("Grid levels must be at least 2")

        if quantity_per_grid <= 0:
            raise ValueError("Quantity must be positive")

        # Get current price
        current_price = bot.get_current_price(symbol)
        logger.info(f"Current price for {symbol}: {current_price}")

        # Calculate grid spacing
        price_range = upper_price - lower_price
        grid_spacing = price_range / (grid_levels - 1)

        # Get symbol info for rounding
        symbol_info = bot.get_symbol_info(symbol)
        if not symbol_info:
            raise ValueError(f"Could not get info for {symbol}")

        tick_size = None
        step_size = None
        for filter_item in symbol_info['filters']:
            if filter_item['filterType'] == 'PRICE_FILTER':
                tick_size = float(filter_item['tickSize'])
            elif filter_item['filterType'] == 'LOT_SIZE':
                step_size = float(filter_item['stepSize'])

        if not tick_size or not step_size:
            raise ValueError("Could not get symbol filters")

        quantity_per_grid = bot.round_step_size(quantity_per_grid, step_size)

        logger.info(f"Creating Grid Strategy for {symbol}")
        logger.info(f"Range: {lower_price} - {upper_price}")
        logger.info(f"Levels: {grid_levels} | Spacing: {grid_spacing}")

        buy_orders = []
        sell_orders = []

        # Place grid orders
        for i in range(grid_levels):
            grid_price = lower_price + (i * grid_spacing)
            grid_price = bot.round_step_size(grid_price, tick_size)

            # Place buy order below current price
            if grid_price < current_price:
                logger.info(f"Placing BUY order at {grid_price}")
                result = bot.place_limit_order(symbol, 'BUY', quantity_per_grid, grid_price)
                if result['success']:
                    buy_orders.append(result['order'])

            # Place sell order above current price
            elif grid_price > current_price:
                logger.info(f"Placing SELL order at {grid_price}")
                result = bot.place_limit_order(symbol, 'SELL', quantity_per_grid, grid_price)
                if result['success']:
                    sell_orders.append(result['order'])

        return {
            'success': True,
            'buy_orders': buy_orders,
            'sell_orders': sell_orders,
            'total_orders': len(buy_orders) + len(sell_orders),
            'message': f'Grid created: {len(buy_orders)} buy + {len(sell_orders)} sell orders'
        }

    except Exception as e:
        error_msg = f"Error creating grid: {str(e)}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
