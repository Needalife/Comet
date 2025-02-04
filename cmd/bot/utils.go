package main

import (
	"Comet/internal/colors"
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
	asciiArt := `
 ██████╗ ██████╗ ███╗   ███╗███████╗████████╗
██╔════╝██╔═══██╗████╗ ████║██╔════╝╚══██╔══╝
██║     ██║   ██║██╔████╔██║█████╗     ██║
██║     ██║   ██║██║╚██╔╝██║██╔══╝     ██║ 
╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗   ██║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝   ╚═╝
`
	fmt.Println(asciiArt)
}

func handleCommand(
	s *discordgo.Session, 
	m *discordgo.MessageCreate, 
	prefix string, 
	registry map[string]func(*discordgo.Session, *discordgo.MessageCreate, []string),
	) bool {
	if !strings.HasPrefix(m.Content, prefix) {
		return false
	}

	fmt.Printf("%v uses '%v'\n", m.Author.GlobalName, m.Content)
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

	embed := &discordgo.MessageEmbed{
		Title: fmt.Sprintf("Unknown command: !%s", commandName),
		Color: colors.Red,
	}
	s.ChannelMessageSendEmbed(m.ChannelID, embed)
	return true
}
