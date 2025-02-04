package command

import (
	"fmt"

	"github.com/bwmarrin/discordgo"
)

func HandleSlashCommand(s *discordgo.Session, i *discordgo.InteractionCreate) {
	if handler, exists := Registry[i.ApplicationCommandData().Name]; exists {
		handler(s, i)
		fmt.Printf("%s uses %v\n",i.Member.User.GlobalName, i.ApplicationCommandData().Name)
	} else {
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: "Unknown command!",
			},
		})
	}
}