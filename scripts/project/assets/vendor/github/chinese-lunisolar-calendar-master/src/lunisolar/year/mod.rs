mod built_in_traits;
use core::fmt::{self, Display, Formatter};

use super::{LunisolarOutOfRangeError, BIG_MONTHS, LEAP_MONTHS};
use crate::{EarthlyBranch, HeavenlyStems, LunarMonth, LunarYear, SolarYear, Zodiac};

/// 最小支援的農曆西曆年。
pub const MIN_YEAR_IN_SOLAR_CALENDAR: u16 = 1901;
/// 最大支援的農曆西曆年。
pub const MAX_YEAR_IN_SOLAR_CALENDAR: u16 = 2101;

/// 農曆西曆年，農曆新年所在的西曆年份。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash)]
pub struct LunisolarYear(SolarYear);

impl Display for LunisolarYear {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2008)).unwrap();
    ///
    /// assert_eq!("二〇〇八", format!("{}", lunisolar_year));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        Display::fmt(&self.0, f)
    }
}

/// 用以建立 `LunisolarYear` 列舉實體的關聯函數。
impl LunisolarYear {
    /// 透過西曆年份來取得 `LunisolarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year = unsafe {
    ///     LunisolarYear::from_solar_year_unsafe(SolarYear::from_u16(2024))
    /// };
    /// ```
    ///
    /// # Safety
    /// 必須先確認傳入的西曆年份是支援的。
    #[inline]
    pub const unsafe fn from_solar_year_unsafe(solar_year: SolarYear) -> Self {
        Self(solar_year)
    }

    /// 透過西曆年份來取得 `LunisolarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    /// ```
    #[inline]
    pub const fn from_solar_year(solar_year: SolarYear) -> Result<Self, LunisolarOutOfRangeError> {
        let year = solar_year.to_u16();

        if year >= MIN_YEAR_IN_SOLAR_CALENDAR && year <= MAX_YEAR_IN_SOLAR_CALENDAR {
            Ok(Self(solar_year))
        } else {
            Err(LunisolarOutOfRangeError)
        }
    }
}

/// 將 `LunisolarYear` 列舉實體轉成其它型別的方法。
impl LunisolarYear {
    /// 取得此西曆年中，農曆新年的中國天干。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{HeavenlyStems, LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(HeavenlyStems::First, lunisolar_year.to_heavenly_stems());
    /// ```
    #[inline]
    pub const fn to_heavenly_stems(self) -> HeavenlyStems {
        let index = ((7 + (self.0.to_u16() - MIN_YEAR_IN_SOLAR_CALENDAR)) % 10) as u8;

        unsafe { HeavenlyStems::from_ordinal_unsafe(index + 1) }
    }

    /// 取得此西曆年中，農曆新年的中國地支。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(EarthlyBranch::Fifth, lunisolar_year.to_earthly_branch());
    /// ```
    #[inline]
    pub const fn to_earthly_branch(self) -> EarthlyBranch {
        let index = ((self.0.to_u16() - MIN_YEAR_IN_SOLAR_CALENDAR + 1) % 12) as u8;

        unsafe { EarthlyBranch::from_ordinal_unsafe(index + 1) }
    }

    /// 取得此西曆年中，農曆新年所屬的生肖。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarYear, SolarYear, Zodiac};
    ///
    /// let lunisolar_year =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(Zodiac::Dragon, lunisolar_year.to_zodiac());
    /// ```
    #[inline]
    pub const fn to_zodiac(self) -> Zodiac {
        let index = ((self.0.to_u16() - MIN_YEAR_IN_SOLAR_CALENDAR + 1) % 12) as u8;

        unsafe { Zodiac::from_ordinal_unsafe(index + 1) }
    }

    /// 取得 `LunarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarYear, LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(
    ///     LunarYear::parse_str("甲辰").unwrap(),
    ///     lunisolar_year.to_lunar_year()
    /// );
    /// ```
    #[inline]
    pub const fn to_lunar_year(self) -> LunarYear {
        let heavenly_stems = self.to_heavenly_stems();
        let earthly_branch = self.to_earthly_branch();

        match LunarYear::from_era(heavenly_stems, earthly_branch) {
            Ok(lunar_year) => lunar_year,
            Err(_) => unreachable!(),
        }
    }

    /// 取得 `SolarYear` 實體。
    #[inline]
    pub const fn to_solar_year(self) -> SolarYear {
        self.0
    }

    /// 取得 `LunisolarYear` 實體所代表的西曆年份數值。
    #[inline]
    pub const fn to_u16(self) -> u16 {
        self.0.to_u16()
    }
}

/// 農曆西曆年相關計算方法。
impl LunisolarYear {
    /// 取得此年的農曆閏月月份。如果沒有的話就回傳 `None`。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarMonth, LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year_2023 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2023)).unwrap();
    ///
    /// let lunisolar_year_2024 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(
    ///     Some(LunarMonth::LeapSecond),
    ///     lunisolar_year_2023.get_leap_lunar_month()
    /// );
    ///
    /// assert_eq!(None, lunisolar_year_2024.get_leap_lunar_month());
    /// ```
    #[inline]
    pub const fn get_leap_lunar_month(self) -> Option<LunarMonth> {
        let year = self.to_u16();

        let date = LEAP_MONTHS[((year - MIN_YEAR_IN_SOLAR_CALENDAR) / 2) as usize];

        let index = if year % 2 == 1 { (date & 0xF0) >> 4 } else { date & 0x0F };

        if index == 0 {
            None
        } else {
            Some(unsafe { LunarMonth::from_u8_with_leap_unsafe(index, true) })
        }
    }

    /// 計算此西曆年下的農曆閏月共有幾天。如果沒有閏月，則回傳 `0`。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year_2023 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2023)).unwrap();
    ///
    /// let lunisolar_year_2024 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(29, lunisolar_year_2023.get_total_days_in_leap_month());
    ///
    /// assert_eq!(0, lunisolar_year_2024.get_total_days_in_leap_month());
    /// ```
    #[inline]
    pub const fn get_total_days_in_leap_month(self) -> u16 {
        let leap_lunar_month = self.get_leap_lunar_month();

        match leap_lunar_month {
            Some(leap_lunar_month) => self.get_total_days_in_leap_month_inner(leap_lunar_month),
            None => 0,
        }
    }

    /// 計算指定的農曆閏月共有幾天。
    #[inline]
    pub(crate) const fn get_total_days_in_leap_month_inner(
        self,
        leap_lunar_month: LunarMonth,
    ) -> u16 {
        let year = self.to_u16();

        let leap_month = leap_lunar_month.to_u8();

        if BIG_MONTHS[(year - MIN_YEAR_IN_SOLAR_CALENDAR) as usize] & (0x8000 >> leap_month as u16)
            == 0
        {
            29
        } else {
            30
        }
    }

    /// 計算此西曆年下的農曆年共有幾天。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year_2023 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2023)).unwrap();
    ///
    /// let lunisolar_year_2024 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(384, lunisolar_year_2023.get_total_days());
    ///
    /// assert_eq!(354, lunisolar_year_2024.get_total_days());
    /// ```
    pub const fn get_total_days(self) -> u16 {
        let (leap_month, mut n) = match self.get_leap_lunar_month() {
            Some(leap_lunar_month) => (
                leap_lunar_month.to_u8(),
                self.get_total_days_in_leap_month_inner(leap_lunar_month),
            ),
            None => (0, 0),
        };

        let year = self.to_u16();

        let bit_months = BIG_MONTHS[(year - MIN_YEAR_IN_SOLAR_CALENDAR) as usize];

        if leap_month > 0 {
            let mut date = 1;

            while date <= leap_month {
                if bit_months & (0x8000 >> (date - 1) as u16) == 0 {
                    n += 29;
                } else {
                    n += 30;
                }

                date += 1;
            }

            while date <= 12 {
                if bit_months & (0x8000 >> (date as u16)) == 0 {
                    n += 29;
                } else {
                    n += 30;
                }

                date += 1;
            }
        } else {
            let mut date = 1;

            while date <= 12 {
                if bit_months & (0x8000 >> (date - 1) as u16) == 0 {
                    n += 29;
                } else {
                    n += 30;
                }

                date += 1;
            }
        }

        n
    }

    /// 計算此西曆年下的農曆年的某個月共有幾天。如果傳入的是閏月，但是該年沒有該閏月的話就回傳 `None`。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarMonth, LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year_2023 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2023)).unwrap();
    ///
    /// let lunisolar_year_2024 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(
    ///     Some(29),
    ///     lunisolar_year_2023.get_total_days_in_a_month(LunarMonth::First)
    /// );
    /// assert_eq!(
    ///     Some(30),
    ///     lunisolar_year_2023.get_total_days_in_a_month(LunarMonth::Second)
    /// );
    /// assert_eq!(
    ///     Some(29),
    ///     lunisolar_year_2023.get_total_days_in_a_month(LunarMonth::LeapSecond)
    /// );
    /// assert_eq!(
    ///     Some(29),
    ///     lunisolar_year_2023.get_total_days_in_a_month(LunarMonth::Third)
    /// );
    /// assert_eq!(
    ///     None,
    ///     lunisolar_year_2023.get_total_days_in_a_month(LunarMonth::LeapThird)
    /// );
    ///
    /// assert_eq!(
    ///     Some(29),
    ///     lunisolar_year_2024.get_total_days_in_a_month(LunarMonth::First)
    /// );
    /// assert_eq!(
    ///     Some(30),
    ///     lunisolar_year_2024.get_total_days_in_a_month(LunarMonth::Second)
    /// );
    /// assert_eq!(
    ///     None,
    ///     lunisolar_year_2024.get_total_days_in_a_month(LunarMonth::LeapSecond)
    /// );
    /// assert_eq!(
    ///     Some(29),
    ///     lunisolar_year_2024.get_total_days_in_a_month(LunarMonth::Third)
    /// );
    /// assert_eq!(
    ///     None,
    ///     lunisolar_year_2024.get_total_days_in_a_month(LunarMonth::LeapThird)
    /// );
    /// ```
    pub const fn get_total_days_in_a_month(self, lunar_month: LunarMonth) -> Option<u8> {
        let year = self.to_u16();

        let mut month = lunar_month.to_u8();

        let leap_month = match self.get_leap_lunar_month() {
            Some(leap_lunar_month) => leap_lunar_month.to_u8(),
            None => 0,
        };

        if lunar_month.is_leap_month() {
            if month != leap_month {
                // 防呆
                None
            } else {
                // 此為閏月，需計算其後一個月的天數
                if (BIG_MONTHS[(year - MIN_YEAR_IN_SOLAR_CALENDAR) as usize]
                    & (0x8000 >> leap_month as u16))
                    == 0
                {
                    Some(29)
                } else {
                    Some(30)
                }
            }
        } else {
            if leap_month > 0 && month > leap_month {
                // 若今年有閏月，且該西曆月應在閏月之後再加一個月
                month += 1;
            }
            if BIG_MONTHS[(year - MIN_YEAR_IN_SOLAR_CALENDAR) as usize]
                & (0x8000 >> (month - 1) as u16)
                == 0
            {
                Some(29)
            } else {
                Some(30)
            }
        }
    }
}

/// 額外的實作。
impl LunarMonth {
    /// 傳入指定的農曆西曆年，並計算此農曆月在這個指定的農曆西曆年內共有幾天。如果自己本身是閏月，但是該年沒有該閏月的話就回傳 None。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarMonth, LunisolarYear, SolarYear};
    ///
    /// let lunisolar_year_2023 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2023)).unwrap();
    ///
    /// let lunisolar_year_2024 =
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap();
    ///
    /// assert_eq!(Some(29), LunarMonth::First.get_total_days(lunisolar_year_2023));
    /// assert_eq!(
    ///     Some(30),
    ///     LunarMonth::Second.get_total_days(lunisolar_year_2023)
    /// );
    /// assert_eq!(
    ///     Some(29),
    ///     LunarMonth::LeapSecond.get_total_days(lunisolar_year_2023)
    /// );
    /// assert_eq!(Some(29), LunarMonth::Third.get_total_days(lunisolar_year_2023));
    /// assert_eq!(None, LunarMonth::LeapThird.get_total_days(lunisolar_year_2023));
    ///
    /// assert_eq!(Some(29), LunarMonth::First.get_total_days(lunisolar_year_2024));
    /// assert_eq!(
    ///     Some(30),
    ///     LunarMonth::Second.get_total_days(lunisolar_year_2024)
    /// );
    /// assert_eq!(
    ///     None,
    ///     LunarMonth::LeapSecond.get_total_days(lunisolar_year_2024)
    /// );
    /// assert_eq!(Some(29), LunarMonth::Third.get_total_days(lunisolar_year_2024));
    /// assert_eq!(None, LunarMonth::LeapThird.get_total_days(lunisolar_year_2024));
    /// ```
    #[inline]
    pub const fn get_total_days(self, lunisolar_year: LunisolarYear) -> Option<u8> {
        lunisolar_year.get_total_days_in_a_month(self)
    }
}
