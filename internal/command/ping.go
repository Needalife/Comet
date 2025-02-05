package command

import (
	"Comet/internal/colors"
	"fmt"
	"time"

	"github.com/bwmarrin/discordgo"
)

func PingCommand(s *discordgo.Session, i *discordgo.InteractionCreate) {
    timestamp, err := discordgo.SnowflakeTimestamp(i.ID)
	if err != nil {
		panic(err)
	}
	latency := time.Since(timestamp).Milliseconds()

    embed := &discordgo.MessageEmbed{
        Title: fmt.Sprintf("🏓 %dms", latency),
        Color: colors.Green,
    }

    s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
        Type: discordgo.InteractionResponseChannelMessageWithSource,
        Data: &discordgo.InteractionResponseData{
            Embeds: []*discordgo.MessageEmbed{embed},
        },
    })
}
