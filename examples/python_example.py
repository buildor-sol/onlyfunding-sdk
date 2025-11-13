#!/usr/bin/env python3
"""
Example usage of onlyfunding.fun Python SDK
Demonstrates basic functionality for working with funding rates API
"""

from onlyfunding_sdk import onlyfundingClient

def main():
    client = onlyfundingClient()
    
    print("=== onlyfunding.fun SDK Example ===\n")
    
    # Get all funding rates
    print("Loading funding rates...")
    data = client.get_funding_rates()
    print(f"✓ Found {len(data.symbols)} symbols across {len(data.exchanges['exchanges'])} exchanges\n")
    
    # Get specific rate
    print("Getting BTC funding rate on Binance...")
    btc_rate = client.get_rate('binance_1_perp', 'BTC')
    if btc_rate:
        print(f"✓ BTC funding rate: {btc_rate:.4f}%\n")
    else:
        print("✗ Rate not found\n")
    
    # Find arbitrage opportunities
    print("Finding arbitrage opportunities for BTC (min spread: 0.01%)...")
    opportunities = client.find_arbitrage_opportunities('BTC', min_spread=0.01)
    print(f"✓ Found {len(opportunities)} opportunities\n")
    
    if opportunities:
        print("Top 5 opportunities:")
        for i, opp in enumerate(opportunities[:5], 1):
            print(f"\n{i}. {opp['symbol']} - Spread: {opp['spread']:.4f}%")
            print(f"   Long:  {opp['long_exchange']} ({opp['rate1']:.4f}%)")
            print(f"   Short: {opp['short_exchange']} ({opp['rate2']:.4f}%)")

if __name__ == "__main__":
    main()

