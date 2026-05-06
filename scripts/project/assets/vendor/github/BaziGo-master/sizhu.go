package bazi

import "fmt"

// NewSiZhu 新四柱
func NewSiZhu(pSolarDate *TSolarDate, pBaziDate *TBaziDate) *TSiZhu {
	p := &TSiZhu{
		pYearZhu:   NewZhu(),
		pMonthZhu:  NewZhu(),
		pDayZhu:    NewZhu(),
		pHourZhu:   NewZhu(),
		pSolarDate: pSolarDate,
		pBaziDate:  pBaziDate,
	}
	p.init()
	return p
}

// TSiZhu 四柱
type TSiZhu struct {
	pYearZhu  *TZhu // 年柱
	pMonthZhu *TZhu // 月柱
	pDayZhu   *TZhu // 日柱
	pHourZhu  *TZhu // 时柱
	// pHeHuaChong *THeHuaChong // 合化冲 这个暂时没写， 后面一定补。
	pSolarDate *TSolarDate // 新历日期
	pBaziDate  *TBaziDate  // 八字历日期
	pXiYong    *TXiYong    // 喜用神
}

func (m *TSiZhu) init() *TSiZhu {

	// 通过公历 年月日计算日柱
	nDayGan := m.pDayZhu.genDayGanZhi(m.pSolarDate.GetAllDays()).Gan().Value() // 获取日干(日主)
	// 通过小时 获取时柱
	m.pHourZhu.setDayGan(nDayGan).genHourGanZhi(m.pSolarDate.Hour())
	// 通过八字年来获取年柱
	nYearGan := m.pYearZhu.setDayGan(nDayGan).genYearGanZhi(m.pBaziDate.Year()).Gan().Value()
	// 通过年干支和八字月
	m.pMonthZhu.setDayGan(nDayGan).genMonthGanZhi(m.pBaziDate.Month(), nYearGan)
	// 生成喜用神数据
	m.pXiYong = NewXiYong(m)
	return m
}

//  genShiShen 计算十神

func (m *TSiZhu) String() string {
	return fmt.Sprintf("四柱:%v %v %v %v\n命盘解析:\n%v(%v)[%v]\t%v(%v)[%v]\t%v(%v)[%v]\t%v(%v)[%v]\t",
		m.pYearZhu.GanZhi(),
		m.pMonthZhu.GanZhi(),
		m.pDayZhu.GanZhi(),
		m.pHourZhu.GanZhi(),
		m.pYearZhu.Gan(), m.pYearZhu.Gan().ToWuXing(), m.pYearZhu.ShiShen(),
		m.pMonthZhu.Gan(), m.pMonthZhu.Gan().ToWuXing(), m.pMonthZhu.ShiShen(),
		m.pDayZhu.Gan(), m.pDayZhu.Gan().ToWuXing(), "主",
		m.pHourZhu.Gan(), m.pHourZhu.Gan().ToWuXing(), m.pHourZhu.ShiShen(),
	) + fmt.Sprintf("\n%v(%v)   \t%v(%v)   \t%v(%v)   \t%v(%v) \n",
		m.pYearZhu.Zhi(), m.pYearZhu.Zhi().ToWuXing(),
		m.pMonthZhu.Zhi(), m.pMonthZhu.Zhi().ToWuXing(),
		m.pDayZhu.Zhi(), m.pDayZhu.Zhi().ToWuXing(),
		m.pHourZhu.Zhi(), m.pHourZhu.Zhi().ToWuXing(),
	) + fmt.Sprintf("藏干:\n%v   \t%v    \t%v    \t%v\n",
		m.pYearZhu.CangGan(),
		m.pMonthZhu.CangGan(),
		m.pDayZhu.CangGan(),
		m.pHourZhu.CangGan(),
	) + fmt.Sprintf("纳音:\n%v   \t%v    \t%v    \t%v\n",
		m.pYearZhu.GanZhi().ToNaYin(),
		m.pMonthZhu.GanZhi().ToNaYin(),
		m.pDayZhu.GanZhi().ToNaYin(),
		m.pHourZhu.GanZhi().ToNaYin(),
	)
}

// YearZhu 返回年柱
func (m *TSiZhu) YearZhu() *TZhu {
	return m.pYearZhu
}

// MonthZhu 返回月柱
func (m *TSiZhu) MonthZhu() *TZhu {
	return m.pMonthZhu
}

// DayZhu 返回日柱
func (m *TSiZhu) DayZhu() *TZhu {
	return m.pDayZhu
}

// HourZhu 返回时柱
func (m *TSiZhu) HourZhu() *TZhu {
	return m.pHourZhu
}

// 喜用神和五行强度
func (m *TSiZhu) XiYong() *TXiYong {
	return m.pXiYong
}
