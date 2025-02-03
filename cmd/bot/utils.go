package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/bwmarrin/discordgo"
)

func open(sess *discordgo.Session) {
	err := sess.Open()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Comet is up!")
}

func handleCommand(s *discordgo.Session, m *discordgo.MessageCreate, prefix string, registry map[string]func(*discordgo.Session, *discordgo.MessageCreate, []string)) bool {
	if !strings.HasPrefix(m.Content, prefix) {
		return false
	}

	content := strings.TrimPrefix(m.Content, prefix)
	args := strings.Fields(content)
	if len(args) == 0 {
		return false
	}

	commandName := args[0]
	
	if handler, exists := registry[commandName]; exists {
		handler(s, m, args[1:])
		return true
	}
	s.ChannelMessageSend(m.ChannelID, fmt.Sprintf("Unknown command: %s", commandName))
	return true
}
