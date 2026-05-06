package calendar

import (
	"encoding/json"
	"time"

	"github.com/Lofanmi/chinese-calendar-golang/ganzhi"
	"github.com/Lofanmi/chinese-calendar-golang/lunar"
	"github.com/Lofanmi/chinese-calendar-golang/solar"
)

// Calendar 日历
type Calendar struct {
	t      *time.Time
	Solar  *solar.Solar
	Lunar  *lunar.Lunar
	Ganzhi *ganzhi.Ganzhi
}

// ByTimestamp 通过时间戳创建
func ByTimestamp(ts int64) *Calendar {
	t := time.Unix(ts, 0)
	sc := solar.NewSolar(&t)
	lc := lunar.NewLunar(&t)
	gz := ganzhi.NewGanzhi(&t)
	return &Calendar{
		t:      &t,
		Solar:  sc,
		Lunar:  lc,
		Ganzhi: gz,
	}
}

// BySolar 通过国历创建
func BySolar(year, month, day, hour, minute, second int64) *Calendar {
	t := time.Date(int(year),
		time.Month(month),
		int(day),
		int(hour),
		int(minute),
		int(second),
		0,
		time.Local,
	)
	return ByTimestamp(t.Unix())
}

// ByLunar 通过农历创建
func ByLunar(year, month, day, hour, minute, second int64, isLeapMonth bool) *Calendar {
	ts := lunar.ToSolarTimestamp(year, month, day, hour, minute, second, isLeapMonth)
	return ByTimestamp(ts)
}

// ToJSON JSON输出
func (calendar *Calendar) ToJSON() ([]byte, error) {
	m := make(map[string]interface{})
	m1 := make(map[string]interface{})
	m2 := make(map[string]interface{})
	m3 := make(map[string]interface{})

	m1["year"] = calendar.Solar.GetYear()
	m1["month"] = calendar.Solar.GetMonth()
	m1["day"] = calendar.Solar.GetDay()
	m1["hour"] = calendar.Solar.GetHour()
	m1["minute"] = calendar.Solar.GetMinute()
	m1["second"] = calendar.Solar.GetSecond()
	m1["nanosecond"] = calendar.Solar.GetNanosecond()
	m1["is_leep"] = calendar.Solar.IsLeep()
	m1["week_number"] = calendar.Solar.WeekNumber()
	m1["week_alias"] = calendar.Solar.WeekAlias()
	m1["animal"] = calendar.Solar.Animal().Alias()
	m1["constellation"] = calendar.Solar.Constellation().Alias()

	m2["year"] = calendar.Lunar.GetYear()
	m2["month"] = calendar.Lunar.GetMonth()
	m2["day"] = calendar.Lunar.GetDay()
	m2["is_leap_month"] = calendar.Lunar.IsLeapMonth()
	m2["is_leap"] = calendar.Lunar.IsLeap()
	m2["leap_month"] = calendar.Lunar.LeapMonth()
	m2["animal"] = calendar.Lunar.Animal().Alias()
	m2["year_alias"] = calendar.Lunar.YearAlias()
	m2["month_alias"] = calendar.Lunar.MonthAlias()
	m2["day_alias"] = calendar.Lunar.DayAlias()

	m3["animal"] = calendar.Ganzhi.Animal().Alias()
	m3["year"] = calendar.Ganzhi.YearGanzhiAlias()
	m3["month"] = calendar.Ganzhi.MonthGanzhiAlias()
	m3["day"] = calendar.Ganzhi.DayGanzhiAlias()
	m3["hour"] = calendar.Ganzhi.HourGanzhiAlias()
	m3["year_order"] = calendar.Ganzhi.YearGanzhiOrder()
	m3["month_order"] = calendar.Ganzhi.MonthGanzhiOrder()
	m3["day_order"] = calendar.Ganzhi.DayGanzhiOrder()
	m3["hour_order"] = calendar.Ganzhi.HourGanzhiOrder()

	m["solar"] = m1
	m["lunar"] = m2
	m["ganzhi"] = m3

	return json.Marshal(m)
}

// Equals 判断两个对象是否相同
func (calendar *Calendar) Equals(b *Calendar) bool {
	return calendar.Ganzhi.Equals(b.Ganzhi) &&
		calendar.Lunar.Equals(b.Lunar) &&
		calendar.Solar.Equals(b.Solar)
}
