package command

import (
	"Comet/internal/utils"
	"fmt"

	"github.com/bwmarrin/discordgo"
)

func ConvertCurrencyCommand(s *discordgo.Session, i *discordgo.InteractionCreate) {
	options := i.ApplicationCommandData().Options
	var amount float64
	var from_currency, to_currency string

	for _, opt := range options {
		switch opt.Name {
		case "amount":
			amount = opt.FloatValue()
		case "from_currency":
			from_currency = opt.StringValue()
		case "to_currency":
			to_currency = opt.StringValue()
		}
	}

	if amount <= 0 || from_currency == "" || to_currency == "" {
		msg := "Please provide a valid amount, from-currency, to-currency"
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Embeds: []*discordgo.MessageEmbed{utils.ErrorEmbed(msg)},
			},
		})
	}
}
