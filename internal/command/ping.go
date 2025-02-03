package command

import (
	"fmt"
	"time"

	"github.com/bwmarrin/discordgo"
)

func pingCommand(s *discordgo.Session, m *discordgo.MessageCreate, args[] string) {
	latency := time.Since(m.Timestamp).Milliseconds()
	response := fmt.Sprintf("pong: %dms!", latency)
    s.ChannelMessageSend(m.ChannelID, response)
}