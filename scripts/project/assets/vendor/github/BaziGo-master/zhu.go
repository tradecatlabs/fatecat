package bazi

// 这里是柱， 四柱之一

import "fmt"

// TZhu 柱
type TZhu struct {
	pGanZhi  *TGanZhi  // 干支
	pGan     *TGan     // 天干
	pZhi     *TZhi     // 地支
	pCangGan *TCangGan // 藏干
	pShiShen *TShiShen // 十神
	nDayGan  int       // 日干值
}

// NewZhu 新建柱子
func NewZhu() *TZhu {
	return &TZhu{}
}

// String 打印
func (m *TZhu) String() string {
	return fmt.Sprintf("%v", m.pGanZhi)
}

// 设置日干值
func (m *TZhu) setDayGan(nDayGan int) *TZhu {
	m.nDayGan = nDayGan
	return m
}

// 生成藏干
func (m *TZhu) genCangGan() {
	// 生成藏干数据
	if m.pZhi != nil {
		m.pCangGan = NewCangGan(m.nDayGan, m.pZhi)
	}
}

// 生成十神
func (m *TZhu) genShiShen() {
	m.pShiShen = NewShiShenFromGan(m.nDayGan, m.pGan)
}

//
func (m *TZhu) genBaseGanZhi(nGanZhi int) *TZhu {
	// 直接设置成品干支
	m.pGanZhi = NewGanZhi(nGanZhi)
	// 拆分干支
	// 获得八字年的干0-9 对应 甲到癸
	// 获得八字年的支0-11 对应 子到亥
	m.pGan, m.pZhi = m.pGanZhi.ExtractGanZhi()

	return m
}

// genYearGanZhi 生成年干支
func (m *TZhu) genYearGanZhi(nYear int) *TZhu {
	// 通过年获取干支
	// 获得八字年的干支，0-59 对应 甲子到癸亥
	m.pGanZhi = NewGanZhiFromYear(nYear)
	// 拆分干支
	// 获得八字年的干0-9 对应 甲到癸
	// 获得八字年的支0-11 对应 子到亥
	m.pGan, m.pZhi = m.pGanZhi.ExtractGanZhi()

	// 在这里计算藏干
	m.genCangGan()
	m.genShiShen()
	return m
}

// genMonthGanZhi 生成月干支
func (m *TZhu) genMonthGanZhi(nMonth int, nYearGan int) *TZhu {
	// 根据口诀从本年干数计算本年首月的干数
	switch nYearGan {
	case 0, 5:
		// 甲己 丙佐首
		nYearGan = 2
	case 1, 6:
		// 乙庚 戊为头
		nYearGan = 4
	case 2, 7:
		// 丙辛 寻庚起
		nYearGan = 6
	case 3, 8:
		// 丁壬 壬位流
		nYearGan = 8
	case 4, 9:
		// 戊癸 甲好求
		nYearGan = 0
	}

	// 计算本月干数
	nYearGan += ((nMonth - 1) % 10)

	// 拆干
	m.pGan = NewGan(nYearGan % 10)
	m.pZhi = NewZhi((nMonth - 1 + 2) % 12)

	// 组合干支
	m.pGanZhi = CombineGanZhi(m.pGan, m.pZhi)
	// 在这里计算藏干
	m.genCangGan()
	m.genShiShen()
	return m
}

// genDayGanZhi 生成日干支
func (m *TZhu) genDayGanZhi(nAllDays int) *TZhu {

	// 通过总天数来获取
	// 获得八字年的干支，0-59 对应 甲子到癸亥
	m.pGanZhi = NewGanZhiFromDay(nAllDays)
	// 拆分干支
	// 获得八字年的干0-9 对应 甲到癸
	// 获得八字年的支0-11 对应 子到亥
	m.pGan, m.pZhi = m.pGanZhi.ExtractGanZhi()

	// 直接保存日干
	m.setDayGan(m.pGan.Value())

	// 在这里计算藏干
	m.genCangGan()
	m.genShiShen()
	return m
}

// genHourGanZhi 生成时干支
func (m *TZhu) genHourGanZhi(nHour int) *TZhu {
	// 取出日干
	nGan := m.nDayGan

	// 24小时校验
	nHour %= 24
	if nHour < 0 {
		nHour += 24
	}

	nZhi := 0
	if nHour == 23 {
		// 次日子时
		nGan = (nGan + 1) % 10
	} else {
		nZhi = (nHour + 1) / 2
	}

	// Gan 此时是本日干数，根据规则换算成本日首时辰干数
	if nGan >= 5 {
		nGan -= 5
	}

	// 计算此时辰干数
	nGan = (2*nGan + nZhi) % 10

	m.pGan = NewGan(nGan)
	m.pZhi = NewZhi(nZhi)

	// 组合干支
	m.pGanZhi = CombineGanZhi(m.pGan, m.pZhi)

	// 在这里计算藏干
	m.genCangGan()
	m.genShiShen()
	return m
}

// Gan 获取干
func (m *TZhu) Gan() *TGan {
	return m.pGan
}

// Zhi 获取支
func (m *TZhu) Zhi() *TZhi {
	return m.pZhi
}

// GanZhi 获取干支
func (m *TZhu) GanZhi() *TGanZhi {
	return m.pGanZhi
}

// ToYinYang 从柱里获取阴阳 (阴 == 0,  阳 == 1)
func (m *TZhu) ToYinYang() *TYinYang {
	return NewYinYangFromZhu(m)
}

// CangGan 获取藏干
func (m *TZhu) CangGan() *TCangGan {
	return m.pCangGan
}

// ShiShen 获取十神
func (m *TZhu) ShiShen() *TShiShen {
	return m.pShiShen
}
