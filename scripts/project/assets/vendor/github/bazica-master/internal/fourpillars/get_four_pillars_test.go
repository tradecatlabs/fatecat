package fourpillars

import (
	"bytes"
	"encoding/json"
	"github.com/tommitoan/bazica/model"
	"testing"
	"time"
)

func TestGetFourPillarChart(t *testing.T) {
	var path = "../../"
	// Test Cases: Each case defines a birthdate, expected chart, and (optionally) a description.
	testCases := []struct {
		loc                            string
		year, month, day, hour, minute int
		expectedChart                  *model.FourPillars
		description                    string
	}{
		{"Asia/Ho_Chi_Minh",
			1977, 7, 12, 23, 30,
			&model.FourPillars{
				YearPillar: &model.YearPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinFireName, Value: model.YinFireValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Snake, Value: model.SnakeValue},
					Year:          1977,
					GanZhi: model.GanZhi{
						Name:         "Desert earth",
						ElementName:  "Earth",
						ElementValue: 5,
					},
				},
				MonthPillar: &model.MonthPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinFireName, Value: model.YinFireValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Goat, Value: model.GoatValue},
					Month:         7,
					GanZhi: model.GanZhi{
						Name:         "Sky water",
						ElementName:  "Water",
						ElementValue: 1,
					},
				},
				DayPillar: &model.DayPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinMetalName, Value: model.YinMetalValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Goat, Value: model.GoatValue},
					Day:           12,
					GanZhi: model.GanZhi{
						Name:         "Road earth",
						ElementName:  "Earth",
						ElementValue: 5,
					},
				},
				HourPillar: &model.HourPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YangEarthName, Value: model.YangEarthValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Rat, Value: model.RatValue},
					Hour:          model.TimeOfDay{Hour: 23, Minute: 30},
					GanZhi: model.GanZhi{
						Name:         "Lightning fire",
						ElementName:  "Fire",
						ElementValue: 2,
					},
				},
			},
			"case 1"},
		{"Asia/Ho_Chi_Minh",
			1995, 6, 8, 22, 05,
			&model.FourPillars{
				YearPillar: &model.YearPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinWoodName, Value: model.YinWoodValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Pig, Value: model.PigValue},
					Year:          1995,
					GanZhi: model.GanZhi{
						Name:         "Volcanic fire",
						ElementName:  "Fire",
						ElementValue: 2,
					},
				},
				MonthPillar: &model.MonthPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YangWaterName, Value: model.YangWaterValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Horse, Value: model.HorseValue},
					Month:         6,
					GanZhi: model.GanZhi{
						Name:         "Willow Tree Wood",
						ElementName:  "Wood",
						ElementValue: 3,
					},
				},
				DayPillar: &model.DayPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YangMetalName, Value: model.YangMetalValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Horse, Value: model.HorseValue},
					Day:           8,
					GanZhi: model.GanZhi{
						Name:         "Earth on the Roadside",
						ElementName:  "Earth",
						ElementValue: 5,
					},
				},
				HourPillar: &model.HourPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinFireName, Value: model.YinFireValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Pig, Value: model.PigValue},
					Hour:          model.TimeOfDay{Hour: 22, Minute: 05},
					GanZhi: model.GanZhi{
						Name:         "Earth on the Roof",
						ElementName:  "Earth",
						ElementValue: 5,
					},
				},
			},
			"case 2"},
	}

	// Loop through each test case
	for _, tc := range testCases {
		// Create time object
		location, _ := time.LoadLocation(tc.loc)
		dateTime := time.Date(tc.year, time.Month(tc.month), tc.day, tc.hour, tc.minute, 0, 0, location)

		// Get the chart
		baziChart, _, _, err := GetFourPillars(dateTime, location, path)
		if err != nil {
			t.Errorf("Error for %s: %v", tc.description, err) // Include description in error message
			continue                                          // Skip to next case if this one failed
		}

		jsonData, _ := json.Marshal(baziChart)
		expectData, _ := json.Marshal(tc.expectedChart)

		// Compare JSON output
		if !bytes.Equal(jsonData, expectData) {
			t.Errorf("Mismatch for %s:\nExpected: %v\nGot: %v", tc.description, tc.expectedChart, baziChart)
		}
	}
}
