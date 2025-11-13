/**
 * onlyfunding.fun SDK for TypeScript/JavaScript
 * Official TypeScript/JavaScript client for onlyfunding.fun funding rates API
 */

export interface ExchangeInfo {
  name: string;
  display: string;
}

export interface ExchangesData {
  exchange_names: ExchangeInfo[];
  exchanges: string[];
}

export interface FundingRatesData {
  symbols: string[];
  exchanges: ExchangesData;
  funding_rates: Record<string, Record<string, number>>;
  oi_rankings: Record<string, string>;
  default_oi_rank: string;
  timestamp: string;
}

export class onlyfundingError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'onlyfundingError';
  }
}

export interface onlyfundingClientOptions {
  baseUrl?: string;
  timeout?: number;
}

export class onlyfundingClient {
  private baseUrl: string;
  private timeout: number;

  constructor(options: onlyfundingClientOptions = {}) {
    this.baseUrl = options.baseUrl || 'https://api.onlyfunding.fun';
    this.timeout = options.timeout || 30000;
  }

  /**
   * Get current funding rates from all exchanges
   */
  async getFundingRates(): Promise<FundingRatesData> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      const response = await fetch(`${this.baseUrl}/funding`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'onlyfunding-JS-SDK/1.0.0',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new onlyfundingError(
          `API request failed: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return data as FundingRatesData;
    } catch (error) {
      if (error instanceof onlyfundingError) {
        throw error;
      }
      if (error instanceof Error) {
        throw new onlyfundingError(`Failed to fetch funding rates: ${error.message}`);
      }
      throw new onlyfundingError('Unknown error occurred');
    }
  }

  /**
   * Get funding rate for a specific exchange and symbol
   */
  async getRate(
    exchange: string,
    symbol: string
  ): Promise<number | null> {
    const data = await this.getFundingRates();

    if (data.funding_rates[exchange]?.[symbol] !== undefined) {
      return data.funding_rates[exchange][symbol] / 10000.0;
    }

    return null;
  }

  /**
   * Find arbitrage opportunities for a symbol
   */
  async findArbitrageOpportunities(
    symbol: string,
    minSpread: number = 0.0
  ): Promise<Array<{
    symbol: string;
    exchange1: string;
    rate1: number;
    exchange2: string;
    rate2: number;
    spread: number;
    longExchange: string;
    shortExchange: string;
  }>> {
    const data = await this.getFundingRates();
    const opportunities: Array<{
      symbol: string;
      exchange1: string;
      rate1: number;
      exchange2: string;
      rate2: number;
      spread: number;
      longExchange: string;
      shortExchange: string;
    }> = [];

    // Collect all rates for the symbol
    const rates: Record<string, number> = {};
    for (const [exchange, symbols] of Object.entries(data.funding_rates)) {
      if (symbols[symbol] !== undefined) {
        rates[exchange] = symbols[symbol];
      }
    }

    if (Object.keys(rates).length < 2) {
      return opportunities;
    }

    // Find all pairs
    const exchanges = Object.keys(rates);
    for (let i = 0; i < exchanges.length; i++) {
      for (let j = i + 1; j < exchanges.length; j++) {
        const exchange1 = exchanges[i];
        const exchange2 = exchanges[j];
        const rate1 = rates[exchange1];
        const rate2 = rates[exchange2];
        const spread = Math.abs(rate1 - rate2) / 10000.0;

        if (spread >= minSpread) {
          opportunities.push({
            symbol,
            exchange1,
            rate1: rate1 / 10000.0,
            exchange2,
            rate2: rate2 / 10000.0,
            spread,
            longExchange: rate1 < rate2 ? exchange1 : exchange2,
            shortExchange: rate1 < rate2 ? exchange2 : exchange1,
          });
        }
      }
    }

    // Sort by spread descending
    opportunities.sort((a, b) => b.spread - a.spread);

    return opportunities;
  }
}

// Example usage
if (require.main === module) {
  (async () => {
    const client = new onlyfundingClient();

    try {
      // Get all funding rates
      const data = await client.getFundingRates();
      console.log(
        `Found ${data.symbols.length} symbols across ${data.exchanges.exchanges.length} exchanges`
      );

      // Get specific rate
      const btcRate = await client.getRate('binance_1_perp', 'BTC');
      if (btcRate !== null) {
        console.log(`BTC funding rate on Binance: ${btcRate.toFixed(4)}%`);
      }

      // Find arbitrage opportunities
      const opportunities = await client.findArbitrageOpportunities('BTC', 0.01);
      console.log(`\nFound ${opportunities.length} arbitrage opportunities for BTC:`);
      opportunities.slice(0, 5).forEach((opp) => {
        console.log(`  ${opp.symbol}: ${opp.spread.toFixed(4)}% spread`);
        console.log(`    Long: ${opp.longExchange} (${opp.rate1.toFixed(4)}%)`);
        console.log(`    Short: ${opp.shortExchange} (${opp.rate2.toFixed(4)}%)`);
      });
    } catch (error) {
      if (error instanceof onlyfundingError) {
        console.error('onlyfunding Error:', error.message);
      } else {
        console.error('Error:', error);
      }
    }
  })();
}

