package config

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

type Mongo struct {
	URI string
}

func LoadMongo() Mongo {
	err := godotenv.Load(".env") 
	if err != nil {
		fmt.Println("No .env file found (MongoDB config), proceed to use env variables")
	}

	return Mongo {
		URI: os.Getenv("MONGO_URI"),
	}
}