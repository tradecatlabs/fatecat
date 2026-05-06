package utils

import (
	"math"
)

// OrderMod 取模函数, 等价于a % b, 但当结果为0时, 返回b
func OrderMod(a, b int64) (result int64) {
	result = a % b
	if result == 0 {
		result = b
	}
	return
}

// DD 儒略日数转公历
// int2 (取整数部分) <=> math.Floor
func DD(jd float64) (_Y, _M, _D, _h, _m, _s int) {
	// 取得日数的整数部份A及小数部分F
	D := math.Floor(jd + 0.5)
	F := jd + 0.5 - D
	c := 0.0

	if D >= 2299161 {
		c = math.Floor((D - 1867216.25) / 36524.25)
		D += 1 + c - math.Floor(c/4)
	}

	// 年数
	D += 1524
	_Y = int(math.Floor((D - 122.1) / 365.25))
	// 月数
	D -= math.Floor(365.25 * float64(_Y))
	_M = int(math.Floor(D / 30.601))
	// 日数
	D -= math.Floor(30.601 * float64(_M))
	_D = int(D)

	if _M > 13 {
		_M -= 13
		_Y -= 4715
	} else {
		_M--
		_Y -= 4716
	}

	// 日的小数转为时分秒
	F *= 24
	_h = int(math.Floor(F))
	F -= float64(_h)

	F *= 60
	_m = int(math.Floor(F))
	F -= float64(_m)

	F *= 60
	_s = int(F)

	return
}
