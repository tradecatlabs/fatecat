package bazi

/*
大运的作用
每一步大运统管十年祸福，在这十年之中，又有十个不同的干支，这十个不同的干支对大运来说，有相生、相合、有扶有泄的不同之说。
这十个干支同样对四柱中干支也会出现生扶抑克的影响。所以只推大运还不行，还要加上流年。所谓“流年”，又叫行年太岁。
就是从命造出生的那年开始，不论阴年和阳年，也不管男命女命，一律往下排，如某人出生于甲子年，就从甲子为一岁流年，乙丑为二岁流年，丙寅为三岁流年，依次一直排到寿终。
推排流年有两种作用：第一种是给求测从生至死的每一年的事情；第二种是答复求测人所问某一年的吉凶。
比如一个人要问45那年的吉凶如何？就从出生年起推出45那年是什么干支，再结合命局与大运进行分析，定其吉凶祸福。
*/

// NewDaYun 新大运
func NewDaYun(pSiZhu *TSiZhu, nSex int) *TDaYun {
	p := &TDaYun{}
	p.init(pSiZhu, nSex)
	return p
}

// TDaYun 大运
type TDaYun struct {
	zhuList  [12]*TZhu // 12个大运柱列表
	nAge     [12]int   // 12个大运对应年龄
	isShunNi bool      // 顺转还是逆转(true 顺,  false 逆)
}

func (m *TDaYun) init(pSiZhu *TSiZhu, nSex int) *TDaYun {
	for i := 0; i < 12; i++ {
		m.zhuList[i] = NewZhu() // 新建12个柱
	}

	// 第一判断年柱的阴阳
	yinyang := pSiZhu.YearZhu().ToYinYang()
	// ! 第二判断性别的男女

	// 月柱的干支
	nMonthGanZhi := pSiZhu.MonthZhu().GanZhi().Value()

	for i := 0; i < 12; i++ {
		if yinyang.Value() == nSex {
			m.isShunNi = true
			m.zhuList[i].genBaseGanZhi((nMonthGanZhi + 61 + i) % 60)
		} else {
			m.isShunNi = false
			m.zhuList[i].genBaseGanZhi((nMonthGanZhi + 59 - i) % 60)

		}
	}

	return m
}

// String
func (m *TDaYun) String() string {
	strResult := "大运:\n"

	for i := 0; i < 12; i++ {
		strResult += m.zhuList[i].GanZhi().String() + " "
	}

	return strResult
}

// ShunNi 顺逆
func (m *TDaYun) ShunNi() bool {
	return m.isShunNi
}

// Zhu 获取柱
func (m *TDaYun) Zhu(nIndex int) *TZhu {
	nIndex %= 12
	return m.zhuList[nIndex]
}

// Size 容量就是12
func (m *TDaYun) Size() int {
	return 12
}

// Age 获取年龄
func (m *TDaYun) Age(nIndex int) int {
	nIndex %= 12
	return m.nAge[nIndex]
}
