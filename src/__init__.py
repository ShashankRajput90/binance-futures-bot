"""
Binance Futures Trading Bot Package
"""

from .bot import BasicBot
from .config import API_KEY, API_SECRET
from .logger_setup import setup_logger, logger

__version__ = '1.0.0'
__all__ = ['BasicBot', 'API_KEY', 'API_SECRET', 'setup_logger', 'logger']
