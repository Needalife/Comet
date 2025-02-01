package main

import (
	"Comet/internal/config"
)


func main() {
    app := &bot{
        config: config.LoadConfig(),
    }

	app.run()
}