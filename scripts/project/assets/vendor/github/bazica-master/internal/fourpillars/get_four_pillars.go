package fourpillars

import (
	"encoding/json"
	"github.com/tommitoan/bazica/internal/ultis"
	"github.com/tommitoan/bazica/model"
	"log/slog"
	"strings"
	"time"
)

func GetFourPillars(dateTime time.Time, loc *time.Location, prefixPath ...string) (*model.FourPillars, int, int, error) {
	var path string
	if len(prefixPath) != 0 {
		path = prefixPath[0]
	}

	var fourPillars model.FourPillars
	var ganzhi, mainElement string
	var valueElement int

	// Get Year pillar
	yearPillar, err := GetYearPillar(path, dateTime)
	if err != nil {
		return nil, 0, 0, err
	}
	fourPillars.YearPillar = yearPillar

	var yearStemBranch strings.Builder
	yearStemBranch.WriteString(yearPillar.HeavenlyStem.Name)
	yearStemBranch.WriteString(" ")
	yearStemBranch.WriteString(yearPillar.EarthlyBranch.Name)

	ganzhi, mainElement, valueElement = ultis.GetGanzhi(yearStemBranch.String())
	fourPillars.YearPillar.GanZhi.Name = ganzhi
	fourPillars.YearPillar.GanZhi.ElementName = mainElement
	fourPillars.YearPillar.GanZhi.ElementValue = valueElement

	// Get Month pillar
	monthPillar, passed, remaining, err := GetMonthPillar(path, yearPillar, dateTime)
	if err != nil {
		return nil, 0, 0, err
	}
	fourPillars.MonthPillar = monthPillar

	var monthStemBranch strings.Builder
	monthStemBranch.WriteString(monthPillar.HeavenlyStem.Name)
	monthStemBranch.WriteString(" ")
	monthStemBranch.WriteString(monthPillar.EarthlyBranch.Name)

	ganzhi, mainElement, valueElement = ultis.GetGanzhi(monthStemBranch.String())
	fourPillars.MonthPillar.GanZhi.Name = ganzhi
	fourPillars.MonthPillar.GanZhi.ElementName = mainElement
	fourPillars.MonthPillar.GanZhi.ElementValue = valueElement

	// Get Day pillar
	dayPillar, err := GetDayPillar(dateTime, loc)
	if err != nil {
		return nil, 0, 0, err
	}
	fourPillars.DayPillar = dayPillar

	var dayStemBranch strings.Builder
	dayStemBranch.WriteString(dayPillar.HeavenlyStem.Name)
	dayStemBranch.WriteString(" ")
	dayStemBranch.WriteString(dayPillar.EarthlyBranch.Name)

	ganzhi, mainElement, valueElement = ultis.GetGanzhi(dayStemBranch.String())
	fourPillars.DayPillar.GanZhi.Name = ganzhi
	fourPillars.DayPillar.GanZhi.ElementName = mainElement
	fourPillars.DayPillar.GanZhi.ElementValue = valueElement

	// Get Hour pillar
	hourPillar, err := GetHourPillar(dayPillar, dateTime)
	if err != nil {
		return nil, 0, 0, err
	}
	fourPillars.HourPillar = hourPillar

	var hourStemBranch strings.Builder
	hourStemBranch.WriteString(hourPillar.HeavenlyStem.Name)
	hourStemBranch.WriteString(" ")
	hourStemBranch.WriteString(hourPillar.EarthlyBranch.Name)

	ganzhi, mainElement, valueElement = ultis.GetGanzhi(hourStemBranch.String())
	fourPillars.HourPillar.GanZhi.Name = ganzhi
	fourPillars.HourPillar.GanZhi.ElementName = mainElement
	fourPillars.HourPillar.GanZhi.ElementValue = valueElement

	jsonData, _ := json.Marshal(fourPillars)
	slog.Info(string(jsonData))
	return &fourPillars, passed, remaining, nil
}
