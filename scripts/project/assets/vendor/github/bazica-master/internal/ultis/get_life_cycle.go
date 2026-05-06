package ultis

import "github.com/tommitoan/bazica/model"

func GetLifeCycleFromFourPillar(pillars *model.FourPillars) *model.FourPillars {
	dayValue := pillars.DayPillar.HeavenlyStem.Value
	lifeCycleValue := GetLifeCycleRule(dayValue)

	pillars.YearPillar.LifeCycle = GetLifeCycleByRuleAndBranch(pillars.YearPillar.EarthlyBranch.Value, lifeCycleValue)
	pillars.MonthPillar.LifeCycle = GetLifeCycleByRuleAndBranch(pillars.MonthPillar.EarthlyBranch.Value, lifeCycleValue)
	pillars.DayPillar.LifeCycle = GetLifeCycleByRuleAndBranch(pillars.DayPillar.EarthlyBranch.Value, lifeCycleValue)
	pillars.HourPillar.LifeCycle = GetLifeCycleByRuleAndBranch(pillars.HourPillar.EarthlyBranch.Value, lifeCycleValue)

	return pillars
}

func GetLifeCycleByRuleAndBranch(branchValue int, lifeCycleValue int) string {
	valueToCal := (lifeCycleValue - 1) + branchValue
	if valueToCal > 12 {
		valueToCal = valueToCal - 12
	}
	return ConvertValueToLifeCycle(valueToCal)
}
