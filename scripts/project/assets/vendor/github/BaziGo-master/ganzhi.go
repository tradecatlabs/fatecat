package bazi

// 干支

// GetGanZhiFromNumber 从数字获得天干地支名, 0-59
func GetGanZhiFromNumber(nValue int) string {
	switch nValue {
	case 0:
		return "甲子"
	case 1:
		return "乙丑"
	case 2:
		return "丙寅"
	case 3:
		return "丁卯"
	case 4:
		return "戊辰"
	case 5:
		return "己巳"
	case 6:
		return "庚午"
	case 7:
		return "辛未"
	case 8:
		return "壬申"
	case 9:
		return "癸酉"
	case 10:
		return "甲戌"
	case 11:
		return "乙亥"
	case 12:
		return "丙子"
	case 13:
		return "丁丑"
	case 14:
		return "戊寅"
	case 15:
		return "己卯"
	case 16:
		return "庚辰"
	case 17:
		return "辛巳"
	case 18:
		return "壬午"
	case 19:
		return "癸未"
	case 20:
		return "甲申"
	case 21:
		return "乙酉"
	case 22:
		return "丙戌"
	case 23:
		return "丁亥"
	case 24:
		return "戊子"
	case 25:
		return "己丑"
	case 26:
		return "庚寅"
	case 27:
		return "辛卯"
	case 28:
		return "壬辰"
	case 29:
		return "癸巳"
	case 30:
		return "甲午"
	case 31:
		return "乙未"
	case 32:
		return "丙申"
	case 33:
		return "丁酉"
	case 34:
		return "戊戌"
	case 35:
		return "己亥"
	case 36:
		return "庚子"
	case 37:
		return "辛丑"
	case 38:
		return "壬寅"
	case 39:
		return "癸卯"
	case 40:
		return "甲辰"
	case 41:
		return "乙巳"
	case 42:
		return "丙午"
	case 43:
		return "丁未"
	case 44:
		return "戊申"
	case 45:
		return "己酉"
	case 46:
		return "庚戌"
	case 47:
		return "辛亥"
	case 48:
		return "壬子"
	case 49:
		return "癸丑"
	case 50:
		return "甲寅"
	case 51:
		return "乙卯"
	case 52:
		return "丙辰"
	case 53:
		return "丁巳"
	case 54:
		return "戊午"
	case 55:
		return "己未"
	case 56:
		return "庚申"
	case 57:
		return "辛酉"
	case 58:
		return "壬戌"
	case 59:
		return "癸亥"
	}

	return ""
}

// NewGanZhi 创建干支
func NewGanZhi(nValue int) *TGanZhi {
	nValue %= 60
	pGanZhi := TGanZhi(nValue)
	return &pGanZhi
}

// NewGanZhiFromYear 获得八字年的干支，0-59 对应 甲子到癸亥
func NewGanZhiFromYear(nYear int) *TGanZhi {
	if nYear > 0 {
		return NewGanZhi(nYear - 4)
	}
	// 需要独立判断公元前的原因是没有公元 0 年
	return NewGanZhi(nYear - 3)
}

// NewGanZhiFromDay 获得八字天的干支, 0-59 对应 甲子到癸亥
func NewGanZhiFromDay(nAllDays int) *TGanZhi {
	return NewGanZhi(nAllDays + 12)
}

// CombineGanZhi 将天干地支组合成干支，0-9 0-11 转换成 0-59
func CombineGanZhi(pGan *TGan, pZhi *TZhi) *TGanZhi {
	nGan := pGan.Value()
	nZhi := pZhi.Value()
	for i := 0; i <= 6; i++ {
		if (i*10+nGan)%12 == nZhi {
			return NewGanZhi(i*10 + nGan)
		}
	}
	return nil
}

// TGanZhi 干支
type TGanZhi int

// ToString 转换成可阅读的字符串
func (m *TGanZhi) ToString() string {
	return m.String()
}

// ExtractGanZhi   将干支拆分成天干地支，0-59 转换成 0-9 0-11
func (m *TGanZhi) ExtractGanZhi() (*TGan, *TZhi) {
	return NewGan(m.Value()), NewZhi(m.Value())
}

// ToNaYin 纳音
func (m *TGanZhi) ToNaYin() *TNaYin {
	return NewNaYin(m.Value() / 2)
}

// ToInt 转换成int
func (m *TGanZhi) ToInt() int {
	return m.Value()
}

// Value 转换成int
func (m *TGanZhi) Value() int {
	return (int)(*m)
}

// String 转换成可阅读的字符串
func (m *TGanZhi) String() string {
	return GetGanZhiFromNumber(m.Value())
}
