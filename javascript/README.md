# onlyfunding.fun JavaScript/TypeScript SDK

Official TypeScript/JavaScript SDK for accessing the onlyfunding.fun funding rates API.

## Installation

```bash
npm install @onlyfunding/sdk
# or
yarn add @onlyfunding/sdk
```

## Usage

```typescript
import { onlyfundingClient } from '@onlyfunding/sdk';

const client = new onlyfundingClient();

// Get all funding rates
const data = await client.getFundingRates();
console.log(`Found ${data.symbols.length} symbols`);

// Get specific rate
const rate = await client.getRate('binance_1_perp', 'BTC');
console.log(`BTC rate: ${rate?.toFixed(4)}%`);

// Find arbitrage opportunities
const opportunities = await client.findArbitrageOpportunities('BTC', 0.01);
opportunities.forEach(opp => {
    console.log(`Spread: ${opp.spread.toFixed(4)}%`);
});
```

## Documentation

See the main [SDK README](../README.md) for full documentation.

## Links

- **Website:** [https://onlyfunding.fun](https://onlyfunding.fun)
- **Twitter:** [@onlyfunding_fun](https://x.com/onlyfunding_fun)

