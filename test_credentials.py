"""
Quick API Credentials Test Script
Run this to verify your Binance API credentials work correctly
"""

import os
from binance_trading_bot.src import BinanceFuturesBot

def test_credentials():
    print("=" * 60)
    print("Binance API Credentials Test")
    print("=" * 60)
    
    # Get credentials
    print("\nEnter your API credentials:")
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()
    
    testnet = input("Use Testnet? (y/n) [default: y]: ").strip().lower()
    use_testnet = testnet != 'n'
    
    print(f"\n🔄 Testing connection to {'TESTNET' if use_testnet else 'PRODUCTION'}...")
    print("⏰ Syncing time with Binance server...")
    
    try:
        # Initialize bot (will auto-sync time)
        bot = BinanceFuturesBot(api_key, api_secret, testnet=use_testnet)
        
        # Test connection
        result = bot.test_connection()
        
        print("\n" + "=" * 60)
        if result['success']:
            print("✅ SUCCESS!")
            print(f"   {result['message']}")
            print(f"   💰 Wallet Balance: ${result.get('balance', 0):,.2f} USDT")
            print("\n✨ Your credentials are working correctly!")
        else:
            print("❌ FAILED!")
            print(f"   {result['message']}")
            print("\n📋 Troubleshooting Steps:")
            print("   1. Verify your API Key and Secret are correct")
            print("   2. For testnet: https://testnet.binancefuture.com")
            print("   3. For production: https://www.binance.com")
            print("   4. Ensure 'Enable Futures' is checked for your API key")
            print("   5. Check if IP restrictions are set (if so, whitelist your IP)")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60)
        print("\n📋 Common Issues:")
        print("   • Invalid API credentials")
        print("   • Network connection problems")
        print("   • API key doesn't have Futures permission")
        print("   • Wrong testnet/production setting")

if __name__ == "__main__":
    test_credentials()
