package main

import (
	"flag"
	"fmt"

	bazi "github.com/warrially/BaziGo"
)

func main() {
	var nYear int
	var nMonth int
	var nDay int
	var nHour int
	var nMinute int
	var nSecond int
	var nSex int

	flag.IntVar(&nYear, "y", 2020, "-y=1995 ")
	flag.IntVar(&nMonth, "m", 1, "-m=6 ")
	flag.IntVar(&nDay, "d", 1, "-d=16 ")
	flag.IntVar(&nHour, "h", 1, "-h=19 ")
	flag.IntVar(&nMinute, "n", 0, "-n=7 ")
	flag.IntVar(&nSecond, "s", 0, "-s=0 ")
	flag.IntVar(&nSex, "x", 0, "-x=0  1是男0是女 ")

	flag.Parse() //解析输入的参数

	pBazi := bazi.GetBazi(nYear, nMonth, nDay, nHour, nMinute, nSecond, nSex)
	fmt.Println(pBazi)
}
