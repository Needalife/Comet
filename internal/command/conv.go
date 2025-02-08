package command

import (
	"Comet/internal/utils"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/bwmarrin/discordgo"
)

func ConvertCurrencyCommand(s *discordgo.Session, i *discordgo.InteractionCreate) {
	options := i.ApplicationCommandData().Options
	var amount float64
	var from_currency, to_currency string

	for _, opt := range options {
		switch opt.Name {
		case "amount":
			amount = opt.FloatValue()
		case "from_currency":
			from_currency = opt.StringValue()
		case "to_currency":
			to_currency = opt.StringValue()
		}
	}

	if amount <= 0 || from_currency == "" || to_currency == "" {
		msg := "Please provide a valid amount, from-currency, to-currency"
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Embeds: []*discordgo.MessageEmbed{utils.ErrorEmbed(msg)},
			},
		})
	}
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
