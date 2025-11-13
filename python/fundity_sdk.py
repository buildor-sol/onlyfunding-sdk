"""
onlyfunding.fun SDK for Python
Official Python client for onlyfunding.fun funding rates API
"""

import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExchangeInfo:
    """Exchange information"""
    name: str
    display: str


@dataclass
class FundingRatesData:
    """Funding rates API response"""
    symbols: List[str]
    exchanges: Dict[str, Any]
    funding_rates: Dict[str, Dict[str, int]]
    oi_rankings: Dict[str, str]
    default_oi_rank: str
    timestamp: str


class onlyfundingError(Exception):
    """Base exception for onlyfunding.fun SDK"""
    pass


class onlyfundingClient:
    """Client for accessing onlyfunding.fun funding rates API"""
    
    BASE_URL = "https://api.onlyfunding.fun"
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        """
        Initialize the onlyfunding client
        
        Args:
            base_url: Optional custom base URL (default: https://api.onlyfunding.fun)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'onlyfunding-Python-SDK/1.0.0'
        })
    
    def get_funding_rates(self) -> FundingRatesData:
        """
        Get current funding rates from all exchanges
        
        Returns:
            FundingRatesData: Funding rates data
            
        Raises:
            onlyfundingError: If API request fails
        """
        try:
            response = self.session.get(
                f"{self.base_url}/funding",
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            return FundingRatesData(
                symbols=data.get('symbols', []),
                exchanges=data.get('exchanges', {}),
                funding_rates=data.get('funding_rates', {}),
                oi_rankings=data.get('oi_rankings', {}),
                default_oi_rank=data.get('default_oi_rank', '500+'),
                timestamp=data.get('timestamp', '')
            )
        except requests.exceptions.RequestException as e:
            raise onlyfundingError(f"Failed to fetch funding rates: {str(e)}")
        except (KeyError, ValueError) as e:
            raise onlyfundingError(f"Invalid API response: {str(e)}")
    
    def get_rate(self, exchange: str, symbol: str) -> Optional[float]:
        """
        Get funding rate for a specific exchange and symbol
        
        Args:
            exchange: Exchange name (e.g., 'binance_1_perp')
            symbol: Symbol name (e.g., 'BTC')
            
        Returns:
            Optional[float]: Funding rate as percentage, or None if not found
        """
        data = self.get_funding_rates()
        
        if exchange in data.funding_rates:
            if symbol in data.funding_rates[exchange]:
                rate = data.funding_rates[exchange][symbol]
                return rate / 10000.0
        
        return None
    
    def find_arbitrage_opportunities(
        self, 
        symbol: str, 
        min_spread: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Find arbitrage opportunities for a symbol
        
        Args:
            symbol: Symbol to analyze (e.g., 'BTC')
            min_spread: Minimum spread in percentage to consider (default: 0.0)
            
        Returns:
            List of opportunities with exchange pairs and spreads
        """
        data = self.get_funding_rates()
        opportunities = []
        
        # Collect all rates for the symbol
        rates = {}
        for exchange, symbols in data.funding_rates.items():
            if symbol in symbols:
                rates[exchange] = symbols[symbol]
        
        if len(rates) < 2:
            return opportunities
        
        # Find all pairs
        exchanges = list(rates.keys())
        for i, exchange1 in enumerate(exchanges):
            for exchange2 in exchanges[i+1:]:
                rate1 = rates[exchange1]
                rate2 = rates[exchange2]
                spread = abs(rate1 - rate2) / 10000.0
                
                if spread >= min_spread:
                    opportunities.append({
                        'symbol': symbol,
                        'exchange1': exchange1,
                        'rate1': rate1 / 10000.0,
                        'exchange2': exchange2,
                        'rate2': rate2 / 10000.0,
                        'spread': spread,
                        'long_exchange': exchange1 if rate1 < rate2 else exchange2,
                        'short_exchange': exchange2 if rate1 < rate2 else exchange1
                    })
        
        # Sort by spread descending
        opportunities.sort(key=lambda x: x['spread'], reverse=True)
        
        return opportunities


# Example usage
if __name__ == "__main__":
    client = onlyfundingClient()
    
    # Get all funding rates
    data = client.get_funding_rates()
    print(f"Found {len(data.symbols)} symbols across {len(data.exchanges['exchanges'])} exchanges")
    
    # Get specific rate
    btc_rate = client.get_rate('binance_1_perp', 'BTC')
    if btc_rate:
        print(f"BTC funding rate on Binance: {btc_rate:.4f}%")
    
    # Find arbitrage opportunities
    opportunities = client.find_arbitrage_opportunities('BTC', min_spread=0.01)
    print(f"\nFound {len(opportunities)} arbitrage opportunities for BTC:")
    for opp in opportunities[:5]:  # Show top 5
        print(f"  {opp['symbol']}: {opp['spread']:.4f}% spread")
        print(f"    Long: {opp['long_exchange']} ({opp['rate1']:.4f}%)")
        print(f"    Short: {opp['short_exchange']} ({opp['rate2']:.4f}%)")

