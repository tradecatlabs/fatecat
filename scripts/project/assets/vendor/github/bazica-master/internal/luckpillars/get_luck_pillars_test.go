package luckpillars

import (
	"encoding/json"
	"fmt"
	"github.com/tommitoan/bazica/model"
	"reflect"
	"testing"
	"time"
)

func TestGetLuckPillars(t *testing.T) {
	type args struct {
		fourPillars *model.FourPillars
		gender      int
		passed      int
		remaining   int
		time        time.Time
		prefixPath  []string
	}

	tests := []struct {
		name    string
		args    args
		want    time.Time
		wantErr bool
	}{
		{"happy case", args{
			fourPillars: &model.FourPillars{
				YearPillar: &model.YearPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinWoodName, Value: model.YinWoodValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Pig, Value: model.PigValue},
					Year:          1995,
				},
				MonthPillar: &model.MonthPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YangWaterName, Value: model.YangWaterValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Horse, Value: model.HorseValue},
					Month:         6,
				},
				DayPillar: &model.DayPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YangMetalName, Value: model.YangMetalValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Horse, Value: model.HorseValue},
					Day:           8,
				},
				HourPillar: &model.HourPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinFireName, Value: model.YinFireValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Pig, Value: model.PigValue},
					Hour:          model.TimeOfDay{Hour: 22, Minute: 05},
				},
			},
			gender:     1,
			passed:     4124,
			remaining:  21429,
			time:       time.Date(1995, time.June, 8, 22, 05, 0, 0, time.UTC),
			prefixPath: nil,
		}, time.Date(1996, time.May, 18, 22, 05, 0, 0, time.UTC), false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := GetLuckPillars(tt.args.fourPillars, tt.args.gender, tt.args.passed, tt.args.remaining, tt.args.time, tt.args.prefixPath...)
			jsonData, _ := json.Marshal(got)
			fmt.Println(string(jsonData))
			if (err != nil) != tt.wantErr {
				t.Errorf("GetLuckPillars() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got.LuckPillars[1].Time, tt.want) {
				t.Errorf("GetLuckPillars() got = %v, want %v", got, tt.want)
			}
		})
	}
}
