package lunar

import (
	"reflect"
	"testing"
	"time"

	"github.com/Lofanmi/chinese-calendar-golang/animal"
)

func TestFromSolarTimestamp(t *testing.T) {
	type args struct {
		ts int64
	}
	tests := []struct {
		name                 string
		args                 args
		wantLunarYear        int64
		wantLunarMonth       int64
		wantLunarDay         int64
		wantLunarMonthIsLeap bool
	}{
		{"test_1", args{1502769600}, 2017, 6, 24, true},
		{"test_2", args{1522422690}, 2018, 2, 14, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotLunarYear, gotLunarMonth, gotLunarDay, gotLunarMonthIsLeap := FromSolarTimestamp(tt.args.ts)
			if gotLunarYear != tt.wantLunarYear {
				t.Errorf("FromSolarTimestamp() gotLunarYear = %v, want %v", gotLunarYear, tt.wantLunarYear)
			}
			if gotLunarMonth != tt.wantLunarMonth {
				t.Errorf("FromSolarTimestamp() gotLunarMonth = %v, want %v", gotLunarMonth, tt.wantLunarMonth)
			}
			if gotLunarDay != tt.wantLunarDay {
				t.Errorf("FromSolarTimestamp() gotLunarDay = %v, want %v", gotLunarDay, tt.wantLunarDay)
			}
			if gotLunarMonthIsLeap != tt.wantLunarMonthIsLeap {
				t.Errorf("FromSolarTimestamp() gotLunarMonthIsLeap = %v, want %v", gotLunarMonthIsLeap, tt.wantLunarMonthIsLeap)
			}
		})
	}
}

func TestToSolarTimestamp(t *testing.T) {
	type args struct {
		year        int64
		month       int64
		day         int64
		hour        int64
		minute      int64
		second      int64
		isLeapMonth bool
	}
	tests := []struct {
		name string
		args args
		want int64
	}{
		{"test_1", args{2017, 6, 24, 12, 0, 0, true}, 1502769600},
		{"test_2", args{2018, 2, 14, 23, 11, 30, true}, 1522422690},
		{"test_3", args{2018, 2, 14, 23, 11, 30, false}, 1522422690},
		{"test_4", args{1900, 1, 14, 23, 11, 30, false}, 0},
		{"test_5", args{3000, 12, 14, 23, 11, 30, false}, 0},
		{"test_6", args{1900 - 1, 1, 14, 23, 11, 30, false}, 0},
		{"test_7", args{3000 + 1, 12, 14, 23, 11, 30, false}, 0},
		{"test_8", args{1900, 2, 100000, 23, 11, 30, false}, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := ToSolarTimestamp(tt.args.year, tt.args.month, tt.args.day, tt.args.hour, tt.args.minute, tt.args.second, tt.args.isLeapMonth); got != tt.want {
				t.Errorf("ToSolarTimestamp() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestNewLunar(t *testing.T) {
	t1 := time.Date(2017, 8, 15, 12, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 3, 30, 23, 11, 30, 0, time.Local)
	type args struct {
		t *time.Time
	}
	tests := []struct {
		name string
		args args
		want *Lunar
	}{
		{"test_1", args{&t1}, &Lunar{
			t:           &t1,
			year:        2017,
			month:       6,
			day:         24,
			monthIsLeap: true,
		}},
		{"test_2", args{&t2}, &Lunar{
			t:           &t2,
			year:        2018,
			month:       2,
			day:         14,
			monthIsLeap: false,
		}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := NewLunar(tt.args.t); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("NewLunar() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_LeapMonth(t *testing.T) {
	t1 := time.Date(2018, 6, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 1, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  int64
	}{
		{"test_1", NewLunar(&t1), 0},
		{"test_2", NewLunar(&t2), 6},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.LeapMonth(); got != tt.want {
				t.Errorf("Lunar.LeapMonth() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_IsLeap(t *testing.T) {
	t1 := time.Date(2018, 6, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 1, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  bool
	}{
		{"test_1", NewLunar(&t1), false},
		{"test_2", NewLunar(&t2), true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.IsLeap(); got != tt.want {
				t.Errorf("Lunar.IsLeap() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_IsLeapMonth(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 15, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 8, 15, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  bool
	}{
		{"test_1", NewLunar(&t1), false},
		{"test_2", NewLunar(&t2), false},
		{"test_3", NewLunar(&t3), true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.IsLeapMonth(); got != tt.want {
				t.Errorf("Lunar.IsLeapMonth() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_Animal(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 15, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 8, 15, 0, 0, 0, 0, time.Local)

	tests := []struct {
		name  string
		lunar *Lunar
		want  *animal.Animal
	}{
		{"test_1", NewLunar(&t1), animal.NewAnimal(11)},
		{"test_2", NewLunar(&t2), animal.NewAnimal(10)},
		{"test_3", NewLunar(&t3), animal.NewAnimal(10)},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.Animal(); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Lunar.Animal() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_YearAlias(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 15, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 8, 15, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  string
	}{
		{"test_1", NewLunar(&t1), "二零一八"},
		{"test_2", NewLunar(&t2), "二零一七"},
		{"test_3", NewLunar(&t3), "二零一七"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.YearAlias(); got != tt.want {
				t.Errorf("Lunar.YearAlias() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_GetYear(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 15, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 8, 15, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  int64
	}{
		{"test_1", NewLunar(&t1), 2018},
		{"test_2", NewLunar(&t2), 2017},
		{"test_3", NewLunar(&t3), 2017},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.GetYear(); got != tt.want {
				t.Errorf("Lunar.GetYear() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_MonthAlias(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 15, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 8, 15, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  string
	}{
		{"test_1", NewLunar(&t1), "三月"},
		{"test_2", NewLunar(&t2), "五月"},
		{"test_3", NewLunar(&t3), "闰六月"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.MonthAlias(); got != tt.want {
				t.Errorf("Lunar.MonthAlias() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_GetMonth(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 15, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 8, 15, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name  string
		lunar *Lunar
		want  int64
	}{
		{"test_1", NewLunar(&t1), 3},
		{"test_2", NewLunar(&t2), 5},
		{"test_3", NewLunar(&t3), 6},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.lunar.GetMonth(); got != tt.want {
				t.Errorf("Lunar.GetMonth() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestLunar_DayAlias(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 4, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 6, 14, 0, 0, 0, 0, time.Local)
	t4 := time.Date(2017, 8, 21, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name      string
		lunar     *Lunar
		wantAlias string
	}{
		{"test_1", NewLunar(&t1), "十六"},
		{"test_2", NewLunar(&t2), "初十"},
		{"test_3", NewLunar(&t3), "二十"},
		{"test_33", NewLunar(&t4), "三十"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotAlias := tt.lunar.DayAlias(); gotAlias != tt.wantAlias {
				t.Errorf("Lunar.DayAlias() = %v, want %v", gotAlias, tt.wantAlias)
			}
		})
	}
}

func TestLunar_GetDay(t *testing.T) {
	t1 := time.Date(2018, 5, 1, 0, 0, 0, 0, time.Local)
	t2 := time.Date(2017, 6, 4, 0, 0, 0, 0, time.Local)
	t3 := time.Date(2017, 6, 14, 0, 0, 0, 0, time.Local)
	t4 := time.Date(2017, 8, 21, 0, 0, 0, 0, time.Local)
	t5 := time.Date(2057, 9, 28, 0, 0, 0, 0, time.Local)
	t6 := time.Date(2057, 10, 27, 0, 0, 0, 0, time.Local)
	tests := []struct {
		name      string
		lunar     *Lunar
		wantAlias int64
	}{
		{"test_1", NewLunar(&t1), 16},
		{"test_2", NewLunar(&t2), 10},
		{"test_3", NewLunar(&t3), 20},
		{"test_4", NewLunar(&t4), 30},
		{"test_5", NewLunar(&t5), 1},  // 2057-09-28（九月初一）
		{"test_6", NewLunar(&t6), 30}, // 2057-10-27（九月三十）
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotAlias := tt.lunar.GetDay(); gotAlias != tt.wantAlias {
				t.Errorf("Lunar.GetDay() = %v, want %v", gotAlias, tt.wantAlias)
			}
		})
	}
}

func Test_lunarDays(t *testing.T) {
	type args struct {
		year  int64
		month int64
	}
	tests := []struct {
		name     string
		args     args
		wantDays int64
	}{
		{"test_1", args{2018, 0}, -1},
		{"test_2", args{2018, 13}, -1},
		{"test_3", args{2017, 6}, 29},
		{"test_3", args{2017, 8}, 30},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotDays := lunarDays(tt.args.year, tt.args.month); gotDays != tt.wantDays {
				t.Errorf("lunarDays() = %v, want %v", gotDays, tt.wantDays)
			}
		})
	}
}

func TestLunar_Equals(t *testing.T) {
	t1 := time.Now()
	t2 := t1.Add(24 * time.Hour)
	tests := []struct {
		name   string
		lunar  *Lunar
		lunar2 *Lunar
		want   bool
	}{
		{"test_1", NewLunar(&t1), NewLunar(&t1), true},
		{"test_2", NewLunar(&t1), NewLunar(&t2), false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.lunar.Equals(tt.lunar2) != tt.want {
				t.Errorf("Lunar.Equals() failed")
			}
		})
	}
}
