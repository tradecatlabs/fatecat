# lunar [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg?style=flat-square)](https://github.com/6tail/lunar-swift/blob/master/LICENSE)

lunar是一款无第三方依赖的日历工具，支持公历(阳历)、农历(阴历、老黄历)、道历和佛历，支持星座、儒略日、干支、生肖、节气、节日、彭祖百忌、吉神(喜神/福神/财神/阳贵神/阴贵神)方位、胎神方位、冲煞、纳音、星宿、八字、五行、十神、建除十二值星、青龙名堂等十二神、黄道日及吉凶、法定节假日及调休等。

> 基于swift 5.5.1版本开发

[English](https://github.com/6tail/lunar-swift/blob/master/README_EN.md)

## 示例

    let lunar = Lunar.fromYmdHms(lunarYear: 1986, lunarMonth: 4, lunarDay: 21)
    print(lunar.description)
    print(lunar.solar.fullString)

输出结果：

    一九八六年四月廿一
    1986-05-29 00:00:00 星期四 双子座

## 文档

请移步至 [https://6tail.cn/calendar/api.html](https://6tail.cn/calendar/api.html "https://6tail.cn/calendar/api.html")

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=6tail/lunar-swift&type=Date)](https://star-history.com/#6tail/lunar-swift&Date)
