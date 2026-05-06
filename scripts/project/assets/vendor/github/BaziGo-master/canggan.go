package bazi

// 地支藏干表
var cangganlist = [12][3]int{
	{9, -1, -1}, // 子水 藏干 癸水。
	{5, 9, 7},   // 丑土 藏干 己土、癸水、辛金。
	{0, 2, 4},   // 寅木 藏干 甲木、丙火、戊土。
	{1, -1, -1}, // 卯木 藏干 乙木。
	{4, 1, 9},   // 辰土 藏干 戊土、乙木、癸水。
	{2, 4, 6},   // 巳火 藏干 丙火、戊土、庚金。
	{3, 5, -1},  // 午火 藏干 丁火、己土。
	{5, 1, 3},   // 未土 藏干 己土、乙木、丁火。
	{6, 4, 8},   // 申金 藏干 庚金、戊土、壬水。
	{7, -1, -1}, // 酉金 藏干 辛金。
	{4, 7, 3},   // 戌土 藏干 戊土、辛金、丁火。
	{8, 0, -1}}  // 亥水 藏干 壬水、甲木。

// NewCangGan 新建藏干
func NewCangGan(nDayGan int, pZhi *TZhi) *TCangGan {
	pCangGan := &TCangGan{
		nDayGan: nDayGan,
	}

	pCangGan.init(nDayGan, pZhi)

	return pCangGan
}

// TCangGan 藏干
type TCangGan struct {
	cangGanList []*TGan
	shishenList []*TShiShen
	nDayGan     int // 记录用日干
}

func (m *TCangGan) init(nDayGan int, pZhi *TZhi) {
	nZhi := pZhi.Value()
	for i := 0; i < 3; i++ {
		// 判断藏干有效性
		if cangganlist[nZhi][i] >= 0 {
			// 添加藏干
			pGan := NewGan(cangganlist[nZhi][i])
			pShiShen := NewShiShenFromGan(nDayGan, pGan)
			m.cangGanList = append(m.cangGanList, pGan)
			m.shishenList = append(m.shishenList, pShiShen)
			// 添加十神
		} else {
			break
		}
	}
}

// Size 内容
func (m *TCangGan) Size() int {
	return len(m.cangGanList)
}

// Gan 获取具体某个索引
func (m *TCangGan) Gan(nIdx int) *TGan {
	if nIdx < 0 {
		return nil
	}
	if nIdx >= m.Size() {
		return nil
	}
	return m.cangGanList[nIdx]
}

// ShiShen 十神
func (m *TCangGan) ShiShen(nIdx int) *TShiShen {
	if nIdx < 0 {
		return nil
	}
	if nIdx >= m.Size() {
		return nil
	}
	return m.shishenList[nIdx]
}

func (m *TCangGan) String() string {
	strResult := ""

	for i := 0; i < m.Size(); i++ {
		strResult += m.Gan(i).String() + "[" + m.ShiShen(i).String() + "]"
	}

	return strResult
}
