# src/main.py
import argparse
from .bot import BasicBot
from .config import API_KEY, API_SECRET
from .logger_setup import logger

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI [cite: 3]")
    
    # Subparsers for different order types
    subparsers = parser.add_subparsers(dest='order_type', required=True)

    # Market Order Parser [cite: 6]
    market_parser = subparsers.add_parser('market', help='Place a market order')
    market_parser.add_argument('symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    market_parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    market_parser.add_argument('quantity', type=float, help='Order quantity')

    # Limit Order Parser [cite: 7]
    limit_parser = subparsers.add_parser('limit', help='Place a limit order')
    limit_parser.add_argument('symbol', type=str, help='Trading symbol')
    limit_parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    limit_parser.add_argument('quantity', type=float, help='Order quantity')
    limit_parser.add_argument('price', type=float, help='Order price')

    # (Bonus) Stop-Limit Order Parser [cite: 9]
    stop_limit_parser = subparsers.add_parser('stop_limit', help='Place a stop-limit order')
    stop_limit_parser.add_argument('symbol', type=str, help='Trading symbol')
    stop_limit_parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    stop_limit_parser.add_argument('quantity', type=float, help='Order quantity')
    stop_limit_parser.add_argument('stop_price', type=float, help='The price to trigger the limit order')
    stop_limit_parser.add_argument('limit_price', type=float, help='The price of the limit order')

    args = parser.parse_args()

    try:
        bot = BasicBot(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
        
        if args.order_type == 'market':
            bot.place_market_order(args.symbol, args.side, args.quantity)
        
        elif args.order_type == 'limit':
            bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)
            
        elif args.order_type == 'stop_limit':
            bot.place_stop_limit_order(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()