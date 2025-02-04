package main

import (
	"Comet/internal/command"
	"Comet/internal/config"
	"Comet/internal/db"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
	"go.mongodb.org/mongo-driver/v2/mongo"
)

type bot struct {
	config    config.Config
	db_client *mongo.Client
}

func mount(sess *discordgo.Session) {
	sess.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		command.HandleSlashCommand(s, i)
	})

	for _, cmd := range command.CommandDefinitions {
		_, err := sess.ApplicationCommandCreate(sess.State.Application.ID, "", cmd)
		if err != nil {
			fmt.Printf("Error registering command %s: %v\n", cmd.Name, err)
		}
	}

	fmt.Println("Finish adding handlers and registering commands!")
	sess.Identify.Intents = discordgo.IntentsAllWithoutPrivileged
}

func (app *bot) run() {
	app.db_client = db.ConnectMongo(app.config.Mongo.URI)
	defer db.DisconnectMongo(app.db_client)

	sess, err := discordgo.New("Bot " + app.config.Discord.Token)
	if err != nil {
		log.Fatal(err)
	}

	open(sess) //open session
	defer sess.Close() 

	mount(sess) //add handlers and privs
	
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
}
