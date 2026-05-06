package fourpillars

import (
	"github.com/tommitoan/bazica/internal/ultis"
	"github.com/tommitoan/bazica/model"
	"time"
)

func GetMonthPillar(path string, yearPillar *model.YearPillar, dateTime time.Time) (*model.MonthPillar, int, int, error) {
	var monthPillar model.MonthPillar
	monthPillar.Month = int(dateTime.Month())

	// Detect solar term
	termName, passed, remaining, err := ultis.GetSolarTerm(path, dateTime)
	if err != nil {
		return nil, 0, 0, err
	}

	// Get earthly branch
	earthBranch := ultis.ConvertTermToBranch(termName)
	monthPillar.EarthlyBranch = earthBranch

	// Get heavenly stem
	valueOfFirstMonth := ultis.GetStemRuleByFiveTigers(yearPillar.HeavenlyStem.Value)
	valueToCal := (valueOfFirstMonth - 1) + monthPillar.EarthlyBranch.Value
	if valueToCal > 10 {
		valueToCal = valueToCal - 10
	}
	heavenlyStem := ultis.CalculateHeavenlyStem(valueToCal)
	monthPillar.HeavenlyStem = heavenlyStem

	return &monthPillar, passed, remaining, nil
}
