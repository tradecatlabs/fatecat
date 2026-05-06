package solar

import (
	"reflect"
	"testing"
	"time"

	"github.com/Lofanmi/chinese-calendar-golang/animal"
	"github.com/Lofanmi/chinese-calendar-golang/constellation"
	"github.com/Lofanmi/chinese-calendar-golang/solarterm"
)

func TestNewSolar(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 26, 0, time.Local)
	t2 := time.Date(2018, 3, 21, 0, 15, 26, 0, time.Local)
	t3 := time.Date(2018, 3, 21, 0, 15, 27, 0, time.Local)
	t4 := time.Date(2018, 3, 21, 0, 16, 26, 0, time.Local)
	t5 := time.Date(2018, 4, 1, 0, 0, 0, 0, time.Local)
	type args struct {
		t *time.Time
	}
	tests := []struct {
		name string
		args args
		want *Solar
	}{
		{"test_1", args{&t1}, &Solar{
			t:                &t1,
			CurrentSolarterm: solarterm.NewSolarterm(2741),
			PrevSolarterm:    solarterm.NewSolarterm(2740),
			NextSolarterm:    solarterm.NewSolarterm(2742),
		}},
		{"test_2", args{&t2}, &Solar{
			t:                &t2,
			CurrentSolarterm: solarterm.NewSolarterm(2741),
			PrevSolarterm:    solarterm.NewSolarterm(2740),
			NextSolarterm:    solarterm.NewSolarterm(2742),
		}},
		{"test_3", args{&t3}, &Solar{
			t:                &t3,
			CurrentSolarterm: solarterm.NewSolarterm(2741),
			PrevSolarterm:    solarterm.NewSolarterm(2740),
			NextSolarterm:    solarterm.NewSolarterm(2742),
		}},
		{"test_4", args{&t4}, &Solar{
			t:                &t4,
			CurrentSolarterm: solarterm.NewSolarterm(2741),
			PrevSolarterm:    solarterm.NewSolarterm(2740),
			NextSolarterm:    solarterm.NewSolarterm(2742),
		}},
		{"test_5", args{&t5}, &Solar{
			t:                &t5,
			CurrentSolarterm: nil,
			PrevSolarterm:    solarterm.NewSolarterm(2741),
			NextSolarterm:    solarterm.NewSolarterm(2742),
		}},
	}
	equal := func(a, b *Solar) (result bool) {
		if a.t.Nanosecond() != b.t.Nanosecond() {
			result = false
		} else if a.CurrentSolarterm != nil && b.CurrentSolarterm != nil && a.CurrentSolarterm.Index() != b.CurrentSolarterm.Index() {
			result = false
		} else if a.PrevSolarterm != nil && b.PrevSolarterm != nil && a.PrevSolarterm.Index() != b.PrevSolarterm.Index() {
			result = false
		} else if a.NextSolarterm != nil && b.NextSolarterm != nil && a.NextSolarterm.Index() != b.NextSolarterm.Index() {
			result = false
		} else {
			result = true
		}
		return
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := NewSolar(tt.args.t); !equal(got, tt.want) {
				t.Errorf("NewSolar() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_IsLeep(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2020, 3, 21, 0, 1, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  bool
	}{
		{"test_2018", NewSolar(&t1), false},
		{"test_2020", NewSolar(&t2), true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.IsLeep(); got != tt.want {
				t.Errorf("Solar.IsLeep() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_WeekNumber(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 3, 25, 0, 1, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 3},
		{"test_2", NewSolar(&t2), 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.WeekNumber(); got != tt.want {
				t.Errorf("Solar.WeekNumber() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_WeekAlias(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 3, 25, 0, 1, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  string
	}{
		{"test_1", NewSolar(&t1), "三"},
		{"test_2", NewSolar(&t2), "日"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.WeekAlias(); got != tt.want {
				t.Errorf("Solar.WeekAlias() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_Animal(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2019, 3, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  *animal.Animal
	}{
		{"test_1", NewSolar(&t1), animal.NewAnimal(11)},
		{"test_1", NewSolar(&t2), animal.NewAnimal(12)},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.Animal(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.Animal() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_Constellation(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  *constellation.Constellation
	}{
		{"test_1", NewSolar(&t1), constellation.NewConstellation(&t1)},
		{"test_2", NewSolar(&t2), constellation.NewConstellation(&t2)},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.Constellation(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.Constellation() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_GetYear(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 2015},
		{"test_2", NewSolar(&t2), 2018},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetYear(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetYear() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_GetMonth(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 1},
		{"test_2", NewSolar(&t2), 11},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetMonth(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetMonth() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_GetDay(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 20},
		{"test_2", NewSolar(&t2), 21},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetDay(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetDay() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_GetHour(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 0},
		{"test_2", NewSolar(&t2), 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetHour(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetHour() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_GetMinute(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 0},
		{"test_2", NewSolar(&t2), 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetMinute(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetMinute() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_GetSecond(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 0},
		{"test_2", NewSolar(&t2), 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetSecond(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetSecond() = %v, want %v", got, tt.want)
			}
		})
	}
}
func TestSolar_GetNanosecond(t *testing.T) {
	t1 := time.Date(2015, 1, 20, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 11, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		solar *Solar
		want  int64
	}{
		{"test_1", NewSolar(&t1), 0},
		{"test_2", NewSolar(&t2), 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.solar.GetNanosecond(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Solar.GetNanosecond() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSolar_Equals(t *testing.T) {
	t1 := time.Now()
	t2 := t1.Add(24 * time.Hour)
	tests := []struct {
		name   string
		solar  *Solar
		solar2 *Solar
		want   bool
	}{
		{"test_1", NewSolar(&t1), NewSolar(&t1), true},
		{"test_2", NewSolar(&t1), NewSolar(&t2), false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.solar.Equals(tt.solar2) != tt.want {
				t.Errorf("Solar.Equals() failed")
			}
		})
	}
}
