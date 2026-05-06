mod built_in_traits;

#[cfg(feature = "ba-zi-weight")]
mod ba_zi_weight;
mod parse;

use core::{
    cmp::Ordering,
    fmt::{self, Display, Formatter, Write},
};

use chrono::prelude::*;

use super::{LunisolarDateError, LunisolarOutOfRangeError, LunisolarYear, NEW_YEAR_DIFFERENCE};
use crate::{
    LunarDay, LunarMonth, LunarYear, SolarDate, SolarDay, SolarMonth, SolarYear,
    MAX_YEAR_IN_SOLAR_CALENDAR, MIN_YEAR_IN_SOLAR_CALENDAR,
};

/// 最小支援的農曆日期(以西曆日期表示)：1901-02-19。
pub const MIN_LUNISOLAR_DATE_IN_SOLAR_DATE: SolarDate = unsafe {
    SolarDate::from_solar_year_month_day_unsafe(
        SolarYear::from_u16(1901),
        SolarMonth::from_u8_unsafe(2),
        SolarDay::from_u8_unsafe(19),
    )
};

/// 最大支援的農曆日期(以西曆日期表示)：2101-01-28。
pub const MAX_LUNISOLAR_DATE_IN_SOLAR_DATE: SolarDate = unsafe {
    SolarDate::from_solar_year_month_day_unsafe(
        SolarYear::from_u16(2101),
        SolarMonth::from_u8_unsafe(1),
        SolarDay::from_u8_unsafe(28),
    )
};

const MAX_LUNISOLAR_DATE_IN_SOLAR_CALENDAR_NEW_YEAR_DIFFERENCE: u16 =
    MAX_LUNISOLAR_DATE_IN_SOLAR_DATE.the_n_day_in_this_year();

/// 農曆年月日，必須包含西曆年。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct LunisolarDate {
    solar_year:     SolarYear,
    lunisolar_year: LunisolarYear,
    lunar_month:    LunarMonth,
    lunar_day:      LunarDay,
}

impl PartialOrd for LunisolarDate {
    #[inline]
    fn partial_cmp(&self, other: &LunisolarDate) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for LunisolarDate {
    #[inline]
    fn cmp(&self, other: &LunisolarDate) -> Ordering {
        if self.lunisolar_year > other.lunisolar_year || self.lunar_month > other.lunar_month {
            Ordering::Greater
        } else {
            self.lunar_day.cmp(&other.lunar_day)
        }
    }
}

impl Display for LunisolarDate {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!("二〇二四　甲辰、龍年　正月　初一", format!("{lunisolar_date}"));
    /// assert_eq!("二〇二四　甲辰、龙年　正月　初一", format!("{lunisolar_date:#}"));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        Display::fmt(&self.to_lunisolar_year(), f)?;
        f.write_char('　')?;
        Display::fmt(&self.to_lunar_year(), f)?;
        f.write_char('、')?;
        Display::fmt(&self.to_lunisolar_year().to_zodiac(), f)?;
        f.write_char('年')?;
        f.write_char('　')?;
        Display::fmt(&self.to_lunar_month(), f)?;
        f.write_char('　')?;
        Display::fmt(&self.to_lunar_day(), f)
    }
}

/// 用以建立 `LunisolarDate` 列舉實體的關聯函數。
impl LunisolarDate {
    /// 將西曆年月日轉成農曆年月日(包含西曆年)。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    /// ```
    pub const fn from_solar_date(
        solar_date: SolarDate,
    ) -> Result<LunisolarDate, LunisolarOutOfRangeError> {
        if solar_date.is_safe() {
            let solar_year = solar_date.to_solar_year();

            let year = solar_year.to_u16();

            let lunisolar_year = unsafe { LunisolarYear::from_solar_year_unsafe(solar_year) };

            let mut day_diff = solar_date.the_n_day_in_this_year() - 1;

            let (leap_month, leap_days, new_year_diff) = if year == MAX_YEAR_IN_SOLAR_CALENDAR {
                (0, 0, MAX_LUNISOLAR_DATE_IN_SOLAR_CALENDAR_NEW_YEAR_DIFFERENCE)
            } else {
                let new_year_diff =
                    NEW_YEAR_DIFFERENCE[(year - MIN_YEAR_IN_SOLAR_CALENDAR) as usize] as u16;

                let leap_lunar_month = lunisolar_year.get_leap_lunar_month();

                match leap_lunar_month {
                    Some(leap_lunar_month) => (
                        leap_lunar_month.to_u8(),
                        lunisolar_year.get_total_days_in_leap_month_inner(leap_lunar_month),
                        new_year_diff,
                    ),
                    None => (0, 0, new_year_diff),
                }
            };

            if day_diff < new_year_diff {
                // 若天數差距比「西曆新年與對應農曆年新年」之天數差距小，表示此西曆日期尚未進入下一個農曆年(尚未到達正月，還在農曆年尾)。
                let lunisolar_year =
                    unsafe { LunisolarYear::from_solar_year_unsafe(SolarYear::from_u16(year - 1)) };

                let leap_lunar_month = lunisolar_year.get_leap_lunar_month();

                let (leap_month, leap_days) = match leap_lunar_month {
                    Some(leap_lunar_month) => (
                        leap_lunar_month.to_u8(),
                        lunisolar_year.get_total_days_in_leap_month_inner(leap_lunar_month),
                    ),
                    None => (0, 0),
                };

                let mut day_diff = new_year_diff - day_diff; // 此時天數差距為此西曆日期到該西曆年應該對應的農曆年新年之差距天數(若西曆日期為2/3，農曆新年對應的西曆日期為2/10，則兩天數差距為40-(30+3)=7)。

                let mut is_leap = false;

                let mut month = 12;

                loop {
                    if month == leap_month {
                        if day_diff > leap_days {
                            day_diff -= leap_days;
                        } else {
                            is_leap = true;
                        }
                    }

                    let month_days = match lunisolar_year.get_total_days_in_a_month(unsafe {
                        LunarMonth::from_u8_with_leap_unsafe(month, false)
                    }) {
                        Some(days) => days as u16,
                        None => unreachable!(),
                    };

                    if day_diff <= month_days {
                        break;
                    }

                    day_diff -= month_days;
                    is_leap = false;
                    month -= 1;
                }

                if day_diff == 0 {
                    Ok(LunisolarDate {
                        solar_year,
                        lunisolar_year,
                        lunar_month: unsafe {
                            LunarMonth::from_u8_with_leap_unsafe((month + 1) % 12 + 1, is_leap)
                        },
                        lunar_day: unsafe { LunarDay::from_u8_unsafe(1) },
                    })
                } else {
                    let lunar_month =
                        unsafe { LunarMonth::from_u8_with_leap_unsafe(month, is_leap) };

                    Ok(LunisolarDate {
                        solar_year,
                        lunisolar_year,
                        lunar_month,
                        lunar_day: unsafe {
                            LunarDay::from_u8_unsafe(
                                match lunar_month.get_total_days(lunisolar_year) {
                                    Some(days) => days,
                                    None => unreachable!(),
                                } - day_diff as u8
                                    + 1,
                            )
                        },
                    })
                }
            } else {
                // 若天數差距沒比「西曆新年與對應農曆年新年」之天數差距小，表示此西曆日期已經進入下一個農曆年(已到達正月，從在農曆年頭開始)。
                day_diff -= new_year_diff; // 此時天數差距為西曆日期與對應農曆年第一天之距離(若西曆日期為2/23(此時天數差距為53)，而對應農曆年第一天是西曆的2/10(新年偏差為40)，則這兩個日期的天數差距為53-40=13)。

                let mut is_leap = false;

                let mut month = 1;

                loop {
                    let month_days = match lunisolar_year.get_total_days_in_a_month(unsafe {
                        LunarMonth::from_u8_with_leap_unsafe(month, false)
                    }) {
                        Some(days) => days as u16,
                        None => unreachable!(),
                    };

                    if day_diff < month_days {
                        break;
                    }

                    day_diff -= month_days;

                    if month == leap_month {
                        if day_diff < leap_days {
                            is_leap = true;
                            break;
                        } else {
                            day_diff -= leap_days;
                        }
                    }

                    month += 1;
                }

                Ok(LunisolarDate {
                    solar_year,
                    lunisolar_year,
                    lunar_month: unsafe { LunarMonth::from_u8_with_leap_unsafe(month, is_leap) },
                    lunar_day: unsafe { LunarDay::from_u8_unsafe(day_diff as u8 + 1) },
                })
            }
        } else {
            Err(LunisolarOutOfRangeError)
        }
    }

    /// 將日期轉成農曆年月日(包含西曆年)。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::LunisolarDate;
    /// use chrono::prelude::*;
    ///
    /// let date = NaiveDate::from_ymd_opt(2024, 1, 1).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_date(date).unwrap();
    /// ```
    #[inline]
    pub fn from_date<D: Datelike>(date: D) -> Result<LunisolarDate, LunisolarOutOfRangeError> {
        let solar_date = SolarDate::from_date(date).map_err(|_| LunisolarOutOfRangeError)?;

        Self::from_solar_date(solar_date)
    }

    /// 利用農曆西曆年和農曆月日來產生 `LunisolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{
    ///     LunarDay, LunarMonth, LunisolarDate, LunisolarYear, SolarYear,
    /// };
    ///
    /// let lunisolar_date = unsafe {
    ///     LunisolarDate::from_lunisolar_year_lunar_month_day_unsafe(
    ///         LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap(),
    ///         LunarMonth::First,
    ///         LunarDay::First,
    ///     )
    /// };
    /// ```
    ///
    /// # Safety
    /// 請先確保傳入的農曆西曆年和農曆月日組合是正確的。
    #[inline]
    pub const unsafe fn from_lunisolar_year_lunar_month_day_unsafe(
        lunisolar_year: LunisolarYear,
        lunar_month: LunarMonth,
        lunar_day: LunarDay,
    ) -> LunisolarDate {
        let n = Self::the_n_day_in_this_year_inner(lunisolar_year, lunar_month, lunar_day);

        let solar_year = lunisolar_year.to_solar_year();

        let year = solar_year.to_u16();

        let solar_year = if n + NEW_YEAR_DIFFERENCE[(year - MIN_YEAR_IN_SOLAR_CALENDAR) as usize]
            as u16
            >= solar_year.get_total_days()
        {
            SolarYear::from_u16(year + 1)
        } else {
            solar_year
        };

        LunisolarDate {
            solar_year,
            lunisolar_year,
            lunar_month,
            lunar_day,
        }
    }

    /// 利用農曆西曆年和農曆月日來產生 `LunisolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{
    ///     LunarDay, LunarMonth, LunisolarDate, LunisolarYear, SolarYear,
    /// };
    ///
    /// let lunisolar_date = LunisolarDate::from_lunisolar_year_lunar_month_day(
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap(),
    ///     LunarMonth::First,
    ///     LunarDay::First,
    /// )
    /// .unwrap();
    /// ```
    #[inline]
    pub const fn from_lunisolar_year_lunar_month_day(
        lunisolar_year: LunisolarYear,
        lunar_month: LunarMonth,
        lunar_day: LunarDay,
    ) -> Result<LunisolarDate, LunisolarDateError> {
        if lunar_month.is_leap_month() {
            let leap_lunar_month = lunisolar_year.get_leap_lunar_month();

            match leap_lunar_month {
                Some(leap_lunar_month) => {
                    if lunar_month.to_u8() != leap_lunar_month.to_u8() {
                        return Err(LunisolarDateError::MonthIncorrect);
                    }
                },
                None => return Err(LunisolarDateError::MonthIncorrect),
            }
        }

        let days = match lunar_month.get_total_days(lunisolar_year) {
            Some(days) => days,
            None => unreachable!(),
        };

        if lunar_day.to_u8() > days {
            Err(LunisolarDateError::DayIncorrect)
        } else {
            Ok(unsafe {
                Self::from_lunisolar_year_lunar_month_day_unsafe(
                    lunisolar_year,
                    lunar_month,
                    lunar_day,
                )
            })
        }
    }

    /// 利用**農曆西曆年**和**農曆月日**來產生 `LunisolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunisolarDate;
    ///
    /// let lunisolar_date = LunisolarDate::from_ymd(2023, 11, false, 20).unwrap();
    /// ```
    #[inline]
    pub const fn from_ymd(
        year: u16,
        month: u8,
        leap: bool,
        day: u8,
    ) -> Result<LunisolarDate, LunisolarDateError> {
        let lunisolar_year = match LunisolarYear::from_solar_year(SolarYear::from_u16(year)) {
            Ok(lunisolar_year) => lunisolar_year,
            Err(_) => return Err(LunisolarDateError::OutOfRange),
        };

        let lunar_month = match LunarMonth::from_u8_with_leap(month, leap) {
            Ok(lunar_month) => lunar_month,
            Err(_) => return Err(LunisolarDateError::MonthIncorrect),
        };

        let lunar_day = match LunarDay::from_u8(day) {
            Ok(lunar_day) => lunar_day,
            Err(_) => return Err(LunisolarDateError::DayIncorrect),
        };

        Self::from_lunisolar_year_lunar_month_day(lunisolar_year, lunar_month, lunar_day)
    }

    /// 以目前的年月日來產生 `LunisolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunisolarDate;
    /// let lunisolar_date = LunisolarDate::now().unwrap();
    /// ```
    #[inline]
    pub fn now() -> Result<LunisolarDate, LunisolarOutOfRangeError> {
        Self::from_date(Utc::now().date_naive())
    }
}

/// 將 `LunisolarDate` 列舉實體轉成其它型別的方法。
impl LunisolarDate {
    /// 轉成西曆年月日。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(solar_date, lunisolar_date.to_solar_date());
    /// ```
    #[inline]
    pub const fn to_solar_date(self) -> SolarDate {
        let n = self.the_n_day_in_this_year();

        let ly = self.lunisolar_year.to_u16();

        // 天數差距為該農曆日期與對應西曆年新年的天數差距。其實就是轉換成西曆日期後，西曆日期與新年的距離。(舉例，農曆2012-01-03，為第3天，和農曆新年差了2天。加上西曆農曆偏差52天。因此天數差距為54)
        let mut days_diff =
            n - 1 + NEW_YEAR_DIFFERENCE[(ly - MIN_YEAR_IN_SOLAR_CALENDAR) as usize] as u16;

        let mut solar_year = SolarYear::from_u16(ly);

        let mut month = 1;

        let mut solar_month = unsafe { SolarMonth::from_u8_unsafe(month) };

        let mut month_days = solar_month.get_total_days(solar_year) as u16;

        while days_diff >= month_days {
            days_diff -= month_days;

            if month == 12 {
                solar_year = SolarYear::from_u16(solar_year.to_u16() + 1);

                month = 1;
            } else {
                month += 1;
            }

            solar_month = unsafe { SolarMonth::from_u8_unsafe(month) };

            month_days = solar_month.get_total_days(solar_year) as u16;
        }

        SolarDate {
            solar_year,
            solar_month,
            solar_day: unsafe { SolarDay::from_u8_unsafe(days_diff as u8 + 1) },
        }
    }

    /// 將 `LunisolarDate` 實體轉成無時區的 `Chrono` 年月日實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    /// use chrono::prelude::*;
    ///
    /// let date = NaiveDate::from_ymd_opt(2024, 2, 10).unwrap();
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(date, lunisolar_date.to_naive_date());
    /// ```
    #[inline]
    pub const fn to_naive_date(self) -> NaiveDate {
        self.to_solar_date().to_naive_date()
    }

    /// 取得西曆年。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(solar_date.to_solar_year(), lunisolar_date.to_solar_year());
    /// ```
    #[inline]
    pub const fn to_solar_year(self) -> SolarYear {
        self.solar_year
    }

    /// 取得農曆西曆年。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{
    ///     LunisolarDate, LunisolarYear, SolarDate, SolarYear,
    /// };
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(
    ///     LunisolarYear::from_solar_year(SolarYear::from_u16(2024)).unwrap(),
    ///     lunisolar_date.to_lunisolar_year()
    /// );
    /// ```
    #[inline]
    pub const fn to_lunisolar_year(self) -> LunisolarYear {
        self.lunisolar_year
    }

    /// 取得農曆年。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarYear, LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(
    ///     LunarYear::parse_str("甲辰").unwrap(),
    ///     lunisolar_date.to_lunar_year()
    /// );
    /// ```
    #[inline]
    pub const fn to_lunar_year(self) -> LunarYear {
        self.lunisolar_year.to_lunar_year()
    }

    /// 取得農曆月。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarMonth, LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(LunarMonth::First, lunisolar_date.to_lunar_month());
    /// ```
    #[inline]
    pub const fn to_lunar_month(self) -> LunarMonth {
        self.lunar_month
    }

    /// 取得農曆日。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunarDay, LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(LunarDay::First, lunisolar_date.to_lunar_day());
    /// ```
    #[inline]
    pub const fn to_lunar_day(self) -> LunarDay {
        self.lunar_day
    }
}

/// 農曆年月日相關計算方法。
impl LunisolarDate {
    /// 計算此農曆年月日是該農曆年的第幾天。舉例：2013/正月/初五，就是第五天。
    #[inline]
    pub(crate) const fn the_n_day_in_this_year_inner(
        lunisolar_year: LunisolarYear,
        lunar_month: LunarMonth,
        lunar_day: LunarDay,
    ) -> u16 {
        let mut n = lunar_day.to_u8() as u16;

        let month = lunar_month.to_u8();

        if lunar_month.is_leap_month() {
            let mut i = 1;

            while i <= month {
                let lunar_month = unsafe { LunarMonth::from_u8_with_leap_unsafe(i, false) };

                n += match lunar_month.get_total_days(lunisolar_year) {
                    Some(days) => days as u16,
                    None => unreachable!(),
                };

                i += 1;
            }
        } else {
            let mut i = 1;

            while i < month {
                let lunar_month = unsafe { LunarMonth::from_u8_with_leap_unsafe(i, false) };

                n += match lunar_month.get_total_days(lunisolar_year) {
                    Some(days) => days as u16,
                    None => unreachable!(),
                };

                i += 1;
            }

            if let Some(leap_lunar_month) = lunisolar_year.get_leap_lunar_month() {
                if month > leap_lunar_month.to_u8() {
                    n += lunisolar_year.get_total_days_in_leap_month_inner(leap_lunar_month);
                }
            }
        }

        n
    }

    /// 計算此農曆年月日是該農曆年的第幾天。舉例：2013/正月/初五，就是第五天。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(
    ///     SolarDate::from_ymd(2024, 2, 10).unwrap(),
    /// )
    /// .unwrap();
    ///
    /// assert_eq!(1, lunisolar_date.the_n_day_in_this_year());
    /// ```
    #[inline]
    pub const fn the_n_day_in_this_year(self) -> u16 {
        Self::the_n_day_in_this_year_inner(self.lunisolar_year, self.lunar_month, self.lunar_day)
    }
}

/// 額外的實作。
impl SolarDate {
    /// 判斷此 `SolarDate` 結構實體是否可以被安全地轉為 `LunisolarDate` 結構實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDate;
    /// let solar_date_1 = SolarDate::from_ymd(2024, 1, 1).unwrap();
    /// let solar_date_2 = SolarDate::from_ymd(3000, 1, 2).unwrap();
    ///
    /// assert_eq!(true, solar_date_1.is_safe());
    /// assert_eq!(false, solar_date_2.is_safe());
    /// ```
    #[inline]
    pub const fn is_safe(&self) -> bool {
        if let Ordering::Less = self.cmp(&MIN_LUNISOLAR_DATE_IN_SOLAR_DATE) {
            return false;
        } else if let Ordering::Greater = self.cmp(&MAX_LUNISOLAR_DATE_IN_SOLAR_DATE) {
            return false;
        }

        true
    }

    /// 利用農曆年月日來產生 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(solar_date, SolarDate::from_lunisolar_date(lunisolar_date));
    /// ```
    pub const fn from_lunisolar_date(lunisolar_date: LunisolarDate) -> SolarDate {
        lunisolar_date.to_solar_date()
    }

    /// 轉成農曆年月日。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    ///
    /// let lunisolar_date = solar_date.to_lunisolar_date().unwrap();
    /// ```
    #[inline]
    pub const fn to_lunisolar_date(self) -> Result<LunisolarDate, LunisolarOutOfRangeError> {
        LunisolarDate::from_solar_date(self)
    }
}
