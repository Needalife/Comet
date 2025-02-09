package utils

import (
	"fmt"
	"strings"

	"github.com/dustin/go-humanize"
)

func FormatNumberWithComas(number float64) string {
	parts := strings.Split(fmt.Sprintf("%.2f", number), ".")
	parts[0] = humanize.Comma(int64(number))
	return strings.Join(parts, ".")
}