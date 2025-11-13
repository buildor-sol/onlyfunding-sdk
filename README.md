![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)
![TypeScript](https://img.shields.io/badge/typescript-4.0+-blue.svg)
![Go](https://img.shields.io/badge/go-1.18+-00ADD8.svg)
![Rust](https://img.shields.io/badge/rust-1.60+-orange.svg)
![Node.js](https://img.shields.io/badge/node.js-16+-green.svg)

# onlyfunding.fun SDK

Official SDK for accessing the onlyfunding.fun API, providing real-time cryptocurrency funding rates data from 24+ exchanges.

## Overview

onlyfunding.fun provides real-time funding rates data from major cryptocurrency exchanges including Binance, Bybit, OKX, Hyperliquid, Drift, and more. This SDK provides easy integration for various programming languages.

**API Endpoint:** `https://api.onlyfunding.fun/funding`

## Features

- ✅ Real-time funding rates from 24+ exchanges
- ✅ Normalized symbol names for easy comparison
- ✅ Open interest rankings
- ✅ Multi-language support
- ✅ Type-safe implementations
- ✅ Error handling and retry logic
- ✅ Rate limit management

## Quick Start

### Python

```python
from onlyfunding_sdk import onlyfundingClient

client = onlyfundingClient()
data = client.get_funding_rates()

# Get funding rate for BTC on Binance
btc_rate = data.funding_rates['binance_1_perp']['BTC']
print(f"BTC funding rate: {btc_rate / 10000}%")
```

### JavaScript/TypeScript

```typescript
import { onlyfundingClient } from '@onlyfunding/sdk';

const client = new onlyfundingClient();
const data = await client.getFundingRates();

// Get funding rate for BTC on Binance
const btcRate = data.fundingRates.binance_1_perp.BTC;
console.log(`BTC funding rate: ${btcRate / 10000}%`);
```

### Go

```go
package main

import (
    "fmt"
    "github.com/onlyfunding/go-sdk"
)

func main() {
    client := onlyfunding.NewClient()
    data, err := client.GetFundingRates()
    if err != nil {
        panic(err)
    }
    
    // Get funding rate for BTC on Binance
    btcRate := data.FundingRates["binance_1_perp"]["BTC"]
    fmt.Printf("BTC funding rate: %.4f%%\n", float64(btcRate)/10000)
}
```

### Rust

```rust
use onlyfunding_sdk::onlyfundingClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = onlyfundingClient::new();
    let data = client.get_funding_rates().await?;
    
    // Get funding rate for BTC on Binance
    let btc_rate = data.funding_rates["binance_1_perp"]["BTC"];
    println!("BTC funding rate: {:.4}%", btc_rate as f64 / 10000.0);
    
    Ok(())
}
```

## Installation

### Python

```bash
pip install onlyfunding-sdk
```

### JavaScript/TypeScript

```bash
npm install @onlyfunding/sdk
# or
yarn add @onlyfunding/sdk
```

### Go

```bash
go get github.com/onlyfunding/go-sdk
```

### Rust

```toml
[dependencies]
onlyfunding-sdk = "0.1.0"
tokio = { version = "1.0", features = ["full"] }
```

## API Response Format

```json
{
  "symbols": ["BTC", "ETH", "SOL", "DOGE", ...],
  "exchanges": {
    "exchange_names": [
      {"name": "binance_1_perp", "display": "BINANCE"},
      {"name": "bybit_1_perp", "display": "BYBIT"},
      ...
    ],
    "exchanges": ["binance_1_perp", "bybit_1_perp", ...]
  },
  "funding_rates": {
    "binance_1_perp": {
      "BTC": 8,
      "ETH": -15,
      "SOL": 25,
      ...
    },
    "bybit_1_perp": {
      "BTC": 12,
      "ETH": -10,
      "SOL": 30,
      ...
    }
  },
  "oi_rankings": {
    "BTC": "1",
    "ETH": "2",
    "SOL": "3",
    ...
  },
  "default_oi_rank": "500+",
  "timestamp": "2024-01-15 14:30:25"
}
```

**Note:** Funding rates are multiplied by 10,000 for precision. A value of `25` represents `0.0025` or `0.25%`.

## Examples

### Find Arbitrage Opportunities

```python
from onlyfunding_sdk import onlyfundingClient

client = onlyfundingClient()
data = client.get_funding_rates()

# Find best funding rate spread for BTC
symbol = "BTC"
rates = {}

for exchange, symbols in data.funding_rates.items():
    if symbol in symbols:
        rates[exchange] = symbols[symbol]

if rates:
    max_rate = max(rates.values())
    min_rate = min(rates.values())
    spread = max_rate - min_rate
    
    max_exchange = [k for k, v in rates.items() if v == max_rate][0]
    min_exchange = [k for k, v in rates.items() if v == min_rate][0]
    
    print(f"Best spread for {symbol}: {spread/10000}%")
    print(f"Long on {min_exchange}, Short on {max_exchange}")
```

### Monitor Funding Rates

```typescript
import { onlyfundingClient } from '@onlyfunding/sdk';

const client = new onlyfundingClient();

async function monitorRates() {
    setInterval(async () => {
        const data = await client.getFundingRates();
        
        // Monitor BTC rates
        const btcRates = Object.entries(data.fundingRates)
            .map(([exchange, symbols]) => ({
                exchange,
                rate: symbols.BTC
            }))
            .filter(r => r.rate !== undefined);
        
        console.log('Current BTC funding rates:');
        btcRates.forEach(({ exchange, rate }) => {
            console.log(`${exchange}: ${(rate / 10000).toFixed(4)}%`);
        });
    }, 60000); // Update every 60 seconds
}

monitorRates();
```

### Filter by Exchange

```go
package main

import (
    "fmt"
    "github.com/onlyfunding/go-sdk"
)

func main() {
    client := onlyfunding.NewClient()
    data, _ := client.GetFundingRates()
    
    // Get all rates from Binance
    binanceRates := data.FundingRates["binance_1_perp"]
    
    fmt.Println("Binance Funding Rates:")
    for symbol, rate := range binanceRates {
        fmt.Printf("%s: %.4f%%\n", symbol, float64(rate)/10000)
    }
}
```

## Supported Exchanges

- Binance
- Bybit
- OKX
- Hyperliquid
- Drift
- Gate.io
- KuCoin
- MEXC
- BingX
- Bitget
- And 14+ more exchanges...

## Rate Limits

API data is updated every 60 seconds. While there are no strict rate limits, please maintain reasonable intervals between requests. There's no point in making requests more frequently than once every 60 seconds.

## Error Handling

All SDK implementations include proper error handling:

```python
from onlyfunding_sdk import onlyfundingClient, onlyfundingError

client = onlyfundingClient()
try:
    data = client.get_funding_rates()
except onlyfundingError as e:
    print(f"API Error: {e.message}")
except Exception as e:
    print(f"Network Error: {e}")
```

## Exchange Notes

- **Extended, Hyperliquid, Lighter, Vest:** These exchanges use 1-hour funding intervals. Rates are multiplied by 8 for comparison with exchanges using 8-hour intervals.
- **Symbol Normalization:** Symbols are cleaned and normalized to remove quote currencies and separators for uniform comparison.
- **Quote Currency Priority:** When multiple quote currencies are available, the API prioritizes USDT → USD → USDC → BUSD → UST.

## Commercial Use

If you use this API for commercial purposes, you must attribute the source by linking to [onlyfunding.fun](https://onlyfunding.fun).

Required attribution format:
```html
Funding rates data provided by <a href="https://onlyfunding.fun">onlyfunding.fun</a>
```

## Links

- **Website:** [https://onlyfunding.fun](https://onlyfunding.fun)
- **API Documentation:** [https://onlyfunding.fun/api-docs](https://onlyfunding.fun/api-docs)
- **Twitter:** [@onlyfunding_fun](https://x.com/onlyfunding_fun)
- **GitHub:** [https://github.com/onlyfunding/onlyfunding-sdk](https://github.com/onlyfunding/onlyfunding-sdk)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

