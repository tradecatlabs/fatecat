package bazi

// 天干
// 甲木、乙木、丙火、丁火、戊土、己土、庚金、辛金、壬水、癸水，其中甲 丙 戊 庚 壬为阳性，乙丁己辛癸为阴性
// 诗曰：
// 春季甲乙东方木，夏季丙丁南方火；
// 秋季庚辛西方金，冬季壬癸北方水；
// 戊己中央四季土。

// GetTianGanFromNumber 从数字获得天干名, 0-9
func GetTianGanFromNumber(nValue int) string {
	switch nValue {
	case 0:
		return "甲"
	case 1:
		return "乙"
	case 2:
		return "丙"
	case 3:
		return "丁"
	case 4:
		return "戊"
	case 5:
		return "己"
	case 6:
		return "庚"
	case 7:
		return "辛"
	case 8:
		return "壬"
	case 9:
		return "癸"
	}

	return ""
}

// NewGan 创建天干
func NewGan(nValue int) *TGan {
	nValue %= 10
	pGan := TGan(nValue)
	return &pGan
}

// TGan 天干
type TGan int

// ToString 转换成可阅读的字符串
func (m *TGan) ToString() string {
	return m.String()
}

// ToInt 转换成int
func (m *TGan) ToInt() int {
	return m.Value()
}

// ToWuXing 天干转化成五行
func (m *TGan) ToWuXing() *TWuXing {
	// todo
	// 甲木、乙木、丙火、丁火、戊土、己土、庚金、辛金、壬水、癸水，其中甲 丙 戊 庚 壬为阳性，乙丁己辛癸为阴性
	switch m.Value() {
	case 0, 1:
		return NewWuXing(1) // 甲 阳木 乙 阴木
	case 2, 3:
		return NewWuXing(3) // 丙 阳火 丁 阴火
	case 4, 5:
		return NewWuXing(4) // 戊 阳土 己 阴土
	case 6, 7:
		return NewWuXing(0) // 庚 阳金 辛 阴金
	case 8, 9:
		return NewWuXing(2) // 壬 阳水 癸 阴水
	}
	return nil
}

// Value 转换成int
func (m *TGan) Value() int {
	return (int)(*m)
}

// String 转换成可阅读的字符串
func (m *TGan) String() string {
	return GetTianGanFromNumber(m.Value())
}
