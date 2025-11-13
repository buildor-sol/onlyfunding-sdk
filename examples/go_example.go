package main

// Example usage of onlyfunding.fun Go SDK
// Demonstrates basic functionality for working with funding rates API

import (
	"fmt"
	"log"

	"github.com/onlyfunding/go-sdk"
)

func main() {
	client := onlyfunding.NewClient()

	fmt.Println("=== onlyfunding.fun SDK Example ===\n")

	// Get all funding rates
	fmt.Println("Loading funding rates...")
	data, err := client.GetFundingRates()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("✓ Found %d symbols across %d exchanges\n\n", len(data.Symbols), len(data.Exchanges.Exchanges))

	// Get specific rate
	fmt.Println("Getting BTC funding rate on Binance...")
	rate, err := client.GetRate("binance_1_perp", "BTC")
	if err != nil {
		fmt.Printf("✗ Rate not found: %v\n\n", err)
	} else {
		fmt.Printf("✓ BTC funding rate: %.4f%%\n\n", rate)
	}

	// Find arbitrage opportunities
	fmt.Println("Finding arbitrage opportunities for BTC (min spread: 0.01%)...")
	opportunities, err := client.FindArbitrageOpportunities("BTC", 0.01)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("✓ Found %d opportunities\n\n", len(opportunities))

	if len(opportunities) > 0 {
		fmt.Println("Top 5 opportunities:")
		max := 5
		if len(opportunities) < max {
			max = len(opportunities)
		}
		for i, opp := range opportunities[:max] {
			fmt.Printf("\n%d. %s - Spread: %.4f%%\n", i+1, opp.Symbol, opp.Spread)
			fmt.Printf("   Long:  %s (%.4f%%)\n", opp.LongExchange, opp.Rate1)
			fmt.Printf("   Short: %s (%.4f%%)\n", opp.ShortExchange, opp.Rate2)
		}
	}
}

