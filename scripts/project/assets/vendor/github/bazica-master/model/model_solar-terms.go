package model

type SolarTermYear struct {
	MinorCold          string `json:"minor_cold"`
	MajorCold          string `json:"major_cold"`
	StartOfSpring      string `json:"start_of_spring"`
	SpringShowers      string `json:"spring_showers"`
	AwakeningOfInsects string `json:"awakening_of_insects"`
	SpringEquinox      string `json:"spring_equinox"`
	PureBrightness     string `json:"pure_brightness"`
	GrainRain          string `json:"grain_rain"`
	StartOfSummer      string `json:"start_of_summer"`
	GrainBuds          string `json:"grain_buds"`
	GrainInEar         string `json:"grain_in_ear"`
	SummerSolstice     string `json:"summer_solstice"`
	MinorHeat          string `json:"minor_heat"`
	MajorHeat          string `json:"major_heat"`
	StartOfAutumn      string `json:"start_of_autumn"`
	EndOfHeat          string `json:"end_of_heat"`
	WhiteDew           string `json:"white_dew"`
	AutumnEquinox      string `json:"autumn_equinox"`
	ColdDew            string `json:"cold_dew"`
	Frost              string `json:"frost"`
	StartOfWinter      string `json:"start_of_winter"`
	MinorSnow          string `json:"minor_snow"`
	MajorSnow          string `json:"major_snow"`
	WinterSolstice     string `json:"winter_solstice"`
}

const (
	MinorCold          = "minor_cold"
	MajorCold          = "major_cold"
	StartOfSpring      = "start_of_spring"
	SpringShowers      = "spring_showers"
	AwakeningOfInsects = "awakening_of_insects"
	SpringEquinox      = "spring_equinox"
	PureBrightness     = "pure_brightness"
	GrainRain          = "grain_rain"
	StartOfSummer      = "start_of_summer"
	GrainBuds          = "grain_buds"
	GrainInEar         = "grain_in_ear"
	SummerSolstice     = "summer_solstice"
	MinorHeat          = "minor_heat"
	MajorHeat          = "major_heat"
	StartOfAutumn      = "start_of_autumn"
	EndOfHeat          = "end_of_heat"
	WhiteDew           = "white_dew"
	AutumnEquinox      = "autumn_equinox"
	ColdDew            = "cold_dew"
	Frost              = "frost"
	StartOfWinter      = "start_of_winter"
	MinorSnow          = "minor_snow"
	MajorSnow          = "major_snow"
	WinterSolstice     = "winter_solstice"
)
