// Package onlyfunding provides a Go client for onlyfunding.fun funding rates API
package onlyfunding

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	DefaultBaseURL = "https://api.onlyfunding.fun"
	DefaultTimeout = 30 * time.Second
)

// ExchangeInfo represents exchange information
type ExchangeInfo struct {
	Name    string `json:"name"`
	Display string `json:"display"`
}

// ExchangesData contains exchange information
type ExchangesData struct {
	ExchangeNames []ExchangeInfo `json:"exchange_names"`
	Exchanges     []string       `json:"exchanges"`
}

// FundingRatesData represents the API response
type FundingRatesData struct {
	Symbols       []string                          `json:"symbols"`
	Exchanges     ExchangesData                     `json:"exchanges"`
	FundingRates  map[string]map[string]int         `json:"funding_rates"`
	OIRankings    map[string]string                 `json:"oi_rankings"`
	DefaultOIRank string                           `json:"default_oi_rank"`
	Timestamp     string                           `json:"timestamp"`
}

// ArbitrageOpportunity represents an arbitrage opportunity
type ArbitrageOpportunity struct {
	Symbol       string
	Exchange1    string
	Rate1        float64
	Exchange2    string
	Rate2        float64
	Spread       float64
	LongExchange string
	ShortExchange string
}

// Client is the main client for interacting with the onlyfunding API
type Client struct {
	baseURL string
	timeout time.Duration
	client  *http.Client
}

// NewClient creates a new onlyfunding client with default settings
func NewClient() *Client {
	return &Client{
		baseURL: DefaultBaseURL,
		timeout: DefaultTimeout,
		client: &http.Client{
			Timeout: DefaultTimeout,
		},
	}
}

// NewClientWithOptions creates a new client with custom options
func NewClientWithOptions(baseURL string, timeout time.Duration) *Client {
	return &Client{
		baseURL: baseURL,
		timeout: timeout,
		client: &http.Client{
			Timeout: timeout,
		},
	}
}

// GetFundingRates fetches current funding rates from all exchanges
func (c *Client) GetFundingRates() (*FundingRatesData, error) {
	req, err := http.NewRequest("GET", fmt.Sprintf("%s/funding", c.baseURL), nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", "onlyfunding-Go-SDK/1.0.0")

	resp, err := c.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch funding rates: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API request failed: %d %s: %s", resp.StatusCode, resp.Status, string(body))
	}

	var data FundingRatesData
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &data, nil
}

// GetRate gets funding rate for a specific exchange and symbol
func (c *Client) GetRate(exchange, symbol string) (float64, error) {
	data, err := c.GetFundingRates()
	if err != nil {
		return 0, err
	}

	if rates, ok := data.FundingRates[exchange]; ok {
		if rate, ok := rates[symbol]; ok {
			return float64(rate) / 10000.0, nil
		}
	}

	return 0, fmt.Errorf("rate not found for %s on %s", symbol, exchange)
}

// FindArbitrageOpportunities finds arbitrage opportunities for a symbol
func (c *Client) FindArbitrageOpportunities(symbol string, minSpread float64) ([]ArbitrageOpportunity, error) {
	data, err := c.GetFundingRates()
	if err != nil {
		return nil, err
	}

	// Collect all rates for the symbol
	rates := make(map[string]int)
	for exchange, symbols := range data.FundingRates {
		if rate, ok := symbols[symbol]; ok {
			rates[exchange] = rate
		}
	}

	if len(rates) < 2 {
		return []ArbitrageOpportunity{}, nil
	}

	var opportunities []ArbitrageOpportunity
	exchanges := make([]string, 0, len(rates))
	for exchange := range rates {
		exchanges = append(exchanges, exchange)
	}

	// Find all pairs
	for i, exchange1 := range exchanges {
		for _, exchange2 := range exchanges[i+1:] {
			rate1 := rates[exchange1]
			rate2 := rates[exchange2]
			spread := abs(float64(rate1-rate2)) / 10000.0

			if spread >= minSpread {
				longExchange := exchange1
				shortExchange := exchange2
				if rate1 > rate2 {
					longExchange = exchange2
					shortExchange = exchange1
				}

				opportunities = append(opportunities, ArbitrageOpportunity{
					Symbol:        symbol,
					Exchange1:     exchange1,
					Rate1:         float64(rate1) / 10000.0,
					Exchange2:     exchange2,
					Rate2:         float64(rate2) / 10000.0,
					Spread:        spread,
					LongExchange:  longExchange,
					ShortExchange: shortExchange,
				})
			}
		}
	}

	// Sort by spread descending
	for i := 0; i < len(opportunities)-1; i++ {
		for j := i + 1; j < len(opportunities); j++ {
			if opportunities[i].Spread < opportunities[j].Spread {
				opportunities[i], opportunities[j] = opportunities[j], opportunities[i]
			}
		}
	}

	return opportunities, nil
}

func abs(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}

