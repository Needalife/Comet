package core

import (
	"github.com/bwmarrin/discordgo"
)

var CommandDefinitions = []*discordgo.ApplicationCommand{
	{
		Name:        "ping",
		Description: "Replies with pong!",
	},
	{
		Name: "author",
		Description: "Vally",
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
	{
		Name:        "conv",
		Description: "Convert money from one currency to another",
		Options: []*discordgo.ApplicationCommandOption{
			{
				Type:        discordgo.ApplicationCommandOptionNumber,
				Name:        "amount",
				Description: "Amount of money to convert",
				Required:    true,
			},
			{
				Type:        discordgo.ApplicationCommandOptionString,
				Name:        "from_country",
				Description: "Country code/name to convert from (e.g., VN/Vietnam)",
				Required:    true,
			},
			{
				Type:        discordgo.ApplicationCommandOptionString,
				Name:        "to_country",
				Description: "Country code/name to convert to (e.g., USA/United States)",
				Required:    true,
			},
		},
	},
}
