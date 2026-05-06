package ultis

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/tommitoan/bazica/model"
	"log/slog"
	"os"
	"slices"
	"time"
)

var InititalTerms = []string{
	model.MinorCold,
	model.StartOfSpring,
	model.AwakeningOfInsects,
	model.PureBrightness,
	model.StartOfSummer,
	model.GrainInEar,
	model.MinorHeat,
	model.StartOfAutumn,
	model.WhiteDew,
	model.ColdDew,
	model.StartOfWinter,
	model.MajorSnow,
}

var MidpointTerms = []string{
	model.MajorCold,
	model.SpringShowers,
	model.SpringEquinox,
	model.GrainRain,
	model.GrainBuds,
	model.SummerSolstice,
	model.MajorHeat,
	model.EndOfHeat,
	model.AutumnEquinox,
	model.Frost,
	model.MinorSnow,
	model.WinterSolstice,
}

func GetSolarTerm(path string, dateTime time.Time) (string, int, int, error) {
	// Extract the year

	yearStr := fmt.Sprint(dateTime.Year())
	nextYear := fmt.Sprint(dateTime.Year() + 1)
	previousYear := fmt.Sprint(dateTime.Year() - 1)
	result, nextYearResult, previousYearResult, err := GetSolarTermsByYear(yearStr, nextYear, previousYear, path)
	if err != nil {
		fmt.Println(err)
		return "", 0, 0, err
	}

	// Use the correctly parsed time object when calling findSolarTerm
	term, passed, remaining, err := findSolarTerm(dateTime.Format("2006-01-02 15:04:05.999999999-07:00"), result, nextYearResult, previousYearResult)
	if err != nil {
		return "", 0, 0, errors.New(fmt.Sprintf("Error finding solar term: %v", err))
	} else {
		if passed == 0 || remaining == 0 {
			slog.Error("Time passed/remaining = 0")
		}
		return term, passed, remaining, nil
	}
}

func findSolarTerm(inputTime string, currentYearData, nextYearData, previousYearData model.SolarTermYear) (string, int, int, error) {
	t, err := time.Parse("2006-01-02 15:04:05.999999999-07:00", inputTime)
	if err != nil {
		return "", 0, 0, fmt.Errorf("invalid input time format: %v", err)
	}
	slog.Info("Input Time", "time", t)

	termList := []struct {
		name string
		time time.Time
	}{
		{"minor_cold", mustParseTime(currentYearData.MinorCold)},
		{"major_cold", mustParseTime(currentYearData.MajorCold)},
		{"start_of_spring", mustParseTime(currentYearData.StartOfSpring)},
		{"spring_showers", mustParseTime(currentYearData.SpringShowers)},
		{"awakening_of_insects", mustParseTime(currentYearData.AwakeningOfInsects)},
		{"spring_equinox", mustParseTime(currentYearData.SpringEquinox)},
		{"pure_brightness", mustParseTime(currentYearData.PureBrightness)},
		{"grain_rain", mustParseTime(currentYearData.GrainRain)},
		{"start_of_summer", mustParseTime(currentYearData.StartOfSummer)},
		{"grain_buds", mustParseTime(currentYearData.GrainBuds)},
		{"grain_in_ear", mustParseTime(currentYearData.GrainInEar)},
		{"summer_solstice", mustParseTime(currentYearData.SummerSolstice)},
		{"minor_heat", mustParseTime(currentYearData.MinorHeat)},
		{"major_heat", mustParseTime(currentYearData.MajorHeat)},
		{"start_of_autumn", mustParseTime(currentYearData.StartOfAutumn)},
		{"end_of_heat", mustParseTime(currentYearData.EndOfHeat)},
		{"white_dew", mustParseTime(currentYearData.WhiteDew)},
		{"autumn_equinox", mustParseTime(currentYearData.AutumnEquinox)},
		{"cold_dew", mustParseTime(currentYearData.ColdDew)},
		{"frost", mustParseTime(currentYearData.Frost)},
		{"start_of_winter", mustParseTime(currentYearData.StartOfWinter)},
		{"minor_snow", mustParseTime(currentYearData.MinorSnow)},
		{"major_snow", mustParseTime(currentYearData.MajorSnow)},
		{"winter_solstice", mustParseTime(currentYearData.WinterSolstice)},
	}

	var previousTermName string
	var timePassedMinutes, timeRemainingMinutes int
	for i, term := range termList {
		if t.After(term.time) && (i+1 == len(termList) || t.Before(termList[i+1].time)) {
			slog.Info("Solar Term Found", "term", term.name, "timePassedMinutes", timePassedMinutes)
			timePassedMinutes = int(t.Sub(term.time).Minutes())
			if slices.Contains(MidpointTerms, term.name) {
				timePassedMinutes += int(term.time.Sub(termList[i-1].time).Minutes())
			}

			if slices.Contains(InititalTerms, term.name) {
				if term.name == model.MajorSnow {
					minorColdNextYear := mustParseTime(nextYearData.MinorCold)

					timeRemainingMinutes = int(termList[i+1].time.Sub(t).Minutes())
					timeRemainingMinutes += int(minorColdNextYear.Sub(termList[i+1].time).Minutes())

				} else {
					timeRemainingMinutes = int(termList[i+1].time.Sub(t).Minutes())
					timeRemainingMinutes += int(termList[i+2].time.Sub(termList[i+1].time).Minutes())
				}
			} else {
				timeRemainingMinutes = int(termList[i+1].time.Sub(t).Minutes())
			}

			return term.name, timePassedMinutes, timeRemainingMinutes, nil // Return the name,time passed, time remaining if the time falls within this term
		}

		if i > 0 {
			previousTermName = termList[i-1].name // Keep track of the previous term (except for the first term)
		}
	}
	// Handle the case where input time is before the first term in the list
	slog.Warn(fmt.Sprintf("Input date precedes the first solar term of %d", t.Year()))
	timePassedMinutes = int(t.Sub(mustParseTime(previousYearData.WinterSolstice)).Minutes() + mustParseTime(previousYearData.WinterSolstice).Sub(mustParseTime(previousYearData.MajorSnow)).Minutes())
	timeRemainingMinutes = int(mustParseTime(currentYearData.MinorCold).Sub(t).Minutes())

	return previousTermName, timePassedMinutes, timeRemainingMinutes, nil // Return the last term of the previous year (or empty if there's none) and time passed 0
}

// Helper function to parse time with timezone offset
func mustParseTime(timeStr string) time.Time {
	loc, _ := time.LoadLocation("UTC")
	t, err := time.ParseInLocation("2006-01-02 15:04:05.999999999-07:00", timeStr, loc)
	if err != nil {
		panic("invalid time format in solar term data: " + err.Error())
	}
	return t
}

var PrefixPath string

func GetSolarTermsByYear(year, nextYear, previousYear string, path ...string) (model.SolarTermYear, model.SolarTermYear, model.SolarTermYear, error) {
	var prefix string
	if len(path) != 0 {
		prefix = path[0]
	}
	data := getSolarTermData(prefix)
	if data == nil {
		return model.SolarTermYear{}, model.SolarTermYear{}, model.SolarTermYear{}, errors.New("Cannot find solar term data for year " + year)
	}
	return data[year].Data, data[nextYear].Data, data[previousYear].Data, nil
}

func getSolarTermData(path string) map[string]model.CombinedData {
	// Assuming the combined JSON file is named "solar-term.json"
	prefix := PrefixPath
	if path != "" {
		prefix = path
	}

	fileToRead := prefix + "data/solar-term.json"

	data, err := os.ReadFile(fileToRead)

	// Use slog directly from the beginning
	if err != nil {
		slog.Error("Error reading combined JSON", "error", err)
		return nil
	}

	err = json.Unmarshal(data, &model.TempCombinedData)
	if err != nil {
		slog.Error("Error unmarshalling combined JSON", "error", err)
		return nil
	}

	// Check if combinedData is nil (optional)
	if model.TempCombinedData == nil {
		slog.Warn("combinedData is nil. Check JSON structure and struct definition.")
		return nil
	} else {
		return model.TempCombinedData
	}
}
