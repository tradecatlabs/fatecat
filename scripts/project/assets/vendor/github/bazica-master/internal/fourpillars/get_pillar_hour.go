package fourpillars

import (
	"github.com/tommitoan/bazica/internal/ultis"
	"github.com/tommitoan/bazica/model"
	"math"
	"time"
)

func GetHourPillar(dayPillar *model.DayPillar, dateTime time.Time) (*model.HourPillar, error) {
	var hourPillar model.HourPillar
	hourPillar.Hour = model.TimeOfDay{
		Hour:   dateTime.Hour(),
		Minute: dateTime.Minute(),
	}

	// Get earthly branch
	dateHour := dateTime.Hour()
	valueToGetBranch := (math.Round(float64(dateHour) / 2)) - 1
	if valueToGetBranch < 1 {
		valueToGetBranch = valueToGetBranch + 12
	}
	branch := ultis.CalculateEarthlyBranch(int(valueToGetBranch))
	hourPillar.EarthlyBranch = branch

	// Get heavenly stem
	valueOfRatHour := ultis.GetStemRuleByFiveRats(dayPillar.HeavenlyStem.Value)
	var stem int
	diff := hourPillar.EarthlyBranch.Value - 11
	if diff < 0 {
		diff = diff + 12
	}
	stem = valueOfRatHour + diff
	if stem > 10 {
		stem = stem - 10
	}

	heavenlyStem := ultis.CalculateHeavenlyStem(stem)
	hourPillar.HeavenlyStem = heavenlyStem

	return &hourPillar, nil
}
