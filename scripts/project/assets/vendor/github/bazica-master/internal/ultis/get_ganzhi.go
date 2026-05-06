package ultis

import "strings"

var baziMap = map[string]string{
	"Yang Wood Rat":     "Sea metal",
	"Yin Wood Ox":       "Sea metal",
	"Yang Fire Tiger":   "Furnace fire",
	"Yin Fire Rabbit":   "Furnace fire",
	"Yang Earth Dragon": "Forest wood",
	"Yin Earth Snake":   "Forest wood",
	"Yang Metal Horse":  "Road earth",
	"Yin Metal Goat":    "Road earth",
	"Yang Water Monkey": "Sword metal",
	"Yin Water Rooster": "Sword metal",
	"Yang Wood Dog":     "Volcanic fire",
	"Yin Wood Pig":      "Volcanic fire",
	"Yang Fire Rat":     "Cave water",
	"Yin Fire Ox":       "Cave water",
	"Yang Earth Tiger":  "Fortress earth",
	"Yin Earth Rabbit":  "Fortress earth",
	"Yang Metal Dragon": "Wax metal",
	"Yin Metal Snake":   "Wax metal",
	"Yang Water Horse":  "Willow wood",
	"Yin Water Goat":    "Willow wood",
	"Yang Wood Monkey":  "Stream water",
	"Yin Wood Rooster":  "Stream water",
	"Yang Fire Dog":     "Roof tiles earth",
	"Yin Fire Pig":      "Roof tiles earth",
	"Yang Earth Rat":    "Lightning fire",
	"Yin Earth Ox":      "Lightning fire",
	"Yang Metal Tiger":  "Conifer wood",
	"Yin Metal Rabbit":  "Conifer wood",
	"Yang Water Dragon": "River water",
	"Yin Water Snake":   "River water",
	"Yang Wood Horse":   "Sand metal",
	"Yin Wood Goat":     "Sand metal",
	"Yang Fire Monkey":  "Forest fire",
	"Yin Fire Rooster":  "Forest fire",
	"Yang Earth Dog":    "Meadow wood",
	"Yin Earth Pig":     "Meadow wood",
	"Yang Metal Rat":    "Adobe earth",
	"Yin Metal Ox":      "Adobe earth",
	"Yang Water Tiger":  "Precious metal",
	"Yin Water Rabbit":  "Precious metal",
	"Yang Wood Dragon":  "Lamp fire",
	"Yin Wood Snake":    "Lamp fire",
	"Yang Fire Horse":   "Sky water",
	"Yin Fire Goat":     "Sky water",
	"Yang Earth Monkey": "Highway earth",
	"Yin Earth Rooster": "Highway earth",
	"Yang Metal Dog":    "Jewellery metal",
	"Yin Metal Pig":     "Jewellery metal",
	"Yang Water Rat":    "Mulberry wood",
	"Yin Water Ox":      "Mulberry wood",
	"Yang Wood Tiger":   "Rapids water",
	"Yin Wood Rabbit":   "Rapids water",
	"Yang Fire Dragon":  "Desert earth",
	"Yin Fire Snake":    "Desert earth",
	"Yang Earth Horse":  "Sun fire",
	"Yin Earth Goat":    "Sun fire",
	"Yang Metal Monkey": "Pomegranate wood",
	"Yin Metal Rooster": "Pomegranate wood",
	"Yang Water Dog":    "Ocean water",
	"Yin Water Pig":     "Ocean water",
}

// Function to get the corresponding element
func GetGanzhi(sign string) (string, string, int) {
	if element, exists := baziMap[sign]; exists {
		mainElement := ""
		valueElement := 0
		switch {
		case strings.Contains(element, "fire"):
			mainElement = "Fire"
			valueElement = 2
		case strings.Contains(element, "wood"):
			mainElement = "Wood"
			valueElement = 3
		case strings.Contains(element, "water"):
			mainElement = "Water"
			valueElement = 1
		case strings.Contains(element, "earth"):
			mainElement = "Earth"
			valueElement = 5
		case strings.Contains(element, "gold") || strings.Contains(element, "metal"):
			mainElement = "Metal"
			valueElement = 4
		default:
			mainElement = ""
			valueElement = 0
		}
		return element, mainElement, valueElement
	}
	return "", "", 0
}
