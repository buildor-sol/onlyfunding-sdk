# onlyfunding.fun Python SDK

Official Python SDK for accessing the onlyfunding.fun funding rates API.

## Installation

```bash
pip install onlyfunding-sdk
```

## Usage

```python
from onlyfunding_sdk import onlyfundingClient

client = onlyfundingClient()

# Get all funding rates
data = client.get_funding_rates()
print(f"Found {len(data.symbols)} symbols")

# Get specific rate
rate = client.get_rate('binance_1_perp', 'BTC')
print(f"BTC rate: {rate:.4f}%")

# Find arbitrage opportunities
opportunities = client.find_arbitrage_opportunities('BTC', min_spread=0.01)
for opp in opportunities:
    print(f"Spread: {opp['spread']:.4f}%")
```

## Documentation

See the main [SDK README](../README.md) for full documentation.

## Links

- **Website:** [https://onlyfunding.fun](https://onlyfunding.fun)
- **Twitter:** [@onlyfunding_fun](https://x.com/onlyfunding_fun)

