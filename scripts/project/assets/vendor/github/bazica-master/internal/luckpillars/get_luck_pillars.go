package luckpillars

import (
	"fmt"
	"github.com/tommitoan/bazica/internal/ultis"
	"github.com/tommitoan/bazica/model"
	"log/slog"
	"strings"
	"time"
)

func GetLuckPillars(fourPillars *model.FourPillars, gender, passed, remaining int, dateTime time.Time, prefixPath ...string) (*model.LuckPillars, error) {
	luckPillars := model.LuckPillars{}

	// Get 0 luck pillar
	zeroLuckPillars := &model.LuckPillar{
		HeavenlyStem:  fourPillars.MonthPillar.HeavenlyStem,
		EarthlyBranch: fourPillars.MonthPillar.EarthlyBranch,
		Number:        0,
		Time:          dateTime,
		YearStart:     dateTime.Year(),
	}

	var zeroGanzhi, zeroMainElement string
	var zeroValueElement int
	var zeroTempStemBranch strings.Builder
	zeroTempStemBranch.WriteString(zeroLuckPillars.HeavenlyStem.Name)
	zeroTempStemBranch.WriteString(" ")
	zeroTempStemBranch.WriteString(zeroLuckPillars.EarthlyBranch.Name)

	zeroGanzhi, zeroMainElement, zeroValueElement = ultis.GetGanzhi(zeroTempStemBranch.String())
	zeroLuckPillars.GanZhi.Name = zeroGanzhi
	zeroLuckPillars.GanZhi.ElementName = zeroMainElement
	zeroLuckPillars.GanZhi.ElementValue = zeroValueElement

	luckPillars.LuckPillars = append(luckPillars.LuckPillars, zeroLuckPillars)

	// Get Dayun rule (Increment or Decrement) with Yin/Yang Male/Female by Year Stem
	var incrementRule, age int
	if (fourPillars.YearPillar.HeavenlyStem.Value+gender)%2 == 0 {
		// Yang Male or Yin Female || Dương Nam Âm Nữ
		incrementRule = 1
		age = remaining
	} else {
		// Yin Male or Yang Female || Âm Nam Dương Nữ
		incrementRule = -1
		age = passed
	}
	slog.Info(fmt.Sprintf("LuckPillars increment rule: %v", incrementRule))

	// Calculate the remaining 11 luck pillars (excluding age and year)
	var branchValue int = fourPillars.MonthPillar.EarthlyBranch.Value
	var stemValue int = fourPillars.MonthPillar.HeavenlyStem.Value

	// pillar1
	for i := 1; i < 12; i++ {
		var luckPeriod time.Time
		branchValue += incrementRule
		if branchValue > 12 {
			branchValue = branchValue - 12
		} else if branchValue < 1 {
			branchValue = branchValue + 12
		}
		stemValue += incrementRule
		if stemValue > 10 {
			stemValue = stemValue - 10
		} else if stemValue < 1 {
			stemValue = stemValue + 10
		}

		branch := ultis.CalculateEarthlyBranch(branchValue)
		stem := ultis.CalculateHeavenlyStem(stemValue)

		if i == 1 {
			years := age / (60 * 24 * 3)
			months := ((age % (60 * 24 * 3)) / (60 * 24)) * 4
			days := (((age % (60 * 24 * 3)) % (60 * 24)) / 60) * 5

			luckPeriod = dateTime.AddDate(years, months, days)
			if luckPillars.LuckPillars[i-1].Time.Year() == luckPeriod.Year() {
				luckPillars.LuckPillars[i-1].YearEnd = luckPillars.LuckPillars[i-1].Time.Year()
			} else {
				luckPillars.LuckPillars[i-1].YearEnd = luckPeriod.Year() - 1
			}
		} else {
			luckPeriod = luckPillars.LuckPillars[i-1].Time.AddDate(10, 0, 0)
		}

		tempLuckPillars := &model.LuckPillar{
			HeavenlyStem:  stem,
			EarthlyBranch: branch,
			Number:        i,
			Time:          luckPeriod,
			YearStart:     luckPeriod.Year(),
			YearEnd:       luckPeriod.Year() + 9,
		}

		var ganzhi, mainElement string
		var valueElement int
		var tempStemBranch strings.Builder
		tempStemBranch.WriteString(tempLuckPillars.HeavenlyStem.Name)
		tempStemBranch.WriteString(" ")
		tempStemBranch.WriteString(tempLuckPillars.EarthlyBranch.Name)

		ganzhi, mainElement, valueElement = ultis.GetGanzhi(tempStemBranch.String())
		tempLuckPillars.GanZhi.Name = ganzhi
		tempLuckPillars.GanZhi.ElementName = mainElement
		tempLuckPillars.GanZhi.ElementValue = valueElement

		luckPillars.LuckPillars = append(luckPillars.LuckPillars, tempLuckPillars)
	}

	return &luckPillars, nil
}
