package solar

import (
	"time"

	"github.com/Lofanmi/chinese-calendar-golang/animal"
	"github.com/Lofanmi/chinese-calendar-golang/constellation"
	"github.com/Lofanmi/chinese-calendar-golang/solarterm"
	"github.com/Lofanmi/chinese-calendar-golang/utils"
)

// Solar 公历
type Solar struct {
	t                *time.Time
	CurrentSolarterm *solarterm.Solarterm
	PrevSolarterm    *solarterm.Solarterm
	NextSolarterm    *solarterm.Solarterm
}

var weekAlias = [...]string{
	"日", "一", "二", "三", "四", "五", "六",
}

// NewSolar 创建公历对象
func NewSolar(t *time.Time) *Solar {
	var c *solarterm.Solarterm
	p, n := solarterm.CalcSolarterm(t)
	if n.Index()-p.Index() == 1 {
		if p.IsInDay(t) {
			c = p
			p = p.Prev()
		}
		if n.IsInDay(t) {
			c = n
			p = c.Prev()
			n = c.Next()
		}
	}
	return &Solar{
		t:                t,
		CurrentSolarterm: c,
		PrevSolarterm:    p,
		NextSolarterm:    n,
	}
}

// IsLeep 是否为闰年
func (solar *Solar) IsLeep() bool {
	year := solar.t.Year()
	return year%4 == 0 && year%100 != 0 || year%400 == 0
}

// WeekNumber 返回当前周次(周日为0, 周一为1...)
func (solar *Solar) WeekNumber() int64 {
	return int64(solar.t.Weekday())
}

// WeekAlias 返回当前周次(日, 一...)
func (solar *Solar) WeekAlias() string {
	return weekAlias[solar.WeekNumber()]
}

// Animal 返回年份生肖
func (solar *Solar) Animal() *animal.Animal {
	return animal.NewAnimal(utils.OrderMod(int64(solar.t.Year()-3), 12))
}

// Constellation 返回星座
func (solar *Solar) Constellation() *constellation.Constellation {
	return constellation.NewConstellation(solar.t)
}

// GetYear 年
func (solar *Solar) GetYear() int64 {
	return int64(solar.t.Year())
}

// GetMonth 月
func (solar *Solar) GetMonth() int64 {
	return int64(solar.t.Month())
}

// GetDay 日
func (solar *Solar) GetDay() int64 {
	return int64(solar.t.Day())
}

// GetHour 时
func (solar *Solar) GetHour() int64 {
	return int64(solar.t.Hour())
}

// GetMinute 分
func (solar *Solar) GetMinute() int64 {
	return int64(solar.t.Minute())
}

// GetSecond 秒
func (solar *Solar) GetSecond() int64 {
	return int64(solar.t.Second())
}

// GetNanosecond 毫秒
func (solar *Solar) GetNanosecond() int64 {
	return int64(solar.t.Nanosecond())
}

// Equals 返回两个对象是否相同
func (solar *Solar) Equals(b *Solar) bool {
	return solar.GetYear() == b.GetYear() &&
		solar.GetMonth() == b.GetMonth() &&
		solar.GetDay() == b.GetDay() &&
		solar.GetHour() == b.GetHour() &&
		solar.GetMinute() == b.GetMinute() &&
		solar.GetSecond() == b.GetSecond() &&
		solar.GetNanosecond() == b.GetNanosecond()
}
