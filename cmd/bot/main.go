package main

import (
	"Comet/internal/config"
)


func main() {
	cfg := config.LoadConfig()

	app := &bot{
		config: cfg,
	}

	app.run()
}