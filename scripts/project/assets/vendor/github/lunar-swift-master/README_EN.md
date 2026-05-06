# lunar [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg?style=flat-square)](https://github.com/6tail/lunar-swift/blob/master/LICENSE)

lunar is a calendar library for Solar and Chinese Lunar.

> Support since swift 5.5.1

[简体中文](https://github.com/6tail/lunar-swift/blob/master/README.md)

## Example

    let lunar = Lunar.fromYmdHms(lunarYear: 1986, lunarMonth: 4, lunarDay: 21)
    print(lunar.description)
    print(lunar.solar.fullString)

Output:

    一九八六年四月廿一
    1986-05-29 00:00:00 星期四 双子座

## Documentation

Please visit [https://6tail.cn/calendar/api.html](https://6tail.cn/calendar/api.html "https://6tail.cn/calendar/api.html")

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=6tail/lunar-swift&type=Date)](https://star-history.com/#6tail/lunar-swift&Date)
