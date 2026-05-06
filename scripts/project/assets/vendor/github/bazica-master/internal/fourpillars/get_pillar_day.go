package fourpillars

import (
	"github.com/tommitoan/bazica/internal/ultis"
	"github.com/tommitoan/bazica/model"
	"time"
)

func GetDayPillar(dateTime time.Time, loc *time.Location) (*model.DayPillar, error) {
	var dayPillar model.DayPillar
	dayPillar.Day = dateTime.Day()

	// From 23:00 is new day (Rat hour)
	dateTime = dateTime.Add(time.Hour)
	dateTime = dateTime.In(loc)

	milestone := time.Date(1900, 1, 1, 0, 0, 0, 0, loc)
	num := dateTime.Sub(milestone).Hours() / 24.0

	// Get day stem
	stemRule := (int(num) + 1) % 10
	if stemRule < 1 {
		stemRule = stemRule + 10
	}
	stem := ultis.CalculateHeavenlyStem(stemRule)
	dayPillar.HeavenlyStem = stem

	// Get day branch
	branchRule := (int(num) - 3) % 12
	if branchRule < 1 {
		branchRule = branchRule + 12
	}
	branch := ultis.CalculateEarthlyBranch(branchRule)
	dayPillar.EarthlyBranch = branch

	return &dayPillar, nil
}
