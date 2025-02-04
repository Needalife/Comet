package command

import "github.com/bwmarrin/discordgo"


var Registry = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate) {
	"ping": pingCommand,
}

var CommandDefinitions = []*discordgo.ApplicationCommand{
	{
		Name: "ping",
		Description: "Replies with pong!",
	},
}