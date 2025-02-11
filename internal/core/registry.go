package core

import (
	"Comet/internal/command"

	"github.com/bwmarrin/discordgo"
)

var CommandRegistry = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
	"ping":   command.PingCommand,
	"cal":    command.CalculationCommand,
	"conv":   command.ConvertCurrencyCommand,
	"author": command.AuthorCommand,
	"src":    command.SourceCommand,
	"gw2":    command.GW2Commands,
}
