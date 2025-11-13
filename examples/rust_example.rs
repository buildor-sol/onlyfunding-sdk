// Example usage of onlyfunding.fun Rust SDK
// Demonstrates basic functionality for working with funding rates API

use onlyfunding_sdk::onlyfundingClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = onlyfundingClient::new();

    println!("=== onlyfunding.fun SDK Example ===\n");

    // Get all funding rates
    println!("Loading funding rates...");
    let data = client.get_funding_rates().await?;
    println!(
        "✓ Found {} symbols across {} exchanges\n",
        data.symbols.len(),
        data.exchanges.exchanges.len()
    );

    // Get specific rate
    println!("Getting BTC funding rate on Binance...");
    match client.get_rate("binance_1_perp", "BTC").await {
        Ok(rate) => println!("✓ BTC funding rate: {:.4}%\n", rate),
        Err(_) => println!("✗ Rate not found\n"),
    }

    // Find arbitrage opportunities
    println!("Finding arbitrage opportunities for BTC (min spread: 0.01%)...");
    let opportunities = client.find_arbitrage_opportunities("BTC", 0.01).await?;
    println!("✓ Found {} opportunities\n", opportunities.len());

    if !opportunities.is_empty() {
        println!("Top 5 opportunities:");
        for (i, opp) in opportunities.iter().take(5).enumerate() {
            println!("\n{}. {} - Spread: {:.4}%", i + 1, opp.symbol, opp.spread);
            println!("   Long:  {} ({:.4}%)", opp.long_exchange, opp.rate1);
            println!("   Short: {} ({:.4}%)", opp.short_exchange, opp.rate2);
        }
    }

    Ok(())
}

