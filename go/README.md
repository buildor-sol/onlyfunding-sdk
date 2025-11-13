# onlyfunding.fun Go SDK

Official Go SDK for accessing the onlyfunding.fun funding rates API.

## Installation

```bash
go get github.com/onlyfunding/go-sdk
```

## Usage

```go
package main

import (
    "fmt"
    "github.com/onlyfunding/go-sdk"
)

func main() {
    client := onlyfunding.NewClient()
    
    // Get all funding rates
    data, err := client.GetFundingRates()
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Found %d symbols\n", len(data.Symbols))
    
    // Get specific rate
    rate, err := client.GetRate("binance_1_perp", "BTC")
    if err != nil {
        panic(err)
    }
    fmt.Printf("BTC rate: %.4f%%\n", rate)
    
    // Find arbitrage opportunities
    opportunities, err := client.FindArbitrageOpportunities("BTC", 0.01)
    if err != nil {
        panic(err)
    }
    
    for _, opp := range opportunities {
        fmt.Printf("Spread: %.4f%%\n", opp.Spread)
    }
}
```

## Documentation

See the main [SDK README](../README.md) for full documentation.

## Links

- **Website:** [https://onlyfunding.fun](https://onlyfunding.fun)
- **Twitter:** [@onlyfunding_fun](https://x.com/onlyfunding_fun)

