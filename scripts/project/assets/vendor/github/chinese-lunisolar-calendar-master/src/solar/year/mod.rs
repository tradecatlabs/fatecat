mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter, Write};

use chinese::{ALTERNATIVE_ZERO, THE_SOLAR_YEAR_NUMBERS_CHAR};

use super::{SolarMonth, SolarOutOfRangeError, SolarYearError};

/// 西曆年份。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash)]
pub struct SolarYear(u16);

impl Display for SolarYear {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarYear;
    /// let solar_year = SolarYear::from_u16(2008);
    ///
    /// assert_eq!("二〇〇八", format!("{}", solar_year));
    /// ```
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let mut year = self.0;

        if year == 0 {
            f.write_char(THE_SOLAR_YEAR_NUMBERS_CHAR[0])?;
        } else {
            let mut base = 10u16.pow(year.ilog10());

            loop {
                let digit = year / base;
                year -= digit * base;

                f.write_char(THE_SOLAR_YEAR_NUMBERS_CHAR[digit as usize])?;

                base /= 10;

                if base == 0 {
                    break;
                }
            }
        }

        Ok(())
    }
}

/// 用以建立 `SolarYear` 列舉實體的關聯函數。
impl SolarYear {
    /// 透過西曆年份數值來取得 `SolarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarYear;
    /// let solar_year = SolarYear::from_u16(2008);
    /// ```
    #[inline]
    pub const fn from_u16(year: u16) -> Self {
        Self(year)
    }

    /// 透過西曆年份數值來取得 `SolarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarYear;
    /// let solar_year = SolarYear::from_i32(2008).unwrap();
    /// ```
    #[inline]
    pub const fn from_i32(year: i32) -> Result<Self, SolarOutOfRangeError> {
        if year >= 0 && year <= u16::MAX as i32 {
            Ok(Self::from_u16(year as u16))
        } else {
            Err(SolarOutOfRangeError)
        }
    }
}

/// 將 `SolarYear` 列舉實體轉成其它型別的方法。
impl SolarYear {
    /// 取得 `SolarYear` 實體所代表的西曆年份數值。
    #[inline]
    pub const fn to_u16(self) -> u16 {
        self.0
    }

    /// 取得 `SolarYear` 實體所代表的西曆年份數值。
    #[inline]
    pub const fn to_i32(self) -> i32 {
        self.0 as i32
    }
}

/// 西曆年份相關計算方法。
impl SolarYear {
    /// 判斷此西曆年是否為閏年。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarYear;
    /// assert_eq!(true, SolarYear::from_u16(2008).is_leap());
    /// assert_eq!(false, SolarYear::from_u16(2009).is_leap());
    /// assert_eq!(false, SolarYear::from_u16(2100).is_leap());
    /// ```
    #[inline]
    pub const fn is_leap(self) -> bool {
        year_helper::is_leap_year(self.0 as i32)
    }

    /// 計算此西曆年共有幾天。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarYear;
    /// assert_eq!(366, SolarYear::from_u16(2008).get_total_days());
    /// assert_eq!(365, SolarYear::from_u16(2009).get_total_days());
    /// ```
    #[inline]
    pub const fn get_total_days(self) -> u16 {
        year_helper::get_days_in_year(self.0 as i32)
    }

    /// 計算此西曆年下的某個月共有幾天。。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::{SolarMonth, SolarYear};
    /// assert_eq!(
    ///     31,
    ///     SolarYear::from_u16(2008)
    ///         .get_total_days_in_a_month(SolarMonth::January)
    /// );
    /// assert_eq!(
    ///     29,
    ///     SolarYear::from_u16(2008)
    ///         .get_total_days_in_a_month(SolarMonth::February)
    /// );
    /// assert_eq!(
    ///     30,
    ///     SolarYear::from_u16(2008).get_total_days_in_a_month(SolarMonth::April)
    /// );
    /// assert_eq!(
    ///     28,
    ///     SolarYear::from_u16(2009)
    ///         .get_total_days_in_a_month(SolarMonth::February)
    /// );
    /// ```
    #[inline]
    pub const fn get_total_days_in_a_month(self, solar_month: SolarMonth) -> u8 {
        match year_helper::get_days_in_month(self.0 as i32, solar_month.to_u8()) {
            Some(d) => d,
            None => unreachable!(),
        }
    }
}
