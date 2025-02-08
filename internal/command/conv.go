package command

import (
	"Comet/internal/config"
	"Comet/internal/utils"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/bwmarrin/discordgo"
)

var key = config.LoadExchangeRateAPIKey()

func ConvertCurrencyCommand(s *discordgo.Session, i *discordgo.InteractionCreate) {
	options := i.ApplicationCommandData().Options
	var amount float64
	var from_country, to_country string

	for _, opt := range options {
		switch opt.Name {
		case "amount":
			amount = opt.FloatValue()
		case "from_country":
			from_country = opt.StringValue()
		case "to_country":
			to_country = opt.StringValue()
		}
	}

	if amount <= 0 || from_country == "" || to_country == "" {
		msg := "Please provide a valid amount, from-country, to-country"
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Embeds: []*discordgo.MessageEmbed{utils.ErrorEmbed(msg)},
			},
		})
	}
	
	from_currency, from_exists := utils.CountryToCurrency[from_country]
	to_currency, to_exists := utils.CountryToCurrency[to_country]
	if !from_exists || !to_exists {
		msg := fmt.Sprintf("%s or %s is not a valid country", from_country, to_country)
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Embeds: []*discordgo.MessageEmbed{utils.ErrorEmbed(msg)},
			},
		})
	}

	exchangeRate, err := fetchExchangeRate(key, from_currency, to_currency)
	if err != nil {
		msg := fmt.Sprintf("Error fetching API: %s", err)
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Embeds: []*discordgo.MessageEmbed{utils.ErrorEmbed(msg)},
			},
		})
	}

	result := amount * exchangeRate
	embed := &discordgo.MessageEmbed {
		Title: fmt.Sprintf("%v",result),
	}

	s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
		Type: discordgo.InteractionResponseChannelMessageWithSource,
		Data: &discordgo.InteractionResponseData{
			Embeds: []*discordgo.MessageEmbed{embed},
		},
	})
}

type exchangeRateResponse struct {
	Result         string  `json:"result"`
	ConversionRate float64 `json:"conversion_rate"`
}

func fetchExchangeRate(apiKey, baseCurrency, targetCurrency string) (float64, error) {
	url := fmt.Sprintf("https://v6.exchangerate-api.com/v6/%s/pair/%s/%s",
		apiKey,
		baseCurrency,
		targetCurrency)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return 0, fmt.Errorf("Failed to fetch exchange rate api: %v\n",err)
	}
	defer resp.Body.Close()

	var exchangeRate exchangeRateResponse
	err = json.NewDecoder(resp.Body).Decode(&exchangeRate)
	if err != nil {
		return 0, fmt.Errorf("Fail to decode response: %v\n", err)
	}

	if exchangeRate.Result != "success" {
		return 0, fmt.Errorf("API returned an error: %s\n", exchangeRate.Result)
	}


	return exchangeRate.ConversionRate, nil
}
