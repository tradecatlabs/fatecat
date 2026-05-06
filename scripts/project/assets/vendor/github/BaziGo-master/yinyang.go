package bazi

// 阴阳
// 从柱里获取阴阳

// GetYinYangFromNumber (阴 == 0,  阳 == 1)
func GetYinYangFromNumber(nValue int) string {
	switch nValue {
	case 0:
		return "阴"
	case 1:
		return "阳"
	}
	return ""
}

// func GetYinYangFromZhu(pZhu *TZhu) int {

// 	return (pZhu.Gan.Value + 1) % 2
// }

// NewYinYang 创建阴阳
func NewYinYang(nValue int) *TYinYang {
	nValue %= 2
	yinyang := TYinYang(nValue)
	return &yinyang
}

// NewYinYangFromZhu 从柱里创建阴阳
func NewYinYangFromZhu(pZhu *TZhu) *TYinYang {
	return NewYinYangFromGan(pZhu.Gan())
}

// NewYinYangFromGan 从干里创建阴阳
func NewYinYangFromGan(pGan *TGan) *TYinYang {
	nGan := pGan.Value()
	switch nGan {
	// 甲丙戊庚壬 0, 2, 4, 6, 8 阳 (1)
	case 0, 2, 4, 6, 8:
		return NewYinYang(1)
	// 乙丁己辛癸 1, 3, 5, 7, 9 阴 (0)
	case 1, 3, 5, 7, 9:
		return NewYinYang(0)
	}
	return nil
}

// TYinYang  阴阳
type TYinYang int

// ToString 转换成可阅读的字符串
func (m *TYinYang) ToString() string {
	return m.String()
}

// ToInt 转换成int
func (m *TYinYang) ToInt() int {
	return m.Value()
}

// Value 转换成int
func (m *TYinYang) Value() int {
	return (int)(*m)
}

// String 转换成可阅读的字符串
func (m *TYinYang) String() string {
	return GetYinYangFromNumber(m.Value())
}
