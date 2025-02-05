package utils

import (
	"Comet/internal/colors"

	"github.com/bwmarrin/discordgo"
)

func ErrorEmbed(err string) *discordgo.MessageEmbed {
	return &discordgo.MessageEmbed{
		Title: err,
		Color: colors.Red,
	}
}