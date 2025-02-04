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

func mount(sess *discordgo.Session, servId string) {
    sess.Identify.Intents = discordgo.IntentsAllWithoutPrivileged

    sess.AddHandler(func(s *discordgo.Session, r *discordgo.Ready) {
        fmt.Println("Registering commands...")
        for _, cmd := range command.CommandDefinitions {
            _, err := s.ApplicationCommandCreate(s.State.Application.ID, servId, cmd)
            if err != nil {
                log.Printf("Error registering %s: %v", cmd.Name, err)
            }
        }
    })

    sess.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
        fmt.Print("Handling interaction: ")
        command.HandleSlashCommand(s, i)
    })
}

func (app *bot) run() {
	app.db_client = db.ConnectMongo(app.config.Mongo.URI)
	defer db.DisconnectMongo(app.db_client)

	sess, err := discordgo.New("Bot " + app.config.Discord.Token)
	if err != nil {
		log.Fatal(err)
	}

	mount(sess, app.config.Discord.ServerID) //add handlers and privs
	open(sess) //open session
	defer sess.Close() 

	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
}
