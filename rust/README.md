# onlyfunding.fun Rust SDK

Official Rust SDK for accessing the onlyfunding.fun funding rates API.

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
onlyfunding-sdk = "0.1.0"
tokio = { version = "1.0", features = ["full"] }
```

## Usage

```rust
use onlyfunding_sdk::onlyfundingClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = onlyfundingClient::new();
    
    // Get all funding rates
    let data = client.get_funding_rates().await?;
    println!("Found {} symbols", data.symbols.len());
    
    // Get specific rate
    let rate = client.get_rate("binance_1_perp", "BTC").await?;
    println!("BTC rate: {:.4}%", rate);
    
    // Find arbitrage opportunities
    let opportunities = client.find_arbitrage_opportunities("BTC", 0.01).await?;
    for opp in opportunities {
        println!("Spread: {:.4}%", opp.spread);
    }
    
    Ok(())
}
```

## Documentation

See the main [SDK README](../README.md) for full documentation.

## Links

- **Website:** [https://onlyfunding.fun](https://onlyfunding.fun)
- **Twitter:** [@onlyfunding_fun](https://x.com/onlyfunding_fun)

