package config

import (
	"fmt"
	"github.com/joho/godotenv"
	"os"
)

type Discord struct {
	Token  string
	Prefix string
}

func LoadDiscord() Discord {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("No .env file found!")
	}

	return Discord{
		Token:  os.Getenv("TOKEN"),
		Prefix: os.Getenv("PREFIX"),
	}
}
