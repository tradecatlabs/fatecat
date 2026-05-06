package bazi

// 新历日期时间， 采用标准的日历

import (
	"fmt"
)

// NewSolarDate 创建一个新历时间
func NewSolarDate(nYear, nMonth, nDay, nHour, nMinute, nSecond int) *TSolarDate {
	// 把具体时间实例化出来
	pDate := &TSolarDate{
		nYear:   nYear,   // 年
		nMonth:  nMonth,  // 月
		nDay:    nDay,    // 日
		nHour:   nHour,   // 时
		nMinute: nMinute, // 分
		nSecond: nSecond, // 秒
	}

	if !pDate.GetDateIsValid(nYear, nMonth, nDay) {
		fmt.Println("无效的日期", nYear, nMonth, nDay)
		return nil
	}

	// 检查时间是否合法, 传入一个大值HOUR导致崩溃的BUG // fix chadwi https://github.com/warrially/BaziGo/issues/3
	if !pDate.GetTimeIsValid(nHour, nMinute, nSecond) {
		fmt.Println("无效的时间", nHour, nMinute, nSecond)
		return nil
	}
	// 计算64位时间戳值
	// pDate.Get64TimeStamp()

	return pDate
}

// NewSolarDateFrom64TimeStamp 从64位时间戳反推日期
func NewSolarDateFrom64TimeStamp(nTimeStamp int64) *TSolarDate {
	pDate := &TSolarDate{}
	// 计算出年份
	pDate.GetYearFrom64TimeStamp(nTimeStamp)
	// 计算月份
	pDate.GetMonthFrom64TimeStamp(nTimeStamp)
	// 计算其他参数
	pDate.GetDayTimeFrom64TimeStamp(nTimeStamp)

	return pDate
}

// TSolarDate 日期
type TSolarDate struct {
	nYear   int // 年
	nMonth  int // 月
	nDay    int // 日
	nHour   int // 时
	nMinute int // 分
	nSecond int // 秒
}

// GetDiffSeconds 获取两个日期之间相差的秒数
func (m *TSolarDate) GetDiffSeconds(other *TSolarDate) int64 {
	return other.Get64TimeStamp() - m.Get64TimeStamp()
}

// Get64TimeStamp 生成64位时间戳
func (m *TSolarDate) Get64TimeStamp() int64 {
	nAllDays := m.GetAllDays() // 先获取公元原点的日数
	nResult := int64(nAllDays)
	nResult *= 24 * 60 * 60 // 天数换成秒

	//再计算出秒数
	nResult += int64(m.nHour) * 60 * 60
	nResult += int64(m.nMinute) * 60
	nResult += int64(m.nSecond)

	return nResult
}

// GetYearFrom64TimeStamp 从64位时间戳反推年
func (m *TSolarDate) GetYearFrom64TimeStamp(nTimeStamp int64) *TSolarDate {
	// 准备进行二分法
	nLow := 0
	nHigh := 3001

	for {
		nMid := (nLow + nHigh) / 2

		// 拿到中间年的数据
		v := NewSolarDate(nMid, 1, 1, 0, 0, 0).Get64TimeStamp()

		if v <= nTimeStamp {
			nLow = nMid
		} else {
			nHigh = nMid
		}

		if nHigh == nLow+1 {
			break
		}
	}
	m.nYear = nLow
	return m
}

// GetMonthFrom64TimeStamp 从64位时间戳反推月,
func (m *TSolarDate) GetMonthFrom64TimeStamp(nTimeStamp int64) {
	// 这里开始特殊处理
	for i := 1; i <= 11; i++ {
		if nTimeStamp < NewSolarDate(m.nYear, i+1, 1, 0, 0, 0).Get64TimeStamp() {
			m.nMonth = i
			return
		}
	}
	m.nMonth = 12
}

// GetDayTimeFrom64TimeStamp 从64位时间戳反推其他参数
func (m *TSolarDate) GetDayTimeFrom64TimeStamp(nTimeStamp int64) {
	nTimeStamp -= NewSolarDate(m.nYear, m.nMonth, 1, 0, 0, 0).Get64TimeStamp()

	// 计算日
	m.nDay = int(nTimeStamp / (24 * 60 * 60))
	// 扣掉日
	nTimeStamp -= int64(m.nDay) * 24 * 60 * 60

	m.nDay++ // 因为每个月的天数是从1开始的, 所以这里需要补1天
	if m.nYear == 1582 && m.nMonth == 10 && m.nDay >= 5 {
		m.nDay += 10 // 1582 年需要补10天
	}
	m.nHour = int(nTimeStamp / (60 * 60))
	nTimeStamp -= int64(m.nHour) * 60 * 60
	m.nMinute = int(nTimeStamp / 60)
	nTimeStamp -= int64(m.nMinute) * 60
	m.nSecond = int(nTimeStamp)
}

// GetMonthDays 取本月天数，不考虑 1582 年 10 月的特殊情况
func (m *TSolarDate) GetMonthDays(nYear, nMonth int) int {
	switch nMonth {
	case 1, 3, 5, 7, 8, 10, 12:
		return 31
	case 4, 6, 9, 11:
		return 30
	case 2: // 闰年
		if m.GetIsLeapYear(nYear) {
			return 29
		}
		return 28
	}
	return 0
}

// GetIsLeapYear 返回某公历是否闰年
func (m *TSolarDate) GetIsLeapYear(nYear int) bool {
	if m.GetCalendarType(nYear, 1, 1) == ctGregorian {
		return (nYear%4 == 0) && ((nYear%100 != 0) || (nYear%400 == 0))
	} else if nYear >= 0 {
		return nYear%4 == 0
	} else { // 需要独立判断公元前的原因是没有公元 0 年
		return (nYear-3)%4 == 0
	}
}

const (
	ctInvalid   = iota //非法，
	ctJulian           //儒略，
	ctGregorian        //格利高里
)

// GetCalendarType 根据公历日期判断当时历法
func (m *TSolarDate) GetCalendarType(nYear, nMonth, nDay int) int {
	if !m.GetDateIsValid(nYear, nMonth, nDay) {
		return ctInvalid
	}
	if nYear > 1582 {
		return ctGregorian
	} else if nYear < 1582 {
		return ctJulian
	} else if nMonth < 10 {
		return ctJulian
	} else if (nMonth == 10) && (nDay <= 4) {
		return ctJulian
	} else if (nMonth == 10) && (nDay <= 14) {
		return ctInvalid
	} else {
		return ctGregorian
	}
	// 在现在通行的历法记载上，全世界居然有十天没有任何人出生过，也没有任何人死亡过，也没有发生过大大小小值得纪念的人或事。这就是1582年10月5日至10月14日。格里奥，提出了公历历法。这个历法被罗马教皇格里高利十三世采纳了。那么误差的十天怎么办？罗马教皇格里高利十三世下令，把1582年10月4日的后一天改为10月15日，这样误差的十天没有了，历史上也就无影无踪地消失了十天，当然史书上也就没有这十天的记载了。“格里高利公历”一直沿用到今天。
}

// GetDateIsValid 返回公历日期是否合法
func (m *TSolarDate) GetDateIsValid(nYear, nMonth, nDay int) bool {
	// 没有公元0年
	if nYear == 0 {
		return false
	}

	// 1月开始, 12月结束
	if nMonth < 1 || nMonth > 12 {
		return false
	}

	// 1号开始, 获取每个月有多少天结束
	if nDay < 1 || nDay > m.GetMonthDays(nYear, nMonth) {
		return false
	}

	// 1582 年的特殊情况
	if nYear != 1582 {
		return true
	}
	if nMonth != 10 {
		return true
	}
	//
	if nDay < 5 || nDay > 14 {
		return true
	}

	return false
}

// GetTimeIsValid 检查时间是否合法
func (m *TSolarDate) GetTimeIsValid(nHour, nMinute, nSecond int) bool {
	if nHour < 0 || nHour > 23 {
		return false
	}

	if nMinute < 0 || nMinute > 59 {
		return false
	}

	if nSecond < 0 || nSecond > 59 {
		return false
	}
	return true
}

// GetAllDays 获得距公元原点的日数 这里是公历的年月日
func (m *TSolarDate) GetAllDays() int {
	nYear := m.Year()
	nMonth := m.Month()
	nDay := m.Day()
	if m.GetDateIsValid(nYear, nMonth, nDay) {
		return m.GetBasicDays(nYear, nMonth, nDay) + m.GetLeapDays(nYear, nMonth, nDay)
	}
	return 0
}

// GetBasicDays 获取基本数据
func (m *TSolarDate) GetBasicDays(nYear, nMonth, nDay int) int {
	if !m.GetDateIsValid(nYear, nMonth, nDay) {
		return 0
	}

	var Result int

	// 去掉公元0年
	if nYear > 0 {
		Result = (nYear - 1) * 365
	} else {
		Result = nYear * 365
	}

	// 加上月天数
	for i := 1; i < nMonth; i++ {
		Result += m.GetMonthDays(nYear, i)
	}

	// 加上日天数
	Result += nDay
	// 返回基础天数
	return Result
}

// GetLeapDays 获取闰年天数
func (m *TSolarDate) GetLeapDays(nYear, nMonth, nDay int) int {
	if !m.GetDateIsValid(nYear, nMonth, nDay) {
		return 0
	}
	var Result int

	if nYear >= 0 {
		// 公元后
		if m.GetCalendarType(nYear, nMonth, nDay) < ctGregorian {
			Result = 0
		} else {
			// 1582.10.5/15 前的 Julian 历只有四年一闰，历法此日后调整为 Gregorian 历
			Result = 10 // 被 Gregory 删去的 10 天

			// 修正算法简化版，从 1701 年的 11 起
			if nYear > 1700 {
				// 每一世纪累加一
				Result += (1 + ((nYear - 1701) / 100))
				// 但 400 整除的世纪不加
				Result -= ((nYear - 1601) / 400)
			}
		}
		Result = ((nYear - 1) / 4) - Result // 4 年一闰数
	} else {
		// 公元前
		Result = -((-nYear + 3) / 4)
	}
	return Result
}

func (m *TSolarDate) String() string {
	return fmt.Sprintf("新历: %d 年 %02d 月 %02d 日 %02d:%02d:%02d",
		m.nYear, m.nMonth, m.nDay, m.nHour, m.nMinute, m.nSecond)
}

// ToBaziDate 转成八字日期
func (m *TSolarDate) ToBaziDate() *TBaziDate {
	return NewBaziDate(m)
}

// Year 年
func (m *TSolarDate) Year() int {
	return m.nYear
}

// Month 月
func (m *TSolarDate) Month() int {
	return m.nMonth
}

// Day 日
func (m *TSolarDate) Day() int {
	return m.nDay
}

// Hour 时
func (m *TSolarDate) Hour() int {
	return m.nHour
}

// Minute 分
func (m *TSolarDate) Minute() int {
	return m.nMinute
}

// Second 秒
func (m *TSolarDate) Second() int {
	return m.nSecond
}

// ToLunarDate 转成农历年
func (m *TSolarDate) ToLunarDate() *TLunarDate {
	return NewLunarDateFrom64TimeStamp(m.Get64TimeStamp())
}
