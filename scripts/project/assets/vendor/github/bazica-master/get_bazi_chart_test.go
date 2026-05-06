package bazica

import (
	"fmt"
	"github.com/tommitoan/bazica/model"
	"testing"
	"time"
)

func TestGetBaziChart(t *testing.T) {
	type args struct {
		year, month, day, hour, minute int
		loc                            string
		gender                         int
		prefixPath                     []string
	}
	tests := []struct {
		name    string
		args    args
		want    *model.BaziChart
		wantErr bool
	}{
		{"123", args{
			year: 1995, month: 6, day: 8, hour: 22, minute: 05,
			loc:        "Asia/Ho_Chi_Minh",
			gender:     1,
			prefixPath: nil,
		}, &model.BaziChart{
			PersonalInfo: nil,
			FourPillar: &model.FourPillars{
				YearPillar: &model.YearPillar{
					HeavenlyStem:  model.HeavenlyStem{Name: model.YinWoodName, Value: model.YinWoodValue},
					EarthlyBranch: model.EarthlyBranch{Name: model.Pig, Value: model.PigValue},
					Year:          1995,
					GanZhi: model.GanZhi{
						Name:         "Fire on the Mountain",
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
			LuckPillars: nil,
		}, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			location, _ := time.LoadLocation(tt.args.loc)
			date := time.Date(tt.args.year, time.Month(tt.args.month), tt.args.day, tt.args.hour, tt.args.minute, 0, 0, location)
			got, err := GetBaziChart(date, location, tt.args.gender, tt.args.prefixPath...)
			if (err != nil) != tt.wantErr {
				t.Errorf("GetBaziChart() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			fmt.Println(got)
			//if !reflect.DeepEqual(got, tt.want) {
			//	t.Errorf("GetBaziChart() got = %v, want %v", got, tt.want)
			//}
		})
	}
}
