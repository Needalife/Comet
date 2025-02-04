package main

import (
	"fmt"
	"log"

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


