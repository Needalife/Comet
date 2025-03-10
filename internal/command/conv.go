package command

import (
	"Comet/internal/colors"
	"Comet/internal/config"
	"Comet/internal/utils"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/bwmarrin/discordgo"
	"github.com/dustin/go-humanize"
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

	exchangeRate, exchangeResult, err := convertCurrency(key, amount, from_currency, to_currency)
	if err != nil {
		msg := fmt.Sprintf("Error fetching API: %s", err)
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Embeds: []*discordgo.MessageEmbed{utils.ErrorEmbed(msg)},
			},
		})
	}

	embed := &discordgo.MessageEmbed{
		Title: fmt.Sprintf("%s -> %s", from_currency, to_currency),
		Description: fmt.Sprintf("**Amount**: *%v*\n**Result**: *%s*\n**Rate**: *%v*",
			humanize.Commaf(amount),
			utils.FormatNumberWithComas(exchangeResult),
			humanize.Commaf(exchangeRate)),
		Color: colors.BrightPurple,
		Thumbnail: &discordgo.MessageEmbedThumbnail{
			URL: "https://i.imgur.com/cn6QoeG.png",
		},
		Footer: &discordgo.MessageEmbedFooter{
			Text: "Powered by exchangerate-api.com",
		},
	}

	s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
		Type: discordgo.InteractionResponseChannelMessageWithSource,
		Data: &discordgo.InteractionResponseData{
			Embeds: []*discordgo.MessageEmbed{embed},
		},
	})
}

type exchangeCurrencyResponse struct {
	Result           string  `json:"result"`
	ConversionRate   float64 `json:"conversion_rate"`
	ConversionResult float64 `json:"conversion_result"`
}

func convertCurrency(
	apiKey string,
	amount float64,
	baseCurrency string,
	targetCurrency string) (
	float64, float64, error) {
	url := fmt.Sprintf("https://v6.exchangerate-api.com/v6/%s/pair/%s/%s/%.0f",
		apiKey,
		baseCurrency,
		targetCurrency,
		amount)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return 0, 0, fmt.Errorf("failed to fetch exchange rate api: %v", err)
	}
	defer resp.Body.Close()

	var exchangeCurrency exchangeCurrencyResponse
	err = json.NewDecoder(resp.Body).Decode(&exchangeCurrency)
	if err != nil {
		return 0, 0, fmt.Errorf("fail to decode response: %v", err)
	}

	if exchangeCurrency.Result != "success" {
		return 0, 0, fmt.Errorf("api returned an error: %s", exchangeCurrency.Result)
	}

	return exchangeCurrency.ConversionRate, exchangeCurrency.ConversionResult, nil
}
