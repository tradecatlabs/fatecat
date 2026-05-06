# BaziGo
GO语言的八字库

作者只想保留版权，无任何使用或者发布限制。您只需要在您的发行版本中注明代码出处
https://github.com/warrially/BaziGo


如果有商业谈合作可以直接电话联系
+86-167-632-33049
本人从事八字研发多年






八字部分参考的是三清宫命理
https://weibo.com/bazishequ

日历部分参考中国日历类
中国日历类（Chinese Calendar Class (CCC)）
版本：v0.1，JavaScript版本
版权所有 (C) 2002-2003 neweroica (wy25@mail.bnu.edu.cn)
联系方式： Email:  wy25@mail.bnu.edu.cn
QQ: 32460746

日历部分参考CNPACK
作者：刘啸 (liuxiao@cnpack.org)
周劲羽(zjy@cnpack.org)



出生日期新历：  1995 年 6 月 16 日   19 : 7 : 0
基本八字： 乙亥 壬午 戊寅 壬戌

#### 命盘解析 Tables

| 年 | 月 |日 |时 |
| :--------:   | :------:  | :---------:  |  :---------:  |
|**乙**(木)[官]|**壬**(水)[才]|**戊**(土)[主]|**壬**(水)[才]
|**亥**(水)[才杀]|**午**(火)[印劫]|**寅**(木)[杀卩比]|**戌**(土)[比伤印]
|山头火|               杨柳木|                  城墙土|                  大海水

所属节令：
芒种 1995 年 6 月 6 日   11 : 42 : 28
小暑 1995 年 7 月 7 日   22 : 1 : 0
大运： 癸未 甲申 乙酉 丙戌 丁亥 戊子 己丑 庚寅 辛卯 壬辰
起运时间 2002 年 5 月 25 日   7 : 7 : 0

```
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

	flag.IntVar(&nYear, "y", 1995, "-y=1995 ")
	flag.IntVar(&nMonth, "m", 6, "-m=6 ")
	flag.IntVar(&nDay, "d", 16, "-d=16 ")
	flag.IntVar(&nHour, "h", 19, "-h=19 ")
	flag.IntVar(&nMinute, "n", 7, "-n=7 ")
	flag.IntVar(&nSecond, "s", 0, "-s=0 ")
	flag.IntVar(&nSex, "x", 0, "-x=0  1是男0是女 ")

	flag.Parse() //解析输入的参数

	pBazi := bazi.GetBazi(nYear, nMonth, nDay, nHour, nMinute, nSecond, nSex)
	fmt.Println(pBazi)
}
```

```
// HTTP 版本
package main

import (
	"fmt"
	"net/http"

	bazi "github.com/warrially/BaziGo"
)

type Myhandler struct{}

func main() {
	http.HandleFunc("/", IndexHandler)
	http.ListenAndServe(":7890", nil)
}
func IndexHandler(w http.ResponseWriter, r *http.Request) {
	pBazi := bazi.GetBazi(1995, 6, 16, 19, 7, 0, 0)
	fmt.Fprintln(w, pBazi.ToHTML())
}
```