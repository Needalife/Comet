package db

import (
	"context"
	"fmt"

	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

func ConnectMongo(uri string) *mongo.Client {
	client, err := mongo.Connect(options.Client().ApplyURI(uri))
	if err != nil {
		panic(err)
	}

	fmt.Println("MongoDB connected!")

	return client
}

func DisconnectMongo(client *mongo.Client) {
	client.Disconnect(context.TODO())
	fmt.Println("MongoDB disconnected!")
}