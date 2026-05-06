package bazi

// TJieQi 节气类
type TJieQi int

// GetJieQiFromNumber 从数字获得节气名, 0-23
func GetJieQiFromNumber(nValue int) string {
	switch nValue {
	case 0: // 节气  Beginning of Spring   0
		return "立春"
	case 1: // 中气  Rain Water            1
		return "雨水"
	case 2: // 节气  Waking of Insects     2
		return "惊蛰"
	case 3: // 中气  March Equinox         3
		return "春分"
	case 4: // 节气  Pure Brightness       4
		return "清明"
	case 5: // 中气  Grain Rain            5
		return "谷雨"
	case 6: // 节气  Beginning of Summer   6
		return "立夏"
	case 7: // 中气  Grain Full            7
		return "小满"
	case 8: // 节气  Grain in Ear          8
		return "芒种"
	case 9: // 中气  Summer Solstice       9
		return "夏至"
	case 10: // 节气  Slight Heat           10
		return "小暑"
	case 11: // 中气  Great Heat            11
		return "大暑"
	case 12: // 节气  Beginning of Autumn   12
		return "立秋"
	case 13: // 中气  Limit of Heat         13
		return "处暑"
	case 14: // 节气  White Dew             14
		return "白露"
	case 15: // 中气  September Equinox     15
		return "秋分"
	case 16: // 节气  Cold Dew              16
		return "寒露"
	case 17: // 中气  Descent of Frost      17
		return "霜降"
	case 18: // 节气  Beginning of Winter   18
		return "立冬"
	case 19: // 中气  Slight Snow           19
		return "小雪"
	case 20: // 节气  Great Snow            20
		return "大雪"
	case 21: // 中气  Winter Solstice       21
		return "冬至"
	case 22: // 节气  Slight Cold           22   	，这是一公历年中的第一个节气
		return "小寒"
	case 23: // 中气  Great Cold            23
		return "大寒"
	}
	return ""
}

// IsJie 节气是否是节,   节气分成节和气,
func (m *TJieQi) IsJie() bool {
	n := m.Value()
	return n%2 == 0
}

// ToString 转换成可阅读的字符串
func (m *TJieQi) ToString() string {
	return m.String()
}

// ToInt 转换成int
func (m *TJieQi) ToInt() int {
	return m.Value()
}

// Month 节气月份
func (m *TJieQi) Month() int {
	return m.ToMonth()
}

// ToMonth 转成节气月
func (m *TJieQi) ToMonth() int {
	// 节气0 是立春 是1月
	return m.Value()/2 + 1
}

// Value 转换成int
func (m *TJieQi) Value() int {
	return (int)(*m)
}

// String 转换成可阅读的字符串
func (m *TJieQi) String() string {
	return GetJieQiFromNumber(m.Value())
}
