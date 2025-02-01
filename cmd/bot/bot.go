package main

import (
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

func open(sess *discordgo.Session) {
	err := sess.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer sess.Close()

	fmt.Println("Comet is up!")
}

func mount(sess *discordgo.Session, prefix string) {
	sess.AddHandler(func(s *discordgo.Session, m *discordgo.MessageCreate) {
		if m.Author.ID == s.State.User.ID {
			return
		}

		args := strings.Split(m.Content, " ")
		if args[0] != prefix {
			return
		}

		if args[1] == "hello" {
			s.ChannelMessageSend(m.ChannelID, "world!")
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
	open(sess) //start session

	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
}
