package constellation

import (
	"time"
)

// Constellation 星座
type Constellation struct {
	t *time.Time
}

// NewConstellation 创建星座对象
func NewConstellation(t *time.Time) *Constellation {
	return &Constellation{t: t}
}

// Alias 返回星座名称
func (constellation *Constellation) Alias() (s string) {
	month := constellation.t.Month()
	day := constellation.t.Day()
	if (month == 1 && day >= 20) || (month == 2 && day <= 18) {
		s = "水瓶"
	} else if (month == 2 && day >= 19) || (month == 3 && day <= 20) {
		s = "双鱼"
	} else if (month == 3 && day >= 21) || (month == 4 && day <= 19) {
		s = "白羊"
	} else if (month == 4 && day >= 20) || (month == 5 && day <= 20) {
		s = "金牛"
	} else if (month == 5 && day >= 21) || (month == 6 && day <= 21) {
		s = "双子"
	} else if (month == 6 && day >= 22) || (month == 7 && day <= 22) {
		s = "巨蟹"
	} else if (month == 7 && day >= 23) || (month == 8 && day <= 22) {
		s = "狮子"
	} else if (month == 8 && day >= 23) || (month == 9 && day <= 22) {
		s = "处女"
	} else if (month == 9 && day >= 23) || (month == 10 && day <= 23) {
		s = "天秤"
	} else if (month == 10 && day >= 24) || (month == 11 && day <= 22) {
		s = "天蝎"
	} else if (month == 11 && day >= 23) || (month == 12 && day <= 21) {
		s = "射手"
	} else if (month == 12 && day >= 22) || (month == 1 && day <= 19) {
		s = "摩羯"
	}
	return
}
