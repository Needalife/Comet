package config

import (
	"fmt"
	"os"
	"github.com/joho/godotenv"
)

type Config struct {
	Token string
}

func LoadConfig() Config {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("No .env file found!")
	}

	return Config {
		Token: os.Getenv("TOKEN"),
	}
}
