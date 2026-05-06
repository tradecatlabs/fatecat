package calendar

import (
	"fmt"
	"reflect"
	"strings"
	"testing"
	"time"

	"github.com/Lofanmi/chinese-calendar-golang/ganzhi"
	"github.com/Lofanmi/chinese-calendar-golang/lunar"
	"github.com/Lofanmi/chinese-calendar-golang/solar"
	"github.com/Lofanmi/chinese-calendar-golang/solarterm"
)

var equals = func(a, b *Calendar) bool {
	if a == nil {
		return b == nil
	}
	if b == nil {
		return a == nil
	}
	return a.Equals(b)
}

func TestBySolar(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 26, 0, time.Local)
	t2 := time.Date(2018, 3, 21, 0, 15, 26, 0, time.Local)
	type args struct {
		year   int64
		month  int64
		day    int64
		hour   int64
		minute int64
		second int64
	}
	tests := []struct {
		name string
		args args
		want *Calendar
	}{
		{"test_1", args{2018, 3, 21, 0, 0, 26}, &Calendar{
			t:      &t1,
			Solar:  solar.NewSolar(&t1),
			Lunar:  lunar.NewLunar(&t1),
			Ganzhi: ganzhi.NewGanzhi(&t1),
		}},
		{"test_2", args{2018, 3, 21, 0, 15, 26}, &Calendar{
			t:      &t2,
			Solar:  solar.NewSolar(&t2),
			Lunar:  lunar.NewLunar(&t2),
			Ganzhi: ganzhi.NewGanzhi(&t2),
		}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := BySolar(tt.args.year, tt.args.month, tt.args.day, tt.args.hour, tt.args.minute, tt.args.second); !equals(got, tt.want) {
				t.Errorf("BySolar() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestByLunar(t *testing.T) {
	t1 := time.Date(2017, 8, 15, 12, 0, 0, 0, time.Local)
	t2 := time.Date(2018, 3, 30, 23, 11, 30, 0, time.Local)
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
		want *Calendar
	}{
		{"test_1", args{2017, 6, 24, 12, 0, 0, true}, &Calendar{
			t:      &t1,
			Solar:  solar.NewSolar(&t1),
			Lunar:  lunar.NewLunar(&t1),
			Ganzhi: ganzhi.NewGanzhi(&t1),
		}},
		{"test_2", args{2018, 2, 14, 23, 11, 30, false}, &Calendar{
			t:      &t2,
			Solar:  solar.NewSolar(&t2),
			Lunar:  lunar.NewLunar(&t2),
			Ganzhi: ganzhi.NewGanzhi(&t2),
		}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := ByLunar(tt.args.year, tt.args.month, tt.args.day, tt.args.hour, tt.args.minute, tt.args.second, tt.args.isLeapMonth); !equals(got, tt.want) {
				t.Errorf("ByLunar() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestByTimestamp(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 26, 0, time.Local)
	t2 := time.Date(2018, 3, 21, 0, 15, 26, 0, time.Local)
	type args struct {
		ts int64
	}
	tests := []struct {
		name string
		args args
		want *Calendar
	}{
		{"test_1", args{t1.Unix()}, &Calendar{
			t:      &t1,
			Solar:  solar.NewSolar(&t1),
			Lunar:  lunar.NewLunar(&t1),
			Ganzhi: ganzhi.NewGanzhi(&t1),
		}},
		{"test_2", args{t2.Unix()}, &Calendar{
			t:      &t2,
			Solar:  solar.NewSolar(&t2),
			Lunar:  lunar.NewLunar(&t2),
			Ganzhi: ganzhi.NewGanzhi(&t2),
		}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := ByTimestamp(tt.args.ts); !equals(got, tt.want) {
				t.Errorf("ByTimestamp() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestCalendar_ToJSON(t *testing.T) {
	t1 := time.Date(2018, 3, 21, 0, 0, 26, 0, time.Local)
	c1 := ByTimestamp(t1.Unix())
	json1 := `{"ganzhi":{"animal":"狗","day":"壬子","day_order":49,"hour":"庚子","hour_order":37,"month":"乙卯","month_order":52,"year":"戊戌","year_order":35},"lunar":{"animal":"狗","day":5,"day_alias":"初五","is_leap":false,"is_leap_month":false,"leap_month":0,"month":2,"month_alias":"二月","year":2018,"year_alias":"二零一八"},"solar":{"animal":"狗","constellation":"白羊","day":21,"hour":0,"is_leep":false,"minute":0,"month":3,"nanosecond":0,"second":26,"week_alias":"三","week_number":3,"year":2018}}`

	t2 := time.Date(2020, 9, 20, 5, 15, 26, 0, time.Local)
	c2 := ByTimestamp(t2.Unix())
	json2 := `{"ganzhi":{"animal":"鼠","day":"丙寅","day_order":3,"hour":"辛卯","hour_order":28,"month":"乙酉","month_order":22,"year":"庚子","year_order":37},"lunar":{"animal":"鼠","day":4,"day_alias":"初四","is_leap":true,"is_leap_month":false,"leap_month":4,"month":8,"month_alias":"八月","year":2020,"year_alias":"二零二零"},"solar":{"animal":"鼠","constellation":"处女","day":20,"hour":5,"is_leep":true,"minute":15,"month":9,"nanosecond":0,"second":26,"week_alias":"日","week_number":0,"year":2020}}`

	tests := []struct {
		name     string
		calendar *Calendar
		want     []byte
		wantErr  bool
	}{
		{"test_1", c1, []byte(json1), false},
		{"test_2", c2, []byte(json2), false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := tt.calendar.ToJSON()
			if (err != nil) != tt.wantErr {
				t.Errorf("Calendar.ToJSON() error = %s, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Calendar.ToJSON() = %s, want %s", got, tt.want)
			}
		})
	}
}

func TestCalendar_Equals(t *testing.T) {
	t1 := time.Now().Unix()
	t2 := time.Now().Add(24 * time.Hour).Unix()
	tests := []struct {
		name string
		c    *Calendar
		c2   *Calendar
		want bool
	}{
		{"test_1", ByTimestamp(t1), ByTimestamp(t1), true},
		{"test_2", ByTimestamp(t1), ByTimestamp(t2), false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.c.Equals(tt.c2) != tt.want {
				t.Errorf("Calendar.Equals() failed")
			}
		})
	}
}

func TestCalendar(t *testing.T) {
	time.Local, _ = time.LoadLocation("PRC")
	t.Log(output(2025))
	t.Log(output(3000))
}

func output(year int) string {
	timeLayoutYMD := "2006-01-02"
	weekdays := []string{"周日", "周一", "周二", "周三", "周四", "周五", "周六"}

	var sb strings.Builder
	_, _ = sb.WriteString("\n")
	_, _ = sb.WriteString("公历日期   周   农历日期         干支               节气\n")
	_, _ = sb.WriteString("----------------------------------------------------------------------------\n")
	ti := time.Date(year, 1, 1, 0, 0, 0, 0, time.Local)
	for {
		if ti.Year() > year {
			break
		}
		c := ByTimestamp(ti.Unix())
		solarDate := ti.Format(timeLayoutYMD)
		weekday := weekdays[int(ti.Weekday())]
		lunarDate := fmt.Sprintf("%d%s年%s%s", c.Lunar.GetYear(), c.Lunar.Animal().Alias(), c.Lunar.MonthAlias(), c.Lunar.DayAlias())
		gzDate := fmt.Sprintf("%s年%s月%s日", c.Ganzhi.YearGanzhiAlias(), c.Ganzhi.MonthGanzhiAlias(), c.Ganzhi.DayGanzhiAlias())
		stInfo := ""
		p, n := solarterm.CalcSolarterm(&ti)
		if p != nil && p.Time().Format(timeLayoutYMD) == solarDate {
			stInfo = fmt.Sprintf("%s %s", p.Alias(), p.Time().Format("2006-01-02 15:04:05"))
		}
		if n != nil && n.Time().Format(timeLayoutYMD) == solarDate {
			stInfo = fmt.Sprintf("%s %s", n.Alias(), n.Time().Format("2006-01-02 15:04:05"))
		}
		_, _ = sb.WriteString(fmt.Sprintf("%s %s %s %s %s\n", solarDate, weekday, lunarDate, gzDate, stInfo))
		ti = ti.AddDate(0, 0, 1)
	}

	return sb.String()
}
