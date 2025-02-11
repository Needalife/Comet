package main

import (
	"fmt"
	"time"
)

var gw2Times = map[string][]map[string]string{
	"Tyria": {
		{"stage": "Day", "start": "9:30", "end": "10:39"},
		{"stage": "Dusk", "start": "10:40", "end": "10:44"},
		{"stage": "Night", "start": "10:45", "end": "11:24"},
		{"stage": "Dawn", "start": "11:25", "end": "11:29"},
		{"stage": "Day", "start": "11:30", "end": "12:39"},
		{"stage": "Dusk", "start": "12:40", "end": "12:44"},
		{"stage": "Night", "start": "12:45", "end": "1:24"},
		{"stage": "Dawn", "start": "1:25", "end": "1:29"},
		{"stage": "Day", "start": "1:30", "end": "2:39"},
		{"stage": "Dusk", "start": "2:40", "end": "2:44"},
		{"stage": "Night", "start": "2:45", "end": "3:24"},
		{"stage": "Dawn", "start": "3:25", "end": "3:29"},
		{"stage": "Day", "start": "3:30", "end": "4:39"},
		{"stage": "Dusk", "start": "4:40", "end": "4:44"},
		{"stage": "Night", "start": "4:45", "end": "5:24"},
		{"stage": "Dawn", "start": "5:25", "end": "5:29"},
		{"stage": "Day", "start": "5:30", "end": "6:39"},
		{"stage": "Dusk", "start": "6:40", "end": "6:44"},
		{"stage": "Night", "start": "6:45", "end": "7:24"},
		{"stage": "Dawn", "start": "7:25", "end": "7:29"},
		{"stage": "Day", "start": "7:30", "end": "8:39"},
		{"stage": "Dusk", "start": "8:40", "end": "8:44"},
		{"stage": "Night", "start": "8:45", "end": "9:24"},
		{"stage": "Dawn", "start": "9:25", "end": "9:29"},
	},
}

func convertToUTC(gw2Times map[string][]map[string]string) map[string][]map[string]string {
	converted := make(map[string][]map[string]string)

	for region, timeSlots := range gw2Times {
		var newSlots []map[string]string
		for _, slot := range timeSlots {
			startUTC := convertTime(slot["start"])
			endUTC := convertTime(slot["end"])

			newSlots = append(newSlots, map[string]string{
				"stage": slot["stage"],
				"start": startUTC,
				"end":   endUTC,
			})
		}
		converted[region] = newSlots
	}
	return converted
}

// Function to subtract 7 hours and format time properly
func convertTime(timeStr string) string {
	// Parse time in UTC+7
	layout := "15:04" // "HH:MM" format
	t, err := time.Parse(layout, timeStr)
	if err != nil {
		fmt.Println("Error parsing time:", timeStr)
		return timeStr // Return original if error
	}

	// Subtract 7 hours to convert to UTC
	t = t.Add(-7 * time.Hour)

	// Return formatted UTC time
	return t.Format(layout)
}

func main() {
	// Convert to UTC
	utcTimes := convertToUTC(gw2Times)

	// Print Go map format (not JSON)
	fmt.Println("var gw2Times = map[string][]map[string]string{")
	for region, timeSlots := range utcTimes {
		fmt.Printf("    \"%s\": {\n", region)
		for _, slot := range timeSlots {
			fmt.Printf("        {\"stage\": \"%s\", \"start\": \"%s\", \"end\": \"%s\"},\n",
				slot["stage"], slot["start"], slot["end"])
		}
		fmt.Println("    },")
	}
	fmt.Println("}")
}