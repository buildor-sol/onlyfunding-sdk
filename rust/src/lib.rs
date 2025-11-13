//! onlyfunding.fun SDK for Rust
//! Official Rust client for onlyfunding.fun funding rates API

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::Duration;

const DEFAULT_BASE_URL: &str = "https://api.onlyfunding.fun";
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeInfo {
    pub name: String,
    pub display: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangesData {
    #[serde(rename = "exchange_names")]
    pub exchange_names: Vec<ExchangeInfo>,
    pub exchanges: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FundingRatesData {
    pub symbols: Vec<String>,
    pub exchanges: ExchangesData,
    #[serde(rename = "funding_rates")]
    pub funding_rates: HashMap<String, HashMap<String, i32>>,
    #[serde(rename = "oi_rankings")]
    pub oi_rankings: HashMap<String, String>,
    #[serde(rename = "default_oi_rank")]
    pub default_oi_rank: String,
    pub timestamp: String,
}

#[derive(Debug, Clone)]
pub struct ArbitrageOpportunity {
    pub symbol: String,
    pub exchange1: String,
    pub rate1: f64,
    pub exchange2: String,
    pub rate2: f64,
    pub spread: f64,
    pub long_exchange: String,
    pub short_exchange: String,
}

#[derive(Debug, thiserror::Error)]
pub enum onlyfundingError {
    #[error("HTTP error: {0}")]
    Http(#[from] reqwest::Error),
    #[error("API error: {0}")]
    Api(String),
    #[error("Rate not found")]
    RateNotFound,
}

pub struct onlyfundingClient {
    base_url: String,
    client: reqwest::Client,
}

impl onlyfundingClient {
    /// Create a new onlyfunding client with default settings
    pub fn new() -> Self {
        Self::with_options(None, None)
    }

    /// Create a new client with custom options
    pub fn with_options(base_url: Option<&str>, timeout: Option<Duration>) -> Self {
        let base_url = base_url.unwrap_or(DEFAULT_BASE_URL).to_string();
        let timeout = timeout.unwrap_or(DEFAULT_TIMEOUT);

        let client = reqwest::Client::builder()
            .timeout(timeout)
            .build()
            .expect("Failed to create HTTP client");

        Self { base_url, client }
    }

    /// Get current funding rates from all exchanges
    pub async fn get_funding_rates(&self) -> Result<FundingRatesData, onlyfundingError> {
        let url = format!("{}/funding", self.base_url);

        let response = self
            .client
            .get(&url)
            .header("Accept", "application/json")
            .header("User-Agent", "onlyfunding-Rust-SDK/1.0.0")
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(onlyfundingError::Api(format!(
                "API request failed: {} {}",
                response.status(),
                response.status().canonical_reason().unwrap_or("")
            )));
        }

        let data: FundingRatesData = response.json().await?;
        Ok(data)
    }

    /// Get funding rate for a specific exchange and symbol
    pub async fn get_rate(
        &self,
        exchange: &str,
        symbol: &str,
    ) -> Result<f64, onlyfundingError> {
        let data = self.get_funding_rates().await?;

        if let Some(rates) = data.funding_rates.get(exchange) {
            if let Some(rate) = rates.get(symbol) {
                return Ok(*rate as f64 / 10000.0);
            }
        }

        Err(onlyfundingError::RateNotFound)
    }

    /// Find arbitrage opportunities for a symbol
    pub async fn find_arbitrage_opportunities(
        &self,
        symbol: &str,
        min_spread: f64,
    ) -> Result<Vec<ArbitrageOpportunity>, onlyfundingError> {
        let data = self.get_funding_rates().await?;

        // Collect all rates for the symbol
        let mut rates: HashMap<String, i32> = HashMap::new();
        for (exchange, symbols) in &data.funding_rates {
            if let Some(rate) = symbols.get(symbol) {
                rates.insert(exchange.clone(), *rate);
            }
        }

        if rates.len() < 2 {
            return Ok(vec![]);
        }

        let mut opportunities = Vec::new();
        let exchanges: Vec<&String> = rates.keys().collect();

        // Find all pairs
        for i in 0..exchanges.len() {
            for j in (i + 1)..exchanges.len() {
                let exchange1 = exchanges[i];
                let exchange2 = exchanges[j];
                let rate1 = rates[exchange1];
                let rate2 = rates[exchange2];
                let spread = ((rate1 - rate2).abs() as f64) / 10000.0;

                if spread >= min_spread {
                    let (long_exchange, short_exchange) = if rate1 < rate2 {
                        (exchange1.clone(), exchange2.clone())
                    } else {
                        (exchange2.clone(), exchange1.clone())
                    };

                    opportunities.push(ArbitrageOpportunity {
                        symbol: symbol.to_string(),
                        exchange1: exchange1.clone(),
                        rate1: rate1 as f64 / 10000.0,
                        exchange2: exchange2.clone(),
                        rate2: rate2 as f64 / 10000.0,
                        spread,
                        long_exchange,
                        short_exchange,
                    });
                }
            }
        }

        // Sort by spread descending
        opportunities.sort_by(|a, b| b.spread.partial_cmp(&a.spread).unwrap());

        Ok(opportunities)
    }
}

impl Default for onlyfundingClient {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_get_funding_rates() {
        let client = onlyfundingClient::new();
        let result = client.get_funding_rates().await;
        assert!(result.is_ok());
    }
}

