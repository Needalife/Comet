package command

import "github.com/bwmarrin/discordgo"

var Registry = map[string]func(s *discordgo.Session, m *discordgo.MessageCreate, args []string) {
	"ping": pingCommand,
}