package command

import "github.com/bwmarrin/discordgo"

var Registry = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
	"ping": pingCommand,
	"cal":  calculationCommand,
}

var Definitions = []*discordgo.ApplicationCommand{
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
