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
	fmt.Println("Comet is up!")
}
