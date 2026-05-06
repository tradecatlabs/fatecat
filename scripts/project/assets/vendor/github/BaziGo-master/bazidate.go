package bazi

import (
	"fmt"
)

// NewBaziDate 从新历转成八字历
func NewBaziDate(pSolarDate *TSolarDate) *TBaziDate {
	p := &TBaziDate{}
	p.init(pSolarDate)
	return p
}

// TBaziDate 八字历法
// 八字历法的年  和 新历的 和 农历的都不一样. 八字历法是按照立春为1年. 然后每个节气为月
type TBaziDate struct {
	nYear  int // 年. 立春
	nMonth int // 月.
	nDay   int // 天
	nHour  int // xiaohsi

	pJieQi       *TJieQi     // 节气名称
	pPreviousJie *TJieQiDate // 上一个节(气)
	pNextJie     *TJieQiDate // 下一个节(气)
}

func (m *TBaziDate) init(pSolarDate *TSolarDate) *TBaziDate {
	m.nYear = GetLiChunYear(pSolarDate)                   // 拿到八字年, 根据立春来的
	m.pPreviousJie, m.pNextJie = GetJieQiDate(pSolarDate) // 拿到前后两个的日期
	// 节气
	nJieQi := m.pPreviousJie.JieQi
	m.pJieQi = &nJieQi
	// 月
	m.nMonth = m.pJieQi.Month()
	return m
}

func (m *TBaziDate) String() string {
	return fmt.Sprintf("八字历: %4d 年 %02d 月 \n上一个:%v\n下一个:%v",
		m.nYear, m.nMonth, m.pPreviousJie, m.pNextJie)
}

// Year  年. 立春
func (m *TBaziDate) Year() int {
	return m.nYear
}

// Month  月.
func (m *TBaziDate) Month() int {
	return m.nMonth
}

// Day  天
func (m *TBaziDate) Day() int {
	return m.nDay
}

// Hour 小时
func (m *TBaziDate) Hour() int {
	return m.nHour
}

// PreviousJie 上一个节气
func (m *TBaziDate) PreviousJie() *TJieQiDate {
	return m.pPreviousJie
}

// NextJie 下一个节气
func (m *TBaziDate) NextJie() *TJieQiDate {
	return m.pNextJie
}
