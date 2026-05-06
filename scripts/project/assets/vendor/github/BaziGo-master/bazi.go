package bazi

import "fmt"

// NewBazi 新建八字
func NewBazi(pSolarDate *TSolarDate, nSex int) *TBazi {
	//
	pBazi := &TBazi{
		pSolarDate: pSolarDate,
		nSex:       nSex,
	}
	return pBazi.init()
}

// NewBaziFromLunarDate 新建八字 从农历
func NewBaziFromLunarDate(pLunarDate *TLunarDate, nSex int) *TBazi {
	pBazi := &TBazi{
		pLunarDate: pLunarDate,
		nSex:       nSex,
	}

	return pBazi.init()
}

// GetBazi 旧版八字接口, 八字入口
func GetBazi(nYear, nMonth, nDay, nHour, nMinute, nSecond, nSex int) *TBazi {
	// 先解决时间问题. 然后开始处理八字问题
	pSolarDate := NewSolarDate(nYear, nMonth, nDay, nHour, nMinute, nSecond)
	if pSolarDate == nil {
		return nil
	}

	return NewBazi(pSolarDate, nSex)
}

// TBazi 八字大类
type TBazi struct {
	pSolarDate *TSolarDate // 新历的日期
	pLunarDate *TLunarDate // 农历日期
	pBaziDate  *TBaziDate  // 八字历
	pSiZhu     *TSiZhu     // 四柱嗯
	nSex       int         // 性别1男其他女
	pDaYun     *TDaYun     // 大运
	pQiYunDate *TSolarDate // 起运时间XX年XX月开始起运
}

// 八字初始化
func (m *TBazi) init() *TBazi {
	// 1. 新农互转
	if m.pSolarDate == nil {
		if m.pLunarDate == nil {
			return nil
		}
		// 农转新
		m.pSolarDate = m.pLunarDate.ToSolarDate()
	} else {
		// 新转农
		m.pLunarDate = m.pSolarDate.ToLunarDate()
	}

	// 1. 拿到新历的情况下, 需要计算八字历
	m.pBaziDate = m.pSolarDate.ToBaziDate()

	// 2. 根据八字历, 准备计算四柱了
	m.pSiZhu = NewSiZhu(m.pSolarDate, m.pBaziDate)

	// 3. 计算大运
	m.pDaYun = NewDaYun(m.pSiZhu, m.nSex)

	// 4. 计算起运时间
	m.pQiYunDate = NewQiYun(m.pDaYun.ShunNi(), m.pBaziDate.PreviousJie().ToSolarDate(), m.pBaziDate.NextJie().ToSolarDate(), m.pSolarDate)

	// 5. 起运时间融入到大运中
	nAge := m.QiYunDate().Year() - m.Date().Year()
	for i := 0; i < 12; i++ {
		m.pDaYun.nAge[i] = nAge + 10*i
	}

	return m
}

// String 打印用
func (m *TBazi) String() string {
	return fmt.Sprintf("%v\n %v\n %v\n%v\n%v \n起运时间%v", m.pSolarDate, m.pLunarDate, m.pBaziDate, m.pSiZhu, m.pDaYun, m.pQiYunDate)
}

// SiZhu 四柱
func (m *TBazi) SiZhu() *TSiZhu {
	return m.pSiZhu
}

// Date 获取日期， 默认就是新历
func (m *TBazi) Date() *TSolarDate {
	return m.pSolarDate
}

// SolarData 获取新历日期
func (m *TBazi) SolarData() *TSolarDate {
	return m.Date()
}

// LunarDate 获取农历日期
func (m *TBazi) LunarDate() *TLunarDate {
	return m.pLunarDate
}

// DaYun 获取大运
func (m *TBazi) DaYun() *TDaYun {
	return m.pDaYun
}

// QiYunDate 起运时间
func (m *TBazi) QiYunDate() *TSolarDate {
	return m.pQiYunDate
}
