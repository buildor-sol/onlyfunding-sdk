/**
 * Example usage of onlyfunding.fun JavaScript/TypeScript SDK
 * Demonstrates basic functionality for working with funding rates API
 */

const { onlyfundingClient } = require('@onlyfunding/sdk');

async function main() {
    const client = new onlyfundingClient();
    
    console.log('=== onlyfunding.fun SDK Example ===\n');
    
    // Get all funding rates
    console.log('Loading funding rates...');
    const data = await client.getFundingRates();
    console.log(`✓ Found ${data.symbols.length} symbols across ${data.exchanges.exchanges.length} exchanges\n`);
    
    // Get specific rate
    console.log('Getting BTC funding rate on Binance...');
    const btcRate = await client.getRate('binance_1_perp', 'BTC');
    if (btcRate !== null) {
        console.log(`✓ BTC funding rate: ${btcRate.toFixed(4)}%\n`);
    } else {
        console.log('✗ Rate not found\n');
    }
    
    // Find arbitrage opportunities
    console.log('Finding arbitrage opportunities for BTC (min spread: 0.01%)...');
    const opportunities = await client.findArbitrageOpportunities('BTC', 0.01);
    console.log(`✓ Found ${opportunities.length} opportunities\n`);
    
    if (opportunities.length > 0) {
        console.log('Top 5 opportunities:');
        opportunities.slice(0, 5).forEach((opp, i) => {
            console.log(`\n${i + 1}. ${opp.symbol} - Spread: ${opp.spread.toFixed(4)}%`);
            console.log(`   Long:  ${opp.longExchange} (${opp.rate1.toFixed(4)}%)`);
            console.log(`   Short: ${opp.shortExchange} (${opp.rate2.toFixed(4)}%)`);
        });
    }
}

main().catch(console.error);

