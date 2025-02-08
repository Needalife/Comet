package config

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

func LoadExchangeRateAPIKey() string {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("No .env file found (API key config), proceed to use env variables")
	}

	return os.Getenv("EXCHANGE_RATE_API_KEY")
}