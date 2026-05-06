mod built_in_traits;
mod parse;

use core::{
    cmp::Ordering,
    fmt::{self, Display, Formatter, Write},
};

use chrono::prelude::*;

use super::{SolarDateError, SolarDay, SolarDayError, SolarMonth, SolarOutOfRangeError, SolarYear};

/// 西曆年月日。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SolarDate {
    pub(crate) solar_year:  SolarYear,
    pub(crate) solar_month: SolarMonth,
    pub(crate) solar_day:   SolarDay,
}

impl PartialOrd for SolarDate {
    #[inline]
    fn partial_cmp(&self, other: &SolarDate) -> Option<Ordering> {
        Some(Ord::cmp(self, other))
    }
}

impl Ord for SolarDate {
    #[inline]
    fn cmp(&self, other: &SolarDate) -> Ordering {
        self.cmp(other)
    }
}

impl Display for SolarDate {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDate;
    /// assert_eq!(
    ///     "二〇二四年一月一日",
    ///     format!("{}", SolarDate::from_ymd(2024, 1, 1).unwrap())
    /// );
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        Display::fmt(&self.solar_year, f)?;
        f.write_char('年')?;
        Display::fmt(&self.solar_month, f)?;
        Display::fmt(&self.solar_day, f)?;
        f.write_char('日')
    }
}

/// 用以建立 `SolarDate` 列舉實體的關聯函數。
impl SolarDate {
    /// 將日期轉成 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::SolarDate;
    /// use chrono::prelude::*;
    ///
    /// let date = NaiveDate::from_ymd_opt(2024, 1, 1).unwrap();
    ///
    /// let solar_date = SolarDate::from_date(date).unwrap();
    /// ```
    #[inline]
    pub fn from_date<D: Datelike>(date: D) -> Result<Self, SolarOutOfRangeError> {
        let solar_year = SolarYear::from_i32(date.year())?;
        let solar_month = SolarMonth::from_u32(date.month()).unwrap();
        let solar_day = SolarDay::from_u32(date.day()).unwrap();

        Ok(SolarDate {
            solar_year,
            solar_month,
            solar_day,
        })
    }

    /// 利用西曆的年月日來產生 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{
    ///     SolarDate, SolarDay, SolarMonth, SolarYear,
    /// };
    ///
    /// let solar_date = unsafe {
    ///     SolarDate::from_solar_year_month_day_unsafe(
    ///         SolarYear::from_u16(2004),
    ///         SolarMonth::January,
    ///         SolarDay::First,
    ///     )
    /// };
    /// ```
    ///
    /// # Safety
    /// 必須先確保傳入的 `solar_day` 在該西元年月下是合法的。
    #[inline]
    pub const unsafe fn from_solar_year_month_day_unsafe(
        solar_year: SolarYear,
        solar_month: SolarMonth,
        solar_day: SolarDay,
    ) -> Self {
        SolarDate {
            solar_year,
            solar_month,
            solar_day,
        }
    }

    /// 利用西曆的年月日來產生 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{
    ///     SolarDate, SolarDay, SolarMonth, SolarYear,
    /// };
    ///
    /// let solar_date = SolarDate::from_solar_year_month_day(
    ///     SolarYear::from_u16(2004),
    ///     SolarMonth::January,
    ///     SolarDay::First,
    /// )
    /// .unwrap();
    /// ```
    #[inline]
    pub const fn from_solar_year_month_day(
        solar_year: SolarYear,
        solar_month: SolarMonth,
        solar_day: SolarDay,
    ) -> Result<Self, SolarDayError> {
        let days = solar_month.get_total_days(solar_year);

        let day = solar_day.to_u8();

        if day <= days {
            Ok(SolarDate {
                solar_year,
                solar_month,
                solar_day,
            })
        } else {
            Err(SolarDayError)
        }
    }

    /// 利用西曆的年月日來產生 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDate;
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    /// ```
    #[inline]
    pub const fn from_ymd(year: u16, month: u8, day: u8) -> Result<Self, SolarDateError> {
        let solar_year = SolarYear::from_u16(year);

        match SolarMonth::from_u8(month) {
            Ok(solar_month) => match SolarDay::from_u8(day) {
                Ok(solar_day) => {
                    match Self::from_solar_year_month_day(solar_year, solar_month, solar_day) {
                        Ok(solar_date) => Ok(solar_date),
                        Err(_) => Err(SolarDateError::DayIncorrect),
                    }
                },
                Err(_) => Err(SolarDateError::DayIncorrect),
            },
            Err(_) => Err(SolarDateError::MonthIncorrect),
        }
    }

    /// 以目前的年月日來產生 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDate;
    /// let solar_date = SolarDate::now().unwrap();
    /// ```
    #[inline]
    pub fn now() -> Result<Self, SolarOutOfRangeError> {
        Self::from_date(Utc::now().date_naive())
    }
}

/// 將 `SolarDate` 列舉實體轉成其它型別的方法。
impl SolarDate {
    /// 將 `SolarDate` 實體轉成無時區的 `Chrono` 年月日實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::SolarDate;
    /// use chrono::prelude::*;
    ///
    /// let date = NaiveDate::from_ymd_opt(2024, 1, 1).unwrap();
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    ///
    /// assert_eq!(date, solar_date.to_naive_date());
    /// ```
    #[inline]
    pub const fn to_naive_date(self) -> NaiveDate {
        match NaiveDate::from_ymd_opt(
            self.solar_year.to_i32(),
            self.solar_month.to_u32(),
            self.solar_day.to_u32(),
        ) {
            Some(result) => result,
            None => unreachable!(),
        }
    }

    /// 取得西曆年。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{SolarDate, SolarYear};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    ///
    /// assert_eq!(SolarYear::from_u16(2024), solar_date.to_solar_year());
    /// ```
    #[inline]
    pub const fn to_solar_year(self) -> SolarYear {
        self.solar_year
    }

    /// 取得西曆月。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{SolarDate, SolarMonth};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    ///
    /// assert_eq!(SolarMonth::January, solar_date.to_solar_month());
    /// ```
    #[inline]
    pub const fn to_solar_month(self) -> SolarMonth {
        self.solar_month
    }

    /// 取得西曆日。
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{SolarDate, SolarDay};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 1, 1).unwrap();
    ///
    /// assert_eq!(SolarDay::First, solar_date.to_solar_day());
    /// ```
    #[inline]
    pub const fn to_solar_day(self) -> SolarDay {
        self.solar_day
    }
}

/// 西曆日期相關計算方法。
impl SolarDate {
    /// 計算此西曆年月日是該西曆年的第幾天。舉例：2013-01-04，就是第四天。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDate;
    /// assert_eq!(
    ///     4,
    ///     SolarDate::from_ymd(2013, 1, 4).unwrap().the_n_day_in_this_year()
    /// );
    /// assert_eq!(
    ///     308,
    ///     SolarDate::from_ymd(2013, 11, 4).unwrap().the_n_day_in_this_year()
    /// );
    /// ```
    #[inline]
    pub const fn the_n_day_in_this_year(self) -> u16 {
        let mut n = 0u16;

        let leap_year = year_helper::is_leap_year(self.solar_year.to_i32());

        let month = self.solar_month.to_u8();

        let mut i = 1;

        while i < month {
            match year_helper::get_days_in_month_2(leap_year, i) {
                Some(days) => n += days as u16,
                None => unreachable!(),
            }

            i += 1;
        }

        n += self.solar_day.to_u8() as u16;

        n
    }

    /// 與其它的 `SolarDate` 結構實體進行大小比較。
    ///
    /// # Examples
    ///
    /// ```
    /// use core::cmp::Ordering;
    ///
    /// use chinese_lunisolar_calendar::SolarDate;
    ///
    /// let solar_date_1 = SolarDate::from_ymd(2024, 1, 1).unwrap();
    /// let solar_date_2 = SolarDate::from_ymd(2024, 1, 2).unwrap();
    ///
    /// assert_eq!(Ordering::Less, solar_date_1.cmp(&solar_date_2));
    /// ```
    pub const fn cmp(&self, other: &SolarDate) -> Ordering {
        let year_s = self.solar_year.to_u16();
        let year_o = other.solar_year.to_u16();

        if year_s > year_o {
            return Ordering::Greater;
        } else if year_s < year_o {
            return Ordering::Less;
        }

        let month_s = self.solar_month.to_u8();
        let month_o = other.solar_month.to_u8();

        if month_s > month_o {
            return Ordering::Greater;
        } else if month_s < month_o {
            return Ordering::Less;
        }

        let day_s = self.solar_day.to_u8();
        let day_o = other.solar_day.to_u8();

        if day_s > day_o {
            Ordering::Greater
        } else if day_s == day_o {
            Ordering::Equal
        } else {
            Ordering::Less
        }
    }
}
