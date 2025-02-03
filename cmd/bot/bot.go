package main

import (
	"Comet/internal/command"
	"Comet/internal/config"
	"Comet/internal/db"
	"fmt"
	"log"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/bwmarrin/discordgo"
	"go.mongodb.org/mongo-driver/v2/mongo"
)

type bot struct {
	config    config.Config
	db_client *mongo.Client
}

func mount(sess *discordgo.Session, prefix string) {
	sess.AddHandler(func(s *discordgo.Session, m *discordgo.MessageCreate) {
        if m.Author.ID == s.State.User.ID {
            return
        }

        if !strings.HasPrefix(m.Content, prefix) {
            return
        }

        content := strings.TrimPrefix(m.Content, prefix)
        args := strings.Fields(content) 
        if len(args) == 0 {
            return
        }
		commandName := args[0]
		fmt.Println(args)


        if handler, exists := command.Registry[commandName]; exists {
			handler(s, m, args[1:])
		} else {
			s.ChannelMessageSend(m.ChannelID, fmt.Sprintf("Unknown command: %s", commandName))
		}
	})

	fmt.Println("Finish adding handlers!")
	sess.Identify.Intents = discordgo.IntentsAllWithoutPrivileged
}

func (app *bot) run() {
	app.db_client = db.ConnectMongo(app.config.Mongo.URI)
	defer db.DisconnectMongo(app.db_client)

	sess, err := discordgo.New("Bot " + app.config.Discord.Token)
	if err != nil {
		log.Fatal(err)
	}

	mount(sess, app.config.Discord.Prefix) //add handlers and privs
	open(sess) //open session
	defer sess.Close() 

	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
}
