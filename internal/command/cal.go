package command

import (
	"Comet/internal/colors"
	"fmt"
	"strings"

	"github.com/Knetic/govaluate"
	"github.com/bwmarrin/discordgo"
)

func CalculationCommand(s *discordgo.Session, i *discordgo.InteractionCreate) {
	options := i.ApplicationCommandData().Options
	var expression string

	for _, opt := range options {
		if opt.Name == "expression" {
			expression = opt.StringValue()
			break
		}
	}

	expression = replaceOperator(expression)
	eval, err := govaluate.NewEvaluableExpression(expression)
	if err != nil {
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: fmt.Sprintf("Invalid expression: %s", err.Error()),
			},
		})
		return
	}

	result, err := eval.Evaluate(nil)
	if err != nil {
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: fmt.Sprintf("Fail to evaluate expression: %s", err.Error()),
			},
		})
		return
	}

	embed := &discordgo.MessageEmbed {
		Title: fmt.Sprintf("%s = %v", expression, result),
		Color: colors.Cyan,
	}

	s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
		Type: discordgo.InteractionResponseChannelMessageWithSource,
		Data: &discordgo.InteractionResponseData{
			Embeds: []*discordgo.MessageEmbed{embed},
		},
	})
}

func replaceOperator(expr string) string{
	expr = strings.ReplaceAll(expr, "x", "*")
	expr = strings.ReplaceAll(expr, ":", "/")
	return expr
}