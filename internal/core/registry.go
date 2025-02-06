package core

import (
	"Comet/internal/command"

	"github.com/bwmarrin/discordgo"
)

var CommandRegistry = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
	"ping": command.PingCommand,
	"cal":  command.CalculationCommand,
}

var CommandDefinitions = []*discordgo.ApplicationCommand{
	{
		Name:        "ping",
		Description: "Replies with pong!",
	},
	{
		Name:        "cal",
		Description: "Calculate a mathematical expresison",
		Options: []*discordgo.ApplicationCommandOption{
			{
				Type:        discordgo.ApplicationCommandOptionString,
				Name:        "expression",
				Description: "The mathematical expression to evaluate",
				Required:    true,
			},
		},
	},
}
