package config

type Config struct {
	Discord Discord
	Mongo Mongo
}

func LoadConfig() Config {
	return Config{
		Discord: LoadDiscord(),
		Mongo: LoadMongo(),
	}
}