Chinese Lunisolar Calendar
====================

[![CI](https://github.com/magiclen/chinese-lunisolar-calendar/actions/workflows/ci.yml/badge.svg)](https://github.com/magiclen/chinese-lunisolar-calendar/actions/workflows/ci.yml)

The traditional Chinese Calendar, known as 農曆 or 陰曆 in Chinese, is based on the moon, and is commonly referred to as the Lunar Calendar.

Due to the Lunar Calendar's 60-year cycle and the absence of regular rules for the days in each lunar month, as well as the variable number of months in a lunar year, using the Lunar Calendar without referencing other calendars can be challenging. The Lunisolar Calendar is designed to address this issue by combining both the Solar Calendar (Gregorian Calendar) and the Lunar Calendar, ensuring accuracy, predictability, and practicality.

This library allows you to seamlessly convert dates between the Lunisolar Calendar and the Solar Calendar, compute the Ba Zi (八字) weight, and also convert dates to Chinese text strings. Furthermore, it enables parsing of Chinese text strings into dates in both Simplified Chinese and Traditional Chinese.

## Examples

```rust
use chinese_lunisolar_calendar::SolarDate;

let solar_date = SolarDate::from_ymd(2019, 1, 15).unwrap();

assert_eq!("二〇一九年一月十五日", solar_date.to_string());
```

```rust
use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};

let lunisolar_date = LunisolarDate::from_solar_date(SolarDate::from_ymd(2019, 1, 15).unwrap()).unwrap();

assert_eq!("二〇一八　戊戌、狗年　臘月　初十", lunisolar_date.to_string());

assert_eq!("二〇一八　戊戌、狗年　臘月　初十", format!("{lunisolar_date}"));
assert_eq!("二〇一八　戊戌、狗年　腊月　初十", format!("{lunisolar_date:#}"));

use chinese_lunisolar_calendar::EarthlyBranch;
assert_eq!(43, lunisolar_date.get_ba_zi_weight(EarthlyBranch::Ninth));
```

To calculate the Ba Zi weight, the `ba-zi-weight` feature must be enabled.

## No Std

Disable the default features to compile this crate without std.

```toml
[dependencies.chinese-lunisolar-calendar]
version = "*"
default-features = false
```

## Crates.io

https://crates.io/crates/chinese-lunisolar-calendar

## Documentation

https://docs.rs/chinese-lunisolar-calendar

## License

[MIT](LICENSE)