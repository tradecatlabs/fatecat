package bazi

// THeHuaChong 荷花冲
type THeHuaChong struct {
}

// TTianGanWuHe 天干五合
type TTianGanWuHe struct {
}

// 甲己合化土， 乙庚合化金， 丙辛合化水， 丁壬合化木， 戊癸合化火。
func quickCheckTianGan(pGan1, pGan2 *TGan) (int, string) {
	nGan1 := pGan1.Value()
	nGan2 := pGan2.Value()

	if nGan1 == nGan2 {
		return -1, "" // 相同不合
	}

	nGan1 %= 5
	nGan2 %= 5

	if nGan1 < 0 {
		nGan1 += 5
	}
	if nGan2 < 0 {
		nGan2 += 5
	}

	if nGan1 == nGan2 {
		switch nGan1 {
		case 0:
			return 4, "甲己合化土" // 甲 阳木 + 己 阴土 = 合化土
		case 1:
			return 0, "庚乙合化金" // 庚 阳金 + 乙 阴木 = 合化金
		case 2:
			return 2, "丙辛合化水" // 丙 阳火 + 辛 阴金 = 合化水
		case 3:
			return 1, "壬丁合化木" // 壬 阳水 + 丁 阴火 = 合化木
		case 4:
			return 3, "戊癸合化火" // 戊 阳土 + 癸 阴水 = 合化火
		}
	}

	return -1, ""
}
