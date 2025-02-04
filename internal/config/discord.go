package config

import (
	"fmt"
	"github.com/joho/godotenv"
	"os"
)

type Discord struct {
	Token    string
	ServerID string
}

func LoadDiscord() Discord {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("No .env file found (discord config), proceed to use env variables")
	}

	return Discord{
		Token:    os.Getenv("TOKEN"),
		ServerID: os.Getenv("SERVER_ID"),
	}
}
